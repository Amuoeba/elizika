# -*- coding: utf-8 -*-
import tkinter as tk
import AutoDecode
import prepareString

class Application (tk.Frame):
    def __init__(self,parent):
        """Initializes the frame"""
        tk.Frame.__init__(self,parent)
        self.parent=parent
        self.defVariables()        
        self.create_widgets()
        self.create_menu()
        self.grid()
    
    def quit_app(self):
        self.parent.destroy()
        
    def defVariables(self):
        self.checkVar = tk.BooleanVar()
        
    
    def create_menu(self):
        self.menuBar =tk.Menu(self.parent)
        self.fileMenu = tk.Menu(self.menuBar,tearoff=0)
        self.fileMenu.add_command(label="Open")
        self.fileMenu.add_command(label="Save")
        self.fileMenu.add_command(label="Quit",command = self.quit_app)
        
        self.menuBar.add_cascade(label="file",menu=self.fileMenu)
        self.parent.config(menu=self.menuBar)
        
        
        
        
        
        
        
    def create_widgets(self):
        
        self.instructions = tk.Label(text=
        """How to use the tool:
            - to test the tool input your custom string (preferably around 120
              characters long), click encode to encode the text with a substitution
              cypher with a random key, click decode to automaticaly decode the encoded text
            - If you only have the encoded text paste it in a second text box and click decode""",justify =tk.LEFT)
        self.instructions.grid(row=0)
        
        self.button = tk.Button(self,text="Clear input text")
        self.button.bind("<Button-1>",self.ClearInputText)
        self.button.grid(row=0)
        
        #Custom text from the user
        self.text=tk.Text(self,height=10,width=50)
        self.text.grid(row = 1,columnspan=30,sticky="nsew")
        
        scrollbar = tk.Scrollbar(self,command = self.text.yview)
        scrollbar.grid(row=1,column=31,sticky="nsew")
        self.text["yscrollcommand"]=scrollbar.set
        
        #Encode button
        self.encodeButton = tk.Button(self,text="Encode")
        self.encodeButton.bind("<Button-1>",self.Encode)
        self.encodeButton.grid(row=2)
        #Encoded text
        self.textEncoded=tk.Text(self,height=10,width=50)
        self.textEncoded.grid(row = 3,columnspan=30,sticky="nsew")
    
        scrollbarEncoded = tk.Scrollbar(self,command = self.textEncoded.yview)
        scrollbarEncoded.grid(row=3,column=31,sticky="nsew")
        self.textEncoded["yscrollcommand"]=scrollbarEncoded.set
                        
        #Decode button
        self.decodeButton = tk.Button(self,text="Decode")
        self.decodeButton.bind("<Button-1>",self.Decode)
        self.decodeButton.grid(row=4)
        
        #Decoded text
        self.textDecoded=tk.Text(self,height=10,width=50)
        self.textDecoded.grid(row = 5,columnspan=30,sticky="nsew")
        
        scrollbarDecoded = tk.Scrollbar(self,command = self.textDecoded.yview)
        scrollbarDecoded.grid(row=5,column=31,sticky="nsew")
        self.textDecoded["yscrollcommand"]=scrollbarDecoded.set
        
    def ClearInputText(self,event):
        self.text.delete("1.0",tk.END)
  
    def Encode(self,event):
        text=str(self.text.get("1.0",tk.END))
        prepared = prepareString.PrepareString(text)
        key="".join(AutoDecode.shuffled(AutoDecode.alphabet))
        encoded = AutoDecode.encode(prepared,key)
        self.textEncoded.delete("1.0",tk.END)
        self.textEncoded.insert(tk.END,encoded)
       
    
    def Decode(self,event):
        encodedText = str(self.textEncoded.get("1.0",tk.END))
        decoded=AutoDecode.decode_subst(encodedText)
        self.textDecoded.delete("1.0",tk.END)
        self.textDecoded.insert(tk.END,decoded)

        
        
        
root = tk.Tk()
root.title("OOP gui test")
root.geometry("680x490+100+100")
app = Application(root)

root.mainloop()