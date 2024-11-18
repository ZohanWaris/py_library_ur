import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql

class lib():
    def __init__(self,root):
        self.root = root
        self.root.title("Library Management")

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")

        title = tk.Label(self.root, text="Library Management System", bd=4, relief="groove", bg="sky blue", font=("Arial",50,"bold"))
        title.pack(side="top", fill="x")

        # option Frame

        optFrame =tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(240,130,130)) 
        optFrame.place(width=self.width/3, height=self.height-180, x=70, y=100)

        addBtn = tk.Button(optFrame,command=self.regFrame, text="Register_Student", bd=2, relief="raised", width=20, font=("Arial",20,"bold"))
        addBtn.grid(row=0, column=0, padx=30, pady=40)

        allocateBtn = tk.Button(optFrame,command=self.assignFrame, text="Allocate_Book", bd=2, relief="raised", width=20, font=("Arial",20,"bold"))
        allocateBtn.grid(row=1, column=0, padx=30, pady=40)

        returnBtn = tk.Button(optFrame,command=self.retFrame, text="Return_Book", bd=2, relief="raised", width=20, font=("Arial",20,"bold"))
        returnBtn.grid(row=2, column=0,padx=30,pady=40)

        recBtn = tk.Button(optFrame,command=self.showFun, text="Show_Record", bd=2, relief="raised", width=20, font=("Arial",20,"bold"))
        recBtn.grid(row=3, column=0, padx=30, pady=40)
        # detail Frame

        self.detFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(180,130,200))
        self.detFrame.place(width=self.width/2, height=self.height-180, x=self.width/3+140, y=100)

        lbl = tk.Label(self.detFrame, text="Library Details",bd=3,relief="raised",font=("Arial",30,"bold"), bg=self.clr(200,150,220))
        lbl.pack(side="top", fill="x")
        self.tabFun()

    def tabFun(self):
        tabFrame = tk.Frame(self.detFrame, bd=4, relief="sunken",bg="cyan")
        tabFrame.place(width=self.width/2-40, height=self.height-270, x=18,y=70 )

        x_scrol = tk.Scrollbar(tabFrame, orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")

        y_scrol= tk.Scrollbar(tabFrame, orient="vertical")
        y_scrol.pack(side="right", fill="y")

        self.table = ttk.Treeview(tabFrame,xscrollcommand=x_scrol.set, yscrollcommand=y_scrol.set,
                                  columns=("roll","name","quant"))
        
        x_scrol.config(command=self.table.xview)
        y_scrol.config(command=self.table.yview)
        
        self.table.heading("roll", text="Roll_No")
        self.table.heading("name", text="Student_Name")
        self.table.heading("quant", text="Total")
        self.table["show"]= "headings"
        
        self.table.pack(fill="both", expand=1)

    def regFrame(self):
        
        self.rFrame = tk.Frame(self.root, bd=4, relief="ridge", bg=self.clr(180,220,150))
        self.rFrame.place(width=self.width/3, height=250, x=self.width/3+100, y=120)

        rollLbl = tk.Label(self.rFrame, text="Roll_No:", bg=self.clr(180,220,150), font=("arial",15,"bold"))
        rollLbl.grid(row=0, column=0, padx=20, pady=20)
        self.rollNo = tk.Entry(self.rFrame, bd=2, width=18, font=("Arial",15))
        self.rollNo.grid(row=0, column=1, padx=10, pady=20)

        nameLbl = tk.Label(self.rFrame, text="Name:", bg=self.clr(180,220,150), font=("arial",15,"bold"))
        nameLbl.grid(row=1, column=0, padx=20, pady=20)
        self.name = tk.Entry(self.rFrame, bd=2, width=18, font=("Arial",15))
        self.name.grid(row=1, column=1, padx=10, pady=20)

        okBtn = tk.Button(self.rFrame,command=self.regFun, text="Enter", width=20, bd=4, relief="raised", font=("arial",20,"bold"))
        okBtn.grid(row=3,column=0, padx=30, pady=30, columnspan=2 )

    
        
    def regFun(self):
        roll = self.rollNo.get()
        name = self.name.get()

        if roll and name:
            try:
                self.dbFun()
                self.cur.execute("insert into library (rollNo,name,quant) values(%s,%s,%s)",(roll,name,0))
                self.con.commit()
                tk.messagebox.showinfo("Success", f"Student {name} with RollNo.{roll} is registered!")
                self.desReg()

                self.cur.execute("select * from library where rollNo=%s",roll)
                row = self.cur.fetchone()

                self.tabFun()
                self.table.delete(*self.table.get_children())
                self.table.insert('',tk.END, values=row)

                self.con.close()

            except Exception as e:
                tk.messagebox.showerror("Error", f"Error: {e}")
                self.desReg()

        else:
            tk.messagebox.showerror("Error", "Please Fill All Input Fields!")

    def desReg(self):
        self.rFrame.destroy()

    def dbFun(self):
        self.con = pymysql.connect(host="localhost", user="root", passwd="admin", database="rec")
        self.cur = self.con.cursor()

    def assignFrame(self):
        self.aFrame = tk.Frame(self.root, bd=4, relief="ridge", bg=self.clr(180,220,150))
        self.aFrame.place(width=self.width/3, height=250, x=self.width/3+100, y=120)

        rollLbl = tk.Label(self.aFrame, text="Roll_No:", bg=self.clr(180,220,150), font=("arial",15,"bold"))
        rollLbl.grid(row=0, column=0, padx=20, pady=20)
        self.rollNo = tk.Entry(self.aFrame, bd=2, width=18, font=("Arial",15))
        self.rollNo.grid(row=0, column=1, padx=10, pady=20)

        bookLbl = tk.Label(self.aFrame, text="Book:", bg=self.clr(180,220,150), font=("arial",15,"bold"))
        bookLbl.grid(row=1, column=0, padx=20, pady=20)
        self.book = tk.Entry(self.aFrame, bd=2, width=18, font=("Arial",15))
        self.book.grid(row=1, column=1, padx=10, pady=20)

        okBtn = tk.Button(self.aFrame,command=self.assignFun, text="Enter", width=20, bd=4, relief="raised", font=("arial",20,"bold"))
        okBtn.grid(row=3,column=0, padx=30, pady=30, columnspan=2 )

    def desAssign(self):
        self.aFrame.destroy()

    def assignFun(self):
        roll = self.rollNo.get()
        book = self.book.get()

        if roll and book:
            try:
                self.dbFun()
                self.cur.execute("select quant from library where rollNo=%s",roll)
                row = self.cur.fetchone()
                if row:
                    upd = row[0]+1
                    self.cur.execute("update library set quant=%s where rollNo=%s",(upd,roll))
                    self.con.commit()
                    tk.messagebox.showinfo("Success", f"Book.{book} is assigned to student with rollNo.{roll}")
                    self.desAssign()

                    self.cur.execute("select * from library where rollNo=%s",roll)
                    data = self.cur.fetchone()
                    self.tabFun()
                    self.table.delete(*self.table.get_children())
                    self.table.insert('',tk.END, values=data)

                    self.con.close()


                else:
                    tk.messagebox.showerror("Error","Invalid RollNo!")
            except Exception as e:
                tk.messagebox.showerror("Error", f"Error: {e}")
                self.desAssign()
        else:
            tk.messagebox.showerror("Error", "Please Fill All Input Fields!")

    def retFrame(self):
        self.reFrame = tk.Frame(self.root, bd=4, relief="ridge", bg=self.clr(180,220,150))
        self.reFrame.place(width=self.width/3, height=250, x=self.width/3+100, y=120)

        rollLbl = tk.Label(self.reFrame, text="Roll_No:", bg=self.clr(180,220,150), font=("arial",15,"bold"))
        rollLbl.grid(row=0, column=0, padx=20, pady=20)
        self.rollNo = tk.Entry(self.reFrame, bd=2, width=18, font=("Arial",15))
        self.rollNo.grid(row=0, column=1, padx=10, pady=20)

        bookLbl = tk.Label(self.reFrame, text="Book:", bg=self.clr(180,220,150), font=("arial",15,"bold"))
        bookLbl.grid(row=1, column=0, padx=20, pady=20)
        self.book = tk.Entry(self.reFrame, bd=2, width=18, font=("Arial",15))
        self.book.grid(row=1, column=1, padx=10, pady=20)

        okBtn = tk.Button(self.reFrame,command=self.retFun, text="Enter", width=20, bd=4, relief="raised", font=("arial",20,"bold"))
        okBtn.grid(row=3,column=0, padx=30, pady=30, columnspan=2 )

    def desRet(self):
        self.reFrame.destroy()

    def retFun(self):
        roll = self.rollNo.get()
        book = self.book.get()

        if roll and book:
            try:
                self.dbFun()
                self.cur.execute("select quant from library where rollNo=%s",roll)
                row = self.cur.fetchone()
                if row:
                    upd = row[0]-1
                    self.cur.execute("update library set quant=%s where rollNo=%s",(upd,roll))
                    self.con.commit()
                    tk.messagebox.showinfo("Success", f"Book.{book} is returned from student with rollNo.{roll}")
                    self.desRet()

                    self.cur.execute("select * from library where rollNo=%s",roll)
                    data = self.cur.fetchone()

                    self.tabFun()
                    self.table.delete(*self.table.get_children())
                    self.table.insert('',tk.END, values=data)

                    self.con.close()
                else:
                    tk.messagebox.showerror("Error","Invalid RollNo!")
            except Exception as e:
                tk.messagebox.showerror("Error", f"Error: {e}")
                self.desRet()
        else:
            tk.messagebox.showerror("Error", "Please Fill All Input Fields!")

    def showFun(self):
        try:
            self.dbFun()
            self.cur.execute("Select * from library where quant > 0")
            rows = self.cur.fetchall()

            self.tabFun()
            self.table.delete(*self.table.get_children())
            for i in rows:
                self.table.insert('',tk.END,values=i)
            
            self.con.close()

        except Exception as e:
            tk.messagebox.showerror("Error", f"Error: {e}")


    def clr(self, r,g,b):
        return f"#{r:02x}{g:02x}{b:02x}"

root = tk.Tk()
obj = lib(root)
root.mainloop()