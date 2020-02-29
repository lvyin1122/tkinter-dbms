from tkinter import *
from tkinter import messagebox
import tkinter.filedialog as fd
import os
from mlb import MultiListbox
import sqlite3
from matplotlib import pyplot as plt


# Functions
def db_root_start():
    def db_submit_click():
        conn = sqlite3.connect(file_dir)
        c = conn.cursor()

        try:
            c.execute("INSERT INTO weather VALUES (:id, :time_stamp, :description, :temp, :hum)",
                      {
                          'id': db_entry_id.get(),
                          'time_stamp': db_entry_tmstmp.get(),
                          'description': db_entry_dscrp.get(),
                          'temp': db_entry_temp.get(),
                          'hum': db_entry_hum.get()
                      })
        except sqlite3.IntegrityError:
            messagebox.showwarning(title='Error', message='Duplicated id!')


        mlb.delete(0, END)
        c.execute('SELECT * FROM weather')
        for row in c:
            mlb.insert(END, (str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4])))



        conn.commit()
        conn.close()

    def db_fetch_click():
        conn = sqlite3.connect(file_dir)
        c = conn.cursor()

        try:
            c.execute('SELECT * FROM weather WHERE id = ' + db_entry_id.get())
        except sqlite3.OperationalError:
            db_entry_id.delete(0, END)
            db_entry_tmstmp.delete(0, END)
            db_entry_dscrp.delete(0, END)
            db_entry_temp.delete(0, END)
            db_entry_hum.delete(0, END)
            return

        records = c.fetchall()

        db_entry_id.delete(0, END)
        db_entry_tmstmp.delete(0, END)
        db_entry_dscrp.delete(0, END)
        db_entry_temp.delete(0, END)
        db_entry_hum.delete(0, END)

        for record in records:
            db_entry_id.insert(0, record[0])
            db_entry_tmstmp.insert(0, record[1])
            db_entry_dscrp.insert(0, record[2])
            db_entry_temp.insert(0, record[3])
            db_entry_hum.insert(0, record[4])
            break

        conn.commit()
        conn.close()

    def db_delete_click():
        conn = sqlite3.connect(file_dir)
        c = conn.cursor()

        try:
            c.execute('DELETE from weather WHERE id = ' + db_entry_id.get())
        except sqlite3.OperationalError:
            db_entry_id.delete(0, END)
            conn.commit()
            conn.close()
            return

        mlb.delete(0, END)
        c.execute('SELECT * FROM weather')


        for row in c:
            mlb.insert(END, (str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4])))



        conn.commit()
        conn.close()

    def db_edit_click():
        conn = sqlite3.connect(file_dir)
        c = conn.cursor()

        c.execute("""UPDATE weather SET
                    time_stamp = :time_stamp,
                    description = :description,
                    temp = :temp,
                    hum = :hum
                    
                    WHERE id = :id """,
                  {'time_stamp': str(db_entry_tmstmp.get()),
                   'description': str(db_entry_dscrp.get()),
                   'temp': db_entry_temp.get(),
                   'hum': db_entry_hum.get(),
                   'id': db_entry_id.get()
                   })

        mlb.delete(0, END)
        c.execute('SELECT * FROM weather')

        for row in c:
            mlb.insert(END, (str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4])))



        conn.commit()
        conn.close()

    def db_graph_click(var1, var2):
        if int(var1.get()) == 0 and int(var2.get()) == 0:
            return

        conn = sqlite3.connect(file_dir)
        c = conn.cursor()

        x = []
        y1 = []
        y2 = []

        c.execute('SELECT time_stamp,temp,hum FROM weather')
        for row in c:
            x.append(str(row[0]))
            y1.append(float(row[1]))
            y2.append(int(row[2]))

        if int(var1.get()) == 1 and int(var2.get()) == 1:
            plt.title("Weather")
            plt.xlabel("Time Stamp")
            l1, = plt.plot(x, y1)
            l2, = plt.plot(x, y2)

            ax = plt.gca()
            for tick in ax.get_xticklabels():
                tick.set_rotation(75)

            plt.legend([l1, l2], ['Temperature', 'Humidity'], loc='upper right')
            plt.show()
        elif int(var1.get()) == 1 and int(var2.get()) == 0:
            plt.title("Weather")
            plt.xlabel("Time Stamp")
            l1, = plt.plot(x, y1)
            # l2, = plt.plot(x, y2)

            ax = plt.gca()
            for tick in ax.get_xticklabels():
                tick.set_rotation(75)
            plt.legend([l1], ['Temperature'], loc='upper right')
            plt.show()
        elif int(var1.get()) == 0 and int(var2.get()) == 1:
            plt.title("Weather")
            plt.xlabel("Time Stamp")
            # l1, = plt.plot(x, y1)
            l2, = plt.plot(x, y2)

            ax = plt.gca()
            for tick in ax.get_xticklabels():
                tick.set_rotation(75)
            plt.legend([l2], ['Humidity'], loc='upper right')
            plt.show()

        conn.close()


    db_root = Toplevel()
    db_root.title(file_dir)
    db_root.iconbitmap('favicon.ico')
    db_root.geometry("455x400")
    db_root.resizable(0, 0)

    conn = sqlite3.connect(file_dir)
    c = conn.cursor()


    mlb = MultiListbox(db_root, (('ID', 10),
                                 ('Time Stamp', 20),
                                 ('Description', 15),
                                 ('Temp', 15),
                                 ('Hum', 10)))

    c.execute('SELECT * FROM weather')
    for row in c:
        mlb.insert(END, (str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4])))


    mlb.pack()

    # db_blank = Label(db_root).pack()

    # Frame 1
    db_frame_1 = LabelFrame(db_root)

    db_label_id = Label(db_frame_1, text='ID').grid(row=0, column=0)
    db_label_tmstmp = Label(db_frame_1, text='Time Stamp').grid(row=1, column=0)
    db_label_dscrp = Label(db_frame_1, text='Description').grid(row=2, column=0)
    db_label_temp = Label(db_frame_1, text='Temperature').grid(row=3, column=0)
    db_label_hum = Label(db_frame_1, text='Humidity').grid(row=4, column=0)


    etry_w = 62
    db_entry_id = Entry(db_frame_1, width=etry_w)
    db_entry_id.grid(row=0, column=1)
    db_entry_tmstmp = Entry(db_frame_1, width=etry_w)
    db_entry_tmstmp.grid(row=1, column=1)
    db_entry_dscrp = Entry(db_frame_1, width=etry_w)
    db_entry_dscrp.grid(row=2, column=1)
    db_entry_temp = Entry(db_frame_1, width=etry_w)
    db_entry_temp.grid(row=3, column=1)
    db_entry_hum = Entry(db_frame_1, width=etry_w)
    db_entry_hum.grid(row=4, column=1)




    db_frame_1.pack()
    # Frame 1 ends


    # Frame 2
    db_frame_2 = Frame(db_root)

    btn_x = 5
    btn_y = 5
    btn_w = 14
    db_button_submit = Button(db_frame_2,
                              text='Submit',
                              width=btn_w,
                              padx=btn_x,
                              pady=btn_y,
                              command=db_submit_click
                              ).grid(row=0, column=0)
    db_button_fetch = Button(db_frame_2,
                             text='Fetch',
                             width=btn_w,
                             padx=btn_x,
                             pady=btn_y,
                             command=db_fetch_click
                             ).grid(row=0, column=1)
    db_button_delete = Button(db_frame_2,
                              text='Delete',
                              width=btn_w,
                              padx=btn_x,
                              pady=btn_y,
                              command=db_delete_click
                              ).grid(row=0, column=3)
    db_button_edit = Button(db_frame_2,
                              text='Edit',
                              width=btn_w,
                              padx=btn_x,
                              pady=btn_y,
                              command=db_edit_click
                              ).grid(row=0, column=2)

    db_frame_2.pack()
    # Frame 2 ends

    db_frame_3 = LabelFrame(db_root, text='Graph')

    var1 = IntVar()
    var2 = IntVar()
    db_checkbtn_temp = Checkbutton(db_frame_3, text='Temp', variable=var1).grid(row=0, column=0)
    db_checkbtn_hum = Checkbutton(db_frame_3, text='Hum', variable=var2).grid(row=0, column=1)

    db_button_graph = Button(db_frame_3, text='Graph', width=56, command=lambda: db_graph_click(var1, var2))
    db_button_graph.grid(row=1, column=0, columnspan=2)

    db_frame_3.pack()

    # SQL connection ends
    conn.commit()
    conn.close()


