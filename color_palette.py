import cv2
from tkinter import *
import tkinter as tk
from tkinter import filedialog
import numpy as np
from PIL import Image, ImageTk
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

class App:
    # the init method in python refers to the constructor of the class
    def __init__(self, tkObject):
        
        #self.x : refers to a class variable or class method named x 
        self.tkObject = tkObject 
        self.bg="#100f1f" #class variable that stores the background color for the app
        self.font="Calibri 20 bold" #class variable that stores font style
        self.fg = "white" #class variable that stores font color
        
        tkObject.title("Image Color Palette Generator") #app title
        tkObject["background"] = self.bg #setting the app background color
    
        #1- label is a widget that can show us text or an image
        self.img_text_label = tk.Label(tkObject, fg=self.fg, font=self.font, bg=self.bg, padx = 50, pady=50,text="Color Palette Generator")
        #2- packing "attaching" the widget to the screen or the app, without this method the widget won't appear on the screen
        self.img_text_label.pack()

        self.img_button = tk.Button(tkObject, fg=self.fg, bg=self.bg, font=self.font, text="Select Image", command=self.open_image)
        self.img_button.pack()

        #this is an empty label that simply work as an empty space between widgets "m1 for margin 1"
        self.m1 = tk.Label(tkObject,  bg=self.bg, pady = 15)
        self.m1.pack()

        self.img_label = tk.Label(tkObject, bg=self.bg,)
        self.img_label.pack()

        self.m2 = tk.Label(tkObject,  bg=self.bg, pady = 15)
        self.m2.pack()

        self.palette_title = tk.Label(tkObject, fg=self.fg, font=self.font, bg=self.bg, text="Color Palette:")
        self.palette_title.pack()
        
        #creating a matrix of width and height of 100,500 and each element consists of 3 value all of them are 0 "black"
        placeholder = np.zeros((100, 500, 3), dtype = "uint8")
        placeholder_tk_image = ImageTk.PhotoImage( image= Image.fromarray(placeholder) ) #converting the matrix to tkinter image

        self.palette_image = tk.Label(tkObject, fg=self.fg, font=self.font, bg=self.bg, image=placeholder_tk_image, width=400, height=50)
        self.palette_image.pack()

        self.m0 = tk.Label(tkObject,  bg=self.bg, pady = 5)
        self.m0.pack()

        self.palette_codes= tk.Label(tkObject, padx=40, fg=self.fg, font="Calibri 15 bold", bg=self.bg, text=" ")
        self.palette_codes.pack()

        self.m3 = tk.Label(tkObject,  bg=self.bg, pady = 5)
        self.m3.pack()

        self.quit_button = tk.Button(tkObject, fg=self.fg, font=self.font, bg=self.bg, text="Quit", command=tkObject.quit,)
        self.quit_button.pack()


        self.m4 = tk.Label(tkObject,  bg=self.bg, pady = 15)
        self.m4.pack()
        

    #this function is executed after clicking the "Select Image" button
    def open_image(self):
        file_path = filedialog.askopenfilename() #this function opens a file dialog and return the path of chosen image
        
        #after that we execute the generate_palette class function and pass to it the file_path
        self.generate_palette(file_path)




    def generate_palette(self, file_path):
        
        #reading the image from the file and resizing it to 5 times less so the processing is faster
        image = cv2.imread(file_path)
        image= cv2.resize(image, None, fx=0.2, fy=0.2)



        # We reshape our 2D image matrix into a 1D list of RGB pixels, so the model is able to process it
        #example: 
        """
        [
            [ [25,100,242],[1,200,0] ],
            [ [80,30,125],[3,20,100] ],
            [ [19,45,0],[79,36,244] ],
        ]
        
        becomes
        
        [   [25,100,242],[1,200,0],[80,30,125],[3,20,100],[19,45,0],[79,36,244]   ]     #list of pixels
        
        """
        #end of example
        
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image.reshape((image.shape[0] * image.shape[1], 3))

        
        #number of groups that the knn model will output, in our case it's the number of colors in the color palette
        number_of_clusters = 5      
        clt = KMeans(number_of_clusters)
        
        #knn model process the image
        clt.fit(image)
        

        hist = np.bincount(clt.labels_).astype("float")
        hist/=hist.sum()

        print(hist)
        print("***************************************************")
        print(clt.labels_)
        print("***************************************************")
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

        
        self.palette_image.configure(image=tk_image)
        self.palette_image.image=tk_image



root = tk.Tk()
app = App(root)
root.mainloop()
