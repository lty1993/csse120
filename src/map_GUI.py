import tkinter
from tkinter import *
import math

def main():
    close_flag = [False]

    master = Tk()
    master.title('Map GUI')
    w = Canvas(master, width=400, height=400)

    w.pack()

    for k in range(40, 400, 40):  # Creates grid
        w.create_line(k, 0, k, 400)
        w.create_line(0, k, 400, k)

    w.create_oval(190, 190, 210, 210, fill="blue")
    previous_point = [200, 200]
    points = [200, 200]
    w.bind('<Button-1>', lambda event: mouse_click(close_flag, master, 1, event, previous_point, points))
    w.bind('<Button-3>', lambda event: mouse_click(close_flag, master, 3, event, None, points))

    while not close_flag[0]:
        try:
            master.update()
        except:
            break
    return points

def mouse_click(close_flag, master, signal, event, previous_point, points):
    w = event.widget

    if signal == 1:
        x_new = event.x
        y_new = event.y

        w.create_oval(event.x - 10, event.y - 10, event.x + 10, event.y + 10, fill='green', width=1)
        w.create_line(previous_point[0], previous_point[1], x_new, y_new)
        previous_point[0] = x_new
        previous_point[1] = y_new
        points.append(previous_point[0])
        points.append(previous_point[1])

    elif signal == 3:
        master.destroy()
        close_flag = [True]
        for k in range(len(points)):
            if k % 2 == 1:
                points[k] = round(-(points[k] - 200) / 40)
            else:
                points[k] = round((points[k] - 200) / 40)
        return points

    else:
        pass

if __name__ == '__main__':
    main()

