from tkinter import *
from time import strftime
from tkinter import ttk
import pandas as pd
import tkinter as tk
from tkinter import Toplevel, Label

#import mysql.connector
import pymysql
from tkinter import messagebox
class MarkEntry:
    def __init__(self, root, rows, columns,name, students,selected_class, selected_subject, subject_number ):
        self.root = root
        #self.ClassLbl = Toplevel(self.root)
        self.root.geometry("1450x730+0+0")
        self.root.configure(bg="black")
        self.result_table = "result"
        #self.root.overrideredirect(True)
        #=========================
        
        #=========================
        self.table_frame = Canvas(root)
        self.canvas = Canvas(self.table_frame, bg="white", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.canvas.bind("<Configure>", self.update_scrollregion)
        self.entries = []
        #self.create_table(rows, columns,students)
        self.current_row = 0
        self.current_column = 0
        self.bind_arrow_keys()
        self.root.title("Report Management System | Developed by LarksTeckHub")
        self.rows = rows
        self.columns = columns
        self.name = name
        self.students = students
        self.selected_class = selected_class
        self.selected_subject = selected_subject
        self.result_table = f"result{subject_number}"
        
        self.create_table(rows, columns)

        # Initialize the UI components and create the table
        #========]'] 
        # hn============title================
        title= Label(self.root, text="Marks Entry For Each Subject",compound=LEFT, font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)
        
        self.label_subject = Label(root, text=f"Subject: {selected_subject}", font=("times new roman", 40, "bold"),
                                   bg="#010c48", fg="white", anchor="w", padx=20)
        self.label_subject.place(x=900, y=0, relwidth=1, height=70)
                
        #========clock================
        # Function to display time on the label
        def time():
            string = f"Welcome to Report Management System\t\t Date: {strftime('%d-%m-%Y')}\t\t Time: {strftime('%H:%M:%S')}"  # Format the time string
            self.lbl_clock.config(text=string)  # Update the label with the current time
            self.lbl_clock.after(1000, time)  # Call the time function after 1000ms (1 second)

        # Create a label for the clock
        self.lbl_clock = Label(self.root, text="", font=("times new roman", 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # Call the time function to start displaying the time
        time()
          
        #===========Class Menu==============
        ClassLbl = Frame(self.root,relief=RIDGE, bg="#4d636d")
        ClassLbl.place(x=0,y=100,width=350,height=40)
        
        self.lbl_total_students = Label(ClassLbl, text=f"Total Students: {len(students)}", font=('Arial', 12, 'bold'), fg="white", bg="#4d636d")
        self.lbl_total_students.grid(row=0, column=1, padx=0, pady=3)
        
        self.lblClass = Label(ClassLbl, text=f"Class: {selected_class}", font=('Arial', 12, 'bold'), fg="white", bg="#4d636d")
        self.lblClass.grid(row=0, column=2, padx=75, pady=3)
        
        ClassMenu = Frame(self.root,bd=2,relief=RIDGE, bg="white")
        ClassMenu.place(x=350,y=100,width=1020,height=40)
        
        #================================
        #self.create_table(rows=len(students) + 1, columns=15)
        
        show_marks_button = Button(ClassMenu, text="Show Marks",command=self.show_marks,font=("arial",11,"bold"),bg="black",fg="gold",width=12)
        show_marks_button.grid(row=0,column=0,padx=1)
        
        btnAdd=Button(ClassMenu,text="Save",command=self.save_data,font=("arial",11,"bold"),bg="black",fg="gold",width=12)
        btnAdd.grid(row=0,column=1,padx=1)
        
        #btnPrint=Button(ClassMenu,text="Print Preview",font=("arial",11,"bold"),bg="black",fg="gold",width=12)
        #btnPrint.grid(row=0,column=2,padx=1)
        
        #btnPrintPDF=Button(ClassMenu,text="Print AS PDF",font=("arial",11,"bold"),bg="black",fg="gold",width=12)
        #btnPrintPDF.grid(row=0,column=3,padx=1)
        
        btnExit=Button(ClassMenu,text="Close",command=self.Exit,font=("arial",11,"bold"),bg="black",fg="gold",width=12)
        btnExit.grid(row=0,column=4,padx=1)
        
        #===========Class Menu==============
        table_title = Frame(self.root,relief=RIDGE, bg="#4d636d")
        table_title.place(x=0,y=140,width=5345,height=40)
        
        # Create the title "Student" in the first row
        student_id = Label(table_title, text="ID", font=('Arial', 12, 'bold'), bg="#4d636d",fg="white")
        student_id.place(x=5,y=5,width=50,height=25)
        
        # Create the title "Student" in the first row
        student_title = Label(table_title, text="Student Name", font=('Arial', 12, 'bold'), bg="#4d636d",fg="white")
        student_title.place(x=100,y=5,width=120,height=25)
        
        #===========================Test 1==============================================================================
        # Create the title "Test1" between the 4 cells after the first row
        test1_title = Label(table_title, text="Test 1", font=('Arial', 12, 'bold'), bg="#4d636d",fg="white")
        test1_title.place(x=410,y=5,width=50,height=25)
        
        #===========================Test 2==============================================================================
        test2_title = Label(table_title, text="Test 2", font=('Arial', 12,'bold'), bg="#4d636d",fg="white")
        test2_title.place(x=490,y=5,width=50,height=25)
        
        #===========================Test 3==============================================================================
        test3_title = Label(table_title, text="Test 3", font=('Arial', 12,'bold'), bg="#4d636d",fg="white")
        #test3_title.grid(row=0, column=3,columnspan=10, padx=5, pady=5)
        test3_title.place(x=570,y=5,width=50,height=25)
        
        #===========================Test 4==============================================================================
        test4_title = Label(table_title, text="Exam", font=('Arial', 12,'bold'), bg="#4d636d",fg="white")
        #test4_title.grid(row=0, column=4,columnspan=10,padx=5, pady=5)
        test4_title.place(x=660,y=5,width=50,height=25)
        
        # Create a frame for the table
        self.table_frame = Frame(root)
        self.table_frame.pack(pady=90)
        #=============Marks==================
        
        #========================

        # Create a 2D list to store entries
        self.entries = []
        # Create vertical scrollbar
        vscrollbar = Scrollbar(self.root, orient=VERTICAL)
        vscrollbar.pack(side=RIGHT, fill=Y)

        # Create horizontal scrollbar
        hscrollbar = Scrollbar(self.root, orient=HORIZONTAL)
        hscrollbar.pack(side=BOTTOM, fill=X)
        
        # Create a canvas to hold the table and attach scrollbars
        self.canvas = Canvas(self.root, xscrollcommand=hscrollbar.set , yscrollcommand=vscrollbar.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        vscrollbar.config(command=self.canvas.yview)
        hscrollbar.config(command=self.canvas.xview)
        
        # Create a frame inside the canvas for the table
        self.table_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.table_frame, anchor=NW)

        # Initially, create a 3x3 table
        self.create_table(100, 6 )

        # Configure the canvas to update scroll region when the frame size changes
        self.table_frame.bind("<Configure>", self.update_scrollregion)
        
    def show_marks(self):
        for row in range(len(self.entries)):
            # Get the selected ID and Name from the entries
            selected_id = self.entries[row][0].get()
            selected_name = self.entries[row][1].get()

            # Check if both ID and Name are provided
            if selected_id and selected_name:
                # Connect to the database
                conn = pymysql.connect(host="localhost", user="root", database="report2")
                my_cursor = conn.cursor()

                # Retrieve marks for the selected ID and Name
                result_table = self.result_table
                fetch_query = f"SELECT * FROM {result_table} WHERE studentID = %s AND name = %s"
                my_cursor.execute(fetch_query, (selected_id, selected_name))
                marks_data = my_cursor.fetchone()

                # Check if data is found
                if marks_data:
                    # Update the entries with the retrieved marks starting from column 3
                    for col in range(2, min(len(self.entries[0]), len(marks_data) + 2)):
                        self.entries[row][col].delete(0, END)
                        self.entries[row][col].insert(0, marks_data[col + 2])

                # Close the database connection
                conn.close()
            else:
                #messagebox.showerror("Error", "Please provide both ID and Name." , parent=self.root)
                pass
                    
    def save_data(self):
        # Connect to the database
        conn = pymysql.connect(host="localhost", user="root", database="report2")
        my_cursor = conn.cursor()

        # Loop through the entries and save data to the respective tables (result1, result2, ..., result16)
        for subject_number in range(1, 9):
            #result = f"result{subject_number}"
            result = self.result_table

            # Create the result table if it doesn't exist
            create_table_query = f"CREATE TABLE IF NOT EXISTS {result} (studentID INT PRIMARY KEY, name VARCHAR(255) NOT NULL, class VARCHAR(255) NULL, subject VARCHAR(255) NULL, test1 INT NULL, test2 INT NULL, test3 INT NULL, test4 INT NULL)"
            my_cursor.execute(create_table_query)

            # Insert data into the result table
            for row_index,student_data in enumerate(self.get_entries_data()):
                student_id = student_data[0]
                student_name = student_data[1]
                test1 = student_data[2]
                test2 = student_data[3]
                test3 = student_data[4]
                test4 = student_data[5]
                
                # Check if the record already exists
                check_existence_query = f"SELECT studentID FROM {result} WHERE studentID = %s"
                my_cursor.execute(check_existence_query, (student_id,))
                existing_record = my_cursor.fetchone()

                if existing_record:
                    # Update the existing record
                    update_query = f"UPDATE {result} SET name = %s, class = %s, subject = %s, test1 = %s, test2 = %s,test3 = %s, test4 = %s WHERE studentID = %s"
                    update_values = (student_name, self.selected_class, self.selected_subject, test1,  test2, test3,  test4, student_id)
                    my_cursor.execute(update_query, update_values)
                else:
                    # Insert the new record
                    
                    insert_query = f"INSERT INTO {result} (studentID,name, class, subject, test1, test2, test3,  test4) VALUES (%s,%s, %s, %s, %s, %s, %s, %s)"
                    insert_values = (student_id, student_name, self.selected_class, self.selected_subject, test1, test2,  test3,  test4)

                    my_cursor.execute(insert_query, insert_values)

        # Commit changes and close the connection
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Data saved successfully." , parent=self.root)
        
                
    def create_table(self,rows,columns):
        self.entries = []

    
        for row in range(1, rows):
            row_entries = []
            for col in range(columns):
                if col == 0:
                    entry = Entry(self.table_frame, width=5, font=('Arial', 12))
                    if row - 1 < len(self.students):
                        entry.insert(0, self.students[row - 1])
                elif col == 1:
                    entry = Entry(self.table_frame, width=35, font=('Arial', 12))
                    if row - 1 < len(self.name):
                        entry.insert(1, self.name[row - 1])
                        
                else:
                    entry = Entry(self.table_frame, width=10, font=('Arial', 10))
                entry.grid(row=row, column=col, padx=5, pady=5)
                row_entries.append(entry)
            self.entries.append(row_entries)
    
    def get_entries_data(self):
        data = []
        for row_entries in self.entries:
            row_data = []
            for entry in row_entries:
                row_data.append(entry.get())
            data.append(row_data)
        return data
    
    def add_column(self):
        # Add a new column to the table
        rows = len(self.entries)
        columns = len(self.entries[0])
        for row in range(rows):
            entry = Entry(self.table_frame, width=10, font=('Arial', 10))
            entry.grid(row=row, column=columns, padx=5, pady=5)
            self.entries[row].append(entry)
        self.update_scrollregion(None)
        
    def delete_row(self):
        # Delete the last row from the table
        if len(self.entries) > 1:
            for entry in self.entries[-1]:
                entry.destroy()
            self.entries.pop()
            self.update_scrollregion(None)
    
    def update_total_students_label(self, selected_class):
        # Connect to the database
        conn = pymysql.connect(host="localhost", user="root", database="report2")
        cursor = conn.cursor()

        # Retrieve the total number of students for the selected class
        cursor.execute("SELECT COUNT(*) FROM student WHERE class = %s", (selected_class,))
        total_students = cursor.fetchone()[0]

        # Update the label with the total number of students
        self.lbl_total_students.config(text=f"Total Students: {total_students}")

        # Close the database connection
        conn.close()
            
    def delete_column(self):
        if self.columns > 1:
            for row in self.entries:
                row[-1].destroy()
                row.pop()
            self.columns -= 1
            self.update_scrollregion(None)

    def update_scrollregion(self, event):
        # Update the scroll region of the canvas when the frame size changes
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def bind_arrow_keys(self):
        self.root.bind("<Up>", self.move_up)
        self.root.bind("<Down>", self.move_down)
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)

    def move_up(self, event):
        if self.current_row > 0:
            self.current_row -= 1
            self.entries[self.current_row][self.current_column].focus_set()

    def move_down(self, event):
        if self.current_row < len(self.entries) - 1:
            self.current_row += 1
            self.entries[self.current_row][self.current_column].focus_set()

    def move_left(self, event):
        if self.current_column > 0:
            self.current_column -= 1
            self.entries[self.current_row][self.current_column].focus_set()

    def move_right(self, event):
        if self.current_column < len(self.entries[0]) - 1:
            self.current_column += 1
            self.entries[self.current_row][self.current_column].focus_set()
        

    
    def Exit(self):
           self.Exit= messagebox.askyesno("Report Management System","A you sure you want to close?",parent=self.root)
           if self.Exit>0:
               self.root.destroy()
        
if __name__ == "__main__":
    root = Tk()
    ob = MarkEntry(root,3,3)
    root.mainloop()
#create a fuction to add to numbers

