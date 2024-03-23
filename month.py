from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk
import random
import tkinter as tk
from tkinter import messagebox
import tkinter.messagebox
#import mysql.connector
import pymysql
from time import strftime
from datetime import datetime

class Month:
    def __init__(self,root):
        self.root=root
        self.root.title("Report Management System")
        #self.root.geometry("1150x550+200+100")
        self.root.geometry("1450x730+0+0")
        #self.root.geometry("1170x580+205+100")
        self.root.wm_attributes("-toolwindow", True)
        self.root.wm_attributes("-topmost", True)
        self.root.overrideredirect(True)
        
        #=====================title=======================================================
        lbl_title=Label(self.root,text="Set Month For Each Test",font=("times new roman",18,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
        lbl_title.place(x=0,y=0,width=1150,height=50)
        #===================2st Image===log======================================================
        Image2=Image.open(r"C:\Users\ENG. FRANCIS\Desktop\summer\PYTHON PROJECTS TKINTER\report-management-primary\images\logo.png")
        Image2=Image2.resize((100,40),Image.LANCZOS)
        self.photoImage2=ImageTk.PhotoImage(Image2)
        
        lblimg=Label(self.root,image=self.photoImage2,bd=0,relief=RIDGE)
        lblimg.place(x=5,y=2,width=100,height=40)
        #===================labelframe====================================================
        labelframeleft=LabelFrame(self.root,bd=2,relief=RIDGE,text="Tests",font=("times new roman",18,"bold"),padx=2)
        labelframeleft.place(x=5,y=50,width=425,height=350)
        
        lbl_testID=Label(labelframeleft,text="Test ID",font=("times new roman",12,"bold"),padx=2,pady=6)
        lbl_testID.grid(row=0,column=0,sticky=W,padx=20)
        #===========================testID============================================
        self.var_testID=StringVar()
        x=random.randint(1000,9999)
        self.var_testID.set(str(x))
        entry_testID=ttk.Entry(labelframeleft,textvariable=self.var_testID,width=29,font=("times new roman",13,"bold"),state="readonly")
        entry_testID.grid(row=0,column=1,sticky=W)
        last_reference = self.get_last_reference()  # Function to get the last reference
        
        if last_reference is not None:
            next_reference = str(int(last_reference) + 1)
        else:
            next_reference = "1001"  # Initial reference
        
        self.var_testID.set(next_reference)
        self.var_test=StringVar()
        test=Label(labelframeleft,text="Test",font=("times new roman",12,"bold"),padx=2,pady=6)
        test.grid(row=1,column=0,sticky=W,padx=20)
        #==========================Select Year ========================================

        combo_test = ttk.Combobox(labelframeleft, textvariable=self.var_test, width=27, font=("times new roman", 13, "bold"), state="readonly")
        combo_test["value"]=("Select","Test1","Test2","Test3")
        combo_test.current(0)
        combo_test.grid(row=1, column=1)
        
        month=Label(labelframeleft,text="Month",font=("times new roman",12,"bold"),padx=2,pady=6)
        month.grid(row=2,column=0,sticky=W,padx=20)
        #==========================Term==================================================
        self.var_month=StringVar()
        entry_term=ttk.Entry(labelframeleft,textvariable=self.var_month,width=29,font=("times new roman",13,"bold"))
        entry_term.grid(row=2,column=1,sticky=W)
        
        #================btn===========================================
        btn_frame=Frame(labelframeleft,bd=2,relief=RIDGE)
        btn_frame.place(x=0,y=200,width=412,height=40)
        
        btnAdd=Button(btn_frame,text="Add",command=self.add_data,font=("arial",11,"bold"),bg="black",fg="gold",width=8)
        btnAdd.grid(row=0,column=0,padx=1)
        
        btnUpdate=Button(btn_frame,text="Update",command=self.update,font=("arial",11,"bold"),bg="black",fg="gold",width=8)
        btnUpdate.grid(row=0,column=1,padx=1)
        
        btnDelete=Button(btn_frame,text="Delete",command=self.Delete,font=("arial",11,"bold"),bg="black",fg="gold",width=8)
        btnDelete.grid(row=0,column=2,padx=1)
        
        btnReset=Button(btn_frame,text="Reset",command=self.reset_data,font=("arial",11,"bold"),bg="black",fg="gold",width=8)
        btnReset.grid(row=0,column=3,padx=1)
        
        btnExit=Button(btn_frame,text="Exit",command=self.Exit,font=("arial",11,"bold"),bg="black",fg="gold",width=8)
        btnExit.grid(row=0,column=4,padx=1)
        
        #================table frame search system===========================================
        Table_Frame=LabelFrame(self.root,bd=2,relief=RIDGE,text="Show Test Details",font=("arial",12,"bold"))
        Table_Frame.place(x=550,y=55,width=550,height=350)
        
        Scrollbar_x=ttk.Scrollbar(Table_Frame,orient=HORIZONTAL)
        Scrollbar_y=ttk.Scrollbar(Table_Frame,orient=VERTICAL)
        
        self.term_table=ttk.Treeview(Table_Frame,columns=("testID","test","month"),xscrollcommand=Scrollbar_x.set,yscrollcommand=Scrollbar_y.set)
        Scrollbar_x.pack(side=BOTTOM,fill=X)
        Scrollbar_y.pack(side=RIGHT,fill=Y)
        
        Scrollbar_x.config(command=self.term_table.xview)
        Scrollbar_y.config(command=self.term_table.yview)
        
        self.term_table.heading("testID",text="Test ID",anchor=tk.CENTER)
        self.term_table.heading("test",text="Test",anchor=tk.CENTER)
        self.term_table.heading("month",text="Monnth",anchor=tk.CENTER)
        
        self.term_table["show"]="headings"
        s = ttk.Style(root)
        s.theme_use("clam")
        
        s.configure(".", font=('Helvetice',11))
        s.configure("Treeview.Heading",foreground='red',font=('Helvetica',11,"bold"))
        
        self.term_table.column("testID",width=100,anchor=tk.CENTER)
        self.term_table.column("test",width=100,anchor=tk.CENTER)
        self.term_table.column("month",width=100,anchor=tk.CENTER)
        
        self.term_table.pack(fill=BOTH,expand=1)
        self.term_table.bind("<ButtonRelease-1>",self.get_cusrsor)
        self.fetch_data()
        
        self.term_table.tag_configure("evenrow", background="#f0f0f0")
        self.term_table.tag_configure("oddrow", background="#ffffff")
        
    def add_data(self):
        if self.var_month.get()==""or self.var_test.get()=="":
            messagebox.showerror("Error","All fields are required",parent=self.root)
        else:
            try:
                conn=pymysql.connect(host="localhost",user="root",database="report2")
                my_cursor=conn.cursor()
                # Check if term  already exists
                my_cursor.execute("SELECT * FROM month WHERE testID = %s", (self.var_testID.get(),))
                existing_record = my_cursor.fetchone()

                if existing_record:
                    messagebox.showerror("Error", "Test ID already exists. Please enter a different ID.", parent=self.root)
                else:
                    my_cursor.execute("insert into month values(%s,%s,%s)",(
                        self.var_testID.get(),
                        self.var_test.get(),
                        self.var_month.get(),
                        
                    ))
                    conn.commit()
                    self.fetch_data()
                    conn.close()
                    self.reset_data()
                    messagebox.showinfo("Success","New Term Test And Month Added Successfully",parent=self.root)
            except Exception as es:
                messagebox.showwarning("warning",f"Something went wrong:{str(es)}",parent=self.root) 
    #fetch_data()
    def fetch_data(self):
        conn=pymysql.connect(host="localhost",user="root",database="report2")
        my_cursor=conn.cursor()
        my_cursor.execute("select *from month")
        rows=my_cursor.fetchall()
        if len(rows)!=0:
            self.term_table.delete(*self.term_table.get_children())
            for i in rows:
                self.term_table.insert("",END,values=i)
                conn.commit()
            conn.close()
            for i, item in enumerate(self.term_table.get_children()):
                if i % 2 == 0:
                        self.term_table.item(item, tags=("oddrow",))
                else:
                        self.term_table.item(item, tags=("evenrow",))
                        
    def get_cusrsor(self,event=""):
        cusrsor_row=self.term_table.focus()
        content=self.term_table.item(cusrsor_row)
        row=content["values"]
        # Check if row is not empty and has at least three elements
        if row and len(row) >= 3:
            self.var_testID.set(row[0]),
            self.var_test.set(row[1]),
            self.var_month.set(row[2])
        else:
            # Handle the case where the row is empty or doesn't have enough elements
            # You may want to display an error message or handle it according to your needs
            messagebox.showwarning("Error", "Invalid row selection", parent=self.root)

        
    #update function
    def update(self):
        if self.var_month.get()=="":
            messagebox.showerror("Error","Please enter Month to be updated",parent=self.root)
        else:
            conn=pymysql.connect(host="localhost",user="root",database="report2")
            my_cursor=conn.cursor()
            my_cursor.execute("update  month set month=%s,test=%s where testID=%s",(
                    self.var_month.get(),
                    self.var_test.get(),
                    self.var_testID.get()
                    
            ))
            conn.commit()
            self.fetch_data()
            conn.close()
            self.reset_data()
            messagebox.showinfo("Update","Test details has been updated sucessfully",parent=self.root)
    #delete============================================================
    def Delete(self):
        Delete=messagebox.askyesno("Report Management System","Do you want to delete this New test Details",parent=self.root)
        if Delete>0:
            conn=pymysql.connect(host="localhost",user="root",database="report2")
            my_cursor=conn.cursor()
            query="delete from month where testID=%s"
            value=(self.var_testID.get(),)
            my_cursor.execute(query,value)
        else:
            if not Delete:
                return
        conn.commit()
        self.fetch_data()
        conn.close()
        self.reset_data()
        
    #============================reset===================================================
    def reset_data(self):
        try:
            # Fetch the last reference from the database
            last_reference = self.get_last_reference()

            if last_reference is not None:
                # Increment the last reference by 1
                next_reference = str(int(last_reference) + 1)
            else:
                # If there's no existing reference, set a default value
                next_reference = "1000"

            # Set the incremented reference to self.var_ref
            self.var_testID.set(next_reference)

        except Exception as e:
            print(f"Error fetching or incrementing reference: {e}")
        #x=random.randint(1000,9999)
        #self.var_termID.set(str(x))
        self.var_test.set("Select")
        self.var_month.set("")
    
    def get_last_reference(self):
            try:
                conn = pymysql.connect(host="localhost", user="root", database="report2")
                cursor = conn.cursor()

                # Execute a query to get the maximum reference value from the database
                cursor.execute("SELECT MAX(testID) FROM month")

                # Fetch the result
                result = cursor.fetchone()

                # Close the database connection
                conn.close()

                # If there are no existing references, return None
                if result[0] is not None:
                    return str(result[0])
                else:
                    return None

            except Exception as e:
                print(f"Error: {e}")
                return None
        
    def Exit(self):
            self.Exit= tkinter.messagebox.askyesno("Report Management System","confirm if you want to exit",parent=self.root)
            if self.Exit>0:
                self.root.destroy()
                return
        
        
if __name__=="__main__":
    root=Tk()
    obj=Month(root)
    root.mainloop()