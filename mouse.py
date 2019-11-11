# Sample of how a mouse click works.
# Currently tracks mouse clicks indefinitly
# the listener can be stopped, however once the thread is stopped it
# can't be restarted
from pynput.mouse import Listener

def on_click(x, y, button, pressed):
    if pressed:
        print("Mouse clicked at({0}, {1}) with {2}".format(x,y,button))


with Listener(on_click = on_click) as listener:
    listener.join()