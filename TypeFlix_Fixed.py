from tkinter import *
from tkinter.messagebox import showinfo
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import ttk
import time


loading_windows = Tk()
w = 500
h = 300

ws = loading_windows.winfo_screenwidth()
hs = loading_windows.winfo_screenheight()
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)
loading_windows.geometry('%dx%d+%d+%d' % (w, h, x, y))
loading_windows.overrideredirect(1)
loading_windows.config(bg='#698561')

welcome = Label(loading_windows,
                text="Welcome to",
                font=("Comic Sans MS", 10),
                bg='#698561',
                fg='#F7F7F7')
welcome.pack(pady=(65, 0))
welcome = Label(loading_windows,
                text="TypeFlix",
                font=("Lucida Sans Unicode", 22, 'bold'),
                bg='#698561',
                fg='#F7F7F7')
welcome.pack(pady=(0, 0))


s = ttk.Style()
s.theme_use('default')
s.configure("red.Horizontal.TProgressbar", foreground='#698561', background='#698561', thickness=5)
progress = ttk.Progressbar(loading_windows, style="red.Horizontal.TProgressbar", orient=HORIZONTAL, length=503,
                           mode='determinate')


class MainWindows:
    def __init__(self):
        self.windows = Tk()
        self.windows.title('TypeFlix')
        self.windows.resizable(FALSE, FALSE)
        main_w = 1000
        main_h = 600

        main_ws = self.windows.winfo_screenwidth()
        main_hs = self.windows.winfo_screenheight()
        main_x = (main_ws / 2) - (main_w / 2)
        main_y = (main_hs / 2) - (main_h / 2)
        self.windows.geometry('%dx%d+%d+%d' % (main_w, main_h, main_x, main_y))

        self.top_frame = Frame(self.windows, height=100, bg='#698561')
        self.top_frame.pack(side='top', fill='both')
        self.top_frame.pack_propagate(FALSE)

        Label(self.top_frame, text='TypeFlix',
              bg='#698561',
              fg='#F7F7F7',
              font=("Lucida Sans Unicode", 20, 'bold')).place(x=50, y=30)

        searched = StringVar()

        self.search_icon = PhotoImage(file='search icon.png')
        self.search_icon = self.search_icon.subsample(2, 2)
        self.srch_btn_img = Button(self.top_frame, image=self.search_icon, bg='#698561', border=0, activebackground='#698561')
        self.srch_btn_img.image = self.search_icon
        self.srch_btn_img.place(x=950, y=66)

        search = Entry(self.top_frame, width=40, textvariable=searched)
        search.place(x=700, y=70)
        search.insert(0, "Search")
        search.bind("<FocusIn>", lambda args: search.delete('0', 'end'))

        self.bottom_canvas = Canvas(self.windows, bg='#f7f7f7', highlightthickness=0, borderwidth=0)
        self.bottom_canvas.pack(side=LEFT, expand=True, fill='both')
        self.bottom_canvas.pack_propagate(FALSE)
        self.bottom_canvas.grid_propagate(FALSE)

        scrollbar = Scrollbar(self.bottom_canvas, orient=VERTICAL, command=self.bottom_canvas.yview)
        scrollbar.pack(side=RIGHT, fill='y')

        self.bottom_canvas.configure(yscrollcommand=scrollbar.set)

        self.new_frame = Frame(self.bottom_canvas, bg='#f7f7f7')
        self.bottom_canvas.create_window(0, 0, window=self.new_frame, anchor='nw', width=1000)

        scrollbar.lift()

        self.bottom_canvas.bind('<Configure>', lambda e: self.bottom_canvas.configure(scrollregion=self.new_frame.bbox("all")))
        self.bottom_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.real_image_path = None
        self.movie_btn = None
        self.photo_mess = None
        self.display_movies()

    def _on_mousewheel(self, event):
        self.bottom_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def save_details(self, movie_name):
        if movie_name.strip():
            save_to_database = open('database.txt', 'a')
            if self.real_image_path:
                self.photo_mess.set("Photo has been added.")
                save_to_database.write(f'{movie_name}|{self.real_image_path}|\n')

            else:
                save_to_database.write(f'{movie_name}| |\n')

            self.real_image_path = None
            save_to_database.close()

            self.save_detail_windows.destroy()
            self.windows.destroy()

            self.windows.update()
            self.__init__()

        else:
            showinfo(title='Unfilled info', message='Please type in the movie name.')
            self.show_details_input()

    def image_path(self):

        your_image_path = filedialog.askopenfilename(initialdir='C:/Users/Acer/Pictures/', title='Select an image',
                                                     filetypes=[('image files', ['*.jpeg', '*.png', '*.jpg'])])
        self.real_image_path = str(your_image_path)
        if your_image_path:
            self.photo_mess.set("Photo has been added.")
        self.save_detail_windows.deiconify()
        return self.real_image_path

    def show_details_input(self):
        self.save_detail_windows = Toplevel()
        # self.save_detail_windows.set()
        w_swin = 300
        h_swin = 200

        ws_swin = self.windows.winfo_screenwidth()
        hs_swin = self.windows.winfo_screenheight()
        x_Swin = (ws_swin / 2) - (w_swin / 2)
        y_Swin = (hs_swin / 2) - (h_swin / 2)
        self.save_detail_windows.geometry('%dx%d+%d+%d' % (w_swin, h_swin, x_Swin, y_Swin))
        self.save_detail_windows.config(bg='#698561')
        self.save_detail_windows.overrideredirect(1)

        self.save_detail_windows.grid_columnconfigure(0, weight=1)
        self.save_detail_windows.grid_columnconfigure(1, weight=1)

        self.save_detail_windows.grid_rowconfigure(0, weight=1)
        self.save_detail_windows.grid_rowconfigure(1, weight=1)
        self.save_detail_windows.grid_rowconfigure(2, weight=1)
        self.save_detail_windows.grid_rowconfigure(3, weight=3)
        self.save_detail_windows.grid_rowconfigure(4, weight=1)

        Label(self.save_detail_windows,
              text='Movie Title',
              fg='#f7f7f7',
              bg='#698561',
              font=('Georgia', 13)).grid(row=0, column=0, columnspan=2, pady=(10, 0))

        mov_title = StringVar()
        Entry(self.save_detail_windows, textvariable=mov_title, width=40).grid(row=1, column=0, columnspan=2,
                                                                               ipady=2)

        camera_icon = PhotoImage(file='camera icon.png')
        camera_icon = camera_icon.subsample(2, 2)
        s_image_button = Button(self.save_detail_windows,
                                text='Add Image',
                                activebackground='#698561',
                                activeforeground='#f7f7f7',
                                image=camera_icon,
                                bg='#444444',
                                compound=LEFT,
                                font=('Georgia', 9),
                                fg='#f7f7f7',
                                bd=0,
                                width=120,
                                height=25,
                                command=self.image_path)
        s_image_button.image = camera_icon
        s_image_button.grid(row=2, column=0, columnspan=2)

        self.photo_mess = StringVar()

        add_photo_message = Label(self.save_detail_windows, textvariable=self.photo_mess, bg='#698561',
                                  fg='#f7f7f7')
        add_photo_message.grid(row=3, column=0, columnspan=2)

        submit_button = Button(self.save_detail_windows, text='Submit', bg='#333333', fg='#f7f7f7', width=10, bd=0,
                               command=lambda: self.save_details(mov_title.get()))
        submit_button.grid(row=4, column=0)
        cancel_button = Button(self.save_detail_windows, text='Cancel', bg='#333333', fg='#f7f7f7', width=10, bd=0,
                               command=lambda: self.save_detail_windows.destroy())
        cancel_button.grid(row=4, column=1)

        self.save_detail_windows.grab_release()

    def display_movies(self):
        with open('database.txt', 'r+') as database:
            line = database.readlines()
        # need for configuration
        num_items = len(line)
        self.row = 0
        self.column = 0
        c = 0
        _looping = [m_name.strip().split('|') for m_name in line]

        while c < num_items:
            for i in range(1, num_items + 1):
                if _looping[i - 1][1].strip():
                    movie_image = Image.open(_looping[i - 1][1].strip())
                    img_w, img_h = movie_image.size
                    p = 0.6546
                    img_x = 0
                    img_y = 0
                    if img_h >= img_w:
                        crop_w = (img_w - (img_h * p)) / 2
                        img_x += crop_w
                        cropped_img = movie_image.crop((img_x, img_y, img_w - img_x, img_h))
                    # to configure...
                    else:
                        n_img_s = (img_h * p) / 2
                        x_center = img_w / 2
                        cropped_img = movie_image.crop([x_center - n_img_s, img_y, x_center + n_img_s, img_h])

                    movie_image2 = ImageTk.PhotoImage(cropped_img.resize((180, 275)))

                    self.movie_btn = Button(self.new_frame, height=275, width=180, image=movie_image2,
                                            compound='center', bd=0)
                    self.movie_btn.image = movie_image2
                    self.movie_btn.grid(row=self.row, column=self.column, padx=(50, 0), pady=(20, 5))
                else:
                    self.movie_btn = Button(self.new_frame,
                                            height=18,
                                            width=25,
                                            text='No Image\nAvailable',
                                            fg='#444444',
                                            bd=0
                                            )
                    self.movie_btn.grid(row=self.row, column=self.column, padx=(50, 0), pady=(20, 5))

                Label(self.new_frame, text=_looping[i - 1][0],
                      bg='#f7f7f7',
                      font=("Lucida Sans Unicode", 10), width=20).grid(row=(self.row + 1),
                                                             column=self.column,
                                                             padx=(50, 0),
                                                             pady=(0, 10))
                if (i % 4 == 0) and (i != 0):
                    self.row += 2
                    self.column -= 4
                self.column += 1
                c += 1

        self.add_movie_button()

    def add_movie_button(self):
        if self.row > 0:
            self.column -= 1
        add_icon = PhotoImage(file='add icon.png')
        btn = Button(self.new_frame, height=270, width=180, bd=0, bg='#dddddd', image=add_icon, compound='center',
                     command=self.show_details_input)
        btn.image = add_icon
        btn.grid(row=self.row, column=(self.column + 1), padx=(50, 0), pady=(30, 20))


def bar():
    progress.place(y=293)

    l4 = Label(loading_windows, text='Loading...', fg='#F7F7F7', bg='#698561')
    lst4 = ('Calibri (Body)', 10)
    l4.config(font=lst4)
    l4.place(x=10, y=269)

    import time
    r = 0
    for i in range(100):
        progress['value'] = r
        loading_windows.update_idletasks()
        time.sleep(0.05)
        r += 1

    loading_windows.destroy()
    MainWindows()


b1 = Button(loading_windows,
            width=10,
            height=1,
            text='Get Started',
            font=('Lucida Sans Unicode', 10),
            command=bar,
            border=0,
            activebackground='#698561',
            fg='#F7F7F7',
            bg='#333333')
b1.pack(pady=(90, 0))

mainloop()
