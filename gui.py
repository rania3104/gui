from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO
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

    # Destroy the existing widgets in books_info_frame
    for widget in books_info_frame.winfo_children():
        widget.destroy()

    # Add a canvas for the books info frame with a vertical scrollbar
    canvas = Canvas(books_info_frame, bg="white")
    scrollbar = Scrollbar(books_info_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a new frame to hold the book information
    books_info_frame_inner = Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=books_info_frame_inner, anchor="nw")

    for i in range(0, len(book)):
        # Retrieve book cover
        cover_url = book[i]['attributes']['cover']
        cover_response = requests.get(cover_url)
        cover_image = Image.open(BytesIO(cover_response.content))
        cover_image = cover_image.resize((70, 120))  # Resize the image for display

        # Display book cover above the book title
        cover_image = ImageTk.PhotoImage(cover_image)
        cover_label = Label(books_info_frame_inner, image=cover_image)
        cover_label.image = cover_image
        cover_label.grid(row=i // 3 * 5, column=i % 3, pady=2)

        # Display book title below the cover
        book_title = book[i]['attributes']['title']
        book_title_label = Label(books_info_frame_inner, text=book_title, font=('Arial', 10, 'bold'))
        book_title_label.grid(row=i // 3 * 5 + 1, column=i % 3, pady=2)

        # Display book date below the book title
        book_date = book[i]['attributes']['release_date']
        book_date_label = Label(books_info_frame_inner, text=book_date, font=('Arial', 8))
        book_date_label.grid(row=i // 3 * 5 + 2, column=i % 3, pady=2)

        # Display book summary below the release date
        book_summary = book[i]['attributes']['summary']
        book_summary_label = Label(books_info_frame_inner, text=book_summary, font=('Arial', 8), wraplength=250, justify='left')
        book_summary_label.grid(row=i // 3 * 5 + 3, column=i % 3, pady=2)

        # Add an empty space as a separator
        Label(books_info_frame_inner, text='', font=('Arial', 2)).grid(row=i // 3 * 5 + 4, column=i % 3)

    # Update the canvas to include the new frame
    books_info_frame_inner.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def get_movies_data():
    url = f"https://api.potterdb.com/v1/movies"
    response = requests.get(url)
    data = response.json()

    with open("movies.json", 'w') as file:
        json.dump(data, file, indent=6)

    movie = data['data']

    # Destroy the existing widgets in movies_info_frame
    for widget in movies_info_frame.winfo_children():
        widget.destroy()

    # Add a canvas for the movies info frame with a vertical scrollbar
    canvas = Canvas(movies_info_frame, bg="white")
    scrollbar = Scrollbar(movies_info_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a new frame to hold the movie information
    movies_info_frame_inner = Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=movies_info_frame_inner, anchor="nw")

    for i in range(0, len(movie)):
        # Retrieve movie poster
        poster_url = movie[i]['attributes']['poster']
        poster_response = requests.get(poster_url)
        poster_image = Image.open(BytesIO(poster_response.content))
        poster_image = poster_image.resize((70, 120))  # Resize the image for display

        # Display movie poster above the movie title
        poster_image = ImageTk.PhotoImage(poster_image)
        poster_label = Label(movies_info_frame_inner, image=poster_image)
        poster_label.image = poster_image
        poster_label.grid(row=i // 3 * 6, column=i % 3, pady=2)

        # Display movie title below the poster
        movie_title = movie[i]['attributes']['title']
        movie_title_label = Label(movies_info_frame_inner, text=movie_title, font=('Arial', 10, 'bold'))
        movie_title_label.grid(row=i // 3 * 6 + 1, column=i % 3, pady=2)

        # Display movie date below the movie title
        movie_date = movie[i]['attributes']['release_date']
        movie_date_label = Label(movies_info_frame_inner, text=f"Release Date: {movie_date}", font=('Arial', 8))
        movie_date_label.grid(row=i // 3 * 6 + 2, column=i % 3, pady=2)
        # Display movie directors below the movie date
        movie_directors = ", ".join(movie[i]['attributes']['directors'])
        movie_directors_label = Label(movies_info_frame_inner, text=f"Directors: {movie_directors}", font=('Arial', 8))
        movie_directors_label.grid(row=i // 3 * 6 + 3, column=i % 3, pady=2)

        # Display movie rating below the movie directors
        movie_rating = movie[i]['attributes']['rating']
        movie_rating_label = Label(movies_info_frame_inner, text=f"Rating: {movie_rating}", font=('Arial', 8))
        movie_rating_label.grid(row=i // 3 * 6 + 4, column=i % 3, pady=2)

        # Display movie running time below the movie rating
        movie_running_time = movie[i]['attributes']['running_time']
        movie_running_time_label = Label(movies_info_frame_inner, text=f"Running Time: {movie_running_time}", font=('Arial', 8))
        movie_running_time_label.grid(row=i // 3 * 6 + 5, column=i % 3, pady=2)


    # Update the canvas to include the new frame
    movies_info_frame_inner.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    
root = Tk()
root.title("Harry Potter World")
root.geometry("880x600")
root.resizable(0, 0)

# Create a main frame for the background image
start_frame = Frame(root, width=880, height=600)
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
replacement_frame = Frame(root, width=880, height=600)
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
    global movies_page_frame, movies_info_frame
    movies_page_frame = Frame(main_frame)

    # Add buttons frame
    buttons_frame = Frame(movies_page_frame)
    buttons_frame.pack(side=TOP, pady=10)

    # Add 'Get Movies Data' button
    get_movies_button = Button(buttons_frame, text="Get Movies Data", font=('Arial', 12), bg="blue", fg="white", command=get_movies_data)
    get_movies_button.pack(side=LEFT, padx=5)

    # Add 'Instructions' button
    instructions_button = Button(buttons_frame, text="Instructions", font=('Arial', 12), bg="green", fg="white", command=lambda: switch_indicator(indicator=movies_indicator, page=replace_start_frame))
    instructions_button.pack(side=LEFT, padx=5)

    # Add 'Exit' button
    exit_button = Button(buttons_frame, text="Exit", font=('Arial', 12), bg="red", fg="white", command=lambda: switch_indicator(indicator=movies_indicator, page=replace_main_frame))
    exit_button.pack(side=LEFT, padx=5)

    # Add movies info frame
    movies_info_frame = Frame(movies_page_frame)
    movies_info_frame.pack(fill=BOTH, expand=True)

    movies_page_frame.pack(fill=BOTH, expand=True)

def characters_page():
    characters_page_frame = Frame(main_frame)

    # Add buttons frame
    buttons_frame = Frame(characters_page_frame)
    buttons_frame.pack(side=TOP, pady=10)

    # Add 'Instructions' button
    instructions_button = Button(buttons_frame, text="Instructions", font=('Arial', 12), bg="green", fg="white", command=lambda: switch_indicator(indicator=characters_indicator, page=replace_start_frame))
    instructions_button.pack(side=LEFT, padx=5)

    # Add 'Exit' button
    exit_button = Button(buttons_frame, text="Exit", font=('Arial', 12), bg="red", fg="white", command=lambda: switch_indicator(indicator=characters_indicator, page=replace_main_frame))
    exit_button.pack(side=LEFT, padx=5)

    characters_page_frame.pack(fill=BOTH, expand=True)

def potions_page():
    potions_page_frame = Frame(main_frame)

    # Add buttons frame
    buttons_frame = Frame(potions_page_frame)
    buttons_frame.pack(side=TOP, pady=10)

    # Add 'Instructions' button
    instructions_button = Button(buttons_frame, text="Instructions", font=('Arial', 12), bg="green", fg="white", command=lambda: switch_indicator(indicator=potions_indicator, page=replace_start_frame))
    instructions_button.pack(side=LEFT, padx=5)

    # Add 'Exit' button
    exit_button = Button(buttons_frame, text="Exit", font=('Arial', 12), bg="red", fg="white", command=lambda: switch_indicator(indicator=potions_indicator, page=replace_main_frame))
    exit_button.pack(side=LEFT, padx=5)

    potions_page_frame.pack(fill=BOTH, expand=True)

def spells_page():
    spells_page_frame = Frame(main_frame)

    # Add buttons frame
    buttons_frame = Frame(spells_page_frame)
    buttons_frame.pack(side=TOP, pady=10)

    # Add 'Instructions' button
    instructions_button = Button(buttons_frame, text="Instructions", font=('Arial', 12), bg="green", fg="white", command=lambda: switch_indicator(indicator=spells_indicator, page=replace_start_frame))
    instructions_button.pack(side=LEFT, padx=5)

    # Add 'Exit' button
    exit_button = Button(buttons_frame, text="Exit", font=('Arial', 12), bg="red", fg="white", command=lambda: switch_indicator(indicator=spells_indicator, page=replace_main_frame))
    exit_button.pack(side=LEFT, padx=5)

    spells_page_frame.pack(fill=BOTH, expand=True)

main_frame = Frame(replacement_frame)
main_frame.pack(fill=BOTH, expand=True)

root.mainloop()
