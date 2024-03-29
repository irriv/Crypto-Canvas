
from tkinter import *
from Authenticator import Authenticator
from ImageHandler import ImageHandler

class CryptoCanvas:

    def __init__(self):
        self.Auth = Authenticator()
        self.IH = ImageHandler()
        # Create the GUI.
        self.__main_window = Tk()
        self.__main_window.title("CryptoCanvas")
        self.__main_window.resizable(width=False, height=False)

        self.__status = Label(self.__main_window, font=("Times", 12),
                              text="Status")

        self.__sign_in_button = Button(self.__main_window, text="Sign in",
                                       command=self.Auth.sign_in)
        self.__sign_up_button = Button(self.__main_window, text="Sign up",
                                       command=self.Auth.sign_up)
        self.__sign_out_button = Button(self.__main_window, text="Sign out",
                                       command=self.Auth.sign_out, state=DISABLED)

        self.__encrypt_button = Button(self.__main_window, text="Encrypt image",
                                       command=self.IH.encrypt_image)
        self.__decrypt_button = Button(self.__main_window, text="Decrypt image",
                                       command=self.IH.decrypt_image)

        self.__hide_image_button = Button(self.__main_window, text="Hide image",
                                       command=self.IH.hide_image)
        self.__find_image_button = Button(self.__main_window, text="Find image",
                                       command=self.IH.find_image)

        self.__hide_text_button = Button(self.__main_window, text="Hide text",
                                       command=self.IH.hide_text)
        self.__find_text_button = Button(self.__main_window, text="Find text",
                                       command=self.IH.find_text)

        self.__quit_button = Button(self.__main_window, text="Quit",
                                    command=self.quit)

        # Place all the components into the window.
        self.__status.grid(row=0, column=0, columnspan=4)

        self.__sign_in_button.grid(row=1, column=1, sticky=W+E)
        self.__sign_up_button.grid(row=1, column=2, sticky=W+E)
        self.__sign_out_button.grid(row=1, column=3, sticky=W+E)

        self.__encrypt_button.grid(row=2, column=1, sticky=W+E)
        self.__decrypt_button.grid(row=2, column=2, sticky=W+E)

        self.__hide_image_button.grid(row=3, column=1, sticky=W+E)
        self.__find_image_button.grid(row=3, column=2, sticky=W+E)

        self.__hide_text_button.grid(row=4, column=1, sticky=W+E)
        self.__find_text_button.grid(row=4, column=2, sticky=W+E)

        self.__quit_button.grid(row=5, column=3, sticky=W+E)

        # Wait for input.
        self.__main_window.mainloop()

    def quit(self):
        self.__main_window.destroy()


if __name__ == "__main__":
    CryptoCanvas()
