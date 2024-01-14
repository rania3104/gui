from tkinter import * #importing tkinter module for the GUI
from PIL import Image, ImageTk #importing the pillow library for images
from io import BytesIO #importing BytesIO for images
import requests #importing requests for API
import json #importing json to organize the data
from random import randint #importing randint for randomization

def replace_start_frame():
    #function to replace the start frame with the replacement frame (the menu)
    start_frame.pack_forget() #the start frame will be forgotten and the replacement frame will be packed
    replacement_frame.pack()
    

def replace_main_frame():
    #function to replace the replacement frame with the start frame
    replacement_frame.pack_forget() #the replacement frame will be forgotten and the start frame will be packed
    start_frame.pack()

def reset_indicators():
    #function to remove the indicators
    for child in options_frame.winfo_children():
        if isinstance(child, Label):
            child['bg'] = '#41347D' #will change the ng color of the indicator to the color of the button

def switch_indicator(indicator, page):
    #funtion to switch the indicators with the button
    reset_indicators()
    if page != replace_start_frame:  #to check if the 'Instructions' button is not clicked 
        indicator['bg'] = 'white'

    for widget in main_frame.winfo_children():
        #to hide or deactivate the widgets instead of destroying them
        widget.pack_forget()

    replacement_frame.update()
    page()

def quit_application():
    #function to quit the application
    root.destroy()

