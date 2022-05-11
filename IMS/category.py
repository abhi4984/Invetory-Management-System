from distutils import command
from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk,Image
import sqlite3
class categoryClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+180+127")
        self.root.minsize(1100,500)
        self.root.maxsize(1100,500)
        self.root.title("Inventory Management System | Developed By Abhinav")
        self.root.config(bg="white")
        self.root.focus_force()
        #-----Variables-----#
        self.var_cat_id=StringVar()
        self.var_name=StringVar()
        #-----title------#
        lbl_title = Label(self.root,text="Manage Product Category",font=("georgia",30),bg="black",fg="white",bd=3,relief=RIDGE).pack(side=TOP,padx=10,pady=10,fill=X)

        lbl_name = Label(self.root,text="Enter Category Name",font=("georgia",30),bg="white").place(x=50,y=100)
        txt_name = Entry(self.root,textvariable=self.var_name,font=("georgia",18),bg="lightyellow").place(x=50,y=170,width=300)

        btn_add = Button(self.root,text="ADD",command=self.add,font=("georgia",15,"bold"),bg="#4caf50",fg="white",cursor="hand2").place(x=360,y=170,width=130,height=30)
        btn_delete = Button(self.root,text="Delete",command=self.delete,font=("georgia",15,"bold"),bg="red",fg="white",cursor="hand2").place(x=500,y=170,width=130,height=30)

        # ======Category_Details======= #

        cat_frame = Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=670,y=100,width=400,height=100)

        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)

        self.categoryTable=ttk.Treeview(cat_frame,columns=('cid','name'),xscrollcommand=scrollx,yscrollcommand=scrolly)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.categoryTable.xview)
        scrolly.config(command=self.categoryTable.yview)

        self.categoryTable.heading("cid",text="C_ID")
        self.categoryTable.heading("name",text="Name")

        self.categoryTable["show"]="headings"   # To Remove the Default Column

        self.categoryTable.column("cid",width=90)
        self.categoryTable.column("name",width=100)
        self.categoryTable.pack(fill=BOTH,expand=1)
        self.categoryTable.bind("<ButtonRelease-1>",self.get_data)

        #====Adding_Photos=====#

        self.im1 = Image.open("Images/category.jpg")
        self.im1 = self.im1.resize((500,250),Image.ANTIALIAS)
        self.im1 = ImageTk.PhotoImage(self.im1)

        self.lbl_im1 = Label(self.root,image=self.im1,bd=3,relief="raise")
        self.lbl_im1.place(x=50,y=220)

        self.im2 = Image.open("Images/cat.jpg")
        self.im2 = self.im2.resize((500,250),Image.ANTIALIAS)
        self.im2 = ImageTk.PhotoImage(self.im2)

        self.lbl_im2 = Label(self.root,image=self.im2,bd=3,relief="raise")
        self.lbl_im2.place(x=580,y=220)

        self.show()
#=================Functions================#
    def add(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","Category Name must be required",parent=self.root)
            else:
                cur.execute("Select * from category where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Category already exits!!",parent=self.root)
                else:
                    cur.execute("Insert into category (name) values(?)",(
                        self.var_name.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Category added Successfully",parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def show(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from category")
            rows=cur.fetchall()
            self.categoryTable.delete(*self.categoryTable.get_children())
            for row in rows:
                self.categoryTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def get_data(self,ev):
        f=self.categoryTable.focus()
        content=(self.categoryTable.item(f))
        row=content['values']

        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])

    def delete(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.var_cat_id.get()=="":
                messagebox.showerror("Error","Select Category from the List",parent=self.root)
            else:
                cur.execute("Select * from category where cid=?",(self.var_cat_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Error, Please Try Again!!!",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do You Really Want To Delete ?",parent=self.root)
                    if(op==True):
                        cur.execute("Delete from category where cid=?",(self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Category Deleted Successfully",parent=self.root)
                        self.show()
                        self.var_cat_id.set("")
                        self.var_name.set("")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    

if __name__ == "__main__":
    root = Tk()
    obj = categoryClass(root)
    root.mainloop()