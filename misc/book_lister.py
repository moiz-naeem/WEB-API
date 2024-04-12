""" Displays GUI to look up human readable list of books found in any of the system libraries """
import tkinter as tk
import requests




SERVER_URL = "http://localhost:5000"

def find_work(isbn):
    """ Look up work item based on isbn """
    resp = requests.get(SERVER_URL + "/api/works/", timeout=20)
    works = resp.json()
    for item in works["items"]:
        if item["isbn"] == isbn:
            return item
    return "No title found with the requested ISBN. Try looking for 978-4-7659-7000-1"

def find_work_title(work_id):
    """ Look up work item based on ID """
    resp = requests.get(SERVER_URL + "/api/works/", timeout=20)
    works = resp.json()
    return works["items"][work_id-1]["title"]

def locate_book(work_id):
    """ Look up libraries where a copy of work exists """
    resp = requests.get(SERVER_URL + "/api/libraries/", timeout=20)
    libraries = resp.json()
    result_libraries = []
    for item in libraries["items"]:
        #print(item["name"])
        for book in item["books"]:
            #print(book["work_id"])
            #print(work_id)
            if book["work_id"] == work_id:
                result_libraries.append([item["name"], item["city"]])
                #print(item["name"])
    if len(result_libraries) > 0:
        return result_libraries
    return "No books found. Did you populate the database with gen-db ?"


window = tk.Tk()
resultlabel = tk.Label(
    text="", height=20, wraplength=500, justify="left"
)


# create listbox object
listbox = tk.Listbox(window, height = 15,
                  width = 125,
                  bg = "grey",
                  activestyle = 'dotbox')
label = tk.Label(window, text = "Books in the system")

def find_all_books():
    """ Look up all books in the system """
    resp = requests.get(SERVER_URL + "/api/books/", timeout=20)
    books = resp.json()
    index = 0
    listbox.delete(0, tk.END)
    for item in books["items"]:
        title = find_work_title(item["work_id"])
        listbox.insert(index, str(item["work_id"]) +"; "+ str(title))
        index += 1
    where_is_button.pack()
    resultlabel.pack()

def locate_book_by_listbox_selection():
    """ Look up book based on what was selected in listbox """
    work_id = listbox.get(listbox.curselection())
    work_id = work_id.split(';')[0]
    work_id = int(work_id)
    libraries_list = locate_book(work_id)
    resultlabel.configure(text=libraries_list)

list_all_button = tk.Button(window,
    text="List all book titles in the system",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
    command=find_all_books
)
list_all_button.pack()
label.pack()
listbox.pack()


where_is_button = tk.Button(window,
    text="Where is this book?",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
    command=locate_book_by_listbox_selection
)

window.mainloop()
