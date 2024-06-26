from tkinter import *
import tkinter.messagebox
import pymysql
import random
from time import strftime
from PIL import Image,ImageTk
from user import User
from term import termYear
from year import Year
from teacherDash import Teacher
from dashboard import IMS
from reset import Reset
import tkinter.messagebox as messagebox

class Admin:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1450x730+0+0")
        self.root.overrideredirect(True)
        self.root.title('Color Changer')
        # List of colors
        colors = ["#000000","#000426","#000848"]

        # Function to change the background color
        def change_color():
            color = random.choice(colors)  # Select a random color from the list
            self.root.configure(bg=color)  # Change the background color of the window
            self.root.after(10000, change_color)  # Call the change_color function after 300000ms (5 minutes)

        # Call the change_color function to start changing the color
        change_color()
        #self.root.configure(bg="black")
        self.root .title("Report Management System | Developed by LarksTeckHub")
        
        
        #====================title================
        self.icon_title = PhotoImage(file="images/logo.png")
        desired_width = 100
        desired_height = 50
        self.icon_title = self.icon_title.subsample(int(self.icon_title.width() / desired_width), int(self.icon_title.height() / desired_height)) 
        title= Label(self.root, text="ADMIN DASHBOARD",image=self.icon_title,compound=LEFT, font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)
        
        #============btn_logout=====
        #btn_history = Button(self.root,text="History",font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1150,y=10,height=50,width=150)
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
        
        #===========Left Menu==============
        LeftMenu = Frame(self.root,bd=2,relief=RIDGE, bg="white")
        LeftMenu.place(x=0,y=102,width=200,height=600)
        
                # Assuming functions to retrieve user information from the database
        def get_user_name():
            # Replace this function with your code to fetch the user's name from the database
            return "Admin"  # Example user name

        def get_user_role():
            # Replace this function with your code to fetch the user's role from the database
            return "Admin"  # Example user role

        # Placeholder for user's photo (Assumed as a box)
        user_photo_placeholder = Label(LeftMenu, text="User Photo", bg="lightgray", height=10)
        user_photo_placeholder.pack(side="top", fill="x")

        # Retrieve user information from the database
        user_name = get_user_name()
        user_role = get_user_role()

        # Label to display the user's name
        label_user_name = Label(LeftMenu, text=f"User: {user_name}",bg="#4d636d", padx=5,font=("times new roman",16,"bold"))
        label_user_name.pack(side="top", fill="x")

        # Label to display the user's role
        label_user_role = Label(LeftMenu, text=f"Role: {user_role}",bg="#4d636d", padx=5,font=("times new roman",16,"bold"))
        label_user_role.pack(side="top", fill="x")
        
        ########################Buttons#############################################
        self.icon_side = PhotoImage(file="images/side.png")
        new_width, new_height = 25, 25  # Set the new dimensions
        self.icon_side = self.icon_side.subsample(self.icon_side.width()// new_width, self.icon_side.height() // new_height)
        
        #=========================BUTTONS===============================================
                ################## Term & Year####################################################
        # Create a Menu for Settings dropdown
        self.termYear = Menu(root, tearoff=0)
        self.termYear.configure(font=("times new roman", 16, "bold"))  # Apply the same font as the Settings button
        self.termYear.add_command(label="Year",command=self.show_loading_year, font=("times new roman", 16, "bold"))  # Apply font to dropdown items
        self.termYear.add_command(label="Term",command=self.show_loading_term, font=("times new roman", 16, "bold"))  # Apply font to dropdown items
        
        # Function to display the Settings dropdown
        def show_TermYear():
            x = btn_termYear.winfo_rootx() + btn_termYear.winfo_width()  # Adjust x-coordinate to place the menu on the right
            y = btn_termYear.winfo_rooty() + btn_termYear.winfo_height()
            self.termYear.post(x, y)
        # Settings Button with dropdown
        btn_termYear = Button(LeftMenu, text="Term & Year", image=self.icon_side, compound=LEFT, padx=5, anchor="w", font=("times new roman", 16, "bold"), bg="white", bd=3, cursor="hand2", command=show_TermYear)
        btn_termYear.pack(side=TOP, fill=X)
        
        btn_user = Button(LeftMenu,text="Users",command=self.show_loading_user,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",16,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        #====================================Delete=======================================
        ################## DELETE####################################################
        # Create a Menu for delete dropdown
        self.delete_menu = Menu(root, tearoff=0)
        self.delete_menu.configure(font=("times new roman", 16, "bold"))  # Apply the same font as the Settings button
        self.delete_menu.add_command(label="Delete All Teachers", command=self.delete_all_teacher, font=("times new roman", 16, "bold"))  # Apply font to dropdown items
        self.delete_menu.add_command(label="Delete All Subjects", command=self.delete_all_subject, font=("times new roman", 16, "bold"))  # Apply font to dropdown items
        self.delete_menu.add_command(label="Delete All Marks", command=self.delete_all_marks, font=("times new roman", 16, "bold"))  # Apply font to dropdown items
        self.delete_menu.add_command(label="Delete All Gradings",command=self.delete_all_grade, font=("times new roman", 16, "bold"))  # Apply font to dropdown items
        self.delete_menu.add_command(label="Delete All Remarks",command=self.delete_all_remarks, font=("times new roman", 16, "bold"))  # Apply font to dropdown items
        self.delete_menu.add_command(label="Delete All Students", command=self.delete_all_students, font=("times new roman", 16, "bold"))  # Apply font to dropdown items
        
        # Function to display the Settings dropdown
        def show_delete_menu():
            x = btn_delete.winfo_rootx() + btn_delete.winfo_width()  # Adjust x-coordinate to place the menu on the right
            y = btn_delete.winfo_rooty() + btn_delete.winfo_height()
            self.delete_menu.post(x, y)
        # Delete Button with dropdown 
        btn_delete = Button(LeftMenu,text="Delete",image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",13,"bold"),bg="white",bd=3,cursor="hand2", command=show_delete_menu)
        btn_delete .pack(side=TOP,fill=X)
        #==================================================END==========================
        btn_Backup = Button(LeftMenu,text="Backup",image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",14,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_reportGenerat = Button(LeftMenu,text="Settings",image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",14,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_DOSDash = Button(LeftMenu,text="DOS's Dash",command=self.show_loading_DOS,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",16,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_teachDash = Button(LeftMenu,text="Teacher's Dash", command=self.show_loading_teacher,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",16,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        
        ################## SETTINGS####################################################
        # Create a Menu for Settings dropdown
        self.settings_menu = Menu(root, tearoff=0)
        self.settings_menu.configure(font=("times new roman", 16, "bold"))  # Apply the same font as the Settings button
        self.settings_menu.add_command(label="Reset Password",command= self.show_reset, font=("times new roman", 16, "bold"))  # Apply font to dropdown items
        self.settings_menu.add_command(label="Edit Profile", font=("times new roman", 16, "bold"))  # Apply font to dropdown items
        
        # Function to display the Settings dropdown
        def show_settings_menu():
            x = btn_settings.winfo_rootx() + btn_settings.winfo_width()  # Adjust x-coordinate to place the menu on the right
            y = btn_settings.winfo_rooty() + btn_settings.winfo_height()
            self.settings_menu.post(x, y)
        # Settings Button with dropdown
        btn_settings = Button(LeftMenu, text="Settings", image=self.icon_side, compound=LEFT, padx=5, anchor="w", font=("times new roman", 16, "bold"), bg="white", bd=3, cursor="hand2", command=show_settings_menu)
        btn_settings.pack(side=TOP, fill=X) 

        # Attach the dropdown menu to the Settings button
        #btn_settings['menu'] = self.settings_menu 
         
        btn_logout = Button(LeftMenu,text="Logout",command=self.logout,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",16,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        
        #===============content==================
        #################################################################
       # Connect to the MySQL database
        mydb = pymysql.connect(host="localhost",user="root",database="report2")

        # Create a cursor object to execute SQL queries
        mycursor = mydb.cursor()

        # Execute an SQL query to get the total number of student
        mycursor.execute("SELECT COUNT(*) FROM student")

        # Fetch the result of the query
        result = mycursor.fetchone()

        # Get the total number of student from the result
        total_student = result[0]

        # Display the total number of steudent
        self.lbl_student = Label(self.root, text=f"Total Pupil's\n{total_student}", bd=5, relief=RIDGE, bg="#33bbf9", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_student.place(x=250, y=120, height=100, width=235)
        
        #####################################################
        # Connect to the MySQL database
        mydb = pymysql.connect(host="localhost",user="root",database="report2")

        # Create a cursor object to execute SQL queries
        mycursor = mydb.cursor()

        # Execute an SQL query to get the total number of stuff
        mycursor.execute("SELECT COUNT(*) FROM teacher")

        # Fetch the result of the query
        result = mycursor.fetchone()

        # Get the total number of stuff from the result
        total_stuff = result[0]

        # Display the total number of stuff
        self.lbl_stuff = Label(self.root, text=f"Total Staff\n{total_stuff}", bd=5, relief=RIDGE, bg="#ff5722", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_stuff.place(x=450, y=120, height=100, width=235)
        ##################################################################
        # Connect to the MySQL database
        mydb = pymysql.connect(host="localhost",user="root",database="report2")

        # Create a cursor object to execute SQL queries
        mycursor = mydb.cursor()

        # Execute an SQL query to get the total number of stuff
        mycursor.execute("SELECT COUNT(*) FROM subject")

        # Fetch the result of the query
        result = mycursor.fetchone()

        # Get the total number of stuff from the result
        total_subject = result[0]

        # Display the total number of stuff
        self.lbl_subject = Label(self.root, text=f"Total Subjects\n{total_subject}", bd=5, relief=RIDGE, bg="#009688", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_subject.place(x=650, y=120, height=100, width=235)
        #################################################################
       # Connect to the MySQL database
        mydb = pymysql.connect(host="localhost",user="root",database="report2")

        # Create a cursor object to execute SQL queries
        mycursor = mydb.cursor()

        # Execute an SQL query to get the total number of stuff
        mycursor.execute("SELECT COUNT(*) FROM term")

        # Fetch the result of the query
        result = mycursor.fetchone()

        # Get the total number of term from the result
        total_term = result[0]

        # Display the total number of term
        self.lbl_term = Label(self.root, text=f"Total Term\n{total_term}", bd=5, relief=RIDGE, bg="#607d8b", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_term.place(x=880, y=120, height=100, width=235)
       #########################################################
       # Connect to the MySQL database
        mydb = pymysql.connect(host="localhost",user="root",database="report2")

        # Create a cursor object to execute SQL queries
        mycursor = mydb.cursor()

        # Execute an SQL query to get the total number of user
        mycursor.execute("SELECT COUNT(*) FROM user")

        # Fetch the result of the query
        result = mycursor.fetchone()

        # Get the total number of user from the result
        total_term = result[0]

        # Display the total number of user
        self.lbl_sales = Label(self.root, text=f"Total Users\n{total_term}", bd=5, relief=RIDGE, bg="#ffc107", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_sales.place(x=1100, y=120, height=100, width=255)
       
        #========footer================
        lbl_footer = Label(self.root,text="Report Management System | Developed by LarksTeckHub \nFor any Technical Issue Contact: 0741789121",font=("times new roman",12),bg="#4d636d",fg="white").pack(side=BOTTOM, fill=X)
    #===========Left Menu==============
        photoMenu = Frame(self.root,bd=2,relief=RIDGE, bg="white")
        photoMenu.place(x=250,y=225,width=1100,height=450)
        
        # Load the logo image
        logo_image = Image.open("images/adm.png")  # Replace "path_to_your_logo_image.png" with the actual path to your logo image
        logo_image = logo_image.resize((1100, 450))  # Resize the image to fit the frame
        self.logo_photo = ImageTk.PhotoImage(logo_image)
        
        # Create a label to display the logo image
        self.logo_label = Label(photoMenu, image=self.logo_photo)
        self.logo_label.pack()
     ######################################### DELETE ALL MARKS===================
    def delete_all_marks(self):
        # Display a message box asking for confirmation
        confirmation = messagebox.askquestion("Confirmation", "Do you want to delete all the students' marks?")

        # Check user's response
        if confirmation == "yes":
            # Establish a connection to the database
            conn = pymysql.connect(host="localhost", user="root", database="report2")
            my_cursor = conn.cursor()

            try:
                # Loop through the result tables and delete all records
                for subject_number in range(1, 9):
                    result_table = f"result{subject_number}"
                    #result_table = self.result_table  # Assuming self.result_table contains the result table name
                    delete_query = f"DELETE FROM {result_table}"
                    my_cursor.execute(delete_query)

                # Commit changes and close the connection
                conn.commit()
                messagebox.showinfo("Success", "All students' marks have been deleted successfully.")
            except Exception as e:
                # Display an error message if an exception occurs
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
            finally:
                conn.close()
    def delete_all_students(self):
        # Display a message box asking for confirmation
        confirmation = messagebox.askquestion("Confirmation", "Do you want to delete all the students?")

        # Check user's response
        if confirmation == "yes":
            # Establish a connection to the database
            conn = pymysql.connect(host="localhost", user="root", database="report2")
            my_cursor = conn.cursor()

            try:
                # Delete all records from the student table
                delete_query = "DELETE FROM student"
                my_cursor.execute(delete_query)

                # Commit changes and close the connection
                conn.commit()
                messagebox.showinfo("Success", "All students have been deleted successfully.")
            except Exception as e:
                # Display an error message if an exception occurs
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
            finally:
                conn.close()
    def delete_all_remarks(self):
        # Display a message box asking for confirmation
        confirmation = messagebox.askquestion("Confirmation", "Do you want to delete all the remarks?")

        # Check user's response
        if confirmation == "yes":
            # Establish a connection to the database
            conn = pymysql.connect(host="localhost", user="root", database="report2")
            my_cursor = conn.cursor()

            try:
                # Delete all records from the student table
                delete_query = "DELETE FROM remarks"
                my_cursor.execute(delete_query)

                # Commit changes and close the connection
                conn.commit()
                messagebox.showinfo("Success", "All remarks details have been deleted successfully.")
            except Exception as e:
                # Display an error message if an exception occurs
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
            finally:
                conn.close()
    def delete_all_grade(self):
        # Display a message box asking for confirmation
        confirmation = messagebox.askquestion("Confirmation", "Do you want to delete all the grade details?")

        # Check user's response
        if confirmation == "yes":
            # Establish a connection to the database
            conn = pymysql.connect(host="localhost", user="root", database="report2")
            my_cursor = conn.cursor()

            try:
                # Delete all records from the student table
                delete_query = "DELETE FROM grade"
                my_cursor.execute(delete_query)

                # Commit changes and close the connection
                conn.commit()
                messagebox.showinfo("Success", "All Grades have been deleted successfully.")
            except Exception as e:
                # Display an error message if an exception occurs
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
            finally:
                conn.close()
    def delete_all_teacher(self):
        # Display a message box asking for confirmation
        confirmation = messagebox.askquestion("Confirmation", "Do you want to delete all the Teacher's details?")

        # Check user's response
        if confirmation == "yes":
            # Establish a connection to the database
            conn = pymysql.connect(host="localhost", user="root", database="report2")
            my_cursor = conn.cursor()

            try:
                # Delete all records from the student table
                delete_query = "DELETE FROM teacher"
                my_cursor.execute(delete_query)

                # Commit changes and close the connection
                conn.commit()
                messagebox.showinfo("Success", "All Teachers have been deleted successfully.")
            except Exception as e:
                # Display an error message if an exception occurs
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
            finally:
                conn.close()
    def delete_all_subject(self):
        # Display a message box asking for confirmation
        confirmation = messagebox.askquestion("Confirmation", "Do you want to delete all the subject's details?")

        # Check user's response
        if confirmation == "yes":
            # Establish a connection to the database
            conn = pymysql.connect(host="localhost", user="root", database="report2")
            my_cursor = conn.cursor()

            try:
                # Delete all records from the student table
                delete_query = "DELETE FROM subject"
                my_cursor.execute(delete_query)

                # Commit changes and close the connection
                conn.commit()
                messagebox.showinfo("Success", "All Subject have been deleted successfully.")
            except Exception as e:
                # Display an error message if an exception occurs
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
            finally:
                conn.close()
    #########################################  
    def show_loading_user(self):
        self.loading_label = Label(self.root, text="Loading...", font=("times new roman", 20, "bold"))
        self.loading_label.pack()
        self.root.after(1000, self.user_details)  # After 30 seconds, show another window
    def user_details(self):
        self.loading_label.destroy()
        self.new_window=Toplevel(self.root)
        self.app=User(self.new_window)
        
    #########################################  
    def show_loading_term(self):
        self.loading_label = Label(self.root, text="Loading...", font=("times new roman", 20, "bold"))
        self.loading_label.pack()
        self.root.after(1000, self.term_details)  # After 30 seconds, show another window
        
    def term_details(self):
        self.loading_label.destroy()
        self.new_window=Toplevel(self.root)
        self.app=termYear(self.new_window)
    #########################################  
    def show_loading_year(self):
        self.loading_label = Label(self.root, text="Loading...", font=("times new roman", 20, "bold"))
        self.loading_label.pack()
        self.root.after(1000, self.year_details)  # After 30 seconds, show another window
    def year_details(self):
        self.loading_label.destroy()
        self.new_window=Toplevel(self.root)
        self.app=Year(self.new_window)
        
    
    def show_loading_teacher(self):
        self.loading_label = Label(self.root, text="Loading...", font=("times new roman", 20, "bold"))
        self.loading_label.pack()
        self.root.after(1000, self.teacher_details)  # After 30 seconds, show another window
    def teacher_details(self):
        self.loading_label.destroy()
        self.new_window=Toplevel(self.root)
        self.app=Teacher(self.new_window)
    def show_loading_DOS(self):
        self.loading_label = Label(self.root, text="Loading...", font=("times new roman", 20, "bold"))
        self.loading_label.pack()
        self.root.after(1000, self.teacher_DOS)  # After 30 seconds, show another window
    def teacher_DOS(self):
        self.loading_label.destroy()
        self.new_window=Toplevel(self.root)
        self.app=IMS(self.new_window)
    def show_reset(self):
        self.loading_label = Label(self.root, text="Loading...", font=("times new roman", 20, "bold"))
        self.loading_label.pack()
        self.root.after(1000, self.reset)  # After 30 seconds, show another window
    def reset(self):
        self.loading_label.destroy()
        self.new_window=Toplevel(self.root)
        self.app=Reset(self.new_window)
        
    def logout(self):
        logout = tkinter.messagebox.askyesno("Report Management System", "Confirm if you want to log out", parent=self.root)
        if logout:
            # Perform logout actions here (e.g., closing the window, resetting variables, etc.)
            self.root.destroy()
    
if __name__=="__main__":
    root=Tk()
    ob = Admin(root)
    root.mainloop()
