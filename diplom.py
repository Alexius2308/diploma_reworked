from tkinter import *
from tkinter import ttk
import datetime
import sqlite3
from tkinter import messagebox as mb

# Ініціалізація інтерфейсу
root = Tk()
root.title('Епдеміологічний збір')
root.geometry("500x450")

# Відкриття бази даних
conn = sqlite3.connect('epidemic_dp.db')
# Create cursor
c = conn.cursor()
# Create table
c.execute("""CREATE TABLE IF NOT EXISTS epidemic_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name text NOT NULL,
        patient_age INTEGER NOT NULL,
        status_id INTEGER NOT NULL,
        region_id TEXT NOT NULL,
        city_id TEXT NOT NULL,
        date text NOT NULL
        );""")

# Збереження до бази
def save():
    answer = mb.askyesno(title="Ви впевнені?", message="Зберегти запис?")
    if answer == True:
        if patient_name.get() != '' or patient_age.get() != '' or patient_status.get() != '' or region.get() != '' or city.get() != '':
            # Create a database or connect to one
            conn = sqlite3.connect('epidemic_dp.db')
            # Create cursor
            c = conn.cursor()
            date_execute = datetime.datetime.now()
            # Insert Into Table
            c.execute("""INSERT INTO epidemic_table(patient_name, patient_age, status_id, region_id, city_id, date) 
                        VALUES (:patient_name, :patient_age, :status_id, :region_id, :city_id, :date)""",
                    {
                        'patient_name' : patient_name.get(),
                        'patient_age' : patient_age.get(),
                        'status_id' : patient_status.get(),
                        'region_id' : region.get(),
                        'city_id' : city.get(),
                        'date' : date_execute.strftime("%d-%m-%Y")
                    }
            )
            # Commit Changes
            conn.commit()
            # Close connection
            conn.close()
            # Clear The Text Boxes
            patient_name.delete(0, END)
            patient_age.delete(0, END)
            patient_status.delete(0, END)
            region.delete(0, END)
            city.delete(0, END)
        else:
            mb.showwarning(title="Помилка введенного значення", message="Заповніть усі поля!")


    # Відобразити записи
def show():
    # Create a database or connect to one
    conn = sqlite3.connect('epidemic_dp.db')
    # Create cursor
    c = conn.cursor()
    tree_root = Tk()
    # Query the database
    c.execute("SELECT * FROM epidemic_table")
    records = c.fetchall()
    print(records)
    tree = ttk.Treeview(tree_root, columns=('ID', 'patient_name', 'patient_age','patient_status','region','city','date'), height=15, show='headings')
    tree.column('ID', width=30, anchor=CENTER)
    tree.column('patient_name', width=200, anchor=CENTER)
    tree.column('patient_age', width=50, anchor=CENTER)
    tree.column('patient_status', width=50, anchor=CENTER)
    tree.column('region', width=200, anchor=CENTER)
    tree.column('city', width=150, anchor=CENTER)
    tree.column('date', width=150, anchor=CENTER)
    
    tree.heading('ID', text='ID')
    tree.heading('patient_name', text="Ім'я")
    tree.heading('patient_age', text='Вік')
    tree.heading('patient_status', text='Статус')
    tree.heading('region', text='Область')
    tree.heading('city', text='Місто')
    tree.heading('date', text='Дата реєстрації')
    
    for i in tree.get_children():
        tree.delete(i) 
    for row in records:
        tree.insert('','end', values=row)
    
    tree.pack()
    # Loop Thru Results
    print_records = ''
    for record in records:
        print_records += str(record) + "\n"
    # Commit Changes
    conn.commit()
    # Close connection
    conn.close()
def delete():
    if(delete_box.get() == ''):
        mb.showwarning(title="Помилка введенного значення", message="Введіть ID випадку!")
    else:
        conn = sqlite3.connect('epidemic_dp.db')
        c = conn.cursor()
    
    
        # Delete a record
        c.execute("DELETE from epidemic_table WHERE id= " + str(delete_box.get()))
        # Commit changes
        conn.commit()

        # Close Connection
        conn.close()
def apply():
    # Create a database or connect to one
    conn = sqlite3.connect('epidemic_dp.db')
    # Create cursor
    c = conn.cursor()
    record_id = delete_box.get()
    c.execute("""UPDATE epidemic_table SET
    patient_name = :name,
    patient_age = :age,
    status_id = :status,
    region_id = :region,
    city_id = :city,
    date = :date

    WHERE id =:oid""",
    {'name': patient_name_editor.get(),
    'age': patient_age_editor.get(),
    'status':patient_status_editor.get(),
    'region':region_editor.get(),
    'city':city_editor.get(),
    'date':date_editor.get(),
    'oid':record_id
    })
    # Commit Changes
    conn.commit()
    # Close connection
    conn.close()
    editor.destroy()
