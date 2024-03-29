
from tkinter import *
from Authenticator import Authenticator
from ImageHandler import ImageHandler

class CryptoCanvas:
    def __init__(self):
        self.Auth = Authenticator()
        self.IH = ImageHandler()
        # Create the GUI.
        self.main_window = Tk()
        self.main_window.title("CryptoCanvas")
        self.main_window.resizable(width=False, height=False)

        self.status = Label(self.main_window, font=("Times", 12),
                              text="Status")

        self.sign_in_button = Button(self.main_window, text="Sign in",
                                       command=self.Auth.sign_in, state=DISABLED)
        self.sign_up_button = Button(self.main_window, text="Sign up",
                                       command=self.Auth.sign_up, state=DISABLED)
        self.sign_out_button = Button(self.main_window, text="Sign out",
                                       command=self.Auth.sign_out, state=DISABLED)

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

        self.quit_button.grid(row=5, column=3, sticky=W+E)

        # Wait for input.
        self.main_window.mainloop()

    def quit(self):
        self.main_window.destroy()


if __name__ == "__main__":
    CryptoCanvas()
