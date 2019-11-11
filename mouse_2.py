from tkinter import *

class MouseLocation( Frame ):
   def __init__( self ):
      Frame.__init__( self )
      self.pack( expand = YES, fill = BOTH )
      self.master.title( "Demonstrating Mouse Events" )
      self.master.geometry(  "275x100" )
      
      self.mousePosition = StringVar() # displays mouse position
      self.mousePosition.set( "Mouse outside window" )
      self.positionLabel = Label( self,
         textvariable = self.mousePosition )
      self.positionLabel.pack( side = BOTTOM )
      self.button_1 = Button(self, text = "Submit", command = self.save).pack()
      # bind mouse events to window
      self.bind( "<Button-1>", self.buttonPressed )
      
      #self.buttonfunc()

    
   global x
   global y

   def buttonPressed( self, event ):
      self.mousePosition.set( "Pressed at [ " + str( event.x ) + 
         ", " + str( event.y ) + " ]" )
        
      global x
      global y
      x = str(event.x)
        
      y = str(event.y)

   def save(self):
       global x
       global y
       print("f," + x + ' , ' + y)
    #def buttonfunc(self)
    # Create Button to open file directory
        #self.button_1 = Button(self, text = "submit", command = self.buttonPressed).pack()
    # self.button = Tk.Button(self.labelFrame, text = "File Browser", command = self.fileDialog)
    #self.button.pack()

def main():
   MouseLocation().mainloop()

if __name__ == "__main__":
   main()