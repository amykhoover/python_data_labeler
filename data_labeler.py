import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import pandas as pd


class ImageLabelingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Labeling App")

        # Variables
        self.image_folder_path = ""
        self.image_paths = []
        self.current_image_index = 0

        # UI Components
        self.label_frame = tk.LabelFrame(root, text="Image")
        self.label_frame.pack(fill="both", expand="yes")

        self.image_label = tk.Label(self.label_frame)
        self.image_label.pack()

        self.entry_label = tk.Entry(root)
        self.entry_label.pack()

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        self.select_button = tk.Button(
            self.button_frame, text="Select Directory", command=self.select_directory
        )
        self.select_button.pack(side=tk.LEFT)

        self.label_button = tk.Button(
            self.button_frame, text="Label Image", command=self.label_image
        )
        self.label_button.pack(side=tk.LEFT)

        self.csv_file = "image_labels.csv"
        # Bind Enter key to label_image function
        root.bind("<Return>", self.label_image)

    def select_directory(self):
        self.image_folder_path = filedialog.askdirectory()
        if self.image_folder_path:
            self.image_paths = [
                os.path.join(self.image_folder_path, f)
                for f in os.listdir(self.image_folder_path)
                if f.lower().endswith((".png", ".jpg", ".jpeg"))
            ]
            self.current_image_index = 0
            self.display_image()

    def display_image(self):
        if self.current_image_index < len(self.image_paths):
            image_path = self.image_paths[self.current_image_index]
            img = Image.open(image_path)
            img = img.resize((250, 250), Image.Resampling.LANCZOS)  # Updated line
            img = ImageTk.PhotoImage(img)
            self.image_label.config(image=img)
            self.image_label.image = img
            self.entry_label.delete(0, tk.END)
        else:
            messagebox.showinfo("End of Directory", "No more images in the directory.")

    def label_image(self, event=None):
        if self.current_image_index < len(self.image_paths):
            label = self.entry_label.get()
            image_path = self.image_paths[self.current_image_index]

            # Append to CSV
            df = pd.DataFrame([[image_path, label]], columns=["Image_Path", "Label"])
            if not os.path.isfile(self.csv_file):
                df.to_csv(self.csv_file, index=False)
            else:
                df.to_csv(self.csv_file, mode="a", header=False, index=False)

            self.current_image_index += 1
            self.display_image()


# Create and run the app
root = tk.Tk()
app = ImageLabelingApp(root)
root.mainloop()