def file_button_click():
    global file_dir
    global file_entry

    file_dir = fd.askopenfilename(initialdir=".",
                                  title="Select a file",
                                  filetypes=(("db files", "*.db"), ("all files", "*.*")))
    file_entry.delete(0, END)
    file_entry.insert(0, file_dir)


def file_import_click():
    global file_entry

    if file_dir == '':
        return

    if file_dir[len(file_dir)-3:] != '.db':
        messagebox.showwarning(title="Error!", message='Please import a .db file!')
        file_entry.delete(0, END)
        return

    db_root_start()


def file_delete_click():
    if file_dir == '':
        return
    os.remove(file_dir)
    file_entry.delete(0, END)


def file_new_button_click():
    global file_dir
    global file_new_entry

    file_dir = fd.askdirectory(initialdir=".", title="Select a file",)
    file_new_entry.delete(0, END)
    file_new_entry.insert(0, file_dir)


def file_create_click():
    global file_dir
    file_dir = file_dir + '/' + file_name_entry.get() + '.db'
    open(file_dir, 'w')

    conn = sqlite3.connect(file_dir)
    c = conn.cursor()
    c.execute("""CREATE TABLE weather (
                id integer NOT NULL,
                time_stamp text NOT NULL,
                description text,
                temp double,
                hum integer,
                PRIMARY KEY(id))
                """)
    conn.close()

    db_root_start()
    # print(file_dir)


