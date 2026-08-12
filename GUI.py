# IMPORTS

import tkinter as tk
from tkinter import messagebox
import sqlite3

# DATABASE

connection = sqlite3.connect("library.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS books(
    book_id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    year INTEGER
)
""")

connection.commit()

# FUNCTIONS

def add_book():
    title = title_entry.get()
    author = author_entry.get()

    if title == "" or author == "":
        result_label.config(
            text="Please enter a title and author.",
            fg="red"
        )
        return

    try:
        year = int(year_entry.get())
    except ValueError:
        result_label.config(
            text="Please enter a valid year.",
            fg="red"
        )
        return

    cursor.execute("""
    INSERT INTO books(title, author, year)
    VALUES (?, ?, ?)
    """, (title, author, year))

    connection.commit()

    result_label.config(
        text="Book added successfully!",
        fg="green"
    )

    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)

    show_books()

def show_books():
    books_listbox.delete(0, tk.END)

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    for book in books:
        books_listbox.insert(
            tk.END,
            f"{book[0]} | {book[1]} | {book[2]} | {book[3]}"
        )

def select_book(event):
    selected = books_listbox.curselection()

    if selected:
        index = selected[0]

        book = books_listbox.get(index)

        parts = book.split(" | ")

        title_entry.delete(0, tk.END)
        title_entry.insert(0, parts[1])

        author_entry.delete(0, tk.END)
        author_entry.insert(0, parts[2])

        year_entry.delete(0, tk.END)
        year_entry.insert(0, parts[3])

def update_book():
    selected = books_listbox.curselection()

    if not selected:
        result_label.config(
            text="Please select a book first.",
            fg="red"
        )
        return

    index = selected[0]

    book = books_listbox.get(index)

    parts = book.split(" | ")

    book_id = int(parts[0])

    title = title_entry.get()
    author = author_entry.get()
    year = int(year_entry.get())

    cursor.execute("""
    UPDATE books
    SET title = ?, author = ?, year = ?
    WHERE book_id = ?
    """, (title, author, year, book_id))

    connection.commit()

    result_label.config(
        text="Book updated successfully!",
        fg="green"
    )
    show_books()


def delete_book():
    selected = books_listbox.curselection()

    if not selected:
        result_label.config(
            text="Please select a book first.",
            fg="red"
        )
        return

    index = selected[0]

    book = books_listbox.get(index)

    parts = book.split(" | ")

    book_id = int(parts[0])

    confirm = messagebox.askyesno(
        "Confirm delete",
        f"Are you sure you want to delete '{parts[1]}'? "
    )
    if not confirm:
        return

    cursor.execute("""
    DELETE FROM books
    WHERE book_id = ?
    """, (book_id,))

    connection.commit()

    result_label.config(
        text="Book deleted successfully!",
        fg="green"
    )

    show_books()

    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)

def clear_fields():
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)

    result_label.config(
        text=""
        )

def close_app():
    connection.close()
    window.destroy()

# GUI

window = tk.Tk()


window.title("Library Management System")
window.geometry("600x500")

heading_label = tk.Label(
    window,
    text="📚 Library Management System",
    font=("Arial", 20, "bold"),
    fg="darkblue"
)

heading_label.pack(pady=25)
input_frame = tk.Frame(window)
input_frame.pack(pady=10)


title_label = tk.Label(input_frame, text="Title:")
title_label.grid(row=0, column=0, padx=5, pady=5)

title_entry = tk.Entry(input_frame, width=30)
title_entry.grid(row=0, column=1, padx=5, pady=5)

author_label = tk.Label(input_frame, text="Author:")
author_label.grid(row=1, column=0, padx=5, pady=5)

author_entry = tk.Entry(input_frame, width=30)
author_entry.grid(row=1, column=1, padx=5,pady=5)

year_label = tk.Label(input_frame, text="Year:")
year_label.grid(row=2, column=0, padx=5, pady=5)

year_entry = tk.Entry(input_frame, width=30)
year_entry.grid(row=2, column=1, padx=5, pady=5)

button_frame = tk.Frame(window)
button_frame.pack(pady=10)

add_button = tk.Button(
    button_frame, 
    text="Add book",
    command=add_book,
    width=12
)

add_button.grid(row=0, column=0, padx=5, pady=5)

result_label = tk.Label(window, text="")
result_label.pack()

books_listbox = tk.Listbox(window, width=60, height=10, font=("Arial", 11))
books_listbox.pack()
books_listbox.bind("<<ListboxSelect>>", select_book)


show_button = tk.Button(
    button_frame,
    text="View Books",
    command=show_books,
    width=12
)
show_button.grid(row=0, column=1, padx=5, pady=5)

update_button = tk.Button(
    button_frame, 
    text="Update Book",
    command=update_book,
    width=12
)

update_button.grid(row=1, column=0, padx=5, pady=5)

delete_button = tk.Button(
    button_frame,
    text="Delete Book",
    command=delete_book,
    width=12
)

delete_button.grid(row=1, column=1, padx=5, pady=5)

clear_button = tk.Button(
    button_frame,
    text="Clear",
    command=clear_fields,
    width=12
)

clear_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

window.protocol("WM_DELETE_WINDOW", close_app)

# RUN APPLICATION

window.mainloop()
