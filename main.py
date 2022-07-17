from tkinter import Tk, Label, Entry, Button, StringVar, W, E, filedialog, messagebox, ttk
import imageResize
import imageNegative
import plotHist
from PIL import Image
import imghdr
import numpy as np
import cv2

class Gui:

    def __init__(self, master):
        self.master = master
        master.title("Image Resizer")

        self.filename = "..."
        self.xOrig = "X"
        self.yOrig = "Y"
        self.aOrig = "Alpha"
        
        self.filter = "Nearest Neighbour"
        self.negative = "None"

        self.filename_label_text = StringVar()
        self.filename_label_text.set(self.filename)
        self.filename_label = Label(master, textvariable=self.filename_label_text)

        self.title_filename_label = Label(master, text="Filename:")
        self.title_original = Label(master, text="Original:")
        self.title_resize = Label(master, text="Resize:")
        self.label_x = Label(master, text="Width:")
        self.label_y = Label(master, text="Height:")
        self.label_a = Label(master, text="Alpha:")

        self.label_x_orig_text = StringVar()
        self.label_x_orig_text.set(self.xOrig)
        self.label_x_orig = Label(master, textvariable=self.label_x_orig_text)
        self.label_y_orig_text = StringVar()
        self.label_y_orig_text.set(self.yOrig)
        self.label_y_orig = Label(master, textvariable=self.label_y_orig_text)
        
        self.label_a_orig_text = StringVar()
        self.label_a_orig_text.set(self.aOrig)
        self.label_a_orig = Label(master, textvariable=self.label_a_orig_text)

        vc = (master.register(self.validate),
              '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.contentX = StringVar()
        self.entryX = Entry(master, text="Width: ", validate='key', validatecommand=vc,  textvariable=self.contentX)
        self.contentY = StringVar()
        self.entryY = Entry(master, text="Height: ", validate='key', validatecommand=vc, textvariable=self.contentY)
        self.contentA = StringVar()
        self.entryA = Entry(master, text="Height: ", validate='key', validatecommand=vc, textvariable=self.contentA)

        self.combobox_value = StringVar()
        self.combobox = ttk.Combobox(master, textvariable=self.combobox_value)
        self.combobox['values'] = ('Nearest Neighbour', 'Bilinear', 'Bicubic', 'Anti-Alias')
        self.combobox.current(0)
        
        self.combobox_value = StringVar()
        self.combobox2 = ttk.Combobox(master, textvariable=self.combobox_value)
        self.combobox2['values'] = ('None', 'Negative')
        self.combobox2.current(0)
        
        self.combobox_value = StringVar()
        self.combobox3 = ttk.Combobox(master, textvariable=self.combobox_value)
        self.combobox3['values'] = ('RGB', 'HSV', 'YCbCr')
        self.combobox3.current(0)

        self.browse_button = Button(master, text="Browse...", command=lambda: self.update("browse"))
        self.generate_button = Button(master, text="Resize", command=lambda: self.update("generate"))
        self.reset_button = Button(master, text="Reset Window", command=lambda: self.update("reset"))
        
        self.equal = Button(master, text="Histogram Equalization", command=lambda: self.update("equal"))
        self.matching = Button(master, text="Matching Histogram", command=lambda: self.update("matching"))
        

        # Layout
        self.title_filename_label.grid(row=0, column=0, sticky=W)
        self.browse_button.grid(row=0, column=4, sticky=W+E)
        self.filename_label.grid(row=0, column=1, columnspan=3, sticky=W)
        self.title_original.grid(row=1, column=1, sticky=W+E)
        self.title_resize.grid(row=1, column=4, sticky=W+E)
        self.label_x.grid(row=2, column=0, sticky=W)
        self.label_y.grid(row=3, column=0, sticky=W)
        #self.label_a.grid(row=4, column=0, sticky=W)
        self.label_x_orig.grid(row=2, column=1, sticky=W+E)
        self.label_y_orig.grid(row=3, column=1, sticky=W+E)
        self.label_a_orig.grid(row=4, column=1, sticky=W+E)
        self.entryX.grid(row=2, column=4, sticky=W+E)
        self.entryY.grid(row=3, column=4, sticky=W+E)
        self.entryA.grid(row=4, column=4, sticky=W+E)
        self.combobox.grid(row=5, column=0, columnspan=3, sticky=W+E)
        self.combobox2.grid(row=5, column=4, columnspan=3, sticky=W+E)
        self.combobox3.grid(row=6, column=0, columnspan=8, sticky=W+E)
        
        self.generate_button.grid(row=7, column=0, columnspan=4, sticky=W+E)
        self.reset_button.grid(row=7, column=4, sticky=W+E)
        
        self.equal.grid(row=8, column=0, columnspan=8, sticky=W+E)
        self.matching.grid(row=9, column=0, columnspan=8, sticky=W+E)

        self.im = Image

    def update(self, method):
        if method == "browse":
            self.clear()
            root = Tk()
            myFormats = [('Portable Network Graphics (.png)', '*.png'),
                         ('JPEG / JFIF (.jpg)', '*.jpg'),
                         ('Windows Bitmap (.bmp)', '*.bmp'),
                         ('CompuServer GIF (.gif)', '*.gif')]
            file = filedialog.askopenfile(parent=root, mode='rb', defaultextension=".png", filetypes=myFormats, title='Choose a file')
            if file is not None:
                if imghdr.what(file) is None:
                    messagebox.showinfo("Error", "Non-image file selected.")
                else:

                    self.filename = file.name
                    self.filename_label_text.set(self.filename)

                    # Populate original width and height fields
                    self.im = Image.open(self.filename)
                    origWidth, origHeight = self.im.size
                    self.xOrig = origWidth
                    self.label_x_orig_text.set(self.xOrig)
                    self.yOrig = origHeight
                    self.label_y_orig_text.set(self.yOrig)
                    self.contentX.set(origWidth)
                    self.contentY.set(origHeight)
                    self.contentA.set(0)   
                    
            root.withdraw()
        elif method == "generate":
            if not (self.contentX.get() == "") or (self.contentY.get() == ""):
                self.filter = self.combobox.get()
                self.negative = self.combobox2.get()
                self.cls = self.combobox3.get()
                img = imageResize.resizeImage(self.im, self.filter, int(self.contentX.get()), int(self.contentY.get()))
                #if(self.negative == 'Negative'):
                img = imageNegative.negativeImage(img, neg = self.negative, cls = self.cls, a=self.contentA.get())
                
                file = filedialog.asksaveasfilename(defaultextension=".png")
                if file:
                    img.save(file)
                imageResize.plot(np.asarray(self.im), np.asarray(img), cls = self.cls)
        
        elif method == "equal":
            self.cls = self.combobox3.get()
            self.cls = self.combobox3.get()
            if self.cls == "HSV":
                img = cv2.cvtColor(np.array(self.im), cv2.COLOR_RGB2HSV)
            elif self.cls == "YCbCr":
                img = cv2.cvtColor(np.array(self.im), cv2.COLOR_RGB2YCrCb)
            else:
                img = np.array(self.im)
            #plotHist.equal(np.asarray(self.im))
            plotHist.equal(img, cls = self.cls)
            new_equal = Image.open('new_img_color.png')     
            #plotHist.plot(np.asarray(self.im), np.asarray(new_equal))
            plotHist.plot(img, np.asarray(new_equal), cls = self.cls)
        
        elif method == "matching":

            root = Tk()
            myFormats = [('Portable Network Graphics (.png)', '*.png'),
                         ('JPEG / JFIF (.jpg)', '*.jpg'),
                         ('Windows Bitmap (.bmp)', '*.bmp'),
                         ('CompuServer GIF (.gif)', '*.gif')]
            file = filedialog.askopenfile(parent=root, mode='rb', defaultextension=".png", filetypes=myFormats, title='Choose a file')
            if file:                   
                target = Image.open(file)
                root.withdraw()
                target = imageResize.resizeImage(target, self.filter, int(self.im.size[0]), int(self.im.size[1]))

                plotHist.match(np.asarray(self.im), np.asarray(target))
                new_match = Image.open('new_img_color_2.png')
                plotHist.plot_matching(np.asarray(self.im), np.asarray(target), np.asarray(new_match))       
        else:  # reset
            self.clear()

    def clear(self):
        self.filename = "..."
        self.filename_label_text.set(self.filename)
        self.xOrig = "X"
        self.label_x_orig_text.set(self.xOrig)
        self.yOrig = "Y"
        self.label_y_orig_text.set(self.yOrig)
        self.contentX.set("")
        self.contentY.set("")
        self.combobox.current(0)

    def validate(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
        if text in '0123456789':
            if len(value_if_allowed) != 0:
                try:
                    int(value_if_allowed)
                    return True
                except ValueError:
                    return False
        else:
            return False


root = Tk()
my_gui = Gui(root)
root.mainloop()
