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

def locate_one_library_for_work(work_id):
    """ Look up one library where a copy of work exists """
    resp = requests.get(SERVER_URL + "/api/works/"+work_id, timeout=20)
    work = resp.json()
    library_url = work["links"]["items"][0]["links"]["collection"]["href"]
    library_url = library_url.rsplit('/', 2)[0] + "/"
    resp = requests.get(SERVER_URL + library_url, timeout=20)
    library = resp.json()
    library_info = library["name"] + ": " + library["city"]
    return library_info


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

def find_work_title_by_book(book_item):
    """ Look up work item based on ID """
    work_url = book_item["links"]["type"]["href"]
    resp = requests.get(SERVER_URL + work_url, timeout=20)
    works = resp.json()
    return works["title"]


def find_all_books():
    """ Look up all books in the system """
    resp = requests.get(SERVER_URL + "/api/books/", timeout=20)
    books = resp.json()
    index = 0
    listbox.delete(0, tk.END)
    for item in books["items"]:
        title = find_work_title_by_book(item)
        listbox.insert(index, str(item["work_id"]) +"; "+ str(title))
        index += 1
    where_is_button.pack()
    resultlabel.pack()

def locate_book_by_listbox_selection():
    """ Look up book based on what was selected in listbox """
    work_id = listbox.get(listbox.curselection())
    work_id = work_id.split(';')[0]
    library_info = locate_one_library_for_work(work_id)
    resultlabel.configure(text=library_info)

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
