from xml.etree.ElementTree import XML
from Robot import Robot
import tkinter
from tkinter import ttk
from logger import robotLogger
from threading import Timer


class Gui():
    def __init__(self, port="sim"):
        """
        A gui used to autonomously control the robot with user-specified speed, rotation, and time.
        Contributor: Matthew O'Brien, Xiangqing Zhang, Tianyu Liu
        """
        self.speed = None
        self.rotation = None
        self.time = None
        self.robot = Robot(port)
        self.robot.connect()

        self.root = tkinter.Tk()
        self.root.title("Robot GUI")

        self.frame = None
        FO = open("mainwindow.xml", "r")
        xml_string = FO.read()
        FO.close()
        self.add_widget(XML(xml_string), self.root).grid()

        self.config_widget("btn_connect", {"command": lambda: self.robot.connect()})
        self.config_widget("btn_stop", {"command": lambda: self.robot.stop()})

        self.config_widget("wilma_bio", {"command": lambda: self.robot.log_information()})

        self.speed = tkinter.IntVar()
        self.config_widget("speed_entry", {"textvariable": self.speed})

        self.rotation = tkinter.IntVar()
        self.config_widget("rotation_entry", {"textvariable": self.rotation})

        self.time = tkinter.IntVar()
        self.config_widget("time_entry", {"textvariable": self.time})

        self.config_widget("btn_move_autonomously", {"command": lambda: self.robot.move_autonomously(self.speed.get(), self.rotation.get(), self.time.get())})

        self.coordinates = tkinter.StringVar()
        self.config_widget("grid_entry", {"textvariable": self.coordinates})
        self.config_widget("grid_button", {"command": lambda: self.robot.grid_movement(self.coordinates.get(), self.speed.get(), self.rotation.get())})

        self.darkness = tkinter.IntVar()
        self.config_widget("darkness_entry", {"textvariable": self.darkness})

        self.config_widget("btn_go_forward_until_black_line", {"command": lambda: self.robot.go_forward_until_black_line(self.speed.get(), self.darkness.get())})

        self.bumper = tkinter.StringVar()
        self.config_widget("bumper_entry", {"textvariable": self.bumper})

        self.config_widget("btn_go_forward_until_bumps", {"command": lambda: self.robot.go_forward_until_bumps(self.speed.get(), self.bumper.get())})

        self.bytecode = tkinter.IntVar()
        self.config_widget("bytecode_entry", {"textvariable": self.bytecode})

        self.config_widget("btn_bytecode_entry", {"command": lambda: self.robot.chat_with_another_robot(self.bytecode.get())})
        self.config_widget("btn_go_forward_until_ir_signal", {"command": lambda: self.robot.go_forward_until_ir_signal(self.speed.get(), self.bytecode.get())})
        self.config_widget("btn_go_forward_until_stuck", {"command": lambda: self.robot.go_forward_until_stuck(self.speed.get())})

        self.config_widget("btn_forward", {"command": lambda: self.robot.teleport("Forward")})
        self.config_widget("btn_backward", {"command": lambda: self.robot.teleport("Backward")})
        self.config_widget("btn_left", {"command": lambda: self.robot.teleport("Left")})
        self.config_widget("btn_right", {"command": lambda: self.robot.teleport("Right")})
        self.config_widget("btn_follow", {"command": lambda: self.robot.follow_black_line(self.speed.get(), self.darkness.get())})

        self.log_frame = ttk.Frame(self.root)
        self.log_frame.grid()
        self.log_text = tkinter.Text(self.log_frame, width=150, height=20, wrap=tkinter.CHAR) #state=tkinter.DISABLED) 
        # self.log_text.insert(tkinter.INSERT, "DEBUG")
        self.log_text.grid()

        robotLogger.logger_list["GuiLogger"].gui = self

        info_time = Timer(2, lambda: self.robot.team_info())
        info_time.start()
        self.root.mainloop()

    def config_widget(self, widget_name, widget_options):
        """
        Config the widget.
        @Parameter widget_name: The widget's name.
        @Parameter widget_options: A DICTIONARY that contains options.

        E.g. self.config_widget("time_entry", {textvariable: self.time})
             is equivalent to
             time_entry["textvariable"] = self.time
        Contributor: Xiangqing Zhang
        """
        assert self.frame, "Please initialize the GUI!"
        self.frame.children[widget_name].config(**widget_options)

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
                ttk_widget, row_column = self.add_widget(each_widget, self.frame)
                if not row_column:
                    ttk_widget.grid()
                else:
                    row_column = row_column.split(",")
                    rows = int(row_column[0])
                    columns = int(row_column[1])
                    ttk_widget.grid(row=rows, column=columns)
            return self.frame
        else:
            opt_list = widget_xml.attrib
            if widget_xml:
                opt_list = opt_list.copy()
                for each_widget in widget_xml:
                    opt_list[each_widget.tag] = each_widget.text
            row_column = None
            if "row_column" in opt_list:
                row_column = opt_list["row_column"]
                del opt_list["row_column"]
            return [getattr(ttk, widget_xml.tag.capitalize())(top_frame, **opt_list), row_column]
    def exit(self):
        """
        Disconnect the robot when interrupted or terminated.

        Contributor: Xiangqing Zhang
        """
        self.robot.stop()
        self.robot.disconnect()

def main():
    g = Gui()
    g.exit()

if __name__ == '__main__':
    main()
