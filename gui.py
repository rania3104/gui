from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO
import requests
import json
from random import randint
from tkinter import PhotoImage

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
            child['bg'] = '#41347D'

def switch_indicator(indicator, page):
    reset_indicators()
    if page != replace_start_frame:  # Check if the 'Instructions' button is not clicked
        indicator['bg'] = 'white'

    for widget in main_frame.winfo_children():
        # Hide or deactivate the widgets instead of destroying them
        widget.pack_forget()  # You can use widget.pack() to restore visibility

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
    canvas = Canvas(books_info_frame, bg="#EFD78E", highlightbackground="#EFD78E")
    scrollbar = Scrollbar(books_info_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a new frame to hold the book information
    books_info_frame_inner = Frame(canvas, bg="#EFD78E")
    canvas.create_window((0, 0), window=books_info_frame_inner, anchor="nw")

    for i in range(0, len(book)):
        # Retrieve book cover
        cover_url = book[i]['attributes']['cover']
        cover_response = requests.get(cover_url)
        cover_image = Image.open(BytesIO(cover_response.content))
        cover_image = cover_image.resize((120, 180))  # Resize the image for display

        # Display book cover above the book title
        cover_image = ImageTk.PhotoImage(cover_image)
        cover_label = Label(books_info_frame_inner, image=cover_image, bg="#EFD78E")
        cover_label.image = cover_image
        cover_label.grid(row=i // 3 * 5, column=i % 3, pady=2)

        # Display book title below the cover
        book_title = book[i]['attributes']['title']
        book_title_label = Label(books_info_frame_inner, text=book_title, font=('Georgia', 10, 'bold'), wraplength=280, bg='#EFD78E')
        book_title_label.grid(row=i // 3 * 5 + 1, column=i % 3, pady=2, padx=12)

        # Display book date below the book title
        book_date = book[i]['attributes']['release_date']
        book_date_label = Label(books_info_frame_inner, text=f"Release Date: {book_date}", font=('Times New Roman', 8), bg="#EFD78E")
        book_date_label.grid(row=i // 3 * 5 + 2, column=i % 3, pady=2)

        book_summary = book[i]['attributes']['summary']

        # Create a button to show the summary when clicked
        show_summary_button = Button(books_info_frame_inner, text=f"Show Summary", font=('Georgia', 8),
                                     command=lambda i=i, summary=book_summary: show_summary(i, summary),
                                     bg="#D0A933")  # Set a specific background color (e.g., yellow)
        show_summary_button.grid(row=i // 3 * 5 + 4, column=i % 3, pady=2, ipadx=20, ipady=5)

        # Add an empty space as a separator
    # Update the canvas to include the new frame
    books_info_frame_inner.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def show_summary(index, summary):
    # Create a new frame for displaying the summary
    summary_frame = Toplevel()
    summary_frame.title("Book Summary")
    summary_frame.geometry("400x340")
    summary_frame.configure(bg="#B09DE4")

    summary_title = Label (summary_frame, text= "SUMMARY", font=('Georgia', 14, 'bold'), bg='#B09DE4')
    summary_title.pack(pady=10)
    # Display the book summary
    summary_label = Label(summary_frame, text=summary, font=('Georgia', 12), wraplength=380, justify='left', bg='#B09DE4')
    summary_label.pack(pady=10)

    # Add a button to close the summary
    close_button = Button(summary_frame, text="Close Summary", command=summary_frame.destroy, font=('Georgia', 8), bg="#D0A933")
    close_button.pack(pady=10, ipady=8, ipadx=7)

    # Update the canvas to include the new frame
    summary_frame.update_idletasks()
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
    canvas = Canvas(movies_info_frame, bg="#EFD78E", highlightbackground="#EFD78E")
    scrollbar = Scrollbar(movies_info_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a new frame to hold the movie information
    movies_info_frame_inner = Frame(canvas, bg="#EFD78E")
    canvas.create_window((0, 0), window=movies_info_frame_inner, anchor="nw")

    for i in range(0, len(movie)):
        # Retrieve movie poster
        poster_url = movie[i]['attributes']['poster']
        poster_response = requests.get(poster_url)
        poster_image = Image.open(BytesIO(poster_response.content))
        poster_image = poster_image.resize((150, 200))  # Resize the image for display

        # Display movie poster above the movie title
        poster_image = ImageTk.PhotoImage(poster_image)
        poster_label = Label(movies_info_frame_inner, image=poster_image, bg='#EFD78E')
        poster_label.image = poster_image
        poster_label.grid(row=i // 3 * 6, column=i % 3, pady=2)

        # Display movie title below the poster
        movie_title = movie[i]['attributes']['title']
        movie_title_label = Label(movies_info_frame_inner, text=movie_title, font=('Georgia', 10, 'bold'), wraplength=280, bg='#EFD78E')
        movie_title_label.grid(row=i // 3 * 6 + 1, column=i % 3, pady=2)

        # Display movie date below the movie title
        movie_date = movie[i]['attributes']['release_date']
        movie_date_label = Label(movies_info_frame_inner, text=f"Release Date: {movie_date}", font=('Times New Roman', 8), bg="#EFD78E")
        movie_date_label.grid(row=i // 3 * 6 + 2, column=i % 3, pady=2)
        # Display movie directors below the movie date
        movie_directors = ", ".join(movie[i]['attributes']['directors'])
        movie_directors_label = Label(movies_info_frame_inner, text=f"Directors: {movie_directors}", font=('Times New Roman', 8), bg="#EFD78E")
        movie_directors_label.grid(row=i // 3 * 6 + 3, column=i % 3, pady=2)

        # Display movie rating below the movie directors
        movie_rating = movie[i]['attributes']['rating']
        movie_rating_label = Label(movies_info_frame_inner, text=f"Rating: {movie_rating}", font=('Times New Roman', 8), bg="#EFD78E")
        movie_rating_label.grid(row=i // 3 * 6 + 4, column=i % 3, pady=2)

        # Display movie running time below the movie rating
        movie_running_time = movie[i]['attributes']['running_time']
        movie_running_time_label = Label(movies_info_frame_inner, text=f"Running Time: {movie_running_time}", font=('Times New Roman', 8), bg="#EFD78E")
        movie_running_time_label.grid(row=i // 3 * 6 + 5, column=i % 3, pady=2)


    # Update the canvas to include the new frame
    movies_info_frame_inner.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def search_characters(search_term):
    url = f"https://api.potterdb.com/v1/characters?page[number]="
    results = []

    for page_number in range(1, 48):
        search_url = f"{url}{page_number}"
        response = requests.get(search_url)
        data = response.json()
        characters = data.get('data', [])

        for character in characters:
            name = character['attributes'].get('name', '')
            house = character['attributes'].get('house', '')
            patronus = character['attributes'].get('patronus', '')
            born = character['attributes'].get('born', '')
            died = character['attributes'].get('died', '')

            if search_term in name:
                results.append((name, house, patronus, born, died))

    if not results:
        display_no_results_message()
    else:
        display_search_results(results)

def display_no_results_message():
    # Destroy the existing widgets in characters_info_frame
    for widget in characters_info_frame.winfo_children():
        widget.destroy()

    # Add a label to display the "No character found" message
    no_results_label = Label(characters_info_frame, text="No character found! Make sure the first letter of each name is in upper case.", font=('Georgia', 14), wraplength=400, justify='center', bg="#EFD78E")
    no_results_label.pack(pady=50)

def display_search_results(results):
    # Destroy the existing widgets in characters_info_frame
    for widget in characters_info_frame.winfo_children():
        widget.destroy()

    # Add a canvas for the characters info frame with a vertical scrollbar
    canvas = Canvas(characters_info_frame, bg="#EFD78E", highlightbackground="#EFD78E")
    scrollbar = Scrollbar(characters_info_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a new frame to hold the character information
    characters_info_frame_inner = Frame(canvas, bg="#EFD78E")
    canvas.create_window((0, 0), window=characters_info_frame_inner, anchor="nw")

    for i, result in enumerate(results):
        name, house, patronus, born, died = result

        # Calculate the column for each label
        column = i % 2

        # Display character name
        character_name_label = Label(characters_info_frame_inner, text=f"Name: {name}", font=('Georgia', 14, 'bold'), wraplength=380, bg='#EFD78E')
        character_name_label.grid(row=i // 2 * 6, column=column * 5, pady=2, padx=14)

        # Display character house
        character_house_label = Label(characters_info_frame_inner, text=f"House: {house}", font=('Times New Roman', 11), bg="#EFD78E")
        character_house_label.grid(row=i // 2 * 6 + 1, column=column * 5, pady=2, padx=14)

        # Display character patronus
        character_patronus_label = Label(characters_info_frame_inner, text=f"Patronus: {patronus}", font=('Times New Roman', 11), bg="#EFD78E")
        character_patronus_label.grid(row=i // 2 * 6 + 2, column=column * 5, pady=2, padx=14)
        
        # Display character birthday
        character_born_label = Label(characters_info_frame_inner, text=f"Born: {born}", font=('Times New Roman',11), bg="#EFD78E",wraplength=380)
        character_born_label.grid(row=i // 2 * 6 + 3, column=column * 5, pady=2, padx=14)

        # Display character death day
        character_death_label = Label(characters_info_frame_inner, text=f"Died: {died}", font=('Times New Roman', 11), bg="#EFD78E",wraplength=380)
        character_death_label.grid(row=i // 2 * 6 + 4, column=column * 5, pady=2, padx=14)

        # Add an empty space as a separator
        Label(characters_info_frame_inner, text='', bg="#EFD78E").grid(row=i // 2 * 6 + 5, column=column * 5)

    # Update the canvas to include the new frame
    characters_info_frame_inner.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    
def get_random_potion_data():
    # Choose a random page number for potions
    random_page_number = randint(1, 2)
    
    url = f"https://api.potterdb.com/v1/potions?page[number]={random_page_number}"
    response = requests.get(url)
    data = response.json()

    with open("potions.json", 'w') as file:
        json.dump(data, file, indent=6)

    potions = data['data']

    if potions:
        # Choose a random potion
        random_potion_index = randint(0, len(potions)-1)
        random_potion = potions[random_potion_index]['attributes']

        # Destroy the existing widgets in potions_info_frame
        for widget in potions_info_frame.winfo_children():
            widget.destroy()

        # Display random potion image
        potion_image_url = random_potion['image']
        potion_image_response = requests.get(potion_image_url)
        potion_image = Image.open(BytesIO(potion_image_response.content))
        potion_image = potion_image.resize((360, 350))  # Resize the image for display

        potion_image = ImageTk.PhotoImage(potion_image)
        potion_image_label = Label(potions_info_frame, image=potion_image, bg='#EFD78E')
        potion_image_label.image = potion_image
        potion_image_label.grid(row=0, rowspan=7, column=0, padx=40,pady=30)

        # Display random potion name
        potion_name = random_potion.get('name', 'N/A')
        potion_name_label = Label(potions_info_frame, text=f"Name: {potion_name}", font=('Georgia', 14, 'bold'), wraplength=340, bg='#EFD78E')
        potion_name_label.grid(row=1, column=1,padx=40)

        # Display random potion effect
        potion_effect = random_potion.get('effect', 'N/A')
        potion_effect_label = Label(potions_info_frame, text=f"Effect: {potion_effect}", font=('Times New Roman', 11), bg="#EFD78E", wraplength=340)
        potion_effect_label.grid(row=2, column=1,padx=40)

        # Display random potion ingredients
        potion_ingredients = random_potion.get('ingredients', 'N/A')
        potion_ingredients_label = Label(potions_info_frame, text=f"Ingredients: {potion_ingredients}", font=('Times New Roman', 11), bg="#EFD78E", wraplength=340)
        potion_ingredients_label.grid(row=3, column=1, padx=40)

        # Display random potion characteristics
        potion_characteristics = random_potion.get('characteristics', 'N/A')
        potion_characteristics_label = Label(potions_info_frame, text=f"Characteristics: {potion_characteristics}", font=('Times New Roman', 11), bg="#EFD78E", wraplength=340)
        potion_characteristics_label.grid(row=4, column=1, padx=40)

        # Display random potion difficulty
        potion_difficulty = random_potion.get('difficulty', 'N/A')
        potion_difficulty_label = Label(potions_info_frame, text=f"Difficulty: {potion_difficulty}", font=('Times New Roman', 11), bg="#EFD78E")
        potion_difficulty_label.grid(row=5, column=1, padx=40)

        # Update the canvas to include the new frame
        potions_info_frame.update_idletasks()
        potions_info_frame.pack_propagate(False)

def get_random_spell_data():
    # Choose a random page number for spells
    random_page_number = randint(1, 4)
    
    url = f"https://api.potterdb.com/v1/spells?page[number]={random_page_number}"
    response = requests.get(url)
    data = response.json()

    with open("spells.json", 'w') as file:
        json.dump(data, file, indent=6)

    spells = data['data']

    if spells:
        # Choose a random spell
        random_spell_index = randint(1, len(spells)-1)
        random_spell = spells[random_spell_index]['attributes']

        # Destroy the existing widgets in spells_info_frame
        for widget in spell_info_frame.winfo_children():
            widget.destroy()

        # Display random spell image
        spell_image_url = random_spell['image']
        spell_image_response = requests.get(spell_image_url)
        spell_image = Image.open(BytesIO(spell_image_response.content))
        spell_image = spell_image.resize((360, 350))  # Resize the image for display

        spell_image = ImageTk.PhotoImage(spell_image)
        spell_image_label = Label(spell_info_frame, image=spell_image, bg='#EFD78E')
        spell_image_label.image = spell_image
        spell_image_label.grid(row=0, rowspan=8, column=0, padx=40,pady=30)

        # Display random spell name
        spell_name = random_spell.get('name', 'N/A')
        spell_name_label = Label(spell_info_frame, text=f"Name: {spell_name}", font=('Georgia', 14, 'bold'), wraplength=340, bg='#EFD78E')
        spell_name_label.grid(row=1, column=1, padx=40)

        # Display random spell effect
        spell_effect = random_spell.get('effect', 'N/A')
        spell_effect_label = Label(spell_info_frame, text=f"Effect: {spell_effect}", font=('Times New Roman', 11), bg="#EFD78E", wraplength=340)
        spell_effect_label.grid(row=2, column=1, padx=40)

        # Display random spell category
        spell_category = random_spell.get('category', 'N/A')
        spell_category_label = Label(spell_info_frame, text=f"Category: {spell_category}", font=('Times New Roman', 11), bg="#EFD78E", wraplength=340)
        spell_category_label.grid(row=3, column=1, padx=40)

        # Display random spell light
        spell_light = random_spell.get('light', 'N/A')
        spell_light_label = Label(spell_info_frame, text=f"Light: {spell_light}",font=('Times New Roman', 11), bg="#EFD78E", wraplength=340)
        spell_light_label.grid(row=4, column=1, padx=40)

        # Display random spell incantation
        spell_incantation = random_spell.get('incantation', 'N/A')
        spell_incantation_label = Label(spell_info_frame, text=f"Incantation: {spell_incantation}", font=('Times New Roman', 11), bg="#EFD78E", wraplength=340)
        spell_incantation_label.grid(row=5, column=1, padx=40)

        spell_difficulty = random_spell.get('difficulty', 'N/A')
        spell_difficulty_label = Label(spell_info_frame, text=f"Difficulty: {spell_difficulty}", font=('Times New Roman', 11), bg="#EFD78E", wraplength=340)
        spell_difficulty_label.grid(row=6, column=1,padx=40)

        # Update the canvas to include the new frame
        spell_info_frame.update_idletasks()
        spell_info_frame.pack_propagate(False)
        
root = Tk()
root.title("Harry Potter World")
root.geometry("880x600")
root.resizable(0, 0)
root.configure(bg='#41347D')

# Create a main frame for the background image
start_frame = Frame(root, width=880, height=600, bg='#41347D')
start_frame.pack_propagate(0)  # Disable automatic resizing of the main frame
start_frame.pack()

# Load the background image using PIL
image = Image.open("background_image.png")  # Replace "background_image.png" with your image file
background_image = ImageTk.PhotoImage(image)

# Create a label to display the background image
background_label = Label(start_frame, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Add a button to the secondary frame that calls the replace_main_frame function
start_button = Button(start_frame, text="Start", font=("Andalus", 16), bg="#D0A933", fg="white", command=lambda: [replace_start_frame(), reset_indicators()])
start_button.place(relx=0.1, rely=0.4, relwidth=0.25)

# Add a Quit button in the same horizontal line
quit_button = Button(start_frame, text="Quit", font=("Andalus", 16), bg="#D0A933", fg="white", command=quit_application)
quit_button.place(relx=0.1, rely=0.5, relwidth=0.25)

# Create a replacement frame with the same size
replacement_frame = Frame(root, width=880, height=600, bg="#41347D")
replacement_frame.pack_propagate(0)  # Disable automatic resizing of the replacement frame


options_frame = Frame(replacement_frame)

books_button = Button(options_frame, text="Books", font=('Georgia',14), bd=0, fg='#BFBFBF', activeforeground="white", bg="#41347D",
                      command=lambda: switch_indicator(indicator=books_indicator, page=books_page))
books_button.place(x=30, y=0, width=160,height=50)

books_indicator= Label(options_frame)
books_indicator.place(x=87, y=46, width=50, height=3)

movies_button = Button(options_frame, text="Movies", font=('Georgia',14), bd=0, fg='#BFBFBF', activeforeground="white", bg="#41347D",
                      command=lambda: switch_indicator(indicator=movies_indicator, page=movies_page))
movies_button.place(x=190, y=0, width=160,height=50)

movies_indicator= Label(options_frame)
movies_indicator.place(x=243, y=46, width=57, height=3)

characters_button = Button(options_frame, text="Characters", font=('Georgia',14), bd=0, fg='#BFBFBF', activeforeground="white", bg="#41347D",
                      command=lambda: switch_indicator(indicator=characters_indicator, page=characters_page))
characters_button.place(x=350, y=0, width=160,height=50)

characters_indicator= Label(options_frame)
characters_indicator.place(x=390, y=46, width=80, height=3)

potions_button = Button(options_frame, text="Potions", font=('Georgia',14), bd=0, fg='#BFBFBF', activeforeground="white", bg="#41347D",
                      command=lambda: switch_indicator(indicator=potions_indicator, page=potions_page))
potions_button.place(x=510, y=0, width=160,height=50)

potions_indicator= Label(options_frame)
potions_indicator.place(x=563, y=46, width=60, height=3)

spells_button = Button(options_frame, text="Spells", font=('Georgia',14), bd=0, fg='#BFBFBF', activeforeground="white", bg="#41347D",
                      command=lambda: switch_indicator(indicator=spells_indicator, page=spells_page))
spells_button.place(x=670, y=0, width=160,height=50)

spells_indicator= Label(options_frame)
spells_indicator.place(x=728, y=46, width=47, height=3)

options_frame.pack(pady=5)
options_frame.pack_propagate(False)
options_frame.configure(width=880,height=60, bg="#41347D")

main_frame = Frame(replacement_frame)
main_frame.pack(fill=BOTH, expand=True)

main_frame_image = Image.open('main_frame_background.png')
main_frame_background_image = ImageTk.PhotoImage(main_frame_image)

# Create a label to display the background image in the main_frame
main_frame_background_label = Label(main_frame, image=main_frame_background_image)
main_frame_background_label.place(relwidth=1, relheight=1)

def books_page():
    global books_page_frame, books_info_frame
    books_page_frame = Frame(main_frame, bg='#EFD78E')

    # Add buttons frame
    buttons_frame = Frame(books_page_frame, bg='#EFD78E')
    buttons_frame.pack(side=TOP, pady=10)

    # Add 'Get Books Data' button
    get_books_button = Button(buttons_frame, text="Get Books Data", font=('Times New Roman', 14), bg="blue", fg="white", command=get_books_data)
    get_books_button.pack(side=LEFT,  padx=5, pady=10, ipady=4, ipadx=7)

    # Add 'Instructions' button
    instructions_button = Button(buttons_frame, text="Instructions", font=('Times New Roman', 14), bg="green", fg="white", command=lambda: switch_indicator(indicator=books_indicator, page=replace_start_frame))
    instructions_button.pack(side=LEFT,  padx=5, pady=10, ipady=4, ipadx=7)

    # Add 'Exit' button
    exit_button = Button(buttons_frame, text="Exit", font=('Times New Roman', 14), bg="red", fg="white", command=lambda: switch_indicator(indicator=books_indicator, page=replace_main_frame))
    exit_button.pack(side=LEFT,  padx=5, pady=10, ipady=4, ipadx=7)

    # Add books info frame
    books_info_frame = Frame(books_page_frame,bg='#EFD78E')
    books_info_frame.pack(fill=BOTH, expand=True)

    books_page_frame.pack(fill=BOTH, expand=True)

def movies_page():
    global movies_page_frame, movies_info_frame
    movies_page_frame = Frame(main_frame, bg='#EFD78E')

    # Add buttons frame
    buttons_frame = Frame(movies_page_frame, bg='#EFD78E')
    buttons_frame.pack(side=TOP, pady=10)

    # Add 'Get Movies Data' button
    get_movies_button = Button(buttons_frame, text="Get Movies Data", font=('Times New Roman', 14), bg="blue", fg="white", command=get_movies_data)
    get_movies_button.pack(side=LEFT, padx=5, pady=10, ipady=4, ipadx=7)

    # Add 'Instructions' button
    instructions_button = Button(buttons_frame, text="Instructions", font=('Times New Roman', 14), bg="green", fg="white", command=lambda: switch_indicator(indicator=movies_indicator, page=replace_start_frame))
    instructions_button.pack(side=LEFT, padx=5, pady=10, ipady=4, ipadx=7)

    # Add 'Exit' button
    exit_button = Button(buttons_frame, text="Exit", font=('Times New Roman', 14), bg="red", fg="white", command=lambda: switch_indicator(indicator=movies_indicator, page=replace_main_frame))
    exit_button.pack(side=LEFT, padx=5, pady=10, ipady=4, ipadx=7)

    # Add movies info frame
    movies_info_frame = Frame(movies_page_frame, bg='#EFD78E')
    movies_info_frame.pack(fill=BOTH, expand=True)

    movies_page_frame.pack(fill=BOTH, expand=True)

def characters_page():
    global characters_info_frame
    characters_page_frame = Frame(main_frame, bg='#EFD78E')

    # Add search bar frame
    search_frame = Frame(characters_page_frame, bg='#EFD78E')
    search_frame.pack(side=TOP, pady=5)

    # Create and pack search label
    search_label = Label(search_frame, text="Search Character By Name:", font=('Georgia', 14), bg='#EFD78E', wraplength=350)
    search_label.pack(side=LEFT, padx=5)

    # Create and pack search entry
    search_entry = Entry(search_frame, font=('Arial', 12), width=30)
    search_entry.pack(side=LEFT, padx=5, pady=10, ipady=8, ipadx=7)

    # Create and pack search button
    search_button = Button(search_frame, text="Search", font=('Times New Roman', 14), bg="blue", fg="white", command=lambda: search_characters(search_entry.get()))
    search_button.pack(side=LEFT, padx=5, pady=10, ipady=1, ipadx=7)

    # Add buttons frame
    buttons_frame = Frame(characters_page_frame, bg='#EFD78E')
    buttons_frame.pack(side=TOP)

    # Add 'Instructions' button
    instructions_button = Button(buttons_frame, text="Instructions", font=('Times New Roman', 14), bg="green", fg="white", command=lambda: switch_indicator(indicator=characters_indicator, page=replace_start_frame))
    instructions_button.pack(side=LEFT, padx=5, pady=10, ipady=4, ipadx=7)

    # Add 'Exit' button
    exit_button = Button(buttons_frame, text="Exit", font=('Times New Roman', 14), bg="red", fg="white", command=lambda: switch_indicator(indicator=characters_indicator, page=replace_main_frame))
    exit_button.pack(side=LEFT, padx=5, pady=10, ipady=4, ipadx=7)

    # Add characters info frame
    characters_info_frame = Frame(characters_page_frame, bg='#EFD78E')
    characters_info_frame.pack(fill=BOTH, expand=True, pady=5)

    characters_page_frame.pack(fill=BOTH, expand=True)

def potions_page():
    global potions_page_frame, potions_info_frame
    potions_page_frame = Frame(main_frame, bg='#EFD78E')

    # Add buttons frame
    buttons_frame = Frame(potions_page_frame, bg='#EFD78E')
    buttons_frame.pack(side=TOP, pady=10)

    # Add 'Get Random Potions' button
    get_random_potions_button = Button(buttons_frame, text="Get A Random Potion", font=('Times New Roman', 14), bg="blue", fg="white", command=get_random_potion_data)
    get_random_potions_button.pack(side=LEFT, padx=5, pady=10, ipady=4, ipadx=7)

    # Add 'Instructions' button
    instructions_button = Button(buttons_frame, text="Instructions", font=('Times New Roman', 14), bg="green", fg="white", command=lambda: switch_indicator(indicator=potions_indicator, page=replace_start_frame))
    instructions_button.pack(side=LEFT, padx=5, pady=10, ipady=4, ipadx=7)

    # Add 'Exit' button
    exit_button = Button(buttons_frame, text="Exit", font=('Times New Roman', 14), bg="red", fg="white", command=lambda: switch_indicator(indicator=potions_indicator, page=replace_main_frame))
    exit_button.pack(side=LEFT, padx=5, pady=10, ipady=4, ipadx=7)

    # Add potions info frame
    potions_info_frame = Frame(potions_page_frame, bg='#EFD78E')
    potions_info_frame.pack(fill=BOTH, expand=True)

    potions_page_frame.pack(fill=BOTH, expand=True)

def spells_page():
    global spells_page_frame, spell_info_frame
    spells_page_frame = Frame(main_frame, bg='#EFD78E')

    # Add buttons frame
    buttons_frame = Frame(spells_page_frame, bg='#EFD78E')
    buttons_frame.pack(side=TOP, pady=10)

    # Add 'Get Random Spell' button
    get_random_spell_button = Button(buttons_frame, text="Get A Random Spell", font=('Times New Roman', 14), bg="blue", fg="white", command=get_random_spell_data)
    get_random_spell_button.pack(side=LEFT, padx=5, pady=10, ipady=4, ipadx=7)

    # Add 'Instructions' button
    instructions_button = Button(buttons_frame, text="Instructions", font=('Times New Roman', 14), bg="green", fg="white", command=lambda: switch_indicator(indicator=spells_indicator, page=replace_start_frame))
    instructions_button.pack(side=LEFT, padx=5, pady=10, ipady=4, ipadx=7)

    # Add 'Exit' button
    exit_button = Button(buttons_frame, text="Exit", font=('Times New Roman', 14), bg="red", fg="white", command=lambda: switch_indicator(indicator=spells_indicator, page=replace_main_frame))
    exit_button.pack(side=LEFT, padx=5, pady=10, ipady=4, ipadx=7)

    # Add spells info frame
    spell_info_frame = Frame(spells_page_frame, bg='#EFD78E')
    spell_info_frame.pack(fill=BOTH, expand=True)

    spells_page_frame.pack(fill=BOTH, expand=True)



root.mainloop()
