import cv2
from tkinter import *
import tkinter as tk
from tkinter import filedialog
import numpy as np
from PIL import Image, ImageTk
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

class App:
    def __init__(self, master):
        self.master = master
        self.bg="#100f1f"
        self.font="Calibri 20 bold"
        self.fg = "white"
        master.title("Image Color Palette Generator")
        master["background"] = self.bg
        

        placeholder = np.zeros((100, 500, 3), dtype = "uint8")
        placeholder_pil_image = Image.fromarray(placeholder)
        placeholder_tk_image = ImageTk.PhotoImage(image=placeholder_pil_image)

        self.img_text_label = tk.Label(master, fg=self.fg, font=self.font, bg=self.bg, padx = 50, pady=50,
                                       text="Color Palette Generator")
        self.img_text_label.pack()

        self.img_button = tk.Button(master, fg=self.fg, bg=self.bg, font=self.font, text="Select Image", command=self.open_image)
        self.img_button.pack()

        self.m1 = tk.Label(master,  bg=self.bg, pady = 15)
        self.m1.pack()

        self.img_label = tk.Label(master, bg=self.bg,)
        self.img_label.pack()

        self.m2 = tk.Label(master,  bg=self.bg, pady = 15)
        self.m2.pack()

        self.palette_label = tk.Label(master, fg=self.fg, font=self.font, bg=self.bg, text="Color Palette:")
        self.palette_label.pack()

        self.palette_canvas = tk.Label(master, fg=self.fg, font=self.font, bg=self.bg, image=placeholder_tk_image, width=400, height=50)
        self.palette_canvas.pack()

        self.m0 = tk.Label(master,  bg=self.bg, pady = 5)
        self.m0.pack()

        self.palette_codes= tk.Label(master, padx=40, fg=self.fg, font="Calibri 15 bold", bg=self.bg, text=" ")
        self.palette_codes.pack()

        self.m3 = tk.Label(master,  bg=self.bg, pady = 5)
        self.m3.pack()

        self.quit_button = tk.Button(master, fg=self.fg, font=self.font, bg=self.bg, text="Quit", command=master.quit,)
        self.quit_button.pack()


        self.m4 = tk.Label(master,  bg=self.bg, pady = 15)
        self.m4.pack()
        

    def open_image(self):
        file_path = filedialog.askopenfilename()
        self.generate_palette(file_path)

    def generate_palette(self, file_path):
        image = cv2.imread(file_path)

        image= cv2.resize(image, None, fx=0.2, fy=0.2)


        # We reshape our image into a list of RGB pixels
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image.reshape((image.shape[0] * image.shape[1], 3))

        number_of_clusters = 5
        
        clt = KMeans(number_of_clusters)
        clt.fit(image)
        

        hist = np.bincount(clt.labels_).astype("float")
        hist/=hist.sum()

        print(hist)
        print(clt.cluster_centers_)

        self.display_palette(hist, clt.cluster_centers_, file_path)

    def display_palette(self, hist , centroids, file_path):

        #displaying the chosen image
        cv_img_bgr = cv2.imread(file_path)
        cv_img_rgb = cv2.cvtColor(cv_img_bgr, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cv_img_rgb)
        image_resized = pil_image.resize((250,250))
        tk_image = ImageTk.PhotoImage(image=image_resized)
        self.img_label.configure(image=tk_image)
        self.img_label.image=tk_image

        #displaying color codes
        text = ""
        i=1
        for color in centroids:
            text += f"rgb({int(color[0])}, {int(color[1])}, {int(color[2])})," + (5*" ")
            i+=1
            
        self.palette_codes.configure(text=text[:-6])
        
        # Create our blank barchart
        bar = np.zeros((100, 500, 3), dtype = "uint8")

        x_start = 0
        # iterate over the percentage and dominant color of each cluster
        
        for (percent, color) in zip(hist, centroids):
          # plot the relative percentage of each cluster
          end = x_start + (percent * 500)
          cv2.rectangle(bar, (int(x_start), 0), (int(end), 100), color.astype("uint8").tolist(), -1)
          x_start = end

        pil_image = Image.fromarray(bar)
        tk_image = ImageTk.PhotoImage(image=pil_image)

        self.palette_canvas.configure(image=tk_image)
        self.palette_canvas.image=tk_image

root = tk.Tk()
app = App(root)
root.mainloop()
