from email import message
from inspect import EndOfBlock
import string
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from matplotlib.pyplot import fill, text
class productClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+180+127")
        self.root.minsize(1100,500)
        self.root.maxsize(1100,500)
        self.root.title("Inventory Management System | Developed By Abhinav")
        self.root.config(bg="white")
        self.root.focus_force()

        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_cat = StringVar()
        self.var_sup = StringVar()
        self.cat_list = []
        self.sup_list =[]
        self.fetch_cat_sup()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_name = StringVar()
        self.var_status = StringVar()

        productFrame = Frame(self.root,bd=2,relief=RIDGE,bg="white")
        productFrame.place(x=10,y=10,width=450,height=480)

        # =====title====== #
        title = Label(productFrame,text="Manage Product Details",font=("georgia",18),bg="black",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X)

        lbl_category = Label(productFrame,text="Category",font=("georgia",18),bg="white").place(x=30,y=60)
        lbl_supplier = Label(productFrame,text="Supplier",font=("georgia",18),bg="white").place(x=30,y=110)
        lbl_product_name = Label(productFrame,text="Name",font=("georgia",18),bg="white").place(x=30,y=160)
        lbl_price = Label(productFrame,text="Price",font=("georgia",18),bg="white").place(x=30,y=210)
        lbl_quantity = Label(productFrame,text="Quantity",font=("georgia",18),bg="white").place(x=30,y=260)
        lbl_status = Label(productFrame,text="Status",font=("georgia",18),bg="white").place(x=30,y=310)

        cmb_cat = ttk.Combobox(productFrame,textvariable=self.var_cat,values=self.cat_list,state="readonly",justify=CENTER,font=("georgia",12))
        cmb_cat.current(0)
        cmb_cat.place(x=182,y=68,width=200)

        cmb_sup = ttk.Combobox(productFrame,textvariable=self.var_sup,values=self.sup_list,state="readonly",justify=CENTER,font=("georgia",12))
        cmb_sup.current(0)
        cmb_sup.place(x=182,y=118,width=200)

        txt_name = Entry(productFrame,textvariable=self.var_name,font=("georgia",12),bg="lightyellow").place(x=182,y=168,width=200)
        txt_price = Entry(productFrame,textvariable=self.var_price,font=("georgia",12),bg="lightyellow").place(x=182,y=218,width=200)
        txt_qty = Entry(productFrame,textvariable=self.var_qty,font=("georgia",12),bg="lightyellow").place(x=182,y=268,width=200)

        cmb_status = ttk.Combobox(productFrame,textvariable=self.var_status,values=("Active","Inactive"),state="readonly",justify=CENTER,font=("georgia",12))
        cmb_status.current(0)
        cmb_status.place(x=182,y=318,width=200)

        #-----Buttons----#
        btn_add = Button(productFrame,text="Save",command=self.add,cursor="hand2",font=("georgia",15),bg="#2196f3",fg="white").place(x=10,y=400,width=100,height=40)
        btn_update = Button(productFrame,text="Update",command=self.update,cursor="hand2",font=("georgia",15),bg="#4caf50",fg="white").place(x=120,y=400,width=100,height=40)
        btn_delete = Button(productFrame,command=self.delete,text="Delete",cursor="hand2",font=("georgia",15),bg="#f44336",fg="white").place(x=230,y=400,width=100,height=40)
        btn_clear = Button(productFrame,text="Clear",command=self.clear,cursor="hand2",font=("georgia",15),bg="#607d8b",fg="white").place(x=340,y=400,width=100,height=40)

        # ------SearchFrame------ #
        SearchFrame = LabelFrame(self.root,text="Search Employee",font=("georgia",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=480,y=5,width=600,height=80)

        # ------Options------ #
        cmb_search = ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Category","Supplier","Name"),state="readonly",justify=CENTER,font=("georgia",12))
        cmb_search.current(0)
        cmb_search.place(x=10,y=10,width=180)

        txt_search = Entry(SearchFrame,textvariable=self.var_searchtxt,font=("geogia",12,),bg="lightyellow")
        txt_search.place(x=205,y=10)
        btn_search = Button(SearchFrame,command=self.search,text="Search",cursor="hand2",font=("georgia",12),bg="#4caf50",fg="black").place(x=416,y=7,width=150,height=25)


        # ------Product Details------- #
        p_frame = Frame(self.root,bd=3,relief=RIDGE)
        p_frame.place(x=480,y=100,width=600,height=390)

        scrolly=Scrollbar(p_frame,orient=VERTICAL)
        scrollx=Scrollbar(p_frame,orient=HORIZONTAL)

        self.ProductTable=ttk.Treeview(p_frame,columns=('pid','Category','Supplier','name','price','qty','status'),xscrollcommand=scrollx,yscrollcommand=scrolly)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)

        self.ProductTable.heading("pid",text="P_ID")
        self.ProductTable.heading("Category",text="Category")
        self.ProductTable.heading("Supplier",text="Supplier")
        self.ProductTable.heading("name",text="Name")
        self.ProductTable.heading("price",text="Price")
        self.ProductTable.heading("qty",text="Qty")
        self.ProductTable.heading("status",text="Status")

        self.ProductTable["show"]="headings"   # To Remove the Default Column

        self.ProductTable.column("pid",width=90)
        self.ProductTable.column("Category",width=100)
        self.ProductTable.column("Supplier",width=100)
        self.ProductTable.column("name",width=100)
        self.ProductTable.column("price",width=100)
        self.ProductTable.column("qty",width=100)
        self.ProductTable.column("status",width=100)

        self.ProductTable.bind("<ButtonRelease-1>",self.get_data)

        self.ProductTable.pack(fill=BOTH,expand=1)

        self.show()

#------------------------------------------------------------------------------------------------------------------------------#
    
    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from category")
            cat=cur.fetchall()
            if len(cat) > 0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])
            cur.execute("Select * from supplier")
            sup=cur.fetchall()

            if len(sup) > 0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])
            
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    
    def add(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.var_cat.get()=="Select" or self.var_sup.get()=="Select" or self.var_name.get()=="":
                messagebox.showerror("Error","All fields are required",parent=self.root)
            else:
                cur.execute("Select * from product where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Product already exits!!",parent=self.root)
                else:
                    cur.execute("Insert into product (Category,Supplier,name,price,qty,status) values(?,?,?,?,?,?) ",(
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(), 
                        self.var_status.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","product added Successfully",parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def show(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from product")
            rows=cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def get_data(self,ev):
        f=self.ProductTable.focus()
        content=(self.ProductTable.item(f))
        row=content['values']

        self.var_emp_id.set(row[0]),
        self.var_name.set(row[1]),
        self.var_email.set(row[2]),
        self.var_gender.set(row[3]),
        self.var_contact.set(row[4]),
        self.var_dob.set(row[5]),
        self.var_doj.set(row[6]),
        self.var_pass.set(row[7]),
        self.var_utype.set(row[8]),
        self.txt_address.delete('1.0',END),
        self.txt_address.insert(END,row[9]),
        self.var_salary.set(row[10])

    def update(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Employee ID Must be required",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
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
                        self.txt_address.get('1.0',END),
                        self.var_salary.get(),
                        self.var_emp_id.get()
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
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Employee ID Must be required",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID!!!!",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do You Really Want To Delete ?",parent=self.root)
                    if(op==True):
                        cur.execute("Delete from employee where eid=?",(self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Employee Deleted Successfully",parent=self.root)
                        # self.show()
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("Admin")
        self.txt_address.delete('1.0',END)
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
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error", "No Record Found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = productClass(root)
    root.mainloop()