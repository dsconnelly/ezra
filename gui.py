import tkinter as tk
import schedule

class ScheduleWindow(object):
    """Defines a window which can display courses and is associated with
    a Schedule object."""
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
        'Saturday', 'Sunday']

    def __init__(self, width=1450, height=970):
        """Initializes the window."""
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=width, height=height)

        col_w = (width - 220) / 6
        for i in range(5):
            p = ((col_w + 10) * i) + 10
            self.canvas.create_rectangle(p, 10, p + col_w, height - 10)
            for j in range(1, 19):
                level = (50 * j) + 10
                color = 'gray' if j % 2 == 0 else 'black'
                self.canvas.create_line(p, level, p + col_w, level, fill=color)
            a_x = p + 102.5
            self.canvas.create_text(a_x, 35, font=('Comic Sans MS', 15),
                text=self.day_names[i])

        p = (215 * 5) + 10
        self.canvas.create_rectangle(p, 10, p + 355, 960)

        self.schedule = schedule.Schedule()

    def add_course_by_dept_and_number(self, dept_short, number):
        self.schedule.add_course_by_dept_and_number(dept_short, number)

    def show(self):
        self.canvas.pack()
        self.root.mainloop()

if __name__ == '__main__':
    sw = ScheduleWindow()
    sw.show()
