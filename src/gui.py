from Robot import Robot
import tkinter
from tkinter import ttk

class Gui():
    def __init__(self):
        """
        A gui used to autonomously control the robot with user-specified speed, rotation, and time.
        Contributor: Matthew O'Brien
        """
        self.speed = None
        self.rotation = None
        self.time = None
        self.robot = Robot()
        self.robot.connect()

        self.root = tkinter.Tk()
        self.frame = ttk.Frame(self.root, padding=(20, 30), relief='raised')
        self.frame.grid()

        self.speed_entry_label = ttk.Label(self.frame, text='Enter a speed')
        self.speed_entry_label.grid(row=0, column=0)
        self.speed_entry = ttk.Entry(self.frame, width=4)
        self.speed_entry.grid(row=0, column=1)
        self.speed = tkinter.IntVar()
        self.speed_entry['textvariable'] = self.speed

        self.rotation_entry_label = ttk.Label(self.frame, text='Enter a rotational speed')
        self.rotation_entry_label.grid(row=1, column=0)
        self.rotation_entry = ttk.Entry(self.frame, width=4)
        self.rotation_entry.grid(row=1, column=1)
        self.rotation = tkinter.IntVar()
        self.rotation_entry['textvariable'] = self.rotation

        self.time_entry_label = ttk.Label(self.frame, text='Enter a time')
        self.time_entry_label.grid(row=2, column=0)
        self.time_entry = ttk.Entry(self.frame, width=4)
        self.time_entry.grid(row=2, column=1)
        self.time = tkinter.IntVar()
        self.time_entry['textvariable'] = self.time

        self.start_button = ttk.Button(self.frame, text='Start')
        self.start_button.grid(row=3, column=0)
        self.start_button['command'] = lambda : self.robot.move_autonomously(self.speed.get(), self.rotation.get(), self.time.get())

        self.root.mainloop()

    def __exit__(self):
        self.robot.disconnect()

def main():
    g = Gui()


if __name__ == '__main__':
    main()
