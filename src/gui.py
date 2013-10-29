# import Robot.py
import tkinter
from tkinter import ttk

class gui(object):
  def __init__(self):
    root = tkinter.Tk()
    frame = ttk.Frame(root, padding=(20, 30), relief='raised')
    frame.grid()
    move_forward_button = ttk.Button(frame, text='Forward')
    move_forward_button.grid(row=0, column=0)
    move_forward_button['command'] = lambda : move_forward()
    move_backward_button = ttk.Button(frame, text='Backward')
    move_backward_button.grid(row=1, column=0)
    move_backward_button['command'] = lambda : move_backward()
    curve_right_button = ttk.Button(frame, text='Curve Right')
    curve_right_button.grid(row=0, column=1)
    curve_right_button['command'] = lambda : curve_right()
    curve_left_button = ttk.Button(frame, text='Curve Left')
    curve_left_button.grid(row=1, column=1)
    curve_left_button['command'] = lambda : curve_left()
    root.mainloop()


g = gui()
