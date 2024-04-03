from os import remove
from os.path import basename
from tkinter import Tk, Button, Label, Listbox, END, DISABLED, NORMAL, \
    messagebox, filedialog, simpledialog, Frame
from Authenticator import Authenticator
from ImageHandler import ImageHandler
from tempfile import NamedTemporaryFile
from sqlite3 import IntegrityError
from PIL import Image, ImageTk, UnidentifiedImageError
from io import BytesIO

class CryptoCanvas:
    def __init__(self):
        self.Auth = Authenticator()
        self.IH = ImageHandler()
        self.current_image_page = 1
        self.images_per_page = 10
        self.photo_image = None
        self.create_gui()

    def create_gui(self):
        self.main_window = Tk()
        self.main_window.title("CryptoCanvas")
        self.main_window.resizable(width=False, height=False)

        self.status = Label(self.main_window, font=("Times", 12),
                            text="Signed out")
        self.status.grid(row=0, column=0, columnspan=5)

        self.create_auth_buttons()
        self.create_image_buttons()
        self.create_image_listbox()
        self.quit_button = Button(self.main_window, text="Quit",
                                  command=self.quit)
        self.quit_button.grid(row=5, column=4, sticky="we")

        self.main_window.mainloop()

    def create_auth_buttons(self):
        self.sign_in_button = Button(self.main_window, text="Sign in",
                                     command=self.on_sign_in)
        self.sign_up_button = Button(self.main_window, text="Sign up",
                                     command=self.on_sign_up)
        self.sign_out_button = Button(self.main_window, text="Sign out",
                                      command=self.on_sign_out, state=DISABLED)

        self.sign_in_button.grid(row=2, column=0, sticky="we")
        self.sign_up_button.grid(row=2, column=1, sticky="we")
        self.sign_out_button.grid(row=2, column=2, sticky="we")

    def create_image_buttons(self):
        self.encrypt_button = Button(self.main_window, text="Encrypt image",
                                     command=self.on_encrypt_image)
        self.decrypt_button = Button(self.main_window, text="Decrypt image",
                                     command=self.on_decrypt_image)
        self.hide_image_button = Button(self.main_window, text="Hide image",
                                        command=self.on_hide_image)
        self.reveal_image_button = Button(self.main_window, text="Reveal image",
                                        command=self.on_reveal_image)
        self.hide_text_button = Button(self.main_window, text="Hide text",
                                       command=self.on_hide_text)
        self.reveal_text_button = Button(self.main_window, text="Reveal text",
                                       command=self.on_reveal_text)

        self.encrypt_button.grid(row=3, column=0, sticky="wes")
        self.decrypt_button.grid(row=3, column=1, sticky="wes")
        self.hide_image_button.grid(row=4, column=0, sticky="we")
        self.reveal_image_button.grid(row=4, column=1, sticky="we")
        self.hide_text_button.grid(row=5, column=0, sticky="we")
        self.reveal_text_button.grid(row=5, column=1, sticky="we")

    def create_image_listbox(self):
        self.image_display_frame = Frame(self.main_window, bg="white")
        self.image_display_frame.pack_propagate(False)
        self.image_display = Label(self.image_display_frame, bg="white", fg="black", text="No image selected.")
        self.image_display.pack(expand=True, fill="both")
        self.images_listbox = Listbox(self.main_window)
        self.next_page_button = Button(self.main_window, text="Next Page",
                                       command=self.show_next_page,
                                       state=DISABLED)
        self.prev_page_button = Button(self.main_window, text="Previous Page",
                                       command=self.show_prev_page,
                                       state=DISABLED)
        self.add_button = Button(self.main_window, text="Add image",
                                 command=self.add_image, state=DISABLED)
        self.delete_button = Button(self.main_window, text="Delete image",
                                 command=self.delete_image, state=DISABLED)

        self.image_display_frame.grid(row=1, column=0, columnspan=3, sticky="wens")
        self.images_listbox.grid(row=1, column=3, columnspan=2, sticky="wens")
        self.prev_page_button.grid(row=2, column=3, sticky="we")
        self.next_page_button.grid(row=2, column=4, sticky="we")
        self.add_button.grid(row=3, column=3, sticky="we")
        self.delete_button.grid(row=3, column=4, sticky="we")

        self.images_listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

    def on_sign_up(self):
        self.Auth.sign_up()
        if self.Auth.logged_in:
            self.update_button_states()
            self.status.config(
                text=f"Signed in: {self.Auth.current_user.name}")

    def on_sign_in(self):
        self.Auth.sign_in()
        if self.Auth.logged_in:
            self.update_images_list()
            self.status.config(
                text=f"Signed in: {self.Auth.current_user.name}")

    def on_sign_out(self):
        self.Auth.sign_out()
        if not self.Auth.logged_in:
            self.images_listbox.delete(0, END)
            self.current_image_page = 1
            self.clear_image_display()
            self.update_button_states()
            self.status.config(text="Signed out")

    def on_encrypt_image(self):
        image_data = self.get_image_data()
        if image_data:
            self.IH.encrypt_image(image_data)

    def on_decrypt_image(self):
        image_data = self.get_image_data()
        if image_data:
            self.IH.decrypt_image(image_data)

    def on_hide_image(self):
        carrier_image_path, is_from_db = self.get_image_filepath()
        if not carrier_image_path:
            return
        secret_image_data = self.get_image_data()
        if not secret_image_data:
            return
        self.IH.hide_image(carrier_image_path, secret_image_data)
        if is_from_db:
            remove(carrier_image_path)

    def on_reveal_image(self):
        image_path, is_from_db = self.get_image_filepath()
        if not image_path:
            return
        self.IH.reveal_image(image_path)
        if is_from_db:
            remove(image_path)

    def on_hide_text(self):
        image_path, is_from_db = self.get_image_filepath()
        if not image_path:
            return
        choice = messagebox.askyesnocancel('Text input', 'Do you want to select a text file?')
        if choice == None:
            messagebox.showerror('Error', 'Operation canceled.')
            return
        if choice == True:
            text_filepath = filedialog.askopenfilename(
                filetypes=[('Text to hide', '*.txt;')])
            if not text_filepath:
                messagebox.showerror('Error', 'Operation canceled.')
                return
            with open(text_filepath, 'r') as f:
                try:
                    text = f.read()
                except UnicodeDecodeError as e:
                    messagebox.showerror('Error', 'Invalid characters found in text file.')
        else:
            text = simpledialog.askstring('Text', 'Enter text to hide:')
            if text is None or text == '':
                messagebox.showerror('Error', 'Operation canceled.')
                return
            try:
                with NamedTemporaryFile(mode='w') as temp_file:
                    temp_file.write(text)
            except UnicodeEncodeError:
                messagebox.showerror('Error', 'Invalid characters found in text.')
                return

        self.IH.hide_text(image_path, text)

    def on_reveal_text(self):
        image_path, is_from_db = self.get_image_filepath()
        if not image_path:
            return
        self.IH.reveal_text(image_path)
        if is_from_db:
            remove(image_path)

    def quit(self):
        self.main_window.destroy()

    def update_button_states(self):
        if self.Auth.logged_in:
            self.sign_in_button.config(state=DISABLED)
            self.sign_up_button.config(state=DISABLED)
            self.sign_out_button.config(state=NORMAL)
            self.add_button.config(state=NORMAL)
            self.delete_button.config(state=NORMAL)
        else:
            self.sign_in_button.config(state=NORMAL)
            self.sign_up_button.config(state=NORMAL)
            self.sign_out_button.config(state=DISABLED)
            self.add_button.config(state=DISABLED)
            self.delete_button.config(state=DISABLED)
        if self.images_listbox.size() < 10:
            self.next_page_button.config(state=DISABLED)
        else:
            self.next_page_button.config(state=NORMAL)
        if self.current_image_page > 1:
            self.prev_page_button.config(state=NORMAL)
        else:
            self.prev_page_button.config(state=DISABLED)

    def show_next_page(self):
        self.current_image_page += 1
        self.update_images_list()
        if self.images_listbox.size() == 0:
            self.current_image_page -= 1
            self.update_images_list()

    def show_prev_page(self):
        if self.current_image_page > 1:
            self.current_image_page -= 1
            self.update_images_list()

    def update_images_list(self):
        offset = (self.current_image_page - 1) * self.images_per_page
        images = self.Auth.db_handler.get_images_by_user_id(
            self.Auth.current_user.id,
            limit=self.images_per_page,
            offset=offset)
        self.images_listbox.delete(0, END)
        for image in images:
            self.images_listbox.insert(END, image)
        self.update_button_states()

    def add_image(self):
        image_path = filedialog.askopenfilename(filetypes=[('Image', '*.jpg;*.jpeg;*.png;')])
        if not image_path:
            return
        image_name = basename(image_path)
        with open(image_path, "rb") as f:
            image_data = f.read()
        try:
            self.Auth.db_handler.add_image(self.Auth.current_user.id,
                                           image_name, image_data)
        except IntegrityError as e:
            return
        self.update_images_list()
        messagebox.showinfo('Success', 'Image added successfully.')

    def delete_image(self):
        selected_image = self.images_listbox.curselection()
        if not selected_image:
            messagebox.showerror('Error', 'No image selected.')
            return
        image_name = self.images_listbox.get(selected_image[0])
        selection = messagebox.askquestion('Confirm Delete', f'Are you sure you want to delete {image_name}?')
        if selection == 'yes':
            self.Auth.db_handler.delete_image(self.Auth.current_user.id, image_name)
            self.update_images_list()
            messagebox.showinfo('Success', 'Image deleted successfully.')

    def get_image_data(self):
        if not self.listbox_has_selection():
            image_data = self.select_image_from_device()
        else:
            selection = messagebox.askquestion('Select Image',
                                               'Do you want to use the database selection?')
            if selection == 'yes':
                image_data = self.select_image_from_db()
            else:
                image_data = self.select_image_from_device()
        return image_data

    def get_image_filepath(self):
        is_from_db = False
        if not self.listbox_has_selection():
            filepath = self.select_image_filepath_from_device()
        else:
            selected_image = self.images_listbox.curselection()
            selection = messagebox.askquestion('Select Image',
                                               'Do you want to use the database selection?')
            if selection == 'yes':
                image_data = self.select_image_from_db()
                filepath = "temp_image_from_db.png"
                with open(filepath, "wb") as file:
                    file.write(image_data)
                is_from_db = True
            else:
                filepath = self.select_image_filepath_from_device()
        return filepath, is_from_db

    def select_image_from_db(self):
        selected_image = self.images_listbox.curselection()
        if selected_image:
            image_name = self.images_listbox.get(selected_image[0])
            image = self.Auth.db_handler.get_image_by_name(
                self.Auth.current_user.id, image_name)
            if image:
                return image[3]
            else:
                messagebox.showerror('Error', 'Image not found in the database.')
                return None
        else:
            messagebox.showerror('Error', 'No image selected.')
            return None

    def select_image_from_device(self):
        filepath = filedialog.askopenfilename(
            filetypes=[('Image', '*.jpg;*.jpeg;*.png;')])
        if not filepath:
            messagebox.showerror('Error', 'Operation canceled.')
            return None
        with open(filepath, 'rb') as file:
            image_data = file.read()
        return image_data

    def select_image_filepath_from_device(self):
        filepath = filedialog.askopenfilename(
            filetypes=[('Image', '*.jpg;*.jpeg;*.png;')])
        if not filepath:
            messagebox.showerror('Error', 'Operation canceled.')
            return None
        return filepath

    def listbox_has_selection(self):
        return bool(self.images_listbox.curselection())

    def fetch_image_data(self):
        selected_image = self.images_listbox.curselection()
        if selected_image:
            image_name = self.images_listbox.get(selected_image[0])
            image = self.Auth.db_handler.get_image_by_name(
                self.Auth.current_user.id, image_name)
            if image:
                return image[3]
        else:
            return None

    def display_image(self):
        image_data = self.fetch_image_data()
        if not image_data:
            self.clear_image_display()
        else:
            try:
                image_stream = BytesIO(image_data)
                image = Image.open(image_stream)
                width = self.image_display_frame.winfo_width()
                image.thumbnail((width, image.height))
                tk_image = ImageTk.PhotoImage(image)
                self.photo_image = tk_image
                self.image_display.config(image=self.photo_image)
                self.image_display.config(text="")
            except UnidentifiedImageError as e:
                self.image_display.config(image='', text='Cannot display image.')

    def on_listbox_select(self, event):
        self.display_image()

    def clear_image_display(self):
        self.image_display.config(image='', text='No image selected.')

if __name__ == "__main__":
    CryptoCanvas()
