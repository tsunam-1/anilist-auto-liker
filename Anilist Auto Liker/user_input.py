from tkinter import *

#UI for the user to input their Anilist user details
class InputWindow:

    def __init__(self, username, email, password, load_more):
        self.username = ""
        self.email = ""
        self.password = ""
        self.load_more = ""
        self.window = Tk()
        self.window.title("Anilist Auto Liker")
        self.window.config(padx=10, pady=10)
        self.escape = False

        self.username_label = Label(text="Username:")
        self.username_label.grid(column=0, row=0)
        self.username_label.focus()

        self.email_label = Label(text="Email:")
        self.email_label.grid(column=0, row=1)

        self.password_label = Label(text="Password:")
        self.password_label.grid(column=0, row=2)

        self.load_more_label = Label(text="Load more:")
        self.load_more_label.grid(column=0, row=3)

        self.username_box = Entry(width=25)
        self.username_box.insert(0, username)
        self.username_box.grid(column=1, row=0)

        self.email_box = Entry(width=25)
        self.email_box.insert(0, email)
        self.email_box.grid(column=1, row=1)

        self.password_box = Entry(width=25, show="*")
        self.password_box.insert(0, password)
        self.password_box.grid(column=1, row=2)

        self.load_more_box = Entry(width=25)
        self.load_more_box.insert(0, load_more)
        self.load_more_box.grid(column=1, row=3)

        self.save_button = Button(text="Save", width=25, command=self.save)
        self.save_button.grid(column=1, row=4)

        self.exit_button = Button(text="Exit", width=15, command=self.exit)
        self.exit_button.grid(column=0, row=4)

        self.information = Label(text="20 seconds to solve the reCAPTCHA after saving")
        self.information.grid(column=0, row=5, columnspan=2)

        self.window.mainloop()

    #Saves user details and closes the window
    def save(self):
        self.username = self.username_box.get()
        self.email = self.email_box.get()
        self.password = self.password_box.get()
        self.load_more = self.load_more_box.get()
        self.window.quit()
        self.window.destroy()

    def exit(self):
        self.escape = True
        self.window.quit()
        self.window.destroy()