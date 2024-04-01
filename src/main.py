
from tkinter import *
from tkinter import filedialog, messagebox
from Authenticator import Authenticator
from ImageHandler import ImageHandler
import os

class CryptoCanvas:
    def __init__(self):
        self.Auth = Authenticator()
        self.IH = ImageHandler()
        # Create the GUI.
        self.main_window = Tk()
        self.main_window.title("CryptoCanvas")
        self.main_window.resizable(width=False, height=False)

        self.status = Label(self.main_window, font=("Times", 12),
                              text="Signed out")

        self.sign_in_button = Button(self.main_window, text="Sign in",
                                       command=self.on_signin)
        self.sign_up_button = Button(self.main_window, text="Sign up",
                                       command=self.on_signup)
        self.sign_out_button = Button(self.main_window, text="Sign out",
                                       command=self.on_signout, state=DISABLED)

        self.encrypt_button = Button(self.main_window, text="Encrypt image",
                                       command=self.IH.encrypt_image)
        self.decrypt_button = Button(self.main_window, text="Decrypt image",
                                       command=self.IH.decrypt_image)

        self.hide_image_button = Button(self.main_window, text="Hide image",
                                       command=self.IH.hide_image)
        self.find_image_button = Button(self.main_window, text="Reveal image",
                                       command=self.IH.reveal_image)

        self.hide_text_button = Button(self.main_window, text="Hide text",
                                       command=self.IH.hide_text)
        self.find_text_button = Button(self.main_window, text="Reveal text",
                                       command=self.IH.reveal_text)

        self.quit_button = Button(self.main_window, text="Quit",
                                    command=self.quit)

        self.images_listbox = Listbox(self.main_window)
        self.current_image_page = 1
        self.images_per_page = 10
        self.next_page_button = Button(self.main_window, text="Next Page",
                                       command=self.show_next_page, state=DISABLED)
        self.prev_page_button = Button(self.main_window, text="Previous Page",
                                       command=self.show_prev_page, state=DISABLED)

        self.add_button = Button(self.main_window, text="Add image",
                                  command=self.add_image, state=DISABLED)

        # Place all the components into the window.
        self.status.grid(row=0, column=0, columnspan=4)

        self.sign_in_button.grid(row=1, column=1, sticky=W+E)
        self.sign_up_button.grid(row=1, column=2, sticky=W+E)
        self.sign_out_button.grid(row=1, column=3, sticky=W+E)

        self.encrypt_button.grid(row=2, column=1, sticky=W+E)
        self.decrypt_button.grid(row=2, column=2, sticky=W+E)

        self.hide_image_button.grid(row=3, column=1, sticky=W+E)
        self.find_image_button.grid(row=3, column=2, sticky=W+E)

        self.hide_text_button.grid(row=4, column=1, sticky=W+E)
        self.find_text_button.grid(row=4, column=2, sticky=W+E)

        self.images_listbox.grid(row=0, column=4, rowspan=4, columnspan=2, sticky=W+E)
        self.next_page_button.grid(row=4, column=5, sticky=W+E)
        self.prev_page_button.grid(row=4, column=4, sticky=W+E)
        self.add_button.grid(row=5, column=4, sticky=W+E)
        self.quit_button.grid(row=5, column=5, sticky=W+E)


        # Wait for input.
        self.main_window.mainloop()

    def on_signup(self):
        self.Auth.sign_up()
        if self.Auth.logged_in:
            self.update_button_states()
            self.status.config(text=f"Signed in: {self.Auth.current_user.name}")

    def on_signin(self):
        self.Auth.sign_in()
        if self.Auth.logged_in:
            self.update_button_states()
            self.update_images_list()
            self.status.config(text=f"Signed in: {self.Auth.current_user.name}")

    def on_signout(self):
        self.Auth.sign_out()
        if not self.Auth.logged_in:
            self.images_listbox.delete(0, END)
            self.current_image_page = 1
            self.update_button_states()
            self.status.config(text="Signed out")

    def quit(self):
        self.main_window.destroy()

    def update_button_states(self):
        if self.Auth.logged_in:
            self.sign_in_button.config(state=DISABLED)
            self.sign_up_button.config(state=DISABLED)
            self.sign_out_button.config(state=NORMAL)
            self.next_page_button.config(state=NORMAL)
            self.add_button.config(state=NORMAL)
        else:
            self.sign_in_button.config(state=NORMAL)
            self.sign_up_button.config(state=NORMAL)
            self.sign_out_button.config(state=DISABLED)
            self.next_page_button.config(state=DISABLED)
            self.prev_page_button.config(state=DISABLED)
            self.add_button.config(state=DISABLED)
        if self.current_image_page > 1:
            self.prev_page_button.config(state=NORMAL)
        else:
            self.prev_page_button.config(state=DISABLED)

    def show_next_page(self):
        self.current_image_page += 1
        self.update_images_list()
        if not self.images_listbox.get(0, END):
            self.current_image_page -= 1
            self.update_images_list()

    def show_prev_page(self):
        if self.current_image_page > 1:
            self.current_image_page -= 1
            self.update_images_list()

    def update_images_list(self):
        offset = (self.current_image_page - 1) * self.images_per_page
        images = self.Auth.db_handler.get_images_by_user_id(self.Auth.current_user.id,
                                                            limit=self.images_per_page,
                                                            offset=offset)
        self.images_listbox.delete(0, END)
        for image in images:
            self.images_listbox.insert(END, image)

    def add_image(self):
        # Ask user to select an image file
        image_path = filedialog.askopenfilename(title="Select Image",
                                                filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if not image_path:
            return
        image_name = os.path.basename(image_path)
        with open(image_path, "rb") as f:
            image_data = f.read()
        self.Auth.db_handler.add_image(self.Auth.current_user.id, image_name, image_data)
        self.update_images_list()
        messagebox.showinfo('Success', 'Image added successfully.')

if __name__ == "__main__":
    CryptoCanvas()
