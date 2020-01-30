import time
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from winsound import PlaySound, SND_FILENAME, SND_ALIAS


class pomodoroApp():

    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.parent.title('PyModoro')
        self.w, self.h, self.x0, self.y0 = (600, 150, 50, 50)
        self.parent.geometry(f'{self.w}x{self.h}+{self.x0}+{self.y0}')
        self.parent.resizable(0, 0)
        try:
            self.parent.iconbitmap('static/logo.ico')
        except:
            pass

        self._bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        self._clockFont = ('Arial', 40)
        self._normalFont = ('Verdana', 10)
        self._clockColor1 = 'black'
        self._clockColor2 = 'green'
        self._clockColor3 = 'blue'
        self.work_minutes = 25
        self.break_minutes = 5
        self.long_break_minutes = 30

        #------------------------------------------------------------------------------
        #------------------------------------------------------------------------------
        #------------------------------------------------------------------------------
        self.clock_frame = tk.Frame(self.parent)
        self.clock_frame.place(relx=0.6, rely=0.35, relheight=0.6, relwidth=0.39)

        self.seperator = tk.Canvas(self.clock_frame)
        self.seperator.place(relx=0.425, rely=0.2, relheight=0.6, relwidth=0.2)
        self.seperator.create_oval(self.circleCoords(parent=self.seperator, relx=0.375, rely=0.275, relr=0.15), fill='black')
        self.seperator.create_oval(self.circleCoords(parent=self.seperator, relx=0.375, rely=0.725, relr=0.15), fill='black')

        self.minutes_one = tk.Frame(self.clock_frame)
        self.minutes_one.place(relx=0.075, rely=0.1, relheight=0.8, relwidth=0.175)
        self.minutes_one.configure(relief='raised', borderwidth="3")

        self.min_label_one = ttk.Label(self.minutes_one)
        self.min_label_one.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.minutes_two = tk.Frame(self.clock_frame)
        self.minutes_two.place(relx=0.275, rely=0.1, relheight=0.8, relwidth=0.175)
        self.minutes_two.configure(relief='raised', borderwidth="3")

        self.min_label_two = ttk.Label(self.minutes_two)
        self.min_label_two.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.seconds_one = tk.Frame(self.clock_frame)
        self.seconds_one.place(relx=0.55, rely=0.1, relheight=0.8, relwidth=0.175)
        self.seconds_one.configure(relief='raised', borderwidth="3")

        self.sec_label_one = ttk.Label(self.seconds_one)
        self.sec_label_one.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.seconds_two = tk.Frame(self.clock_frame)
        self.seconds_two.place(relx=0.75, rely=0.1, relheight=0.8, relwidth=0.175)
        self.seconds_two.configure(relief='raised', borderwidth="3")

        self.sec_label_two = ttk.Label(self.seconds_two)
        self.sec_label_two.place(relx=0, rely=0, relwidth=1, relheight=1)
        #------------------------------------------------------------------------------
        #------------------------------------------------------------------------------
        #------------------------------------------------------------------------------
        self.settings_frame = tk.Frame(self.parent)
        self.settings_frame.place(relx=0.01, rely=0.01, relheight=0.98, relwidth=0.59)
        self.settings_frame.configure(relief='groove', borderwidth="2")

        self.work_text = ttk.Label(self.settings_frame)
        self.work_text.configure(text='Work for', font=self._normalFont)
        self.work_text.grid(row=0, column=0, padx=10)

        self.work_value = ttk.Label(self.settings_frame)
        self.work_value.configure(text=f'{str(self.work_minutes)} minutes', font=self._normalFont)
        self.work_value.grid(row=0, column=2, padx=10)

        self.work_scale = ttk.Scale(self.settings_frame, from_=15, to=45)
        self.work_scale.configure(command=lambda x: self.updateWorkLabel())
        self.work_scale.set(self.work_minutes)
        self.work_scale.grid(row=0, column=1, padx=10, pady=10)
        #------------------------------------------------------------------------------
        self.break_text = ttk.Label(self.settings_frame)
        self.break_text.configure(text='Short Break', font=self._normalFont)
        self.break_text.grid(row=1, column=0, padx=10)

        self.break_value = ttk.Label(self.settings_frame)
        self.break_value.configure(text=f'{str(self.break_minutes)} minutes', font=self._normalFont)
        self.break_value.grid(row=1, column=2, padx=10)

        self.break_scale = ttk.Scale(self.settings_frame, from_=1, to=10)
        self.break_scale.configure(command=lambda x: self.updateBreakLabel())
        self.break_scale.set(self.break_minutes)
        self.break_scale.grid(row=1, column=1, padx=10, pady=10)
        #------------------------------------------------------------------------------
        self.long_break_text = ttk.Label(self.settings_frame)
        self.long_break_text.configure(text='Long Break', font=self._normalFont)
        self.long_break_text.grid(row=2, column=0, padx=10)

        self.long_break_value = ttk.Label(self.settings_frame)
        self.long_break_value.configure(text=f'{str(self.work_minutes)} minutes', font=self._normalFont)
        self.long_break_value.grid(row=2, column=2, padx=10)

        self.long_break_scale = ttk.Scale(self.settings_frame, from_=15, to=45)
        self.long_break_scale.configure(command=lambda x: self.updateLongBreakLabel())
        self.long_break_scale.set(self.long_break_minutes)
        self.long_break_scale.grid(row=2, column=1, padx=10, pady=10)
        #------------------------------------------------------------------------------
        #------------------------------------------------------------------------------
        #------------------------------------------------------------------------------
        self.button_frame = tk.Frame(self.parent)
        self.button_frame.place(relx=0.6, rely=0.05, relwidth=0.4, relheight=0.3)

        self.start_button = ttk.Button(self.button_frame)
        self.start_button.place(relx=0.075, rely=0.01, relwidth=0.375, relheight=1)
        self.start_button.configure(text='START', command=lambda: self.start())

        self.stop_button = ttk.Button(self.button_frame)
        self.stop_button.place(relx=0.525, rely=0.01, relwidth=0.375, relheight=1)
        self.stop_button.configure(text='STOP', command=lambda: self.stop())
        #------------------------------------------------------------------------------
        #------------------------------------------------------------------------------
        #------------------------------------------------------------------------------


    def start(self):
        self.run_timer = True
        self.first_call = True
        self.timer()


    def stop(self):
        self.run_timer = False


    def timer(self):
        if self.run_timer:
            if self.first_call:
                self.work_seconds = self.work_minutes * 60
                self.break_seconds = self.break_minutes * 60
                self.long_break_seconds = self.long_break_minutes * 60

                self.state = 'working'
                self.count = 0
                
                self.first_call = False

            if self.state == 'working':
                if self.work_seconds:
                    self.work_seconds -= 1
                    minutes = int(self.work_seconds / 60)
                    seconds = self.work_seconds % 60
                    self.updateClock(minutes, seconds)
                else:
                    try:
                        PlaySound('static/alarm.wav', SND_FILENAME)
                    except:
                        PlaySound('SystemExit', SND_ALIAS)
                    self.count += 1
                    if self.count % 4 == 0:
                        self.state = 'long_break'
                    else:
                        self.state = 'break'
                    self.work_seconds = self.work_minutes * 60

            elif self.state == 'break':
                if self.break_seconds:
                    self.break_seconds -= 1
                    minutes = int(self.break_seconds / 60)
                    seconds = self.break_seconds % 60
                    self.updateClock(minutes, seconds)
                else:
                    try:
                        PlaySound('static/alarm.wav', SND_FILENAME)
                    except:
                        PlaySound('SystemExit', SND_ALIAS)
                    self.state = 'working'
                    self.break_seconds = self.break_minutes * 60

            else:
                if self.long_break_seconds:
                    self.long_break_seconds -= 1
                    minutes = int(self.long_break_seconds / 60)
                    seconds = self.long_break_seconds % 60
                    self.updateClock(minutes, seconds)
                else:
                    try:
                        PlaySound('static/alarm.wav', SND_FILENAME)
                    except:
                        PlaySound('SystemExit', SND_ALIAS)
                    self.state = 'working'
                    self.long_break_seconds = self.long_break_minutes * 60


            self.parent.after(1000, func=self.timer)


    def updateClock(self, mins, secs):
        min_str = str(mins)
        while len(min_str) < 2:
            min_str = '0' + min_str

        sec_str = str(secs)
        while len(sec_str) < 2:
            sec_str = '0' + sec_str

        if self.state == 'working':
            color = self._clockColor1
        elif self.state == 'break':
            color = self._clockColor2
        else:
            color = self._clockColor3

        self.min_label_one.configure(text=min_str[0], font=self._clockFont, foreground=color)
        self.min_label_two.configure(text=min_str[1], font=self._clockFont, foreground=color)

        self.sec_label_one.configure(text=sec_str[0], font=self._clockFont, foreground=color)
        self.sec_label_two.configure(text=sec_str[1], font=self._clockFont, foreground=color)


    def updateWorkLabel(self):
        self.work_minutes = int(self.work_scale.get())
        self.work_value.configure(text=f'{str(self.work_minutes)} minutes')


    def updateBreakLabel(self):
        self.break_minutes = int(self.break_scale.get())
        self.break_value.configure(text=f'{str(self.break_minutes)} minutes')


    def updateLongBreakLabel(self):
        self.long_break_minutes = int(self.long_break_scale.get())
        self.long_break_value.configure(text=f'{str(self.long_break_minutes)} minutes')


    def circleCoords(self, parent, relx, rely, relr):
        self.parent.update()
        w = parent.winfo_width()
        h = parent.winfo_height()
        x = relx * w
        y = rely * h
        r = relr * w
        return (x-r, y-r, x+r, y+r)



if __name__ == "__main__":
    root = tk.Tk()
    pomodoroApp(root)
    root.attributes('-topmost', True)
    root.update()
    root.mainloop()