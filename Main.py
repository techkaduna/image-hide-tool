'''This script is Authored by Kolawole Andrew and is intended to be part of a collection of tools 
written for cyber security and penetration testing. This tool is specifically written to embed scripts 
images into an image as well as retrieve them. Updates will be written for the script with time'''

import os
import time
from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
import PIL.Image,io



root = Tk()

class App():
    '''The base class for the application'''
    def __init__(self,master):
        
        self.master = master
        self.fileName = ''
        self.hidden = ''
        self.img = None
        
        

        #The main widgets get initialised on every object call off the class
        self.master.geometry('550x600')
        self.master.title('Photo Hide')
        self.master.resizable(0,0)
        self.master.config(bg='lightgrey')
        #frames
        self.frame1 = Frame(self.master,bg='lightgrey')
        self.frame1.pack(fill='x')
        self.frame2 = Frame(self.master,bg='lightgrey')
        self.frame2.pack(fill='both')
        self.frame3 = Frame(self.master,bg='lightgrey')
        self.frame3.pack(fill='both')


        #Title Label
        self.lbl = Label(self.frame1,text='$TEXT IN JPEGS$')
        self.lbl.config(font=('Banschrift',18),bg='lightgrey')
        self.lbl.pack()

        #info label
        self.infolabel = Label(self.frame3,bg='lightgrey')

        #Text Area
        self.txt = scrolledtext.ScrolledText(self.frame2)
        self.txt.config(state='disabled')
        self.txt.pack()

        self.txtbtn = Button(self.frame2,text='Add Text',command=self.addText)
        self.txtbtn.config(bg='#99ccff',font=('Arial',14),state='disabled')
        self.txtbtn.pack(padx=15)

        #buttons
        self.openbtn = Button(self.frame3,text='Open Image',width=10,command=self.openImage)
        self.openbtn.config(bg='#99ccff',font=('Arial',14))
        #self.openbtn.bind('<ctrl+s->',self.openImage)
        self.openbtn.grid(row=0,column=0,padx=15)
        

        self.Xtractbtn = Button(self.frame3,text='Extract',width=10,command=self.topLevel)
        self.Xtractbtn.config(bg='#99ccff',font=('Arial',14),state='disabled')
        self.Xtractbtn.grid(row=1,column=0,padx=5,pady=5)
        
        self.img_write = Button(self.frame3,text='Images',width=10,command=self.img_works)
        self.img_write.config(bg='#99ccff',font=('Arial',14),state='disabled')
        self.img_write.grid(row=1,column=1,padx=5,pady=5)


        # tkinter's mainloop
        self.master.mainloop()

    def openImage(self):
        '''Opens image which an object will be embedded in, for now the image expected is a jpg file'''
        try:
            self.fileName = filedialog.askopenfilename(initialdir=os.getcwd,filetypes=(('JPG Files','*jpg'),('JPG Files','*jpg',)))
            
            if len(self.fileName) < 3:
                self.infolabel = Label(self.frame3,text='No file was opened..',bg='lightgrey')
                self.infolabel.grid(row=0,column=1)
            else:
                self.file = self.fileName.split('/')[-1]
                self.infolabel.config(text=f"{self.file} is opened")
                self.infolabel.grid(row=0,column=1)
                self.txt.config(state='normal')
                self.txtbtn.config(state='normal')
                self.Xtractbtn.config(state='normal')
                self.img_write.config(state='normal')
        except:
            self.infolabel = Label(self.frame3,text='Error while opening Image....',bg='lightgrey')
            self.infolabel.grid(row=0,column=1)
            
            


    def addText(self):
        '''Method used to embed written plain text (from a text feild) into the image. The email is binded to a text feild.'''
        try:
            with open(self.fileName,'ab') as f:
                f.write(self.txt.get('1.0',END).encode())
                f.close()
            self.infolabel.destroy()
            self.txt.delete('1.0',END)
        except Exception as e:
            self.infolabel = Label(self.frame3,text='An error occured...'+str(e),bg='lightgrey')
            self.infolabel.grid(row=1,column=1)


    def topLevel(self):
        '''Top level window that extract texts from an opened image.This method is binded to a button'''
        try:
            with open(self.fileName,'rb') as f:
                self.content  = f.read()
                self.offset = self.content.index(bytes.fromhex('FFD9'))
                f.seek(self.offset + 2)
                self.hidden = f.read()
        except Exception as e:
            self.infolabel = Label(self.frame3,text='An error occured...'+str(e),bg='lightgrey')
            self.infolabel.grid(row=1,column=1)

        #print(self.content)
        top = Toplevel()
        top.geometry('300x400')
        top.resizable(0,0)
        top.title('Xtracor')
        top.config(bg='lightgrey')

        #frames
        frame1 = Frame(top)
        frame1.pack()

        frame2 = Frame(top)
        frame2.pack()

        frame3 = Frame(top)
        frame3.pack()

        #labels
        lbl = Label(frame1,text='Xtractor')
        lbl.config(font=('Arial',18),bg='lightgrey')
        lbl.pack()

        #Xtracted text
        xtxt = scrolledtext.ScrolledText(frame2)
        xtxt.config(height=20)
        xtxt.insert(INSERT,self.hidden)
        xtxt.pack()

        xbtn = Button(frame3,width=15,text='Save Text',command=self.savetext)
        xbtn.config(bg='#99ccff')
        xbtn.pack()

        top.mainloop()



    def savetext(self):
        '''Saves text detached from a script to a file.This method is binded to a button.'''
        try:
            self.saveFile = filedialog.asksaveasfilename(initialdir=os.getcwd,title='Save',filetypes=(('Text Files','*txt'),('Text Files','*txt')))
            with open(self.saveFile,'w') as f:
                f.write(str(self.hidden))
                f.close()
        except:
            pass

    def add_image(self):
        '''embeds an image into an opened image.'''
        try:
            self.img_file = filedialog.askopenfilename(initialdir=os.getcwd,filetypes=(('JPG Files','*jpg'),('JPG Files','*jpg',)))
            
            self.img = PIL.Image.open(self.img_file)
            byte_arr = io.BytesIO()
            self.img.save(byte_arr,format='PNG')
            with open(self.fileName,'ab') as f:
                print('about to write to image')
                f.write(byte_arr.getvalue())
                f.close()
                print('Written to image')
            self._lbl2.config(text='Emeded payload successfully')
        except Exception as e:
            self._lbl2.config(text='An error occured while embeding payload')

    def img_works(self):
        '''Top level window for working with image embedding and extractions'''
        top = Toplevel()
        top.geometry('300x200')
        top.resizable(0,0)
        top.title('Image Hexer')
        top.config(bg='lightgrey')

        lbl =  Label(top,text='Add insert image '.upper(),bg='lightgrey',font=('Banschrift',16))
        lbl.grid(row=0,column=0,columnspan=3,padx=10)
        self._lbl2 = Label(top,bg='lightgrey')
        self._lbl2.grid(row=1,column=0,columnspan=3)
        btn_add = Button(top,text='Add Image',bg='lightgrey',command=self.add_image,width=10)
        btn_add.grid(row=2,column=0,padx=5,pady=5)

        btn_detach = Button(top,text='Detach',bg='lightgrey',command=self.remove_img,width=10)
        btn_detach.grid(row=2,column=1,padx=5,pady=5)

        top.mainloop()

        
    def remove_img(self):
        '''Method used to detach an embedded image(payload) from an image'''
        try:
            with open(self.fileName,'rb') as f:
                content = f.read()
                offset = content.index(bytes.fromhex('FFD9'))
                f.seek(offset+2)
                new_img = PIL.Image.open(io.BytesIO(f.read()))
                self.save_img = filedialog.asksaveasfilename(initialdir=os.getcwd,title='Save',filetypes=(('JPG Files','*jpg'),('PNG Files','*png')))
                new_img.save(self.save_img+'.png')
            self._lbl2.config(text='Detached payload successfully')
        except Exception as e:
            self._lbl2.config(text='An error occured while embeding payload')

if __name__ == '__main__':
    root = App(root)  