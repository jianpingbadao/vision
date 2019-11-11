# This program isolates mouse click coordinates in relation to the GUI window/frame
# The coordinates are displayed at the bottom.
# The Submit button still needs to be fixed to save coordinates
# Tracks using events

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
      self.button_1 = Button(self, text = "Submit", command = self.buttonPressed).pack()
      # bind mouse events to window
      self.bind( "<Button-1>", self.buttonPressed )
      
      #self.buttonfunc()

    
   # global x 
   # x = []
   # global y 
   # y = []
   # global i
   def buttonPressed( self, event ):
      self.mousePosition.set( "Pressed at [ " + str( event.x ) + 
         ", " + str( event.y ) + " ]" )
        
      # global x
      # x = [2]
      # global y 
      # y = [2]
      # global i
      # i = 1
      # x[i] = str(event.x)
        
      # y[i] = str(event.y)

   # def save(self):
     #  global x 
     #  x = [2]
     #  global y 
     #  y = [2]
     #  print("f," + x[0] + ' , ' + y[0])
    #def buttonfunc(self)
    # Create Button to open file directory
        #self.button_1 = Button(self, text = "submit", command = self.buttonPressed).pack()
    # self.button = Tk.Button(self.labelFrame, text = "File Browser", command = self.fileDialog)
    #self.button.pack()

def main():
   MouseLocation().mainloop()

if __name__ == "__main__":
   main()