def update():
    if(delete_box.get() == ''):
        mb.showwarning(title="Помилка введенного значення", message="Введіть ID випадку!")
    else:
        global editor
        editor = Tk()
        editor.title('Update A Record')
        editor.geometry("400x300")
        # Create a database or connect to one
        conn = sqlite3.connect('epidemic_dp.db')
        # Create cursor
        c = conn.cursor()

        record_id = delete_box.get()

        # Query the database
        c.execute("SELECT * FROM epidemic_table WHERE id = " + delete_box.get())
        records = c.fetchall()
        
        # Create Global Variables for text box names
        global patient_name_editor
        global patient_age_editor
        global patient_status_editor
        global region_editor
        global city_editor
        global date_editor
        
        # Create Text Boxes
        patient_name_editor = Entry(editor, width=50)
        patient_name_editor.grid(row = 0, column = 1, padx=20, pady=(10, 0))

        patient_age_editor = Entry(editor, width=50)
        patient_age_editor.grid(row = 1, column = 1, padx=20)

        patient_status_editor = Entry(editor, width=50)
        patient_status_editor.grid(row = 2, column = 1, padx=20)

        region_editor = Entry(editor, width=50)
        region_editor.grid(row = 3, column = 1)

        city_editor = Entry(editor, width=50)
        city_editor.grid(row = 4, column = 1, padx=20)

        date_editor = Entry(editor, width=50)
        date_editor.grid(row = 5, column = 1, padx=20)


        # Create Text Box Labels
        name_label = Label(editor, text="Ім'я пацієнта", width=20)
        name_label.grid(row=0, column = 0, pady=(10, 0))

        age_label = Label(editor, text="Вік пацієнта")
        age_label.grid(row=1, column = 0)

        status_label = Label(editor, text="Стан пацієнта")
        status_label.grid(row=2, column = 0)

        region_label = Label(editor, text="Область")
        region_label.grid(row=3, column = 0)

        city_label = Label(editor, text="Місто")
        city_label.grid(row=4, column = 0)

        date_label = Label(editor, text="Дата запису")
        date_label.grid(row=5, column = 0)

        # Take cell value from database
        for record in records:
            patient_name_editor.insert(0,record[1])
            patient_age_editor.insert(0,record[2])
            patient_status_editor.insert(0,record[3])
            region_editor.insert(0,record[4])
            city_editor.insert(0,record[5])
            date_editor.insert(0,record[6])            
        
        # Commit Changes
        conn.commit()
        # Close connection
        conn.close()
        # Create a Save Button to Save edited record
        save_btn = Button(editor, text="Зберегти запис", command=apply)
        save_btn.grid(row=6, column=0)

# Labels
patient_name = Entry(root, width=50)
patient_name.grid(row = 1, column = 1, padx=20, pady=(10, 0))

patient_age = Entry(root, width=50)
patient_age.grid(row = 2, column = 1, padx=20)

patient_status = Entry(root, width=50)
patient_status.grid(row = 3, column = 1, padx=20)

region = Entry(root, width=50)
region.grid(row = 4, column = 1)

city = Entry(root, width=50)
city.grid(row = 5, column = 1, padx=20)

delete_box = Entry(root, width=50)
delete_box.grid(row = 8, column = 1, pady=5)

# Create Text Box Labels
heading = Label(root, text="Введіть дані пацієнта")
heading.grid(row=0, column=0, columnspan=2)
name_label = Label(root, text="Ім'я пацієнта", width=20)
name_label.grid(row=1, column = 0, pady=(10, 0))

age_label = Label(root, text="Вік пацієнта")
age_label.grid(row=2, column = 0)

status_label = Label(root, text="Стан пацієнта")
status_label.grid(row=3, column = 0)

region_label = Label(root, text="Область")
region_label.grid(row=4, column = 0)

city_label = Label(root, text="Місто")
city_label.grid(row=5, column = 0)

delete_box_label = Label(root, text="Номер запису")
delete_box_label.grid(row=8, column = 0, pady=5)

status_info = Label(root, text="Стан пацієнтів: 1. Хворіє 2. Вилікувався 3. Помер")
status_info.grid(row=20, column = 0, columnspan=2)
# Кнопка збереження
save_btn = Button(root, text="Зберегти запис до бази даних", command=save)
save_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

# Кнопка запиту для відображення
show_btn = Button(root, text="Показати записи", command=show)
show_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=135)

# Кнопка для видалення запису
delete_btn = Button(root, text="Видалити запис", command=delete)
delete_btn.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=135)

# Кнопка для редагування запису
edit_btn = Button(root, text="Редагувати запис", command=update)
edit_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=135)

# Commit Changes
conn.commit()
# Close connection
conn.close()
root.mainloop()