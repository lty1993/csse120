from Robot import Robot
import tkinter
from tkinter import ttk

class Gui():
    def __init__(self):
        self.speed = None
        self.rotation = None
        self.time = None
        self.robot = Robot()
        self.robot.connect()
    def __exit__(self):
        self.robot.disconnect()

def main():
    """
    A gui used to autonomously control the robot with user-specified speed, rotation, and time.
    Contributor: Matthew O'Brien
    """
    g = Gui()
    root = tkinter.Tk()
    frame = ttk.Frame(root, padding=(20, 30), relief='raised')
    frame.grid()

    speed_entry_label = ttk.Label(frame, text='Enter a speed')
    speed_entry_label.grid(row=0, column=0)
    speed_entry = ttk.Entry(frame, width=4)
    speed_entry.grid(row=0, column=1)
    g.speed = tkinter.IntVar()
    speed_entry['textvariable'] = g.speed

    rotation_entry_label = ttk.Label(frame, text='Enter a rotational speed')
    rotation_entry_label.grid(row=1, column=0)
    rotation_entry = ttk.Entry(frame, width=4)
    rotation_entry.grid(row=1, column=1)
    g.rotation = tkinter.IntVar()
    rotation_entry['textvariable'] = g.rotation

    time_entry_label = ttk.Label(frame, text='Enter a time')
    time_entry_label.grid(row=2, column=0)
    time_entry = ttk.Entry(frame, width=4)
    time_entry.grid(row=2, column=1)
    g.time = tkinter.IntVar()
    time_entry['textvariable'] = g.time

    start_button = ttk.Button(frame, text='Start')
    start_button.grid(row=3, column=0)
    start_button['command'] = lambda : g.robot.move_autonomously(g.speed.get(), g.rotation.get(), g.time.get())

    root.mainloop()


if __name__ == '__main__':
    main()
