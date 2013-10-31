from xml.etree.ElementTree import XML
from tkinter import Tk
import tkinter

def realize(master, element):
    if element.tag == "form":
        frame = tkinter.Frame(master, **element.attrib)
        for subelement in element:
            widget = realize(frame, subelement)
            widget.pack()
        return frame
    else:
        options = element.attrib
        if element:
            options = options.copy()
            for subelement in element:
                options[subelement.tag] = subelement.text
        widget_factory = getattr(tkinter, element.tag.capitalize())
        return widget_factory(master, **options)

form = XML("""\
<widget class="QMainWindow" name="MainWindow">
<property name="geometry">
<rect>
<x>0</x>
<y>0</y>
<width>1024</width>
<height>768</height>
</rect>
</property>
<property name="windowTitle">
<string>MainWindow</string>
</property>
<widget class="QWidget" name="centralWidget">
<widget class="QFrame" name="frame">
<property name="enabled">
 <bool>true</bool>
</property>
<property name="geometry">
 <rect>
  <x>10</x>
  <y>10</y>
  <width>1001</width>
  <height>681</height>
 </rect>
</property>
<property name="frameShape">
 <enum>QFrame::StyledPanel</enum>
</property>
<property name="frameShadow">
 <enum>QFrame::Raised</enum>
</property>
</widget>
</widget>
<widget class="QMenuBar" name="menuBar">
<property name="geometry">
<rect>
 <x>0</x>
 <y>0</y>
 <width>1024</width>
 <height>19</height>
</rect>
</property>
</widget>
<widget class="QToolBar" name="mainToolBar">
<attribute name="toolBarArea">
<enum>TopToolBarArea</enum>
</attribute>
<attribute name="toolBarBreak">
<bool>false</bool>
</attribute>
</widget>
<widget class="QStatusBar" name="statusBar"/>
</widget>
<layoutdefault spacing="6" margin="11"/>
<resources/>
<connections/>
""")
root = Tk()
frame = realize(root, form)
frame.grid()

root.mainloop()