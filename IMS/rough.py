from email import message
from inspect import EndOfBlock
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from matplotlib.pyplot import fill, text
class supplierClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+180+127")
        self.root.minsize(1100,500)
        self.root.maxsize(1100,500)
        self.root.title("Inventory Management System | Developed By Abhinav")
        self.root.config(bg="white")
        self.root.focus_force()

        # ALL Variables

        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_sup_invoice=StringVar()
        self.var_name=StringVar()
        self.var_contact=StringVar()

        # ------SearchFrame------ #
        SearchFrame = LabelFrame(self.root,text="Search Employee",font=("georgia",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=250,y=20,width=600,height=70)

        # ------Options------ #
        cmb_search = ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Email","Name","Employee Id"),state="readonly",justify=CENTER,font=("georgia",12))
        cmb_search.current(0)
        cmb_search.place(x=10,y=10,width=180)

        txt_search = Entry(SearchFrame,textvariable=self.var_searchtxt,font=("geogia",12,),bg="lightyellow")
        txt_search.place(x=205,y=10)
        btn_search = Button(SearchFrame,command=self.search,text="Search",cursor="hand2",font=("georgia",12),bg="#4caf50",fg="black").place(x=416,y=7,width=150,height=25)

        # -----Title------ #
        title = Label(self.root,text="Supplier Details",font=("georgia",15),bg="#0f4d7d",fg="white").place(x=50,y=100,width=1000)

        # -----Content----- #
            # ----row1----- #
        lbl_supplier_invoice = Label(self.root,text="Invoice No.",font=("georgia",15),bg="white").place(x=50,y=150)
        txt_supplier_invoice = Entry(self.root,textvariable=self.var_sup_invoice,font=("georgia",15),bg="lightyellow").place(x=150,y=150,width=180)
        
            # ------row2------ #
        lbl_name = Label(self.root,text="Name",font=("georgia",15),bg="white").place(x=50,y=190)
        txt_name = Entry(self.root,textvariable=self.var_name,font=("georgia",15),bg="lightyellow").place(x=150,y=190,width=180)

        # ------row3------ #
        lbl_contact = Label(self.root,text="Contact",font=("georgia",15),bg="white").place(x=50,y=230)
        txt_contact = Entry(self.root,textvariable=self.var_contact,font=("georgia",15),bg="lightyellow").place(x=150,y=230,width=180)
        
            #------row4------#
        lbl_desc = Label(self.root,text="Description",font=("georgia",15),bg="white").place(x=50,y=270)
        self.txt_desc = Text(self.root,font=("georgia",15),bg="lightyellow")
        self.txt_desc.place(x=150,y=270,width=300,height=60)
        
        #-----Buttons----#
        btn_add = Button(self.root,text="Save",command=self.add,cursor="hand2",font=("georgia",15),bg="#2196f3",fg="white").place(x=500,y=305,width=110,height=25)
        btn_update = Button(self.root,text="Update",command=self.update,cursor="hand2",font=("georgia",15),bg="#4caf50",fg="white").place(x=620,y=305,width=110,height=25)
        btn_delete = Button(self.root,command=self.delete,text="Delete",cursor="hand2",font=("georgia",15),bg="#f44336",fg="white").place(x=740,y=305,width=110,height=25)
        btn_clear = Button(self.root,text="Clear",command=self.clear,cursor="hand2",font=("georgia",15),bg="#607d8b",fg="white").place(x=860,y=305,width=110,height=25)

        # ------Employee Details------- #
        emp_frame = Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=350,relwidth=1,height=150)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.supplierTable=ttk.Treeview(emp_frame,columns=('invoice','name','contact','desc'),xscrollcommand=scrollx,yscrollcommand=scrolly)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)

        self.supplierTable.heading("invoice",text="EMP ID")
        self.supplierTable.heading("name",text="Name")
        self.supplierTable.heading("contact",text="Email")
        self.supplierTable.heading("desc",text="Gender")

        self.supplierTable["show"]="headings"   # To Remove the Default Column

        self.supplierTable.column("invoice",width=90)
        self.supplierTable.column("name",width=100)
        self.supplierTable.column("contact",width=100)
        self.supplierTable.column("desc",width=100)
        self.supplierTable.pack(fill=BOTH,expand=1)
        self.supplierTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()
#------------------------------------------------------------------------------------------------------------------------------#
    def add(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice No. Must be required",parent=self.root)
            else:
                cur.execute("Select * from employee where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This supplier already exits!!",parent=self.root)
                else:
                    cur.execute("Insert into employee (eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) values(?,?,?,?,?,?,?,?,?,?,?)",(
                        self.var_sup_invoice.get(),
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.txt_desc.get('1.0',END),
                        self.var_salary.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Employee added Successfully",parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def show(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from employee")
            rows=cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def get_data(self,ev):
        f=self.supplierTable.focus()
        content=(self.supplierTable.item(f))
        row=content['values']

        self.var_sup_invoice.set(row[0]),
        self.var_name.set(row[1]),
        self.var_email.set(row[2]),
        self.var_gender.set(row[3]),
        self.var_contact.set(row[4]),
        self.var_dob.set(row[5]),
        self.var_doj.set(row[6]),
        self.var_pass.set(row[7]),
        self.var_utype.set(row[8]),
        self.txt_desc.delete('1.0',END),
        self.txt_desc.insert(END,row[9]),
        self.var_salary.set(row[10])

    def update(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Employee ID Must be required",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID!!!!",parent=self.root)
                else:
                    cur.execute("Update employee set name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=?,salary=? where eid=?",(
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.txt_desc.get('1.0',END),
                        self.var_salary.get(),
                        self.var_sup_invoice.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Employee Updated Successfully",parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def delete(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Employee ID Must be required",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID!!!!",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do You Really Want To Delete ?",parent=self.root)
                    if(op==True):
                        cur.execute("Delete from employee where eid=?",(self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Employee Deleted Successfully",parent=self.root)
                        # self.show()
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("Admin")
        self.txt_desc.delete('1.0',END)
        self.var_salary.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")

        self.show()

    def search(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if(self.var_searchby.get()=="Select"):
                messagebox.showerror("Error","Select Search by Option!!",parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Search Input is Required!!",parent=self.root)
            else:
                cur.execute("Select * from employee where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if(len(rows)!=0):
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    for row in rows:
                        self.supplierTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error", "No Record Found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = supplierClass(root)
    root.mainloop()