def get_books_data():
    #function to get the books data from the API
    url = f"https://api.potterdb.com/v1/books" #url of the API
    response = requests.get(url) #retrieving the data from the API
    data = response.json() #storing the data in a json file for better understanding

    with open("books.json", 'w') as file: #creating the json file
        json.dump(data, file, indent=6)

    book = data['data']

    #destroying the existing widgets in books_info_frame
    for widget in books_info_frame.winfo_children():
        widget.destroy()

    #adding a canvas for the books_info_frame with a vertical scrollbar
    canvas = Canvas(books_info_frame, bg="#EFD78E", highlightbackground="#EFD78E")
    scrollbar = Scrollbar(books_info_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.configure(yscrollcommand=scrollbar.set)

    #creating a new frame to hold the book information
    books_info_frame_inner = Frame(canvas, bg="#EFD78E")
    canvas.create_window((0, 0), window=books_info_frame_inner, anchor="nw")

    #for loop to retrieve the data for each book
    for i in range(0, len(book)):
        #retrieving the book cover
        cover_url = book[i]['attributes']['cover']
        cover_response = requests.get(cover_url)
        cover_image = Image.open(BytesIO(cover_response.content))
        cover_image = cover_image.resize((120, 180))  #resizing the image

        #displaying book cover above the book title
        cover_image = ImageTk.PhotoImage(cover_image)
        cover_label = Label(books_info_frame_inner, image=cover_image, bg="#EFD78E")
        cover_label.image = cover_image
        cover_label.grid(row=i // 3 * 5, column=i % 3, pady=2)

        #displaying the book title below the cover
        book_title = book[i]['attributes']['title'] #the index for the title
        book_title_label = Label(books_info_frame_inner, text=book_title, font=('Georgia', 10, 'bold'), wraplength=280, bg='#EFD78E')
        book_title_label.grid(row=i // 3 * 5 + 1, column=i % 3, pady=2, padx=12)

        #displaying the book's release date below the book title
        book_date = book[i]['attributes']['release_date'] #the index for the release date
        book_date_label = Label(books_info_frame_inner, text=f"Release Date: {book_date}", font=('Times New Roman', 8), bg="#EFD78E")
        book_date_label.grid(row=i // 3 * 5 + 2, column=i % 3, pady=2)

        book_summary = book[i]['attributes']['summary'] #the index for the summary

        #creating a button to show the summary when clicked
        show_summary_button = Button(books_info_frame_inner, cursor='hand2',text=f"Show Summary", font=('Georgia', 8),
                                     command=lambda i=i, summary=book_summary: show_summary(i, summary),
                                     bg="#D0A933")  #passing the command to run the function when clicked
        show_summary_button.grid(row=i // 3 * 5 + 4, column=i % 3, pady=2, ipadx=20, ipady=5)

    #updating the canvas to include the new frame
    books_info_frame_inner.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def show_summary(index, summary):
    #function to show the summary
    #creating a new frame for displaying the summary
    summary_frame = Toplevel()
    summary_frame.title("Book Summary")
    summary_frame.geometry("400x340")
    summary_frame.configure(bg="#B09DE4")

    #displaying the title of the window
    summary_title = Label (summary_frame, text= "SUMMARY", font=('Georgia', 14, 'bold'), bg='#B09DE4')
    summary_title.pack(pady=10)

    #displaying the book summary
    summary_label = Label(summary_frame, text=summary, font=('Georgia', 12), wraplength=380, justify='left', bg='#B09DE4')
    summary_label.pack(pady=10)

    # button to close the summary window
    close_button = Button(summary_frame, text="Close Summary", command=summary_frame.destroy, font=('Georgia', 8), bg="#D0A933",cursor='hand2')
    close_button.pack(pady=10, ipady=8, ipadx=7) #passing the command to destroy the frame

    #updating the canvas to include the new frame
    summary_frame.update_idletasks()

def get_movies_data():
    #function to get the movies data from the API
    url = f"https://api.potterdb.com/v1/movies"#url of the API
    response = requests.get(url) #retrieving the data from the API
    data = response.json() #storing the data in a json file for better understanding

    with open("movies.json", 'w') as file: #creating the json file
        json.dump(data, file, indent=6)

    movie = data['data']

    #destroying the existing widgets in movies_info_frame
    for widget in movies_info_frame.winfo_children():
        widget.destroy()

    #adding a canvas for the movies_info_frame with a vertical scrollbar
    canvas = Canvas(movies_info_frame, bg="#EFD78E", highlightbackground="#EFD78E")
    scrollbar = Scrollbar(movies_info_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.configure(yscrollcommand=scrollbar.set)

    #creating a new frame to hold the movie information
    movies_info_frame_inner = Frame(canvas, bg="#EFD78E")
    canvas.create_window((0, 0), window=movies_info_frame_inner, anchor="nw")

    #for loop to retrieve the data for each movie
    for i in range(0, len(movie)):

        #retrieving the movie's poster
        poster_url = movie[i]['attributes']['poster'] #the index for the poster
        poster_response = requests.get(poster_url)
        poster_image = Image.open(BytesIO(poster_response.content))
        poster_image = poster_image.resize((150, 200))  #resizing the image

        #displaying the movie poster above the movie title
        poster_image = ImageTk.PhotoImage(poster_image)
        poster_label = Label(movies_info_frame_inner, image=poster_image, bg='#EFD78E')
        poster_label.image = poster_image
        poster_label.grid(row=i // 3 * 6, column=i % 3, pady=2)

        #displaying movie title below the poster
        movie_title = movie[i]['attributes']['title'] #the index for the title
        movie_title_label = Label(movies_info_frame_inner, text=movie_title, font=('Georgia', 10, 'bold'), wraplength=280, bg='#EFD78E')
        movie_title_label.grid(row=i // 3 * 6 + 1, column=i % 3, pady=2)

        #displaying the movie release date below the movie title
        movie_date = movie[i]['attributes']['release_date'] #the index for the release date
        movie_date_label = Label(movies_info_frame_inner, text=f"Release Date: {movie_date}", font=('Times New Roman', 8), bg="#EFD78E")
        movie_date_label.grid(row=i // 3 * 6 + 2, column=i % 3, pady=2)

        #displaying the movie directors below the movie date
        movie_directors = ", ".join(movie[i]['attributes']['directors']) #the index for the directors
        movie_directors_label = Label(movies_info_frame_inner, text=f"Directors: {movie_directors}", font=('Times New Roman', 8), bg="#EFD78E")
        movie_directors_label.grid(row=i // 3 * 6 + 3, column=i % 3, pady=2)

        #displaying the movie rating below the movie directors
        movie_rating = movie[i]['attributes']['rating'] #the index for the rating
        movie_rating_label = Label(movies_info_frame_inner, text=f"Rating: {movie_rating}", font=('Times New Roman', 8), bg="#EFD78E")
        movie_rating_label.grid(row=i // 3 * 6 + 4, column=i % 3, pady=2)

        #displaying the movie running time below the movie rating
        movie_running_time = movie[i]['attributes']['running_time'] #the index for the running time
        movie_running_time_label = Label(movies_info_frame_inner, text=f"Running Time: {movie_running_time}", font=('Times New Roman', 8), bg="#EFD78E")
        movie_running_time_label.grid(row=i // 3 * 6 + 5, column=i % 3, pady=2)


    #updating the canvas to include the new frame
    movies_info_frame_inner.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def search_characters(search_term):
    #function to get the characters data from the API
    url = f"https://api.potterdb.com/v1/characters?page[number]="#url of the API

    #creating an empty list to store the data
    results = []

    for page_number in range(1, 48): #range given because of the multiple data pages
        search_url = f"{url}{page_number}"
        response = requests.get(search_url) #retrieving the data from the API
        data = response.json() #storing the data in a json file for better understanding
        characters = data.get('data', [])

        #for loop to retrieve the data from the API
        for character in characters:
            name = character['attributes'].get('name', '')
            house = character['attributes'].get('house', '')
            patronus = character['attributes'].get('patronus', '')
            born = character['attributes'].get('born', '')
            died = character['attributes'].get('died', '')

            #if the user's search is found in the database then it will append the information to the list
            if search_term in name:
                results.append((name, house, patronus, born, died))

    #if statement to see if the name is available or not
    if not results:
        display_no_results_message()
    else:
        display_search_results(results)

def display_no_results_message():
    #function for if the user's entry does not exist in the database

    #destroying the existing widgets in characters_info_frame
    for widget in characters_info_frame.winfo_children():
        widget.destroy()

    #adding a label to display the "No character found" message
    no_results_label = Label(characters_info_frame, text="No character found! Make sure the first letter of each name is in upper case.", 
                             font=('Georgia', 14), wraplength=400, justify='center', bg="#EFD78E")
    no_results_label.pack(pady=50)

def display_search_results(results):
    #function to display the search results

    #destroying the existing widgets in characters_info_frame
    for widget in characters_info_frame.winfo_children():
        widget.destroy()

    #adding a canvas for the characters info frame with a vertical scrollbar
    canvas = Canvas(characters_info_frame, bg="#EFD78E", highlightbackground="#EFD78E")
    scrollbar = Scrollbar(characters_info_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.configure(yscrollcommand=scrollbar.set)

    #creating a new frame to hold the character information
    characters_info_frame_inner = Frame(canvas, bg="#EFD78E")
    canvas.create_window((0, 0), window=characters_info_frame_inner, anchor="nw")

    #for loop to retrieve and display the data from the list
    for i, result in enumerate(results):
        name, house, patronus, born, died = result

        #calculating the column for each label
        column = i % 2

        #displaying the character name
        character_name_label = Label(characters_info_frame_inner, text=f"Name: {name}", font=('Georgia', 14, 'bold'), wraplength=380, bg='#EFD78E')
        character_name_label.grid(row=i // 2 * 6, column=column * 5, pady=2, padx=14)

        #displaying the character's house
        character_house_label = Label(characters_info_frame_inner, text=f"House: {house}", font=('Times New Roman', 11), bg="#EFD78E")
        character_house_label.grid(row=i // 2 * 6 + 1, column=column * 5, pady=2, padx=14)

        #displaying the character's patronus
        character_patronus_label = Label(characters_info_frame_inner, text=f"Patronus: {patronus}", font=('Times New Roman', 11), bg="#EFD78E")
        character_patronus_label.grid(row=i // 2 * 6 + 2, column=column * 5, pady=2, padx=14)
        
        #displaying the character's birthday
        character_born_label = Label(characters_info_frame_inner, text=f"Born: {born}", font=('Times New Roman',11), bg="#EFD78E",wraplength=380)
        character_born_label.grid(row=i // 2 * 6 + 3, column=column * 5, pady=2, padx=14)

        #displaying the character's death day
        character_death_label = Label(characters_info_frame_inner, text=f"Died: {died}", font=('Times New Roman', 11), bg="#EFD78E",wraplength=380)
        character_death_label.grid(row=i // 2 * 6 + 4, column=column * 5, pady=2, padx=14)

        #adding an empty space as a separator
        Label(characters_info_frame_inner, text='', bg="#EFD78E").grid(row=i // 2 * 6 + 5, column=column * 5)

    #updating the canvas to include the new frame
    characters_info_frame_inner.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    
def get_random_potion_data():
    #function to get the potions data from the API

    #choosing a random page number for potions because of the multiple pages of data
    random_page_number = randint(1, 2)
    
    url = f"https://api.potterdb.com/v1/potions?page[number]={random_page_number}" #url of the API
    response = requests.get(url) #retrieving the data from the API
    data = response.json() #storing the data in a json file for better understanding

    with open("potions.json", 'w') as file: #creating the json file
        json.dump(data, file, indent=6)

    potions = data['data']

    if potions:
        #choosing a random potion
        random_potion_index = randint(0, len(potions)-1)
        random_potion = potions[random_potion_index]['attributes']

        #destroying the existing widgets in potions_info_frame
        for widget in potions_info_frame.winfo_children():
            widget.destroy()

        #displaying the random potion image
        potion_image_url = random_potion['image']
        potion_image_response = requests.get(potion_image_url)
        potion_image = Image.open(BytesIO(potion_image_response.content))
        potion_image = potion_image.resize((360, 350))  # Resize the image for display

        potion_image = ImageTk.PhotoImage(potion_image)
        potion_image_label = Label(potions_info_frame, image=potion_image, bg='#EFD78E')
        potion_image_label.image = potion_image
        potion_image_label.grid(row=0, rowspan=7, column=0, padx=40,pady=30)

        #displaying the random potion name
        potion_name = random_potion.get('name', 'N/A')
        potion_name_label = Label(potions_info_frame, text=f"Name: {potion_name}", font=('Georgia', 14, 'bold'), wraplength=340, bg='#EFD78E')
        potion_name_label.grid(row=1, column=1,padx=40)

        #displaying the random potion effect
        potion_effect = random_potion.get('effect', 'N/A')
        potion_effect_label = Label(potions_info_frame, text=f"Effect: {potion_effect}", font=('Times New Roman', 11), bg="#EFD78E", wraplength=340)
        potion_effect_label.grid(row=2, column=1,padx=40)

        #displaying the random potion ingredients
        potion_ingredients = random_potion.get('ingredients', 'N/A')
        potion_ingredients_label = Label(potions_info_frame, text=f"Ingredients: {potion_ingredients}", font=('Times New Roman', 11), bg="#EFD78E", wraplength=340)
        potion_ingredients_label.grid(row=3, column=1, padx=40)

        #displaying the random potion characteristics
        potion_characteristics = random_potion.get('characteristics', 'N/A')
        potion_characteristics_label = Label(potions_info_frame, text=f"Characteristics: {potion_characteristics}", font=('Times New Roman', 11), bg="#EFD78E", wraplength=340)
        potion_characteristics_label.grid(row=4, column=1, padx=40)

        #displaying the random potion difficulty
        potion_difficulty = random_potion.get('difficulty', 'N/A')
        potion_difficulty_label = Label(potions_info_frame, text=f"Difficulty: {potion_difficulty}", font=('Times New Roman', 11), bg="#EFD78E")
        potion_difficulty_label.grid(row=5, column=1, padx=40)

        #updating the canvas to include the new frame
        potions_info_frame.update_idletasks()
        potions_info_frame.pack_propagate(False)

def get_random_spell_data():
    #function to get the spells data from the API

    #choosing a random page number for spells because of the multiple pages of data
    random_page_number = randint(1, 4)
    
    url = f"https://api.potterdb.com/v1/spells?page[number]={random_page_number}" #url of the API
    response = requests.get(url) #retrieving the data from the API
    data = response.json() #storing the data in a json file for better understanding

    with open("spells.json", 'w') as file: #creating the json file
        json.dump(data, file, indent=6)

    spells = data['data']

    if spells:
        #choosing a random spell
        random_spell_index = randint(1, len(spells)-1)
        random_spell = spells[random_spell_index]['attributes']

        #destroying the existing widgets in spells_info_frame
        for widget in spell_info_frame.winfo_children():
            widget.destroy()

        #displaying the random spell image
        spell_image_url = random_spell['image']
        spell_image_response = requests.get(spell_image_url)
        spell_image = Image.open(BytesIO(spell_image_response.content))
        spell_image = spell_image.resize((360, 350))  # Resize the image for display

        spell_image = ImageTk.PhotoImage(spell_image)
        spell_image_label = Label(spell_info_frame, image=spell_image, bg='#EFD78E')
        spell_image_label.image = spell_image
        spell_image_label.grid(row=0, rowspan=8, column=0, padx=40,pady=30)

        #displaying the random spell name
        spell_name = random_spell.get('name', 'N/A')
        spell_name_label = Label(spell_info_frame, text=f"Name: {spell_name}", font=('Georgia', 14, 'bold'), wraplength=340, bg='#EFD78E')
        spell_name_label.grid(row=1, column=1, padx=40)

        #displaying the random spell effect
        spell_effect = random_spell.get('effect', 'N/A')
        spell_effect_label = Label(spell_info_frame, text=f"Effect: {spell_effect}", font=('Times New Roman', 11), bg="#EFD78E", wraplength=340)
        spell_effect_label.grid(row=2, column=1, padx=40)

        #displaying the random spell category
        spell_category = random_spell.get('category', 'N/A')
        spell_category_label = Label(spell_info_frame, text=f"Category: {spell_category}", font=('Times New Roman', 11), bg="#EFD78E", wraplength=340)
        spell_category_label.grid(row=3, column=1, padx=40)

        #displaying the random spell light
        spell_light = random_spell.get('light', 'N/A')
        spell_light_label = Label(spell_info_frame, text=f"Light: {spell_light}",font=('Times New Roman', 11), bg="#EFD78E", wraplength=340)
        spell_light_label.grid(row=4, column=1, padx=40)

        #displaying the random spell incantation
        spell_incantation = random_spell.get('incantation', 'N/A')
        spell_incantation_label = Label(spell_info_frame, text=f"Incantation: {spell_incantation}", font=('Times New Roman', 11), bg="#EFD78E", wraplength=340)
        spell_incantation_label.grid(row=5, column=1, padx=40)

        #displaying the random spell difficulty
        spell_difficulty = random_spell.get('difficulty', 'N/A')
        spell_difficulty_label = Label(spell_info_frame, text=f"Difficulty: {spell_difficulty}", font=('Times New Roman', 11), bg="#EFD78E", wraplength=340)
        spell_difficulty_label.grid(row=6, column=1,padx=40)

        #updating the canvas to include the new frame
        spell_info_frame.update_idletasks()
        spell_info_frame.pack_propagate(False)
        
root = Tk() #creating the GUI window
root.title("Harry Potter World") #naming the window
root.geometry("880x600") #setting the window size
root.resizable(0, 0) #disabling resizing of the window
root.iconbitmap("icon.ico") #adding an icon to the window
root.configure(bg='#41347D') #adding a background color to the window

#creating a start frame
start_frame = Frame(root, width=880, height=600, bg='#41347D')
start_frame.pack_propagate(0)  #disabling automatic resizing of the start frame
start_frame.pack()

#loading the background image using PIL
image = Image.open("background_image.png") #image url
background_image = ImageTk.PhotoImage(image)

#creating a label to display the background image
background_label = Label(start_frame, image=background_image)
background_label.place(relwidth=1, relheight=1)

#adding a Start button to the start frame that calls the replace_main_frame function
start_button = Button(start_frame, text="Start", font=("Andalus", 16), bg="#D0A933", fg="white",
                      cursor='hand2', command=lambda: [replace_start_frame(), reset_indicators()])
start_button.place(relx=0.1, rely=0.4, relwidth=0.25)

#adding a Quit button in the same horizontal line
quit_button = Button(start_frame, text="Quit", font=("Andalus", 16), bg="#D0A933", fg="white", cursor='hand2',command=quit_application)
quit_button.place(relx=0.1, rely=0.5, relwidth=0.25)

#creating a replacement frame with the same size
replacement_frame = Frame(root, width=880, height=600, bg="#41347D")
replacement_frame.pack_propagate(0)  # Disable automatic resizing of the replacement frame

#creating an options frame on top of the replacement frame
options_frame = Frame(replacement_frame)

#importing all the icons for the option buttons
books_icon = ImageTk.PhotoImage(Image.open('book.png'))
movies_icon = ImageTk.PhotoImage(Image.open('movie.png'))
characters_icon = ImageTk.PhotoImage(Image.open('character.png'))
potions_icon = ImageTk.PhotoImage(Image.open('potion.png'))
spells_icon = ImageTk.PhotoImage(Image.open('spell.png'))

#creating the buttons and indicators for the navigation bar
books_button = Button(options_frame, image=books_icon, compound=LEFT, text=" Books", font=('Georgia',14), bd=0, fg='#BFBFBF', activeforeground="white", bg="#41347D",
                      cursor='hand2', command=lambda: switch_indicator(indicator=books_indicator, page=books_page))
books_button.place(x=30, y=0, width=160,height=50)

books_indicator= Label(options_frame)
books_indicator.place(x=87, y=46, width=50, height=3)

movies_button = Button(options_frame, image=movies_icon, compound=LEFT,text=" Movies", font=('Georgia',14), bd=0, fg='#BFBFBF', activeforeground="white", bg="#41347D",
                      cursor='hand2',command=lambda: switch_indicator(indicator=movies_indicator, page=movies_page))
movies_button.place(x=190, y=0, width=160,height=50)

movies_indicator= Label(options_frame)
movies_indicator.place(x=243, y=46, width=57, height=3)

characters_button = Button(options_frame,image=characters_icon, compound=LEFT, text=" Characters", font=('Georgia',14), bd=0, fg='#BFBFBF', activeforeground="white", bg="#41347D",
                      cursor='hand2',command=lambda: switch_indicator(indicator=characters_indicator, page=characters_page))
characters_button.place(x=350, y=0, width=160,height=50)

characters_indicator= Label(options_frame)
characters_indicator.place(x=390, y=46, width=80, height=3)

potions_button = Button(options_frame, image=potions_icon, compound=LEFT, text=" Potions", font=('Georgia',14), bd=0, fg='#BFBFBF', activeforeground="white", bg="#41347D",
                      cursor='hand2',command=lambda: switch_indicator(indicator=potions_indicator, page=potions_page))
potions_button.place(x=510, y=0, width=160,height=50)

potions_indicator= Label(options_frame)
potions_indicator.place(x=563, y=46, width=60, height=3)

spells_button = Button(options_frame,image=spells_icon, compound=LEFT, text=" Spells", font=('Georgia',14), bd=0, fg='#BFBFBF', activeforeground="white", bg="#41347D",
                      cursor='hand2',command=lambda: switch_indicator(indicator=spells_indicator, page=spells_page))
spells_button.place(x=670, y=0, width=160,height=50)

spells_indicator= Label(options_frame)
spells_indicator.place(x=728, y=46, width=47, height=3)

options_frame.pack(pady=5)
options_frame.pack_propagate(False)
options_frame.configure(width=880,height=60, bg="#41347D")

#creating a main frame to hold the other pages
main_frame = Frame(replacement_frame)
main_frame.pack(fill=BOTH, expand=True)

main_frame_image = Image.open('main_frame_background.png')
main_frame_background_image = ImageTk.PhotoImage(main_frame_image)

#creating a label to display the background image in the main_frame
main_frame_background_label = Label(main_frame, image=main_frame_background_image)
main_frame_background_label.place(relwidth=1, relheight=1)

def books_page():
    #function of the books page
    global books_page_frame, books_info_frame #making the frames global for other functions
    books_page_frame = Frame(main_frame, bg='#EFD78E')

    #adding a buttons frame
    buttons_frame = Frame(books_page_frame, bg='#EFD78E')
    buttons_frame.pack(side=TOP, pady=10)

    #adding a 'Get Books Data' button
    get_books_button = Button(buttons_frame, text="Get Books Data", font=('Times New Roman', 14), bg="blue", fg="white",cursor='hand2', command=get_books_data)
    get_books_button.pack(side=LEFT,  padx=5, pady=10, ipady=4, ipadx=7)

    #adding an 'Instructions' button
    instructions_button = Button(buttons_frame, text="Instructions", font=('Times New Roman', 14), bg="green", fg="white",cursor='hand2', command=lambda: switch_indicator(indicator=books_indicator, page=replace_start_frame))
    instructions_button.pack(side=LEFT,  padx=5, pady=10, ipady=4, ipadx=7)

    #adding an 'Exit' button
    exit_button = Button(buttons_frame, text="Exit", font=('Times New Roman', 14), bg="red", fg="white",cursor='hand2', command=lambda: switch_indicator(indicator=books_indicator, page=replace_main_frame))
    exit_button.pack(side=LEFT,  padx=5, pady=10, ipady=4, ipadx=7)

    #creating a books_info_frame
    books_info_frame = Frame(books_page_frame,bg='#EFD78E')
    books_info_frame.pack(fill=BOTH, expand=True)

    books_page_frame.pack(fill=BOTH, expand=True)

def movies_page():
    #function of the movies page
    global movies_page_frame, movies_info_frame #making the frames global for other functions
    movies_page_frame = Frame(main_frame, bg='#EFD78E')

    #adding a buttons frame
    buttons_frame = Frame(movies_page_frame, bg='#EFD78E')
    buttons_frame.pack(side=TOP, pady=10)

    #adding a 'Get Movies Data' button
    get_movies_button = Button(buttons_frame, text="Get Movies Data", font=('Times New Roman', 14), bg="blue", fg="white",cursor='hand2', command=get_movies_data)
    get_movies_button.pack(side=LEFT, padx=5, pady=10, ipady=4, ipadx=7)

    #adding an 'Instructions' button
    instructions_button = Button(buttons_frame, text="Instructions", font=('Times New Roman', 14), bg="green", fg="white",cursor='hand2', command=lambda: switch_indicator(indicator=movies_indicator, page=replace_start_frame))
    instructions_button.pack(side=LEFT, padx=5, pady=10, ipady=4, ipadx=7)

    #adding an 'Exit' button
    exit_button = Button(buttons_frame, text="Exit", font=('Times New Roman', 14), bg="red", fg="white",cursor='hand2', command=lambda: switch_indicator(indicator=movies_indicator, page=replace_main_frame))
    exit_button.pack(side=LEFT, padx=5, pady=10, ipady=4, ipadx=7)

    #creating a movies info frame
    movies_info_frame = Frame(movies_page_frame, bg='#EFD78E')
    movies_info_frame.pack(fill=BOTH, expand=True)

    movies_page_frame.pack(fill=BOTH, expand=True)

def characters_page():
    #function of the characters page
    global characters_info_frame #making the frame global for other functions
    characters_page_frame = Frame(main_frame, bg='#EFD78E')

    #creating a search bar frame
    search_frame = Frame(characters_page_frame, bg='#EFD78E')
    search_frame.pack(side=TOP, pady=5)

    #adding a search label
    search_label = Label(search_frame, text="Search Character By Name:", font=('Georgia', 14), bg='#EFD78E', wraplength=350)
    search_label.pack(side=LEFT, padx=5)

    #adding a search entry field
    search_entry = Entry(search_frame, font=('Arial', 12), width=30)
    search_entry.pack(side=LEFT, padx=5, pady=10, ipady=8, ipadx=7)

    #adding a 'Search' button
    search_button = Button(search_frame, text="Search", font=('Times New Roman', 14), bg="blue", fg="white",cursor='hand2', command=lambda: search_characters(search_entry.get()))
    search_button.pack(side=LEFT, padx=5, pady=10, ipady=1, ipadx=7)

    #adding a buttons frame
    buttons_frame = Frame(characters_page_frame, bg='#EFD78E')
    buttons_frame.pack(side=TOP)

    #adding an 'Instructions' button
    instructions_button = Button(buttons_frame, text="Instructions", font=('Times New Roman', 14), bg="green", fg="white",cursor='hand2', command=lambda: switch_indicator(indicator=characters_indicator, page=replace_start_frame))
    instructions_button.pack(side=LEFT, padx=5, pady=10, ipady=4, ipadx=7)

    #adding an 'Exit' button
    exit_button = Button(buttons_frame, text="Exit", font=('Times New Roman', 14), bg="red", fg="white",cursor='hand2', command=lambda: switch_indicator(indicator=characters_indicator, page=replace_main_frame))
    exit_button.pack(side=LEFT, padx=5, pady=10, ipady=4, ipadx=7)

    #creating a characters_info_frame
    characters_info_frame = Frame(characters_page_frame, bg='#EFD78E')
    characters_info_frame.pack(fill=BOTH, expand=True, pady=5)

    characters_page_frame.pack(fill=BOTH, expand=True)

def potions_page():
    #function of the potions page
    global potions_page_frame, potions_info_frame #making the frames global for other functions
    potions_page_frame = Frame(main_frame, bg='#EFD78E')

    #adding a buttons frame
    buttons_frame = Frame(potions_page_frame, bg='#EFD78E')
    buttons_frame.pack(side=TOP, pady=10)

    #adding a 'Get Random Potions' button
    get_random_potions_button = Button(buttons_frame, text="Get A Random Potion", font=('Times New Roman', 14), bg="blue", fg="white",cursor='hand2', command=get_random_potion_data)
    get_random_potions_button.pack(side=LEFT, padx=5, pady=10, ipady=4, ipadx=7)

    #adding an 'Instructions' button
    instructions_button = Button(buttons_frame, text="Instructions", font=('Times New Roman', 14), bg="green", fg="white",cursor='hand2', command=lambda: switch_indicator(indicator=potions_indicator, page=replace_start_frame))
    instructions_button.pack(side=LEFT, padx=5, pady=10, ipady=4, ipadx=7)

    #adding an 'Exit' button
    exit_button = Button(buttons_frame, text="Exit", font=('Times New Roman', 14), bg="red", fg="white",cursor='hand2', command=lambda: switch_indicator(indicator=potions_indicator, page=replace_main_frame))
    exit_button.pack(side=LEFT, padx=5, pady=10, ipady=4, ipadx=7)

    #creating a potions_info_frame
    potions_info_frame = Frame(potions_page_frame, bg='#EFD78E')
    potions_info_frame.pack(fill=BOTH, expand=True)

    potions_page_frame.pack(fill=BOTH, expand=True)

def spells_page():
    #function of the spells page
    global spells_page_frame, spell_info_frame #making the frames global for other functions
    spells_page_frame = Frame(main_frame, bg='#EFD78E')

    #adding a buttons frame
    buttons_frame = Frame(spells_page_frame, bg='#EFD78E')
    buttons_frame.pack(side=TOP, pady=10)

    #adding a 'Get Random Spell' button
    get_random_spell_button = Button(buttons_frame, text="Get A Random Spell", font=('Times New Roman', 14), bg="blue", fg="white",cursor='hand2', command=get_random_spell_data)
    get_random_spell_button.pack(side=LEFT, padx=5, pady=10, ipady=4, ipadx=7)

    #adding an 'Instructions' button
    instructions_button = Button(buttons_frame, text="Instructions", font=('Times New Roman', 14), bg="green", fg="white",cursor='hand2', command=lambda: switch_indicator(indicator=spells_indicator, page=replace_start_frame))
    instructions_button.pack(side=LEFT, padx=5, pady=10, ipady=4, ipadx=7)

    #adding an 'Exit' button
    exit_button = Button(buttons_frame, text="Exit", font=('Times New Roman', 14), bg="red", fg="white",cursor='hand2', command=lambda: switch_indicator(indicator=spells_indicator, page=replace_main_frame))
    exit_button.pack(side=LEFT, padx=5, pady=10, ipady=4, ipadx=7)

    #creating a spells_info_frame
    spell_info_frame = Frame(spells_page_frame, bg='#EFD78E')
    spell_info_frame.pack(fill=BOTH, expand=True)

    spells_page_frame.pack(fill=BOTH, expand=True)

root.mainloop() #running the mainloop for the GUI to appear
