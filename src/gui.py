from xml.etree.ElementTree import XML
from Robot import Robot
import tkinter
from tkinter import ttk

class Gui():
    def __init__(self):
        """
        A gui used to autonomously control the robot with user-specified speed, rotation, and time.
        Contributor: Matthew O'Brien, Xiangqing Zhang
        """
        self.speed = None
        self.rotation = None
        self.time = None
        self.robot = Robot()
        self.robot.connect()

        self.root = tkinter.Tk("Robot GUI")
        self.frame = None
        temp = """\
<root>
    <label name="speed_entry_label">
        <text>Enter a speed: </text>
    </label>
    <entry name="speed_entry" width='30' />
    <label name="rotation_entry_label">
        <text>Enter a rotational speed: </text>
    </label>
    <entry name="time_entry" width='30' />
    <label name="rotation_entry_label">
        <text>Enter a time: </text>
    </label>
    <entry name="time_entry" width='30' />
</root>
"""
        self.add_widget(XML(temp), self.root).pack()

        self.speed = tkinter.IntVar()
        self.frame.children['speed_entry'].config(textvariable=self.speed)

        self.rotation = tkinter.IntVar()
        self.frame.children["rotation_entry"].config(textvariable=self.rotation)

        self.time = tkinter.IntVar()
        self.frame.children["time_entry"].config(textvariable=self.time)

        # self.btn_move_autonomously = ttk.Button(self.frame, text='move_autonomously')
        # self.btn_move_autonomously.grid(row=3, column=0)
        # self.btn_move_autonomously['command'] = lambda : self.robot.move_autonomously(self.speed.get(), self.rotation.get(), self.time.get())

        # self.btn_go_forward_until_black_line = ttk.Button(self.frame, text="go_forward_until_black_line")
        # self.btn_go_forward_until_black_line.grid(row=4, column=0)
        # self.btn_go_forward_until_black_line['command'] = lambda : self.robot.go_forward_until_black_line(self.speed.get(), )

        self.root.mainloop()

    def add_widget(self, widget_xml, top_frame=None):
        """
        Adds widget(s) to the frame.
        @Parameter widget_list: The widget(s) that will be added to the top_frame.
                                This widget_xml should be in XML format.
        @Parameter top_frame: Optional. The default value is self.frame

        Reference: http://docs.python.org/3.3/library/xml.etree.elementtree.html
        Contributor: Xiangqing Zhang
        """
        if not top_frame: top_frame = self.frame
        if widget_xml.tag == "root":
            self.frame = ttk.Frame(self.root, padding=(20, 30), **widget_xml.attrib)
            for each_widget in widget_xml:
                ttk_widget = self.add_widget(each_widget, self.frame)
                ttk_widget.pack()
            return self.frame
        else:
            opt_list = widget_xml.attrib
            if widget_xml:
                opt_list = opt_list.copy()
                for each_widget in widget_xml:
                    opt_list[each_widget.tag] = each_widget.text
                    print(each_widget.tag,"," ,each_widget.text)
            return getattr(ttk, widget_xml.tag.capitalize())(top_frame,**opt_list)
    def __exit__(self):
        """
        Disconnect the robot when interrupted or terminated.

        Contributor: Xiangqing Zhang
        """
        self.robot.disconnect()

def main():
    g = Gui()


if __name__ == '__main__':
    main()
