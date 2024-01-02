# Importing necessary libraries
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
from keras.models import load_model

# Loading the model
model = load_model("Age_Sex_Detection.h5")

# Initializing the GUI
top = tk.Tk()
top.geometry("800x600")
top.title("Age & Gender Detector")
top.configure(background="#CDCDCD")

# Initializing the Labels(1 for age and 1 for sex)
label1 = Label(top, background="#CDCDCD", font=("arial", 15, "bold"))
label2 = Label(top, background="#CDCDCD", font=("arial", 15, "bold"))
sign_image = Label(top)


# Defining detect function which detects the age and gender of the person in the image using the model
def Detect(file_path):
    global label1, label2
    image = Image.open(file_path)
    image = image.resize((48, 48))
    image = np.array(image)
    image = image[:, :, :3]  # Keep only RGB channels
    image = np.expand_dims(image, axis=0) / 255.0  # Normalize the image
    print(image.shape)
    sex_f = ["Male", "Female"]
    pred = model.predict(image)
    age = int(np.round(pred[1][0]))
    sex = int(np.round(pred[0][0]))
    print("Predicted Age is " + str(age))
    print("Predicted Gender is " + sex_f[sex])
    label1.configure(foreground="#011638", text="Predicted Age: " + str(age))
    label2.configure(foreground="#011638", text="Predicted Gender: " + sex_f[sex])


# Defining show_detect button function
def show_Detect_button(file_path):
    Detect_b = Button(
        top, text="Detect Image", command=lambda: Detect(file_path), padx=10, pady=5
    )
    Detect_b.configure(
        background="#364156", foreground="white", font=("arial", 10, "bold")
    )
    Detect_b.place(relx=0.79, rely=0.46)


# Defining upload image function
def upload_image():
    try:
        file_path = filedialog.askopenfilename()
        uploaded = Image.open(file_path)
        # Resize the image to make it larger
        uploaded = uploaded.resize((400, 300))
        im = ImageTk.PhotoImage(uploaded)

        sign_image.configure(image=im)
        sign_image.image = im  # Fix the typo in 'image'
        label1.configure(text="")
        label2.configure(text="")
        show_Detect_button(file_path)
    except Exception as e:
        print(e)


upload = Button(top, text="Upload an Image", command=upload_image, padx=10, pady=5)
upload.configure(background="#364156", foreground="white", font=("arial", 10, "bold"))
upload.pack(side="bottom", expand=50)
sign_image.pack(side="bottom", expand=True)
label1.pack(side="bottom", expand=True)
label2.pack(side="bottom", expand=True)
heading = Label(
    top, text="Age and Gender Detector", pady=20, font=("arial", 20, "bold")
)
heading.configure(background="#CDCDCD", foreground="#364156")
heading.pack()

top.mainloop()
