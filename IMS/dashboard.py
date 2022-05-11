from tkinter import *
from tkinter import font
from matplotlib import image
from employee import employeeClass
from sympy import comp
from PIL import Image, ImageTk
from supplier import supplierClass
from category import categoryClass
from product import productClass

class IMS:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.minsize(1350,700)
        self.root.maxsize(1350,700)

        self.root.title("Inventory Management System | Developed By Abhinav")
        self.root.config(bg="white")

        # -----title---- #
        self.icon_title = PhotoImage(file="Images/logo1.png")
        title = Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font=("georgia",40 ,"bold"),bg="black",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        # -----Logout Btn----- #
        btn_logout = Button(self.root,text="Logout",font=("georgia",15,"bold"),bg="yellow",cursor="hand2").place(x=1100,y=10,height=50,width=150)

        # ----Clock---- #
        self.lbl_clock = Label(self.root,text="Welcome to Inventory Management System\t\t Date : DD-MM-YYYY\t Time : HH:MM:SS",font=("georgia",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        # -----Left Menu----- #
        self.MenuLogo = Image.open("Images/menu_im.png")
        self.MenuLogo = self.MenuLogo.resize((170,170),Image.ANTIALIAS)
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)

        LeftMenu = Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=102,width=200,height=497)

        lbl_menuLogo = Label(LeftMenu,image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP,fill=X)
        
        self.icon_side = PhotoImage(file="Images/side.png")
        lbl_menu = Label(LeftMenu,text="Menu",font=("georgia",20),bg="#009688").pack(side=TOP,fill=X)
        
        btn_employee = Button(LeftMenu,text="Employee",command=self.employee,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("georgia",17,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_supplier = Button(LeftMenu,text="Supplier",command=self.supplier,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("georgia",17,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_category = Button(LeftMenu,text="Category",command=self.category,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("georgia",17,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_product = Button(LeftMenu,text="Product",command=self.product,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("georgia",17,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_sales = Button(LeftMenu,text="Sales",image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("georgia",17,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_exit = Button(LeftMenu,text="Exit",image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("georgia",17,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        
        # -----Content----- #
        self.lbl_employee = Label(self.root,text="Total Employee\n[0]",bd=5,relief=RIDGE,bg="blue",fg="white",font=("georgia",20,"bold"))
        self.lbl_employee.place(x=250,y=120,height=150,width=275)
        
        self.lbl_supplier = Label(self.root,text="Total Supplier\n[0]",bd=5,relief=RIDGE,bg="orange",fg="white",font=("georgia",20,"bold"))
        self.lbl_supplier.place(x=600,y=120,height=150,width=275)
        
        self.lbl_category = Label(self.root,text="Total Category\n[0]",bd=5,relief=RIDGE,bg="grey",fg="white",font=("georgia",20,"bold"))
        self.lbl_category.place(x=950,y=120,height=150,width=275)
        
        self.lbl_product = Label(self.root,text="Total Product\n[0]",bd=5,relief=RIDGE,bg="green",fg="white",font=("georgia",20,"bold"))
        self.lbl_product.place(x=250,y=300,height=150,width=275)
        
        self.lbl_sales = Label(self.root,text="Total Sales\n[0]",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("georgia",20,"bold"))
        self.lbl_sales.place(x=600,y=300,height=150,width=275)
        
        
        # ----footer---- #
        lbl_footer = Label(self.root,text="Inventory Management System\nFor any Technical Issue : +917050609780",font=("georgia",12),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)
#=====================================================================================================================================================================================#

    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = employeeClass(self.new_win)

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = supplierClass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = categoryClass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = productClass(self.new_win)

if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()