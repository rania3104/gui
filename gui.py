from tkinter import *
from PIL import Image, ImageTk
import requests
import json

def replace_start_frame():
    # Function to replace the main frame with the replacement frame
    start_frame.pack_forget()
    replacement_frame.pack()

def replace_main_frame():
    replacement_frame.pack_forget()
    start_frame.pack()

def reset_indicators():
    for child in options_frame.winfo_children():
        if isinstance(child, Label):
            child['bg'] = 'SystemButtonFace'

def switch_indicator(indicator, page):
    reset_indicators()
    if page != replace_start_frame:  # Check if the 'Instructions' button is not clicked
        indicator['bg'] = 'blue'

    for frame in main_frame.winfo_children():
        frame.destroy()
        replacement_frame.update()
    page()

def quit_application():
    root.destroy()

def get_books_data():
    url = f"https://api.potterdb.com/v1/books"
    response = requests.get(url)
    data = response.json()

    with open("books.json", 'w') as file:
        json.dump(data, file, indent=6)

    book = data['data']

    for i in range(0, len(book)):
        book_title = book[i]['attributes']['title']
        book_title_label = Label(books_info_frame, text=book_title, font=('Arial', 10))
        book_title_label.grid(row=i // 3, column=i % 3, pady=2)

root = Tk()
root.title("Harry Potter World")
root.geometry("800x530")
root.resizable(0, 0)

# Create a main frame for the background image
start_frame = Frame(root, width=800, height=530)
start_frame.pack_propagate(0)  # Disable automatic resizing of the main frame
start_frame.pack()

# Load the background image using PIL
image = Image.open("background_image.png")  # Replace "background_image.png" with your image file
background_image = ImageTk.PhotoImage(image)

# Create a label to display the background image
background_label = Label(start_frame, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Create a secondary frame for text and button
text_frame = Frame(start_frame, bg="white")  # Set background color to white
text_frame.place(relx=0, rely=0.6, relwidth=1, relheight=0.3)

# Add large text "Harry Potter" to the secondary frame
title_label = Label(text_frame, text="Harry Potter", font=("Arial", 24), bg="white")
title_label.pack(pady=10)

# Add smaller text "Find all the information on Harry Potter here!" to the secondary frame
info_label = Label(text_frame, text="Find all the information on Harry Potter here!", font=("Arial", 12), bg="white")
info_label.pack()

# Add a button to the secondary frame that calls the replace_main_frame function
start_button = Button(text_frame, text="Start", font=("Arial", 16), bg="green", fg="white", command=lambda: [replace_start_frame(), reset_indicators()])
start_button.pack(side=LEFT, padx=10, pady=10)

# Add a Quit button in the same horizontal line
quit_button = Button(text_frame, text="Quit", font=("Arial", 16), bg="red", fg="white", command=quit_application)
quit_button.pack(side=LEFT, padx=10, pady=10)

# Create a replacement frame with the same size
replacement_frame = Frame(root, width=800, height=530)
replacement_frame.pack_propagate(0)  # Disable automatic resizing of the replacement frame

options_frame = Frame(replacement_frame)

books_button = Button(options_frame, text="Books", font=('Arial',13), bd=0, fg='blue', activeforeground="blue",
                      command=lambda: switch_indicator(indicator=books_indicator, page=books_page))
books_button.place(x=0, y=0, width=160,height=50)

books_indicator= Label(options_frame)
books_indicator.place(x=40, y=46, width=80, height=3)

movies_button = Button(options_frame, text="Movies", font=('Arial',13), bd=0, fg='blue', activeforeground="blue",
                      command=lambda: switch_indicator(indicator=movies_indicator, page=movies_page))
movies_button.place(x=160, y=0, width=160,height=50)

movies_indicator= Label(options_frame)
movies_indicator.place(x=200, y=46, width=80, height=3)

characters_button = Button(options_frame, text="Characters", font=('Arial',13), bd=0, fg='blue', activeforeground="blue",
                      command=lambda: switch_indicator(indicator=characters_indicator, page=characters_page))
characters_button.place(x=320, y=0, width=160,height=50)

characters_indicator= Label(options_frame)
characters_indicator.place(x=360, y=46, width=80, height=3)

potions_button = Button(options_frame, text="Potions", font=('Arial',13), bd=0, fg='blue', activeforeground="blue",
                      command=lambda: switch_indicator(indicator=potions_indicator, page=potions_page))
potions_button.place(x=480, y=0, width=160,height=50)

potions_indicator= Label(options_frame)
potions_indicator.place(x=520, y=46, width=80, height=3)

spells_button = Button(options_frame, text="Spells", font=('Arial',13), bd=0, fg='blue', activeforeground="blue",
                      command=lambda: switch_indicator(indicator=spells_indicator, page=spells_page))
spells_button.place(x=640, y=0, width=160,height=50)

spells_indicator= Label(options_frame)
spells_indicator.place(x=680, y=46, width=80, height=3)

options_frame.pack(pady=5)
options_frame.pack_propagate(False)
options_frame.configure(width=800,height=60)

def books_page():
    global books_page_frame, books_info_frame
    books_page_frame = Frame(main_frame)

    # Add buttons frame
    buttons_frame = Frame(books_page_frame)
    buttons_frame.pack(side=TOP, pady=10)

    # Add 'Get Books Data' button
    get_books_button = Button(buttons_frame, text="Get Books Data", font=('Arial', 12), bg="blue", fg="white", command=get_books_data)
    get_books_button.pack(side=LEFT, padx=5)

    # Add 'Instructions' button
    instructions_button = Button(buttons_frame, text="Instructions", font=('Arial', 12), bg="green", fg="white", command=lambda: switch_indicator(indicator=books_indicator, page=replace_start_frame))
    instructions_button.pack(side=LEFT, padx=5)

    # Add 'Exit' button
    exit_button = Button(buttons_frame, text="Exit", font=('Arial', 12), bg="red", fg="white", command=lambda: switch_indicator(indicator=books_indicator, page=replace_main_frame))
    exit_button.pack(side=LEFT, padx=5)

    # Add books info frame
    books_info_frame = Frame(books_page_frame)
    books_info_frame.pack(fill=BOTH, expand=True)

    books_page_frame.pack(fill=BOTH, expand=True)

def movies_page():
    movies_page_frame = Frame(main_frame)
    movies_page_label = Label(movies_page_frame, text="Movies Page", font=('Arial', 25), fg='blue')
    movies_page_label.pack(pady=80)

    # Add 'Instructions' button
    instructions_button = Button(movies_page_frame, text="Instructions", font=('Arial', 16), bg="green", fg="white", command=lambda: switch_indicator(indicator=movies_indicator, page=replace_start_frame))
    instructions_button.pack(pady=10)

    # Add 'Exit' button
    exit_button = Button(movies_page_frame, text="Exit", font=('Arial', 16), bg="red", fg="white", command=lambda: switch_indicator(indicator=movies_indicator, page=replace_main_frame))
    exit_button.pack(pady=10)

    movies_page_frame.pack(fill=BOTH, expand=True)

def characters_page():
    characters_page_frame = Frame(main_frame)
    characters_page_label = Label(characters_page_frame, text="Characters Page", font=('Arial', 25), fg='blue')
    characters_page_label.pack(pady=80)

    # Add 'Instructions' button
    instructions_button = Button(characters_page_frame, text="Instructions", font=('Arial', 16), bg="green", fg="white", command=lambda: switch_indicator(indicator=characters_indicator, page=replace_start_frame))
    instructions_button.pack(pady=10)

    # Add 'Exit' button
    exit_button = Button(characters_page_frame, text="Exit", font=('Arial', 16), bg="red", fg="white", command=lambda: switch_indicator(indicator=characters_indicator, page=replace_main_frame))
    exit_button.pack(pady=10)

    characters_page_frame.pack(fill=BOTH, expand=True)

def potions_page():
    potions_page_frame = Frame(main_frame)
    potions_page_label = Label(potions_page_frame, text="Potions Page", font=('Arial', 25), fg='blue')
    potions_page_label.pack(pady=80)

    # Add 'Instructions' button
    instructions_button = Button(potions_page_frame, text="Instructions", font=('Arial', 16), bg="green", fg="white", command=lambda: switch_indicator(indicator=potions_indicator, page=replace_start_frame))
    instructions_button.pack(pady=10)

    # Add 'Exit' button
    exit_button = Button(potions_page_frame, text="Exit", font=('Arial', 16), bg="red", fg="white", command=lambda: switch_indicator(indicator=potions_indicator, page=replace_main_frame))
    exit_button.pack(pady=10)

    potions_page_frame.pack(fill=BOTH, expand=True)

def spells_page():
    spells_page_frame = Frame(main_frame)
    spells_page_label = Label(spells_page_frame, text="Spells Page", font=('Arial', 25), fg='blue')
    spells_page_label.pack(pady=80)

    # Add 'Instructions' button
    instructions_button = Button(spells_page_frame, text="Instructions", font=('Arial', 16), bg="green", fg="white", command=lambda: switch_indicator(indicator=spells_indicator, page=replace_start_frame))
    instructions_button.pack(pady=10)

    # Add 'Exit' button
    exit_button = Button(spells_page_frame, text="Exit", font=('Arial', 16), bg="red", fg="white", command=lambda: switch_indicator(indicator=spells_indicator, page=replace_main_frame))
    exit_button.pack(pady=10)
    spells_page_frame.pack(fill=BOTH, expand=True)


main_frame = Frame(replacement_frame)
main_frame.pack(fill=BOTH, expand=True)

root.mainloop()
