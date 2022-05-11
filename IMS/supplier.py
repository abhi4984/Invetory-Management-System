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
        
        # ------Options------ #
        lbl_search = Label(self.root,text="Invoice No.",font=("georgia",12))
        lbl_search.place(x=670,y=80)

        txt_search = Entry(self.root,textvariable=self.var_searchtxt,font=("geogia",12,),bg="lightyellow")
        txt_search.place(x=770,y=80)
        btn_search = Button(self.root,command=self.search,text="Search",cursor="hand2",font=("georgia",12),bg="#4caf50",fg="black").place(x=970,y=79,width=100,height=23)

        # -----Title------ #
        title = Label(self.root,text="Supplier Details",font=("georgia",20,"bold"),bg="#0f4d7d",fg="white").place(x=50,y=10,width=1000,height=40)

        # -----Content----- #
            # ----row1----- #
        lbl_supplier_invoice = Label(self.root,text="Invoice No.",font=("georgia",15),bg="white").place(x=50,y=80)
        txt_supplier_invoice = Entry(self.root,textvariable=self.var_sup_invoice,font=("georgia",15),bg="lightyellow").place(x=180,y=80,width=180)
        
            # ------row2------ #
        lbl_name = Label(self.root,text="Name",font=("georgia",15),bg="white").place(x=50,y=120)
        txt_name = Entry(self.root,textvariable=self.var_name,font=("georgia",15),bg="lightyellow").place(x=180,y=120,width=180)
        
            # ------row3------ #
        lbl_contact = Label(self.root,text="Contact",font=("georgia",15),bg="white").place(x=50,y=160)
        txt_contact = Entry(self.root,textvariable=self.var_contact,font=("georgia",15),bg="lightyellow").place(x=180,y=160,width=180)
        
            #------row4------#
        lbl_desc = Label(self.root,text="Description",font=("georgia",15),bg="white").place(x=50,y=200)  
        self.txt_desc = Text(self.root,font=("georgia",15),bg="lightyellow")
        self.txt_desc.place(x=180,y=200,width=470,height=120)
        
        #-----Buttons----#
        btn_add = Button(self.root,text="Save",command=self.add,cursor="hand2",font=("georgia",15),bg="#2196f3",fg="white").place(x=180,y=370,width=110,height=35)
        btn_update = Button(self.root,text="Update",command=self.update,cursor="hand2",font=("georgia",15),bg="#4caf50",fg="white").place(x=300,y=370,width=110,height=35)
        btn_delete = Button(self.root,command=self.delete,text="Delete",cursor="hand2",font=("georgia",15),bg="#f44336",fg="white").place(x=420,y=370,width=110,height=35)
        btn_clear = Button(self.root,text="Clear",command=self.clear,cursor="hand2",font=("georgia",15),bg="#607d8b",fg="white").place(x=540,y=370,width=110,height=35)

        # ------Employee Details------- #
        emp_frame = Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=670,y=120,width=400,height=380)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.supplierTable=ttk.Treeview(emp_frame,columns=('invoice','name','contact','desc'),xscrollcommand=scrollx,yscrollcommand=scrolly)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)

        self.supplierTable.heading("invoice",text="Invoice No.")
        self.supplierTable.heading("name",text="Name")
        self.supplierTable.heading("contact",text="Contact")
        self.supplierTable.heading("desc",text="Description")
        

        self.supplierTable["show"]="headings"   # To Remove the Default Column

        self.supplierTable.column("invoice",width=90)
        self.supplierTable.column("name",width=100)
        self.supplierTable.column("contact",width=100)
        self.supplierTable.column("desc",width=100)

        self.supplierTable.bind("<ButtonRelease-1>",self.get_data)

        self.supplierTable.pack(fill=BOTH,expand=1)

        self.show()
#------------------------------------------------------------------------------------------------------------------------------#
    def add(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice No. must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Invoice No. already exits!!",parent=self.root)
                else:
                    cur.execute("Insert into supplier (invoice,name,contact,desc) values(?,?,?,?)",(
                        self.var_sup_invoice.get(),
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get('1.0',END),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier added Successfully",parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def show(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from supplier")
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
        self.var_contact.set(row[2]),
        self.txt_desc.delete('1.0',END),
        self.txt_desc.insert(END,row[3]),
    
    def update(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice No. Must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice No.!!!!",parent=self.root)
                else:
                    cur.execute("Update supplier set name=?,contact=?,desc=? where invoice=?",(
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get('1.0',END),
                        self.var_sup_invoice.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier Updated Successfully",parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def delete(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice No. Must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice No.!!!!",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do You Really Want To Delete ?",parent=self.root)
                    if(op==True):
                        cur.execute("Delete from supplier where invoice=?",(self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Supplier Deleted Successfully",parent=self.root)
                        # self.show()
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete('1.0',END)
        self.var_searchtxt.set("")

        self.show()

    def search(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Invoice No. is Required!!",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_searchtxt.get(),))
                row=cur.fetchone()
                if row!=None:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    self.supplierTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error", "No Record Found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = supplierClass(root)
    root.mainloop()