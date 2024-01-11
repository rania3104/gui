from tkinter import *
from PIL import Image, ImageTk

def replace_start_frame():
    # Function to replace the main frame with the replacement frame
    start_frame.pack_forget()
    replacement_frame.pack()

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
start_button = Button(text_frame, text="Start", font=("Arial", 16), bg="green", fg="white", command=replace_start_frame)
start_button.pack(pady=10)

# Create a replacement frame with the same size
replacement_frame = Frame(root, width=800, height=530)
replacement_frame.pack_propagate(0)  # Disable automatic resizing of the replacement frame

options_frame = Frame(replacement_frame,bg="gray")

books_button = Button(options_frame, text="Books", font=('Arial',13), bd=0, fg='blue', activeforeground="blue")
books_button.place(x=0, y=0, width=160,height=50)

movies_button = Button(options_frame, text="Movies", font=('Arial',13), bd=0, fg='blue', activeforeground="blue")
movies_button.place(x=160, y=0, width=160,height=50)

characters_button = Button(options_frame, text="Characters", font=('Arial',13), bd=0, fg='blue', activeforeground="blue")
characters_button.place(x=320, y=0, width=160,height=50)

potions_button = Button(options_frame, text="Potions", font=('Arial',13), bd=0, fg='blue', activeforeground="blue")
potions_button.place(x=480, y=0, width=160,height=50)

spells_button = Button(options_frame, text="Spells", font=('Arial',13), bd=0, fg='blue', activeforeground="blue")
spells_button.place(x=640, y=0, width=160,height=50)

options_frame.pack(pady=5)
options_frame.pack_propagate(False)
options_frame.configure(width=800,height=60)

main_frame = Frame(replacement_frame)
main_frame.pack(fill=BOTH, expand=True)

root.mainloop()
