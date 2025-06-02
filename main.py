from tkinter import *
import tkinter as tk
from tkinter import ttk
import datetime
import requests
from tkinter import ttk
from tkinter import messagebox 


    
# curacy exchange fun
def currencyExchange():
    key = "fe94a9d8d9f92496f0660552d937a670"
    url = "http://data.fixer.io/api/latest"
    user_curr =curr_box.get()
    params = {
        "access_key": key,
        "symbols":f"{user_curr},USD"
    }


    response = requests.get(url, params=params)
    data = response.json()
    print(data)
    # amount with dollar 
    if amo_var.get():
        amo_d=float(amo_var.get()) 
        amount_EUR=amo_d * (1 /data["rates"][user_curr])
        amount_USD=amount_EUR*data["rates"]["USD"]
        print(amo_d)
        print(amount_EUR)
        print(amount_USD)
        rounded = round(amount_USD, 2)
        return  rounded
    else:
        return 0
    




# date
x = datetime.datetime.now()

root=tk.Tk()
# setting the windows size
root.geometry("600x500")
root.title("Expense Tracker")

style = ttk.Style(root)


# font
normal_font =('Arial', 10) 


# declaring string variable
# for storing name and password
frame = Frame(root,width=400,height=100)
curr_box = ttk.Combobox(frame, values=["EGP", "EUR", "KWD","USD"],font=normal_font,width=20)
cat_box = ttk.Combobox(frame, values=["Life Expenses","Electricity","Gas","Rental","Grocery","Savings","Education","Charity"],font=normal_font,width=20)
pay_meth_box= ttk.Combobox(frame, values=["Cash","Credit Card","Paypal"],font=normal_font,width=20)

curr_box.set("EGP")
cat_box.set("life expenses")
pay_meth_box.set("Cash")

user_list=[]
amo_var=tk.StringVar()
dat_var=tk.StringVar()
total_arr=[]
total_row_id = None  # Declare at the top






def total():
    global total_row_id
    treev.tag_configure("total", background="#f0f0f0", foreground="blue", font=('Arial', 10, 'bold'))
    c=sum(total_arr)
    # Update the existing row's values
    total_row_id = treev.insert("",'end', values=(f"{c} USD"), tags=("total",))
# defining a function that will submit
def submit():
    
    amo=amo_var.get()
    curr=curr_box.get()
    cat=cat_box.get()
    pay=pay_meth_box.get()
    try:
        ce=currencyExchange()
    except ValueError:
        messagebox.showerror("showerror", "Insert a Valid Number") 
    total_arr.append(ce)
    col1=(amo,curr,cat,pay)
    user_list.append(col1)
    print(user_list)
    amo_var.set("")
    dat_var.set("")
    userListFrame()


amo_label = tk.Label(frame, text = 'Amount    ', font=normal_font,width=30)
amo_entry = tk.Entry(frame,textvariable=amo_var, font=normal_font)
curr_label = tk.Label(frame, text = 'Currency   ', font = normal_font)



# Bind event to selection
cat_label = tk.Label(frame, text = 'Category    ' ,font = normal_font)
pay_meth_label = tk.Label(frame, text = 'Pay Method   ', font =normal_font)


dat_label = tk.Label(frame, text ='Date', font =normal_font)
dat_entry = tk.Label(frame, text =x.strftime("%Y-%m-%d"),font =('Arial', 10,"bold"))


# creating a button using the widget 
# Button that will call the submit function 
sub_btn=tk.Button(frame,text = 'Add Expense', command = submit,font=normal_font)

# placing the label and entry in
# the required position using grid
# method

amo_label.grid(row=0,column=0)
amo_entry.grid(row=0,column=8,pady=5)
curr_label.grid(row=1,column=0)
curr_box.grid(row=1,column=8,pady=5)
cat_label.grid(row=2,column=0,pady=5)
cat_box.grid(row=2,column=8)
pay_meth_label.grid(row=3,column=0,pady=5)
pay_meth_box.grid(row=3,column=8,pady=5)
dat_label.grid(row=4,column=0)
dat_entry.grid(row=4,column=8,pady=5)

sub_btn.grid(row=5,column=8)
frame.grid(row=0,column=0,columnspan=6,pady=5,padx=5)


treev = ttk.Treeview(root, selectmode ='browse')
style.configure("Treeview", 
                    background="lightgrey",
                    foreground="black",
                    font=("Arial", 10),
                    rowheight=25,
                    fieldbackground="white")



# Calling pack method w.r.to treeview
treev.grid(row=6,column=0,columnspan=6,pady=5,padx=5)

# Defining number of columns
treev["columns"] = ("1","2","3","4")

# Defining heading
treev['show'] = 'headings'

# Assigning the width and anchor to  the
# respective columns
treev.column("1", width = 138, anchor ='c')
treev.column("2", width =138, anchor ='c')
treev.column("3", width = 138, anchor ='c')
treev.column("4", width = 138, anchor ='c')


# Assigning the heading names to the 
# respective columns
treev.heading("1",text ="Amount")
treev.heading("2", text ="Currency")
treev.heading("3", text ="Category")
treev.heading("4", text ="Payment Method")

style.configure("Treeview.Heading", 
                    foreground="black",
                    font=("Arial",10, "bold"),
                    relief="flat")



def userListFrame():
    # global total_row_id
    if total_row_id is not None:
        treev.delete(total_row_id)
    treev.insert("",'end', text ="L1", 
            values =(user_list[len(user_list)-1]))
    total()


# performing an infinite loop 
# for the window to display
root.mainloop()









