from tkinter import *
from tkinter import messagebox
import tkinter as tk
import pymysql
from tkinter import ttk
from tkinter import filedialog
from docx import Document
from tkinter import Canvas
from PIL import Image, ImageDraw, ImageTk
import tempfile
import os
from PIL import ImageGrab
from tkinter import Frame, RIDGE, Button
import win32gui

class Card:
    def __init__(self, root):
        self.root = root
        self.root.title("Report Management System")
        self.root.geometry("1550x800+0+0")
        self.root.overrideredirect(True)
        self.current_ref = None  # Initialize current_ref attribute

        
        self.report = Frame(root, relief=tk.RIDGE, bd=2)
        self.report.place(x=0, y=0, width=920, height=1020)
        
        # Create a canvas within the frame
        self.canvas = Canvas(self.report, bg="white", width=880, height=800)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        self.var_ref=StringVar()
        self.var_student_name=StringVar()
        self.var_gender=StringVar()
        self.var_status=StringVar()
        self.var_class=StringVar()
        
        # Add a vertical scrollbar to the canvas
        v_scrollbar = Scrollbar(self.report, orient="vertical", command=self.canvas.yview)
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.config(yscrollcommand=v_scrollbar.set)

        # Add a horizontal scrollbar to the canvas
        h_scrollbar = Scrollbar(self.report, orient="horizontal", command=self.canvas.xview)
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.canvas.config(xscrollcommand=h_scrollbar.set)
        
        # Create a frame to contain the contents of the canvas
        self.frame = Frame(self.canvas , width=920, height=810)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        
        # Update the canvas scroll region
        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        
        # Binding scrollbar movements to canvas
        self.canvas.bind('<Configure>', self.on_configure)
        #v_scrollbar.config(command=self.canvas.yview)
        
        #====================Class============
        self.cl = Frame(root, relief=tk.RIDGE)
        self.cl.place(x=1020, y=3, width=250, height=40)
        
        self.conn = pymysql.connect(host="localhost",user="root",database="report2")
        
        # Retrieve values from the database
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT class FROM subject")  # Modify with your database column and table names
        classs = [classs[0] for classs in cursor.fetchall()]

        self.combo_class = ttk.Combobox(self.cl, width=20, font=("times new roman", 16, "bold"), state="readonly")
        self.combo_class["values"] = tuple(["Select Class"] + classs)
        self.combo_class.current(0)
        self.combo_class.grid(row=0,column=0,padx=0)
        # Bind the combobox selection event to a function
        self.combo_class.bind("<<ComboboxSelected>>", self.update_class_label)
        

        btnExit=Button(root,text="Close",command=self.Exit,font=("arial",11,"bold"),bg="black",fg="gold",width=8)
        btnExit.grid(row=0,column=4,padx=1270)
        
        btnPdf=Button(root,text="Print",font=("arial",11,"bold"),command= self.print_preview,bg="black",fg="gold",width=8)
        btnPdf.grid(row=1,column=4,padx=1270)
        
        btnWord=Button(root,text="PDF",font=("arial",11,"bold"),command= self.generate_pdf,bg="black",fg="gold",width=8)
        btnWord.grid(row=2,column=4,padx=1270)
        
        btnNext=Button(root,text="Next",font=("arial",11,"bold"), command=self.next,bg="black",fg="gold",width=8)
        btnNext.grid(row=3,column=4,padx=1270)
        
        btnPre=Button(root,text="Prev",font=("arial",11,"bold"), command=self.prev,bg="black",fg="gold",width=8)
        btnPre.grid(row=4,column=4,padx=1270)
        
        #===================Seaching frame==============================================
        #===============table===============
        Table_Frame=LabelFrame(root,bd=2,relief=RIDGE,text="Search Student",font=("arial",12,"bold"))
        Table_Frame.place(x=909,y=450,width=500,height=315)
        
        lblSearchBy=Label(Table_Frame,text="Search By:",font=("times new roman",12,"bold"),bg="red",fg="white")
        lblSearchBy.grid(row=0,column=0,sticky=W,padx=2)
        
        self.serch_var=StringVar()
        combo_Search=ttk.Combobox(Table_Frame,textvariable=self.serch_var,width=8,font=("times new roman",13,"bold"),state="readonly")
        combo_Search["value"]=("Ref","Name")
        combo_Search.current(0)
        combo_Search.grid(row=0,column=1,padx=2)
        
        self.txt_search=StringVar()
        txtSearch=ttk.Entry(Table_Frame,textvariable=self.txt_search,width=20,font=("times new roman",13,"bold"))
        txtSearch.grid(row=0,column=2,padx=2)
        
        btnSearch=Button(Table_Frame,text="Search",command=self.search,font=("arial",11,"bold"),bg="black",fg="gold",width=8)
        btnSearch.grid(row=0,column=3,padx=1)
        
        #================Show data table===========================================
        details_table=Frame(Table_Frame,bd=2,relief=RIDGE)
        details_table.place(x=0,y=40,width=465,height=400)
        
        Scrollbar_x=ttk.Scrollbar(details_table,orient=HORIZONTAL)
        Scrollbar_y=ttk.Scrollbar(details_table,orient=VERTICAL)
        
        self.Cust_Details_Table=ttk.Treeview(details_table,columns=("ref","name","gender","status","class"),xscrollcommand=Scrollbar_x.set,yscrollcommand=Scrollbar_y.set)
        Scrollbar_x.pack(side=BOTTOM,fill=X)
        Scrollbar_y.pack(side=RIGHT,fill=Y)
        

        Scrollbar_x.config(command=self.Cust_Details_Table.xview)
        Scrollbar_y.config(command=self.Cust_Details_Table.yview)
        
        self.Cust_Details_Table.heading("ref",text="Ref", anchor=tk.CENTER)
        self.Cust_Details_Table.heading("name",text="Student Name", anchor=tk.CENTER)
        self.Cust_Details_Table.heading("gender",text="Gender", anchor=tk.CENTER)
        self.Cust_Details_Table.heading("status",text="Status", anchor=tk.CENTER)
        self.Cust_Details_Table.heading("class",text="Class", anchor=tk.CENTER)
        
        self.Cust_Details_Table["show"]="headings"
        s = ttk.Style(root)
        s.theme_use("clam")
        
        s.configure(".", font=('Helvetice',11))
        s.configure("Treeview.Heading",foreground='red',font=('Helvetica',11,"bold"))

        self.Cust_Details_Table.column("ref",width=10, anchor=tk.CENTER)
        self.Cust_Details_Table.column("name",width=100)
        self.Cust_Details_Table.column("gender",width=50, anchor=tk.CENTER)
        self.Cust_Details_Table.column("status",width=50, anchor=tk.CENTER)
        self.Cust_Details_Table.column("class",width=50, anchor=tk.CENTER)
        
        self.Cust_Details_Table.pack(fill=BOTH,expand=1)
        self.Cust_Details_Table.bind("<ButtonRelease-1>", self.get_cursor)
        #self.fetch_data()
        self.Cust_Details_Table.tag_configure("evenrow", background="#f0f0f0")
        self.Cust_Details_Table.tag_configure("oddrow", background="#ffffff")
    
        #===================End Seaching frame==============================================
        # Call function to create content inside the card frame
        self.create_card_content()
        
    #==================seaching===========================================
    def get_cursor(self, event=""):
        # Get the selected row
        cursor_row = self.Cust_Details_Table.focus()
        content = self.Cust_Details_Table.item(cursor_row)
        row = content["values"]

        # Update the label variables with the data from the selected row
        self.var_ref.set(row[0])
        self.var_student_name.set(row[1])
        self.var_gender.set(row[2])
        self.var_status.set(row[3])
        self.var_class.set(row[4])

        #self.update_no_label()

    def search(self):
        conn=pymysql.connect(host="localhost",user="root",database="report2")
        my_cursor=conn.cursor()
            
        my_cursor.execute("SELECT * FROM student WHERE " + str(self.serch_var.get()) + " LIKE %s", ('%' + str(self.txt_search.get()) + '%',))

        rows=my_cursor.fetchall()
        if len(rows)!=0:
            self.Cust_Details_Table.delete(*self.Cust_Details_Table.get_children())
            for i in rows:
                self.Cust_Details_Table.insert("",END,values=i)
            conn.commit()
        conn.close()
        # Add tags to alternate rows
        for i, item in enumerate(self.Cust_Details_Table.get_children()):
            if i % 2 == 0:
                self.Cust_Details_Table.item(item, tags=("oddrow",))
            else:
                self.Cust_Details_Table.item(item, tags=("evenrow",))
    #==================End seaching===========================================         
            
    def create_card_content(self):
        # Create the card frame
        self.card = Frame(self.frame, relief=RIDGE, bd=2, bg="white")
        self.card.place(x=5, y=0, width=850, height=770)
        
        # Place other elements inside the card frame
        self.logo = Frame(self.card, relief=tk.RIDGE)
        self.logo.place(x=30, y=4, width=100, height=90)
        
        # Load the logo image
        logo_image = Image.open("images/logo.png")  # Replace "path_to_your_logo_image.png" with the actual path to your logo image
        logo_image = logo_image.resize((100, 100))  # Resize the image to fit the frame
        self.logo_photo = ImageTk.PhotoImage(logo_image)
        
        # Create a label to display the logo image
        self.logo_label = Label(self.logo, image=self.logo_photo)
        self.logo_label.pack()
        
        
        # Placeholder for user's photo (Assumed as a box)
        self.photo = Frame(self.card, relief=tk.RIDGE, bd=1, bg="white")
        self.photo.place(x=700, y=0, width=146, height=120)
        #========================STUDENT PHOTO==================================================
        self.student_photo = tk.Label(self.photo, text="", bg="white", width=146, height=120)
        self.student_photo.grid(row=0, column=0, sticky="nsew" , padx=(0, 0), pady=(0, 0))
    
        # Create a label within the card frame using grid
        title = Label(self.card, text="HANNAH MOSHI PREP SCHOOL", font=("Arial Black", 18, "bold"), bg="white")
        title.grid(row=0, column=0, sticky='WE', padx=(200, 0), pady=(0, 0))

        box = Label(self.card, text="P.O. BOX 1331 JINJA(U)", font=("Arial", 10), bg="white")
        box.grid(row=1, column=0, sticky='WE', padx=(200, 0), pady=(0, 0))

        box = Label(self.card, text="TEL: 077888913/0756942343/0757023912/0709797946", font=("Arial", 13), bg="white")
        box.grid(row=2, column=0, sticky='WE', padx=(150, 0), pady=(0, 0))
        
        self.no = Label(self.card, text="No. ", font=("Arial", 11, "bold"), bg="white")
        self.no.grid(row=3, column=0, sticky='W' , padx=(9, 0), pady=(5, 0))

        title2 = Label(self.card, text="PUPIL’S  PROGRESSIVE REPORT", font=("Arial", 14, "bold"), bg="white")
        title2.grid(row=3, column=0, sticky='WE' , padx=(150, 0), pady=(0, 0))

        self.name = Label(self.card, text="NAME: ..............................................................................................", font=("times new roman", 10, "bold"), bg="white")
        self.name.grid(row=4, column=0, sticky='W', padx=(9, 0), pady=(0, 0))

        self.year = Label(self.card, text="YEAR: .............................................. ", font=("times new roman", 10, "bold"), bg="white")
        self.year.grid(row=4, column=0, sticky='WE', padx=(420, 0), pady=(0, 0))

        self.classL = Label(self.card, text="CLASS:..............................", font=("times new roman", 10, "bold"), bg="white")
        self.classL.grid(row=5, column=0, sticky='W', padx=(9, 0), pady=(0, 0))

        stream = Label(self.card, text="STREAM: ....................... ", font=("times new roman", 10, "bold"), bg="white")
        stream.grid(row=5, column=0, sticky='W', padx=(300, 0), pady=(0, 0))

        self.term = Label(self.card, text="TERM:........................", font=("times new roman", 10, "bold"), bg="white")
        self.term.grid(row=5, column=1, sticky='WE', padx=(0, 0), pady=(0, 0))
        
        self.table1 = Frame(self.card, relief=tk.RIDGE , bg="white")
        self.table1.place(x=0, y=158, width=845, height=305)

        # Create a table within table1 frame
        for i in range(10):
            for j in range(6):
                # Determine label text and font size based on column index
                if i == 0:
                    # Display labels in the first row
                    if j == 0:
                        label_text = "SUBJECT"
                        label_font = ("Times New Roman", 11, "bold")  # Larger font for S
                    elif j == 1:
                        label_text = "FULL MARKS(%)"
                        label_font = ("Times New Roman", 11, "bold")
                    elif j == 2:
                        label_text = "MARKS OBTAINED"
                        label_font = ("Times New Roman", 11 , "bold")
                    elif j == 3:
                        label_text = "GRADE"
                        label_font = ("Times New Roman", 11, "bold")
                    elif j == 4:
                        label_text = "COMMENTS"
                        label_font = ("Times New Roman", 11, "bold")  # Larger font for C
                    elif j == 5:
                        label_text = "INITIATES"
                        label_font = ("Times New Roman", 11, "bold")  # Larger font for I
                else:
                # Display "TOTAL MARKS" in the last cell of the first column
                    if j == 0 and i == 9:
                        label_text = "TOTAL MARKS"
                    else:
                        label_text = ""
                    label_font = ("Times New Roman", 11 , "bold")
                cell_label = Label(self.table1, text=label_text, font=label_font, width=15, height=1, bg="white",
                                    highlightbackground="black", highlightthickness=1)
                cell_label.grid(row=i, column=j)

        # Configure column width for all columns in table1
        self.table1.columnconfigure((0, 1, 2, 3, 4, 5), weight=1, minsize=130)

        titletable2 = Frame(self.card, relief=tk.RIDGE , bg="white")
        titletable2.place(x=150, y=409, width=500, height=25)
        
        term = Label(titletable2, text="PROGRESSIVE  MONTLY TESTS:", font=("times new roman", 10, "bold"), bg="white")
        term.grid(row=0, column=0, sticky='W', padx=(130, 0), pady=(0, 0))
        
        self.table2 = Frame(self.card, relief=tk.RIDGE , bg="white")
        self.table2.place(x=50, y=430, width=785, height=130)
        
        self.one = Frame(self.card, relief=tk.RIDGE , bg="white")
        self.one.place(x=25, y=455, width=20, height=25)
        one = Label(self.one, text="1", font=("times new roman", 11, "bold"), bg="white")
        one.grid(row=0, column=0, sticky='W', padx=(0, 0), pady=(0, 0))
        
        self.two = Frame(self.card, relief=tk.RIDGE , bg="white")
        self.two.place(x=25, y=480, width=20, height=25)
        two = Label(self.two, text="2", font=("times new roman", 11, "bold"), bg="white")
        two.grid(row=0, column=0, sticky='W', padx=(0, 0), pady=(0, 0))
        
        self.three = Frame(self.card, relief=tk.RIDGE , bg="white")
        self.three.place(x=25, y=500, width=20, height=25)
        three = Label(self.three, text="3", font=("times new roman", 11, "bold"), bg="white")
        three.grid(row=0, column=0, sticky='W', padx=(0, 0), pady=(0, 0))
        
        # Create a table within table1 frame
        for i in range(4):
            for j in range(11):
                # Determine label text and font size based on column index
                if i == 0:
                    # Display labels in the first row
                    if j == 0:
                        label_text = "MONTH"
                        label_font = ("Times New Roman", 11, "bold") 
                    elif j == 1:
                        label_text = ""
                        label_font = ("Times New Roman", 11, "bold")
                    elif j == 2:
                        label_text = ""
                        label_font = ("Times New Roman", 11, "bold")
                    elif j == 3:
                        label_text = ""
                        label_font = ("Times New Roman", 11, "bold")
                    elif j == 4:
                        label_text = ""
                        label_font = ("Times New Roman", 11, "bold") 
                    elif j == 5:
                        label_text = ""
                        label_font = ("Times New Roman", 11, "bold") 
                    elif j == 6:
                        label_text = ""
                        label_font = ("Times New Roman", 11, "bold")
                    elif j == 7:
                        label_text = ""
                        label_font = ("Times New Roman", 11, "bold")
                    elif j == 8:
                        label_text = ""
                        label_font = ("Times New Roman", 11, "bold")
                    elif j == 9:
                        label_text = "TOTAL"
                        label_font = ("Times New Roman", 11, "bold")
                    elif j == 10:
                        label_text = "AGG"
                        label_font = ("Times New Roman", 11, "bold")
                else:
                    # Display empty cells for other rows
                    label_text = ""
                    label_font = ("Times New Roman", 11 , "bold")

                # Create label for each cell with black borders
                cell_label = Label(self.table2, text=label_text, font=label_font, width=6, height=1, bg="white",
                                    highlightbackground="black", highlightthickness=1)
                cell_label.grid(row=i, column=j)
                
                # Fetch the term and year for the selected class from the database
                conn = pymysql.connect(host="localhost", user="root", database="report2")
                my_cursor = conn.cursor()
                
                # If it's the first column and not the first row, fetch months from the database
                if j == 0 and i != 0:
                    my_cursor.execute("SELECT month FROM month ")
                    month_records = my_cursor.fetchall()
                    month_list = [record[0] for record in month_records]
                    if i - 1 < len(month_list):
                        label_text = month_list[i - 1]
                    else:
                        label_text = ""
                    cell_label.config(text=label_text)
        
        titletable3 = Frame(self.card, relief=tk.RIDGE , bg="white")
        titletable3.place(x=255, y=530, width=270, height=20)
        
        termgr = Label(titletable3, text="GRADING SCALE", font=("times new roman", 10, "bold"), bg="white")
        termgr.grid(row=0, column=0, sticky='W', padx=(70, 0), pady=(0, 0))
        
        #=====================GRADING SCALE TABLE================
        self.table3 = Frame(self.card, relief=tk.RIDGE , bg="white")
        self.table3.place(x=80, y=550, width=685, height=70)
        
        # Create a table within table1 frame
        for i in range(2):
            for j in range(10):
                # Determine label text and font size based on column index
                if i == 0:
                    # Display labels in the first row
                    if j == 0:
                        label_text = ""
                        label_font = ("Times New Roman", 11, "bold") 
                    elif j == 1:
                        label_text = ""
                        label_font = ("Times New Roman", 11, "bold")
                    elif j == 2:
                        label_text = ""
                        label_font = ("Times New Roman", 11, "bold")
                    elif j == 3:
                        label_text = ""
                        label_font = ("Times New Roman", 11, "bold")
                    elif j == 4:
                        label_text = ""
                        label_font = ("Times New Roman", 11, "bold") 
                    elif j == 5:
                        label_text = ""
                        label_font = ("Times New Roman", 11, "bold") 
                    elif j == 6:
                        label_text = ""
                        label_font = ("Times New Roman", 11, "bold")
                    elif j == 7:
                        label_text = ""
                        label_font = ("Times New Roman", 11, "bold")
                    elif j == 8:
                        label_text = ""
                        label_font = ("Times New Roman", 11, "bold")
                    elif j == 9:
                        label_text = ""
                        label_font = ("Times New Roman", 11, "bold")
                else:
                    # Display empty cells for other rows
                    label_text = ""
                    label_font = ("Times New Roman", 11 , "bold")
                
                # Create label for each cell
                # Create label for each cell with black borders
                grade_label = Label(self.table3, text=label_text, font=label_font, width=6, height=1, bg="white",
                                    highlightbackground="black", highlightthickness=1)
                grade_label.grid(row=i, column=j)
        
        #=====================Footer================
        self.table4 = Frame(self.card, relief=tk.RIDGE, bd=1 , bg="white" , highlightbackground="black", highlightthickness=1)
        self.table4.place(x=0, y=600, width=857, height=198)
        
        self.First = Frame(self.table4, relief=tk.RIDGE, bd=1 , bg="white")
        self.First.place(x=0, y=0, width=846, height=50)
        
        self.label1 = Label(self.First, text="TEACHER'S GENERAL REPORT:  ", font=("times new roman", 10, "bold"), bg="white")
        self.label1.grid(row=0, column=0, sticky='W', padx=(3, 0), pady=(0, 0))
        
         #=======================================SECOND====================================================
        self.second = Frame(self.table4, relief=tk.SOLID, bg="white", highlightbackground="black", highlightthickness=1)
        self.second.place(x=0, y=23, width=845, height=25)
        # Calculate the width of each column
        column_width = 896 // 3

        # Create a Canvas widget to draw the dividing lines
        canvas = Canvas(self.second, bg="white", bd=0, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Draw the dividing lines
        canvas.create_line(column_width, 0, column_width, 35, fill="black")
        canvas.create_line(column_width * 2, 0, column_width * 2, 35, fill="black")

        
        # Add text labels to the columns
        Label(self.second, text="NEXT TERM BEGIN NO: ", font=("times new roman", 10, "bold"), bg="white").place(x=column_width // 18, y=0)
        self.label2 = Label(self.second, text="Day:", font=("times new roman", 10, "bold"), bg="white")
        self.label2.place(x=column_width + column_width // 26, y=0)
        self.label3 = Label(self.second, text="Boarding: ", font=("times new roman", 10, "bold"), bg="white")
        self.label3.place(x=column_width * 2 + column_width // 26, y=0)
        #=======================================END====================================================
        
        #=======================================THIRD====================================================
        self.Third = Frame(self.table4, relief=tk.RIDGE , bg="white" , highlightbackground="black", highlightthickness=1)
        self.Third.place(x=0, y=48, width=845, height=85)
        # Calculate the width of each column
        column_width = 896 // 3

        # Create a Canvas widget to draw the dividing lines
        canvas = Canvas(self.Third, bg="white", bd=0, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Draw the dividing lines
        canvas.create_line(column_width, 0, column_width, 85, fill="black")
        #canvas.create_line(column_width * 2, 0, column_width * 2, 35, fill="black")

        
        # Add text labels to the columns
        self.label_fee = Label(self.Third, text="FEES: ", font=("times new roman", 10, "bold"), bg="white")
        self.label_fee.place(x=column_width // 25, y=10)
        self.label_requirements = Label(self.Third, text="REQUIREMENTS: ", font=("times new roman", 10, "bold"), bg="white")
        self.label_requirements.place(x=column_width + column_width // 35, y=5)
       
        #=======================================END====================================================
        self.sign = Label(self.table4, text="HEADTEACHER \n SIGN AND STAMP", font=("Arial", 10, "bold"), bg="white")
        self.sign.grid(row=7, column=3, sticky='WE' , padx=(40, 0), pady=(126, 0))
        
    def on_configure(self, event):
        # Update the scroll region of the canvas when the frame size changes
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    # Function to update labels based on selected class
    
    def print_preview(self):
        # Capture the content of the frame
        pil_image = self.capture_frame_content()

        # Display the print preview of the frame
        pil_image.show()

    def update_class_label(self, event):
        selected_class = self.combo_class.get()
        # Check if the selected class is equal to "Select Class"
        if selected_class == "Select Class":
            # If it is, display nothing in the class label
            self.classL.config(text=f"CLASS:..............................")
            # Clear table3
            for j in range(10):
                label_font = ("Times New Roman", 11, "bold")
                grade_label = Label(self.table3, text="", font=label_font, width=6, height=1,
                                    highlightbackground="black", highlightthickness=1,bg="white")
                grade_label.grid(row=0, column=j)
        else:
            self.classL.config(text=f"CLASS:   {selected_class}")
            
            # Fetch the term and year for the selected class from the database
            conn = pymysql.connect(host="localhost", user="root", database="report2")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT term, year FROM class WHERE class = %s", (selected_class,))
            class_info = my_cursor.fetchone()
            
            if class_info:
                term, year = class_info
                # Display the term and year in the corresponding labels
                self.term.config(text=f"TERM: {term}")
                self.year.config(text=f"YEAR: {year}")
            else:
                # If no information is found, display default values or handle accordingly
                self.term.config(text="TERM: ")
                self.year.config(text="YEAR: ")
            conn = pymysql.connect(host="localhost", user="root", database="report2")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT MIN(Ref) FROM student WHERE class = %s", (selected_class,))
            least_ref = my_cursor.fetchone()[0]
            
            # Fetch the grades for the selected class from the database
            my_cursor.execute("SELECT grade1, grade2, grade3, grade4, grade5, grade6, grade7, grade8, grade9, grade10 FROM grade WHERE class = %s", (selected_class,))
            grades = my_cursor.fetchone()

            # Populate the first row of table3 with grades
            for j, grade in enumerate(grades, start=0):
                label_font = ("Times New Roman", 11, "bold")
                if grade is not None:
                    grade_label = Label(self.table3, text=grade, font=label_font, width=6, height=1, bg="white",
                                        highlightbackground="black", highlightthickness=1)
                    grade_label.grid(row=0, column=j)
                else:
                    # If the grade is None, display an empty cell
                    grade_label = Label(self.table3, text="", font=label_font, width=6, height=1, bg="white",
                                        highlightbackground="black", highlightthickness=1)
                    grade_label.grid(row=0, column=j)

            # Fetch the subjects for the selected class from the database
            conn = pymysql.connect(host="localhost", user="root", database="report2")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT subject1, subject2, subject3, subject4, subject5, subject6, subject7, subject8 FROM subject WHERE class = %s", (selected_class,))
            subjects = my_cursor.fetchone()
            
            # Populate the first row of self.table2 with subjects starting from j=1
            for j, subject in enumerate(subjects, start=1):  
                label_font = ("Times New Roman", 11, "bold")
                if subject != "":
                    # Create label for the first row with subject name in self.table2
                    cell_label_subject_table2 = Label(self.table2, text=subject, font=label_font, width=6, height=1 , bg="white",
                                                        highlightbackground="black", highlightthickness=1)
                    cell_label_subject_table2.grid(row=0, column=j)
            # Establish database connection
            conn = pymysql.connect(host="localhost", user="root", database="report2")
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM subject WHERE Class=%s", (selected_class,))
            subject_row = cursor.fetchone()
            # Loop through subjects and corresponding teachers
            for j in range(1, 9):
                subject = subject_row[j]  # Get subject from the database row
                if subject:  # Check if subject is not empty
                    # Fetch teacher name for the subject from the database
                    cursor.execute("SELECT Teacher{} FROM subject WHERE Class=%s".format(j), (selected_class,))
                    teacher_name = cursor.fetchone()[0]  # Assuming the teacher's name is in the first column
                    # Check if the teacher name is not "Select"
                    if teacher_name != "Select":
                        if teacher_name != "":
                            # Split the teacher's name if there are two names
                            teacher_names = teacher_name.split()
                            initials = ""
                            # Extract first letter from each name
                            for name in teacher_names:
                                initials += name[0]  # Get the first letter of the name and append to initials
                                # Populate the "Initiates" column with the teacher's initials
                                cell_label_teacher_name = Label(self.table1, text=initials, font=("Times New Roman", 11, "bold"), width=15, height=1, bg="white",
                                                                highlightbackground="black", highlightthickness=1)
                                cell_label_teacher_name.grid(row=j, column=5)  # Assuming "Initiates" column is the 5th column
                        else:
                            cell_label_teacher_name = Label(self.table1, text="", font=("Times New Roman", 11, "bold"), width=15, height=1, bg="white",
                                                            highlightbackground="black", highlightthickness=1)
                            cell_label_teacher_name.grid(row=j, column=5)
                    else:
                        cell_label_teacher_name = Label(self.table1, text="", font=("Times New Roman", 11, "bold"), width=15, height=1, bg="white",
                                                        highlightbackground="black", highlightthickness=1)
                        cell_label_teacher_name.grid(row=j, column=5)
            # Populate the table with subjects
            for i, subject in enumerate(subjects, start=1):  # Start from the first row and iterate through subjects
                label_font = ("Times New Roman", 11, "bold")
                
                # Create label for the first column with subject name
                cell_label_subject = Label(self.table1, text=subject, font=label_font, width=15, height=1 , bg="white",
                                    highlightbackground="black", highlightthickness=1)
                cell_label_subject.grid(row=i, column=0)
                
                # Check if subject is not an empty string before creating label for the second column
                if subject != "":
                    # Create label for the second column with "100%" in line with the subject name
                    cell_label_percentage = Label(self.table1, text="100", font=label_font, width=15, height=1, bg="white",
                                        highlightbackground="black", highlightthickness=1)
                    cell_label_percentage.grid(row=i, column=1)
                # Update the "No" label based on the selected class
                else:
                    # Create label for the second column with "100%" in line with the subject name
                    cell_label_percentage = Label(self.table1, text="", font=label_font, width=15, height=1, bg="white",
                                        highlightbackground="black", highlightthickness=1)
                    cell_label_percentage.grid(row=i, column=1)
                self.update_no_label(event)
        #========================================Grade====================================
    def update_photo(self):
        if self.current_ref:  # Check if the current reference is not None or empty
            conn = pymysql.connect(host="localhost", user="root", database="report2")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT image FROM student WHERE Ref = %s", (self.current_ref,))
            photo_location = my_cursor.fetchone()

            # If photo location exists and is not None, attempt to open the image file
            if photo_location and photo_location[0]:
                try:
                    image = Image.open(photo_location[0])
                    # Resize the image if necessary
                    image = image.resize((146, 120))  # Adjust width and height to cover the frame
                    photo = ImageTk.PhotoImage(image)
                    self.student_photo.configure(image=photo, bg="white")  # Set the background color of the label
                    self.student_photo.image = photo  # Keep a reference to avoid garbage collection
                    self.student_photo.configure(anchor="center")  # Center the photo within the label
                except (FileNotFoundError, IOError) as e:
                    print("Error: Unable to open image file:", e)
                    # Handle the error gracefully, e.g., display a placeholder or an error message to the user
                    self.student_photo.configure(text="", bg="white")  # Set the background color of the label
            else:
                # If no photo location exists or it is None, display a placeholder or handle the case accordingly
                self.student_photo.configure(text="", bg="white")  # Set the background color of the label
        else:
            # If current_ref is None or empty, display a placeholder or handle the case accordingly
            self.student_photo.configure(text="", bg="white")

    def update_no_label(self, event):
        # Retrieve the selected class from the combobox
        selected_class = self.combo_class.get()
        
        if selected_class != "Select Class":
            # Retrieve data from the database based on the selected class
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM remarks WHERE class = %s", (selected_class,))
            record = cursor.fetchone()
            
            def split_text(text, max_chars_per_line=75):
                lines = []
                while len(text) > max_chars_per_line:
                    split_index = text.rfind(' ', 0, max_chars_per_line)
                    if split_index == -1:
                        split_index = max_chars_per_line
                    lines.append(text[:split_index])
                    text = text[split_index:].strip()
                lines.append(text)
                return lines

            # Assuming record[45] contains the text you want to display
            text = record[45]
            lines = split_text(text)

            if len(lines) > 1:
                # Join the lines with newline characters to create a multiline string
                multiline_text = "\n".join(lines)
                self.label_requirements.config(text=f"Requirements:\n{multiline_text}")
            else:
                # If the text is within 60 characters, display it on a single line
                self.label_requirements.config(text=f"Requirements: {text}")

            if record:
                # Update labels with database values
                #self.label1.config(text=f"NEXT TERM BEGIN NO: {record[1]}")  # Assuming the first column is the term begin number
                self.label2.config(text=f"Day: {record[3]}")  # Assuming the second column is the day
                self.label3.config(text=f"Boarding: {record[4]}")  # Assuming the third column is the boarding info
                # Update labels with database values
                self.label_fee.config(text=f"Fee: {record[2]}")
                #self.label_requirements.config(text=f"Requirements: {record[45]}")
                # Call update_photo to display the photo associated with the current reference
                self.update_photo()
                
            # Assuming record[2] contains the data to be displayed
            data = record[2]

            # Check if the length of the data exceeds 30 characters
            if len(data) > 5:
                # Split the data into two lines
                line1 = data[:35]
                line2 = data[35:]
                # Update the label text to display on two lines
                self.label_fee.config(text=f"Fee: \n{line1}\n{line2}")
                self.update_photo()
            else:
                # Update the label text without a new line
                self.label_fee.config(text=f"Fee: ")
                
                # Call update_photo to display the placeholder or handle the case accordingly
                self.update_photo()
                
        # Check if the selected class is equal to "Select Class"
        if selected_class == "Select Class":
            # If it is, display nothing in the class label
            self.no.config(text=f"No: ")
        else:
            # Otherwise, query the database to find the least reference for the selected class
            conn = pymysql.connect(host="localhost", user="root", database="report2")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT MIN(ref) FROM student WHERE class = %s", (selected_class,))
            least_ref = my_cursor.fetchone()[0]

            # Display the least reference for the selected class in the label
            self.no.config(text=f"No: {least_ref}")
            self.current_ref = least_ref  # Update current_ref with least_ref
            
            # Fetch the student's name for the least reference
            my_cursor.execute("SELECT name FROM student WHERE ref = %s", (least_ref,))
            student_name = my_cursor.fetchone()[0]
            # Display the student's name in the label
            self.name.config(text=f"NAME:  {student_name}")
            
            self.classL.config(text=f"CLASS:   {selected_class}")  # Display the selected class
    
            # Fetch the subjects for the selected class from the database
            my_cursor.execute(f"SELECT subject1, subject2, subject3, subject4, subject5, subject6, subject7, subject8 FROM subject WHERE class = %s", (selected_class,))
            subjects = my_cursor.fetchone()
            
            # Populate the first row of self.table2 with subjects starting from j=1
            for j, subject in enumerate(subjects, start=1):  
                label_font = ("Times New Roman", 11, "bold")
                if subject != "":
                    # Create label for the first row with subject name in self.table2
                    cell_label_subject_table2 = Label(self.table2, text=subject, font=label_font, width=6, height=1 , bg="white",
                                                        highlightbackground="black", highlightthickness=1)
                    cell_label_subject_table2.grid(row=0, column=j)

                    # Fetch marks for the current subject
                    result_table = f"result{j}"  # Assuming the result tables are named result1, result2, ...
                    fetch_query = f"SELECT test1 FROM {result_table} WHERE studentID = %s"
                    my_cursor.execute(fetch_query, (least_ref,))
                    marks_data = my_cursor.fetchone()
                    fetch_query = f"SELECT test2 FROM {result_table} WHERE studentID = %s"
                    my_cursor.execute(fetch_query, (least_ref,))
                    marks_data1 = my_cursor.fetchone()
                    fetch_query = f"SELECT test3 FROM {result_table} WHERE studentID = %s"
                    my_cursor.execute(fetch_query, (least_ref,))
                    marks_data2 = my_cursor.fetchone()

                    # Check if marks_data is not None before attempting to display it
                    if marks_data is not None:
                        # Display the marks in the corresponding cell in row 2 and column j
                        cell = self.table2.grid_slaves(row=1, column=j)[0]
                        cell.config(text=", ".join(str(mark) for mark in marks_data))
                    else:
                        # If marks_data is None, display a placeholder or handle the case accordingly
                        cell = self.table2.grid_slaves(row=1, column=j)[0]
                        cell.config(text="")  # Placeholder text or handle the case accordingly
                    
                    # Check if marks_data1 is not None before attempting to display it
                    if marks_data1 is not None:
                        # Display the marks in the corresponding cell in row 2 and column j
                        cell = self.table2.grid_slaves(row=2, column=j)[0]
                        cell.config(text=", ".join(str(mark) for mark in marks_data1))
                    else:
                        # If marks_data1 is None, display a placeholder or handle the case accordingly
                        cell = self.table2.grid_slaves(row=2, column=j)[0]
                        cell.config(text="")  # Placeholder text or handle the case accordingly

                    # Check if marks_data2 is not None before attempting to display it
                    if marks_data2 is not None:
                        # Display the marks in the corresponding cell in row 3 and column j
                        cell = self.table2.grid_slaves(row=3, column=j)[0]
                        cell.config(text=", ".join(str(mark) for mark in marks_data2))
                    else:
                        # If marks_data2 is None, display a placeholder or handle the case accordingly
                        cell = self.table2.grid_slaves(row=3, column=j)[0]
                        cell.config(text="")  # Placeholder text or handle the case accordingly
                else:
                    # Create label for the first row with subject name in self.table2
                    cell_label_subject_table2 = Label(self.table2, text="", font=label_font, width=6, height=1 , bg="white",
                                                        highlightbackground="black", highlightthickness=1)
                    cell_label_subject_table2.grid(row=0, column=j)
                    cell = self.table2.grid_slaves(row=3, column=j)[0]
                    cell.config(text="") 
                    cell = self.table2.grid_slaves(row=2, column=j)[0]
                    cell.config(text="")
                    cell = self.table2.grid_slaves(row=1, column=j)[0]
                    cell.config(text="")
            # Calculate and display the total marks for each row at j=9
            for i in range(1, 4):
                total_marks = 0
                for j in range(1, 9):
                    cell = self.table2.grid_slaves(row=i, column=j)[0]
                    text = cell.cget("text")
                    if text:
                        total_marks += int(text)
                    else:
                        pass
                        #print(f"Empty text found at row {i}, column {j}")
                cell = self.table2.grid_slaves(row=i, column=9)[0]
                cell.config(text=str(total_marks))

            # Fetch the test4 marks for the student
            for subject_number, subject in enumerate(subjects, start=1):
                if subject != "":
                    result_table = f"result{subject_number}"
                    fetch_query = f"SELECT test4 FROM {result_table} WHERE studentID = %s "
                    my_cursor.execute(fetch_query, (least_ref,))
                    marks_data = my_cursor.fetchone()
                            
                    # Check if marks_data is not None before attempting to iterate over it
                    if marks_data is not None:
                        # Display the marks in the corresponding cell in the third column of self.table1
                        cell = self.table1.grid_slaves(row=subject_number, column=2)[0]
                        cell.config(text=", ".join(str(mark) for mark in marks_data))
                    else:
                        cell = self.table1.grid_slaves(row=subject_number, column=2)[0]
                        cell.config(text="")
                    
                    #=======================COMMENT=========================
                    # Fetch the comment for the selected class from the database
                    my_cursor.execute("SELECT mark1, mark1_1, comment1, mark2, mark2_2, comment2, mark3, mark3_3, comment3, mark4, mark4_4, comment4, mark5, mark5_5, comment5, mark6, mark6_6, comment6, mark7, mark7_7, comment7, mark8, mark8_8, comment8, mark9, mark9_9, comment9, mark10, mark10_10, comment10 FROM grade WHERE class = %s", (selected_class,))
                    grade_data1 = my_cursor.fetchone()

                    # Check if grade_data exists for the selected class
                    if grade_data1:
                        # Iterate over the comment and mark ranges
                        for i in range(10):
                            # Extract mark range and comment from the grade_data tuple based on the index
                            mark_index = i * 3
                            mark1, mark1_1, comment = grade_data1[mark_index], grade_data1[mark_index + 1], grade_data1[mark_index + 2]

                            # Determine if the marks fall within the comment range
                            if mark1 is not None and mark1_1 is not None:
                                # Check if the mark from test4 falls within the comment range
                                if mark1 <= marks_data[0] <= mark1_1:
                                    # Display the corresponding comment in the corresponding cell in the fifth column of self.table1
                                    cell = self.table1.grid_slaves(row=subject_number, column=4)[0]
                                    cell.config(text=comment)
                                    break  # Exit the loop once the comment is found

                    # Fetch the grades for the selected class from the database
                    my_cursor.execute("SELECT mark1, mark1_1, grade1, mark2, mark2_2, grade2, mark3, mark3_3, grade3, mark4, mark4_4, grade4, mark5, mark5_5, grade5, mark6, mark6_6, grade6, mark7, mark7_7, grade7, mark8, mark8_8, grade8, mark9, mark9_9, grade9, mark10, mark10_10, grade10 FROM grade WHERE class = %s", (selected_class,))
                    grade_data = my_cursor.fetchone()

                    # Check if grade_data exists for the selected class
                    if grade_data:
                        # Iterate over the grade and mark ranges
                        for i in range(10):
                            # Extract mark range and grade from the grade_data tuple based on the index
                            mark_index = i * 3
                            mark1, mark1_1, grade = grade_data[mark_index], grade_data[mark_index + 1], grade_data[mark_index + 2]

                            # Determine if the marks fall within the grade range
                            if mark1 is not None and mark1_1 is not None:
                                # Check if the mark from test4 falls within the grade range
                                if mark1 <= marks_data[0] <= mark1_1:
                                    # Display the corresponding grade in the corresponding cell in the fourth column of self.table1
                                    cell = self.table1.grid_slaves(row=subject_number, column=3)[0]
                                    cell.config(text=grade)
                                    #break  # Exit the loop once the grade is found
                    #=============================TOTAL=====================================
                    # Calculate and display the total marks for the 3rd column in the 10th cell
                    total_marks = 0
                    for i in range(1, 9):  # Adjusted the range to include the 10th row
                        cell = self.table1.grid_slaves(row=i, column=2)[0]  # Get the cell in the 3rd column
                        text = cell.cget("text")
                        if text:
                            try:
                                total_marks += int(text)
                            except ValueError:
                                pass
                        else:
                            pass
                    cell = self.table1.grid_slaves(row=9, column=2)[0]  # Get the cell in the 10th row, 3rd column
                    cell.config(text=str(total_marks))  # Display total marks in the 10th cell
                    
                    #=============================TOTAL AGG=====================================
                    # Calculate and display the total marks for the 3rd column in the 10th cell
                    total_marks = 0
                    for i in range(1, 9):  # Adjusted the range to include the 10th row
                        cell = self.table1.grid_slaves(row=i, column=3)[0]  # Get the cell in the 3rd column
                        text = cell.cget("text")
                        if text:
                            # Extract numbers from the end of each string and sum them
                            try:
                                # Split the text into words and iterate over them
                                for word in text.split():
                                    # Check if the word ends with a number
                                    if word[-1].isdigit():
                                        # Extract the number at the end of the word and add it to total_marks
                                        number = int(''.join(filter(str.isdigit, word)))  # Extract the number from the word
                                        total_marks += number
                            except ValueError:
                                pass

                    # Update the total marks in the 10th cell
                    cell = self.table1.grid_slaves(row=9, column=3)[0]  # Get the cell in the 10th row, 3rd column
                    cell.config(text=str(total_marks))  # Display total marks in the 10th cell
                    
                    # Fetch the comment for the selected class from the database
                    my_cursor.execute("SELECT mark1_1, mark2_1, tcomm1, mark1_2, mark2_2, tcomm2, mark1_3, mark2_3, tcomm3, mark1_4, mark2_4, tcomm4, mark1_5, mark2_5, tcomm5, mark1_6, mark2_6, tcomm6, mark1_7, mark2_7, tcomm7, mark1_8, mark2_8, tcomm8, mark1_9, mark2_9, tcomm9, mark1_10, mark2_10, tcomm10 FROM remarks WHERE class = %s", (selected_class,))
                    grade_data1 = my_cursor.fetchone()

                    # Check if grade_data exists for the selected class
                    if grade_data1:
                        # Extract the total marks
                        total_marks_text = str(total_marks)

                        # Convert total_marks_text to an integer
                        total_marks = int(total_marks_text)

                        # Iterate over the comment and mark ranges
                        for i in range(10):
                            # Extract mark range and comment from the grade_data tuple based on the index
                            mark_index = i * 3
                            mark1, mark1_1, comment = grade_data1[mark_index], grade_data1[mark_index + 1], grade_data1[mark_index + 2]

                            # Check if mark1 and mark1_1 are not empty before converting them to integers
                            if mark1 and mark1_1:
                                # Convert mark1 and mark1_1 to integers
                                mark1 = int(mark1)
                                mark1_1 = int(mark1_1)

                                # Determine if the total marks fall within the comment range
                                if mark1 is not None and mark1_1 is not None:
                                    if mark1 <= total_marks <= mark1_1:
                                        # Display the corresponding comment in the label
                                        self.label1.config(text=f"TEACHER'S GENERAL REPORT:   {comment}")
                                        #break  # Exit the loop once the comment is found
                                    else:
                                        self.label1.config(text=f"TEACHER'S GENERAL REPORT:   ")
                                else:
                                        self.label1.config(text=f"TEACHER'S GENERAL REPORT:   ")
                            else:
                                        self.label1.config(text=f"TEACHER'S GENERAL REPORT:   ")
                else:
                    cell = self.table1.grid_slaves(row=subject_number, column=2)[0]
                    cell.config(text="")
            #=============================GRADES AND COMMENTS=====================================


                #=============================GRADES AND COMMENTS=====================================
            
            # Fetch the TEST1 marks for the student
            for subject_number, subject in enumerate(subjects, start=1):
                if subject != "":
                    result_table = f"result{subject_number}"
                    fetch_query = f"SELECT test1 FROM {result_table} WHERE studentID = %s"
                    my_cursor.execute(fetch_query, (least_ref,))
                    marks_data = my_cursor.fetchone()

                    # Check if marks_data is not None before attempting to iterate over it
                    if marks_data is not None:
                        # Display the marks in the corresponding cell in row 2 and column subject_number
                        cell = self.table2.grid_slaves(row=1, column=subject_number)[0]
                        cell.config(text=", ".join(str(mark) for mark in marks_data))
                    else:
                        # If marks_data is None, display a placeholder or handle the case accordingly
                        cell = self.table2.grid_slaves(row=2, column=subject_number)[0]
                        cell.config(text="")  # Placeholder text or handle the case accordingly
            # Check if the selected class is not empty
            if selected_class == "" or selected_class == "Select Class":
                # Clear the table if no class is selected or "Select Class" is chosen
                for j in range(10):
                    mark_label = Label(self.table3, text="", font=("Times New Roman", 11, "bold"), width=6, height=1, bg="white",
                                        highlightbackground="black", highlightthickness=1)
                    mark_label.grid(row=1, column=j) 
                
            else:
                # Fetch the grades for the selected class from the database
                my_cursor.execute("SELECT mark1, mark1_1, mark2, mark2_2, mark3, mark3_3, mark4, mark4_4, mark5, mark5_5, mark6, mark6_6, mark7, mark7_7, mark8, mark8_8, mark9, mark9_9, mark10, mark10_10 FROM grade WHERE class = %s", (selected_class,))
                marks = my_cursor.fetchone()

                # Check if marks exist for the selected class
                if marks:
                    # Populate the second row of table3 with marks
                    for j in range(10):
                        # Determine the index of the mark pair in the marks tuple
                        mark_index = j * 2
                        # Extract marks from the tuple based on the index
                        mark1 = marks[mark_index]
                        mark1_1 = marks[mark_index + 1]
                        
                        # Create label for each cell with marks from the database
                        label_font = ("Times New Roman", 11, "bold")
                        # Display marks in the second row
                        mark_label_text = f"{mark1}-{mark1_1}" if mark1 is not None and mark1_1 is not None else ""
                        mark_label = Label(self.table3, text=mark_label_text, font=label_font, width=6, height=1, bg="white",
                                            highlightbackground="black", highlightthickness=1)
                        mark_label.grid(row=1, column=j)
                else:
                    # Clear the table if no marks exist for the selected class
                    for j in range(10):
                        mark_label = Label(self.table3, text="", font=("Times New Roman", 11, "bold"), width=6, height=1, bg="white",
                                            highlightbackground="black", highlightthickness=1)
                        mark_label.grid(row=1, column=j)
                    conn.close()
    #===========================================NEXT======================================
    def next(self):
        # Retrieve the selected class from the combobox
        selected_class = self.combo_class.get()

        # Check if the selected class is equal to "Select Class" or if current_ref is None
        if selected_class == "Select Class" or self.current_ref is None:
            return
        else:
            # Query the database to find the next reference for the selected class
            conn = pymysql.connect(host="localhost", user="root", database="report2")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT ref FROM student WHERE class = %s AND ref > %s ORDER BY ref ASC LIMIT 1", (selected_class, self.current_ref))
            next_ref = my_cursor.fetchone()

            # Check if there is a next reference
            if next_ref:
                # Fetch the student's name for the next reference
                my_cursor.execute("SELECT name FROM student WHERE ref = %s", (next_ref[0],))
                student_name = my_cursor.fetchone()[0]
                # Display the student's name in the label
                self.name.config(text=f"NAME: {student_name}")

                self.current_ref = next_ref[0]
                self.no.config(text=f"No: {self.current_ref}")
                
                # Fetch the subjects for the selected class from the database
                my_cursor.execute(f"SELECT subject1, subject2, subject3, subject4, subject5, subject6, subject7, subject8 FROM subject WHERE class = %s", (selected_class,))
                subjects = my_cursor.fetchone()

                # Fetch the test4 marks for the student
                for subject_number, subject in enumerate(subjects, start=1):
                    if subject != "":
                        result_table = f"result{subject_number}"
                        fetch_query = f"SELECT test4 FROM {result_table} WHERE studentID = %s"
                        my_cursor.execute(fetch_query, (self.current_ref,))
                        marks_data = my_cursor.fetchone()
                        
                        # Fetch the grades for the selected class from the database
                        my_cursor.execute("SELECT mark1, mark1_1, grade1, mark2, mark2_2, grade2, mark3, mark3_3, grade3, mark4, mark4_4, grade4, mark5, mark5_5, grade5, mark6, mark6_6, grade6, mark7, mark7_7, grade7, mark8, mark8_8, grade8, mark9, mark9_9, grade9, mark10, mark10_10, grade10 FROM grade WHERE class = %s", (selected_class,))
                        grade_data = my_cursor.fetchone()

                        # Check if grade_data exists for the selected class
                        if grade_data:
                            # Iterate over the grade and mark ranges
                            for i in range(10):
                                # Extract mark range and grade from the grade_data tuple based on the index
                                mark_index = i * 3
                                mark1, mark1_1, grade = grade_data[mark_index], grade_data[mark_index + 1], grade_data[mark_index + 2]

                                # Determine if the marks fall within the grade range
                                if mark1 is not None and mark1_1 is not None:
                                    # Check if the mark from test4 falls within the grade range
                                    if mark1 <= marks_data[0] <= mark1_1:
                                        # Display the corresponding grade in the corresponding cell in the fourth column of self.table1
                                        cell = self.table1.grid_slaves(row=subject_number, column=3)[0]
                                        cell.config(text=grade)
                                        break  # Exit the loop once the grade is found
                                    
                            #=======================COMMENT=========================
                            # Fetch the comment for the selected class from the database
                            my_cursor.execute("SELECT mark1, mark1_1, comment1, mark2, mark2_2, comment2, mark3, mark3_3, comment3, mark4, mark4_4, comment4, mark5, mark5_5, comment5, mark6, mark6_6, comment6, mark7, mark7_7, comment7, mark8, mark8_8, comment8, mark9, mark9_9, comment9, mark10, mark10_10, comment10 FROM grade WHERE class = %s", (selected_class,))
                            grade_data1 = my_cursor.fetchone()

                            # Check if grade_data exists for the selected class
                            if grade_data1:
                                # Iterate over the comment and mark ranges
                                for i in range(10):
                                    # Extract mark range and comment from the grade_data tuple based on the index
                                    mark_index = i * 3
                                    mark1, mark1_1, comment = grade_data1[mark_index], grade_data1[mark_index + 1], grade_data1[mark_index + 2]

                                    # Determine if the marks fall within the comment range
                                    if mark1 is not None and mark1_1 is not None:
                                        # Check if the mark from test4 falls within the comment range
                                        if mark1 <= marks_data[0] <= mark1_1:
                                            # Display the corresponding comment in the corresponding cell in the fifth column of self.table1
                                            cell = self.table1.grid_slaves(row=subject_number, column=4)[0]
                                            cell.config(text=comment)
                                            break  # Exit the loop once the comment is found
                                        

                        # Check if marks_data is not None before attempting to iterate over it
                        if marks_data is not None:
                            # Display the marks in the corresponding cell in the third column of self.table1
                            cell = self.table1.grid_slaves(row=subject_number, column=2)[0]
                            cell.config(text=", ".join(str(mark) for mark in marks_data))
                        else:
                            # If marks_data is None, display a placeholder or handle the case accordingly
                            cell = self.table1.grid_slaves(row=subject_number, column=2)[0]
                            cell.config(text="")  # Placeholder text or handle the case accordingly
                # Calculate and display the total marks for the 3rd column in the 10th cell
                    total_marks = 0
                    for i in range(1, 9):  # Adjusted the range to include the 10th row
                        cell = self.table1.grid_slaves(row=i, column=2)[0]  # Get the cell in the 3rd column
                        text = cell.cget("text")
                        if text:
                            try:
                                total_marks += int(text)
                            except ValueError:
                                pass
                        else:
                            pass
                    cell = self.table1.grid_slaves(row=9, column=2)[0]  # Get the cell in the 10th row, 3rd column
                    cell.config(text=str(total_marks))  # Display total marks in the 10th cell
                    #=============================TOTAL AGG=====================================
                    # Calculate and display the total marks for the 3rd column in the 10th cell
                    total_marks = 0
                    for i in range(1, 9):  # Adjusted the range to include the 10th row
                        cell = self.table1.grid_slaves(row=i, column=3)[0]  # Get the cell in the 3rd column
                        text = cell.cget("text")
                        if text:
                            # Extract numbers from the end of each string and sum them
                            try:
                                # Split the text into words and iterate over them
                                for word in text.split():
                                    # Check if the word ends with a number
                                    if word[-1].isdigit():
                                        # Extract the number at the end of the word and add it to total_marks
                                        number = int(''.join(filter(str.isdigit, word)))  # Extract the number from the word
                                        total_marks += number
                            except ValueError:
                                pass

                    # Update the total marks in the 10th cell
                    cell = self.table1.grid_slaves(row=9, column=3)[0]  # Get the cell in the 10th row, 3rd column
                    cell.config(text=str(total_marks))  # Display total marks in the 10th cell
                    
                    # Fetch the comment for the selected class from the database
                    my_cursor.execute("SELECT mark1_1, mark2_1, tcomm1, mark1_2, mark2_2, tcomm2, mark1_3, mark2_3, tcomm3, mark1_4, mark2_4, tcomm4, mark1_5, mark2_5, tcomm5, mark1_6, mark2_6, tcomm6, mark1_7, mark2_7, tcomm7, mark1_8, mark2_8, tcomm8, mark1_9, mark2_9, tcomm9, mark1_10, mark2_10, tcomm10 FROM remarks WHERE class = %s", (selected_class,))
                    grade_data1 = my_cursor.fetchone()

                    # Check if grade_data exists for the selected class
                    if grade_data1:
                        # Extract the total marks
                        total_marks_text = str(total_marks)

                        # Convert total_marks_text to an integer
                        total_marks = int(total_marks_text)

                        # Iterate over the comment and mark ranges
                        for i in range(10):
                            # Extract mark range and comment from the grade_data tuple based on the index
                            mark_index = i * 3
                            mark1, mark1_1, comment = grade_data1[mark_index], grade_data1[mark_index + 1], grade_data1[mark_index + 2]

                            # Check if mark1 and mark1_1 are not empty strings
                            if mark1.strip() and mark1_1.strip():
                                # Convert mark1 and mark1_1 to integers
                                mark1 = int(mark1)
                                mark1_1 = int(mark1_1)

                                # Convert total_marks_text to an integer
                                total_marks = int(total_marks_text)

                                # Determine if the total marks fall within the comment range
                                if mark1 <= total_marks <= mark1_1:
                                    # Display the corresponding comment in the label
                                    self.label1.config(text=f"TEACHER'S GENERAL REPORT:   {comment}")
                                    break  # Exit the loop once the comment is found

                                
            
                # Call update_photo to display the photo associated with the current reference
                self.update_photo()
                
                # Fetch the test1, test2, and test3 marks for the student
                for subject_number, subject in enumerate(subjects, start=1):
                    if subject != "":
                        result_table = f"result{subject_number}"
                        for i in range(1, 4):  # Fetch marks for test1, test2, and test3
                            fetch_query = f"SELECT test{i} FROM {result_table} WHERE studentID = %s"
                            my_cursor.execute(fetch_query, (self.current_ref,))
                            marks_data = my_cursor.fetchone()

                            # Display the marks in the corresponding cell in row i and column subject_number
                            cell = self.table2.grid_slaves(row=i, column=subject_number)[0]
                            if marks_data is not None:
                                cell.config(text=", ".join(str(mark) for mark in marks_data))
                            else:
                                cell.config(text="")  # Placeholder text or handle the case accordingly
                # Calculate and display the total marks for each row at j=9
                for i in range(1, 4):
                    total_marks = 0
                    for j in range(1, 9):
                        cell = self.table2.grid_slaves(row=i, column=j)[0]
                        text = cell.cget("text")
                        if text:
                            total_marks += int(text)
                        else:
                            pass
                            #print(f"Empty text found at row {i}, column {j}")
                    cell = self.table2.grid_slaves(row=i, column=9)[0]
                    cell.config(text=str(total_marks))
                

                # Close the database connection
                conn.close()
        #else:
        #    pass
#===========================================PREV======================================
    def prev(self):
        # Retrieve the selected class from the combobox
        selected_class = self.combo_class.get()

        # Check if the selected class is equal to "Select Class" or if current_ref is None
        if selected_class == "Select Class" or self.current_ref is None:
            return

        # Query the database to find the previous reference for the selected class
        conn = pymysql.connect(host="localhost", user="root", database="report2")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT ref FROM student WHERE class = %s AND ref < %s ORDER BY ref DESC LIMIT 1", (selected_class, self.current_ref))
        prev_ref = my_cursor.fetchone()

        # Check if there is a previous reference
        if prev_ref:
            # Fetch the student's name for the previous reference
            my_cursor.execute("SELECT name FROM student WHERE ref = %s", (prev_ref[0],))
            student_name = my_cursor.fetchone()[0]
            # Display the student's name in the label
            self.name.config(text=f"NAME: {student_name}")

            self.current_ref = prev_ref[0]
            self.no.config(text=f"No: {self.current_ref}")
            
            # Fetch the subjects for the selected class from the database
            my_cursor.execute(f"SELECT subject1, subject2, subject3, subject4, subject5, subject6, subject7, subject8 FROM subject WHERE class = %s", (selected_class,))
            subjects = my_cursor.fetchone()

            # Fetch the test4 marks for the student
            for subject_number, subject in enumerate(subjects, start=1):
                if subject != "":
                    result_table = f"result{subject_number}"
                    fetch_query = f"SELECT test4 FROM {result_table} WHERE studentID = %s"
                    my_cursor.execute(fetch_query, (self.current_ref,))
                    marks_data = my_cursor.fetchone()
                    
                    # Fetch the grades for the selected class from the database
                    my_cursor.execute("SELECT mark1, mark1_1, grade1, mark2, mark2_2, grade2, mark3, mark3_3, grade3, mark4, mark4_4, grade4, mark5, mark5_5, grade5, mark6, mark6_6, grade6, mark7, mark7_7, grade7, mark8, mark8_8, grade8, mark9, mark9_9, grade9, mark10, mark10_10, grade10 FROM grade WHERE class = %s", (selected_class,))
                    grade_data = my_cursor.fetchone()

                    # Check if grade_data exists for the selected class
                    if grade_data:
                        # Iterate over the grade and mark ranges
                        for i in range(10):
                            # Extract mark range and grade from the grade_data tuple based on the index
                            mark_index = i * 3
                            mark1, mark1_1, grade = grade_data[mark_index], grade_data[mark_index + 1], grade_data[mark_index + 2]

                            # Determine if the marks fall within the grade range
                            if mark1 is not None and mark1_1 is not None:
                                # Check if the mark from test4 falls within the grade range
                                if mark1 <= marks_data[0] <= mark1_1:
                                    # Display the corresponding grade in the corresponding cell in the fourth column of self.table1
                                    cell = self.table1.grid_slaves(row=subject_number, column=3)[0]
                                    cell.config(text=grade)
                                    break  # Exit the loop once the grade is found
                                
                            #=======================COMMENT=========================
                        # Fetch the comment for the selected class from the database
                        my_cursor.execute("SELECT mark1, mark1_1, comment1, mark2, mark2_2, comment2, mark3, mark3_3, comment3, mark4, mark4_4, comment4, mark5, mark5_5, comment5, mark6, mark6_6, comment6, mark7, mark7_7, comment7, mark8, mark8_8, comment8, mark9, mark9_9, comment9, mark10, mark10_10, comment10 FROM grade WHERE class = %s", (selected_class,))
                        grade_data1 = my_cursor.fetchone()

                        # Check if grade_data exists for the selected class
                        if grade_data1:
                            # Iterate over the comment and mark ranges
                            for i in range(10):
                                # Extract mark range and comment from the grade_data tuple based on the index
                                mark_index = i * 3
                                mark1, mark1_1, comment = grade_data1[mark_index], grade_data1[mark_index + 1], grade_data1[mark_index + 2]

                                # Determine if the marks fall within the comment range
                                if mark1 is not None and mark1_1 is not None:
                                    # Check if the mark from test4 falls within the comment range
                                    if mark1 <= marks_data[0] <= mark1_1:
                                        # Display the corresponding comment in the corresponding cell in the fifth column of self.table1
                                        cell = self.table1.grid_slaves(row=subject_number, column=4)[0]
                                        cell.config(text=comment)
                                        break  # Exit the loop once the comment is found

                    # Check if marks_data is not None before attempting to iterate over it
                    if marks_data is not None:
                        # Display the marks in the corresponding cell in the third column of self.table1
                        cell = self.table1.grid_slaves(row=subject_number, column=2)[0]
                        cell.config(text=", ".join(str(mark) for mark in marks_data))
                    else:
                        # If marks_data is None, display a placeholder or handle the case accordingly
                        cell = self.table1.grid_slaves(row=subject_number, column=2)[0]
                        cell.config(text="")  # Placeholder text or handle the case accordingly
            # Calculate and display the total marks for the 3rd column in the 10th cell
                total_marks = 0
                for i in range(1, 9):  # Adjusted the range to include the 10th row
                    cell = self.table1.grid_slaves(row=i, column=2)[0]  # Get the cell in the 3rd column
                    text = cell.cget("text")
                    if text:
                        try:
                            total_marks += int(text)
                        except ValueError:
                            pass
                    else:
                        pass
                cell = self.table1.grid_slaves(row=9, column=2)[0]  # Get the cell in the 10th row, 3rd column
                cell.config(text=str(total_marks))  # Display total marks in the 10th cell
                #=============================TOTAL AGG=====================================
                # Calculate and display the total marks for the 3rd column in the 10th cell
                total_marks = 0
                for i in range(1, 9):  # Adjusted the range to include the 10th row
                    cell = self.table1.grid_slaves(row=i, column=3)[0]  # Get the cell in the 3rd column
                    text = cell.cget("text")
                    if text:
                        # Extract numbers from the end of each string and sum them
                        try:
                            # Split the text into words and iterate over them
                            for word in text.split():
                                # Check if the word ends with a number
                                if word[-1].isdigit():
                                    # Extract the number at the end of the word and add it to total_marks
                                    number = int(''.join(filter(str.isdigit, word)))  # Extract the number from the word
                                    total_marks += number
                        except ValueError:
                            pass

                # Update the total marks in the 10th cell
                cell = self.table1.grid_slaves(row=9, column=3)[0]  # Get the cell in the 10th row, 3rd column
                cell.config(text=str(total_marks))  # Display total marks in the 10th cell
                # Fetch the comment for the selected class from the database
                my_cursor.execute("SELECT mark1_1, mark2_1, tcomm1, mark1_2, mark2_2, tcomm2, mark1_3, mark2_3, tcomm3, mark1_4, mark2_4, tcomm4, mark1_5, mark2_5, tcomm5, mark1_6, mark2_6, tcomm6, mark1_7, mark2_7, tcomm7, mark1_8, mark2_8, tcomm8, mark1_9, mark2_9, tcomm9, mark1_10, mark2_10, tcomm10 FROM remarks WHERE class = %s", (selected_class,))
                grade_data1 = my_cursor.fetchone()

                # Check if grade_data exists for the selected class
                if grade_data1:
                    # Extract the total marks
                    total_marks_text = str(total_marks)

                    # Convert total_marks_text to an integer
                    total_marks = int(total_marks_text)

                    # Iterate over the comment and mark ranges
                    for i in range(10):
                        # Extract mark range and comment from the grade_data tuple based on the index
                        mark_index = i * 3
                        mark1, mark1_1, comment = grade_data1[mark_index], grade_data1[mark_index + 1], grade_data1[mark_index + 2]

                        # Check if mark1 and mark1_1 are not empty strings
                        if mark1.strip() and mark1_1.strip():
                            # Convert mark1 and mark1_1 to integers
                            mark1 = int(mark1)
                            mark1_1 = int(mark1_1)

                            # Convert total_marks_text to an integer
                            total_marks = int(total_marks_text)

                            # Determine if the total marks fall within the comment range
                            if mark1 <= total_marks <= mark1_1:
                                # Display the corresponding comment in the label
                                self.label1.config(text=f"TEACHER'S GENERAL REPORT:   {comment}")
                                break  # Exit the loop once the comment is found

            
            # Call update_photo to display the photo associated with the current reference
            self.update_photo()
                
            # Fetch the test1, test2, and test3 marks for the student
            for subject_number, subject in enumerate(subjects, start=1):
                if subject != "":
                    result_table = f"result{subject_number}"
                    for i in range(1, 4):  # Fetch marks for test1, test2, and test3
                        fetch_query = f"SELECT test{i} FROM {result_table} WHERE studentID = %s"
                        my_cursor.execute(fetch_query, (self.current_ref,))
                        marks_data = my_cursor.fetchone()

                        # Display the marks in the corresponding cell in row i and column subject_number
                        cell = self.table2.grid_slaves(row=i, column=subject_number)[0]
                        if marks_data is not None:
                            cell.config(text=", ".join(str(mark) for mark in marks_data))
                        else:
                            cell.config(text="")  # Placeholder text or handle the case accordingly
            # Calculate and display the total marks for each row at j=9
            for i in range(1, 4):
                total_marks = 0
                for j in range(1, 9):
                    cell = self.table2.grid_slaves(row=i, column=j)[0]
                    text = cell.cget("text")
                    if text:
                        total_marks += int(text)
                    else:
                        pass
                        #print(f"Empty text found at row {i}, column {j}")
                cell = self.table2.grid_slaves(row=i, column=9)[0]
                cell.config(text=str(total_marks))
            
            # Close the database connection
            conn.close()

                    
    def generate_pdf(self):
        # Create a new Word document
        doc = Document()
        
        # Capture the content of the Tkinter frame as an image
        pil_image = self.capture_frame_content()

        # Save the image to a temporary file
        temp_image_file = tempfile.NamedTemporaryFile(delete=False)
        pil_image.save(temp_image_file.name + ".png")
        
        # Add the image to the Word document
        doc.add_picture(temp_image_file.name + ".png" )

        # Save the Word document
        file_path = filedialog.asksaveasfilename(defaultextension=".docx")
        if file_path:
            doc.save(file_path)
        
        # Close and delete the temporary file
        temp_image_file.close()
        os.unlink(temp_image_file.name + ".png")

    def capture_frame_content(self):
        # Get the size of the card frame
        width = self.card.winfo_width()
        height = self.card.winfo_height()

        # Get the handle of the card frame window
        hwnd = self.card.winfo_id()

        # Find the top-left corner coordinates of the card frame window relative to the screen
        x0, y0, _, _ = win32gui.GetWindowRect(hwnd)

        # Calculate the bottom-right corner coordinates relative to the top-left corner
        x1 = x0 + width
        y1 = y0 + height

        # Create a PIL Image to draw onto
        pil_image = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(pil_image)

        # Render the contents of the card frame onto the PIL Image
        self.card.update()  # Ensure the frame is updated
        draw.rectangle((0, 0, width, height), fill="white")  # Background color of the card frame
        self.card.update_idletasks()  # Ensure all the widgets inside the frame are rendered

        # Grab the rendered content including the hidden information
        pil_image.paste(ImageGrab.grab(bbox=(x0, y0, x1, y1)))

        return pil_image

    def Exit(self):
        self.Exit= messagebox.askyesno("Report Management System","confirm if you want to exit",parent=self.root)
        if self.Exit>0:
            self.root.destroy()
            #self.dashboard_root.deiconify()  # Show the hidden form again

if __name__=="__main__":
    root=Tk()
    obj=Card(root)
    root.mainloop()
