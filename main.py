from tkinter import *
import tkinter
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [(random.choice(letters)) for _ in range(nr_letters)]
    password_symbols = [(random.choice(symbols)) for _ in range(nr_symbols)]
    password_numbers = [(random.choice(numbers)) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers

    random.shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_username_entry.get()
    password = password_entry.get()
    new_data = {
        website:{
            "Email": email,
            "Password": password
        }
    }

    if len(website) == 0 and len(password) == 0:
        messagebox.showerror(title="Ooops!",
                             message="Please don't leave any fields empty! \nPassword and Website are not defined"
                                     "\nTry again")
    elif len(website) == 0:
        messagebox.showerror(title="Ooops!",
                             message="Please don't leave any fields empty! \nWebsite is not defined"
                                     "\nTry again")
    elif len(password) == 0:
        messagebox.showerror(title="Ooops!",
                            message="Please don't leave any fields empty! \nPassword is not defined"
                                    "\nTry again")
    else:
        try:
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)

        except FileNotFoundError:
            with open("data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", mode="w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
    return new_data
# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json", mode="r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error",
                             message="No Data File Found")
    else:
        if website in data:
            email = data[website]["Email"]
            password = data[website]["Password"]
            messagebox.showinfo(title=website, message=f"Email: "
                                                       f"{email}\nPassword: {password}")
        else:
            messagebox.showerror(title="Error",
                                 message=f"No details for the {website} exists")
# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_image = tkinter.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=0)

#Labels
website_label = tkinter.Label(text="Website:")
website_label.grid(column=0, row=1)
email_username = tkinter.Label(text="Email/Username:")
email_username.grid(column=0, row=2)
password_label = tkinter.Label(text="Password:")
password_label.grid(column=0, row=3)

#Buttons
generate_password_button = tkinter.Button(text="Generate Password", activebackground="white", width=14, highlightthickness=0, command=generate_password)
generate_password_button.grid(column=2, row=3, sticky="w")
search_button = tkinter.Button(text="Search", activebackground="white", width=14, highlightthickness=0, command=find_password)
search_button.grid(column=2, row=1, sticky="w")
add_button = tkinter.Button(text="Add", activebackground="white", width=43, highlightthickness=0, command=save)
add_button.grid(column=1, row=4, sticky="w", columnspan=2)

#Entries
website_entry = tkinter.Entry(width=32, highlightthickness=0)
website_entry.grid(column=1, row=1, sticky="w")
website_entry.focus()
email_username_entry = tkinter.Entry(width=51, highlightthickness=0)
email_username_entry.grid(column=1, row=2, sticky="w", columnspan=2)
email_username_entry.insert(0, "your@email.com")
password_entry = tkinter.Entry(width=32, highlightthickness=0)
password_entry.grid(column=1, row=3, sticky="w")
window.mainloop()