# Main
if __name__ == '__main__':
    root = Tk()
    root.title("Mini Database Management System")
    root.geometry("400x220")
    root.resizable(0, 0)
    root.iconbitmap('favicon.ico')

    global file_dir

    # main_title = Label(root, text='Mini Database Management System', bg='blue', fg='white')
    # main_title.config(font=("Courier", 10))
    # main_title.pack()

    # Frame 1: select db file
    file_frame = LabelFrame(root, text='Import a database file', padx=5, pady=5)
    file_frame.pack(padx=10, pady=10)

    file_entry = Entry(file_frame, width=50)
    file_button = Button(file_frame, text='...', command=file_button_click)
    file_import = Button(file_frame, text='Import', command=file_import_click)
    file_delete = Button(file_frame, text='Delete', command=file_delete_click)

    file_entry.grid(row=0, column=0, columnspan=3)
    file_button.grid(row=0, column=3)
    file_import.grid(row=1, column=0, columnspan=2)
    file_delete.grid(row=1, column=2, columnspan=1)

    # Frame 2: create a new db file
    file_new_frame = LabelFrame(root, text='Create a database file', padx=5, pady=5)
    file_new_frame.pack(padx=10, pady=10)

    file_new_label = Label(file_new_frame, text='File path', anchor='w')
    file_name_label = Label(file_new_frame, text='File name')
    file_new_entry = Entry(file_new_frame, width=37)
    file_name_entry = Entry(file_new_frame, width=30)
    file_new_button = Button(file_new_frame, text='...', command=file_new_button_click)
    file_create = Button(file_new_frame, text='Create', command=file_create_click, padx=1)

    file_new_label.grid(row=0, column=0)
    file_new_entry.grid(row=0, column=1, columnspan=2)
    file_new_button.grid(row=0, column=3)
    file_name_label.grid(row=1, column=0)
    file_name_entry.grid(row=1, column=1, columnspan=2)
    file_create.grid(row=1, column=3, columnspan=1)

    root.mainloop()