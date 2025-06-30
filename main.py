import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import db_setting as db_s
from tkinter import messagebox
import datetime


WIDTH, HEIGHT = 800, 400


class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # ---- Var
        self.x = ((self.winfo_screenwidth() // 2) - (WIDTH // 2))
        self.y = ((self.winfo_screenheight() // 2) - (HEIGHT // 2)) - 20

        # ---- setting
        self.title('مدیریت کتابخانه')
        self.geometry(f'{WIDTH}x{HEIGHT}+{self.x}+{self.y}')
        self.resizable(False, False)

        # ----- wi
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab_members()
        self.tab_books()
        self.tab_borrowings()
        self.tab_back_book()

    def tab_members(self):
        
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='افزودن عضو')

        frame_1 = ttk.Frame(tab)
        frame_1.grid(row=0, column=0)

        ttk.Label(frame_1, text='نام و نام خانوادگی:').grid(row=0, column=0, padx=10, pady=(50, 10))
        self.member_name = ttk.Entry(frame_1, width=30)
        self.member_name.grid(row=0, column=1, padx=10, pady=(50, 10))

        ttk.Label(frame_1, text='ایمیل:').grid(row=1, column=0, padx=10, pady=10)
        self.member_email = ttk.Entry(frame_1, width=30)
        self.member_email.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(frame_1, text='شماره همراه:').grid(row=2, column=0, padx=10, pady=10)
        self.member_phone = ttk.Entry(frame_1, width=30)
        self.member_phone.grid(row=2, column=1, padx=10, pady=10)

        ttk.Button(frame_1, text='افزودن عضو', width=45, command=self.add_member).grid(row=3, column=0, columnspan=2)
        ttk.Button(frame_1, text='حذف عضو', width=45, command=self.delete_members).grid(row=4, column=0, columnspan=2, pady=5)

        # -------- Table
        frame_2 = ttk.Frame(tab)
        frame_2.grid(row=0, column=1)

        scrollbar = tk.Scrollbar(frame_2)

        columns_ = ['آیدی', 'نام', 'ایمیل', 'شماره']
        self.table_1 = ttk.Treeview(frame_2, columns=columns_, show='headings', height=15, yscrollcommand=scrollbar.set)
        self.table_1.pack(fill=tk.Y, side=tk.LEFT, padx=10, pady=(20, 10))
        scrollbar.config(command=self.table_1.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(20, 10))
        self.show_member_table()
        

        for column in columns_:
            if column == 'آیدی':
                self.table_1.column(column, width=70, anchor='center')
                self.table_1.heading(column, text=column, anchor='center')
            else:
                self.table_1.column(column, width=120, anchor='center')
                self.table_1.heading(column, text=column, anchor='center')

    def tab_books(self):

        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='افزودن کتاب')

        frame_1 = ttk.Frame(tab)
        frame_1.grid(row=0, column=0)

        ttk.Label(frame_1, text='عنوان کتاب:').grid(row=0, column=0, padx=10, pady=(50, 10))
        self.title_book = ttk.Entry(frame_1, width=30)
        self.title_book.grid(row=0, column=1, padx=10, pady=(50, 10))

        ttk.Label(frame_1, text='نویسنده:').grid(row=1, column=0, padx=10, pady=10)
        self.author_book = ttk.Entry(frame_1, width=30)
        self.author_book.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(frame_1, text='شناسه کتاب:').grid(row=2, column=0, padx=10, pady=10)
        self.isbn_book = ttk.Entry(frame_1, width=30)
        self.isbn_book.grid(row=2, column=1, padx=10, pady=10)

        ttk.Button(frame_1, text='افزودن کتاب', width=45, command=self.add_book).grid(row=3, column=0, columnspan=2)
        ttk.Button(frame_1, text='حذف کتاب', width=45, command=self.delete_books).grid(row=4, column=0, columnspan=2, pady=5)

        # -------- Table
        frame_2 = ttk.Frame(tab)
        frame_2.grid(row=0, column=1)

        scrollbar = tk.Scrollbar(frame_2)

        columns_ = ['آیدی', 'عنوان کتاب', 'نویسنده', 'شناسه کتاب', 'وضعیت']
        self.table_2 = ttk.Treeview(frame_2, columns=columns_, show='headings', height=15, yscrollcommand=scrollbar.set)
        self.table_2.pack(fill=tk.Y, side=tk.LEFT, padx=10, pady=(20, 10))
        scrollbar.config(command=self.table_2.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(20, 10))
        
        self.show_book_table()

        for column in columns_:
            if column == 'آیدی':
                self.table_2.column(column, width=50, anchor='center')
                self.table_2.heading(column, text=column, anchor='center')
            else:
                self.table_2.column(column, width=100, anchor='center')
                self.table_2.heading(column, text=column, anchor='center')
        
    def tab_borrowings(self):

        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='بخش امانت')

        frame_1 = ttk.Frame(tab)
        frame_1.grid(row=0, column=0)

        members, books = db_s.show_member_nam_book_name()

        ttk.Label(frame_1, text='نام عضو:').grid(row=0, column=0, padx=10, pady=(50, 10))
        self.member_name_borrow = ttk.Combobox(frame_1, width=30, values=members)
        self.member_name_borrow.grid(row=0, column=1, padx=10, pady=(50, 10))

        ttk.Label(frame_1, text='نام کتاب:').grid(row=1, column=0, padx=10, pady=10)
        self.title_book_borrow = ttk.Combobox(frame_1, width=30, values=books)
        self.title_book_borrow.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(frame_1, text='تاریخ امانت:').grid(row=2, column=0, padx=10, pady=10)
        self.borrow_date = DateEntry(frame_1, width=30, date_pattern='y-mm-dd')
        self.borrow_date.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(frame_1, text='تاریخ برگشت:').grid(row=3, column=0, padx=10, pady=10)
        self.return_date = DateEntry(frame_1, width=30, date_pattern='y-mm-dd')
        self.return_date.grid(row=3, column=1, padx=10, pady=10)

        ttk.Button(frame_1, text='افزودن امانت', width=45, command=self.add_borrowings).grid(row=4, column=0, columnspan=2)
        ttk.Button(frame_1, text='حذف امانت', width=45, command=self.delete_borrow_table).grid(row=5, column=0, columnspan=2, pady=5)

        # -------- Table
        frame_2 = ttk.Frame(tab)
        frame_2.grid(row=0, column=1)

        scrollbar = tk.Scrollbar(frame_2)

        columns_ = ['آیدی', 'عضو', 'کتاب', 'تاریخ امانت', 'تاریخ برگشت']
        self.table_3 = ttk.Treeview(frame_2, columns=columns_, show='headings', height=15, yscrollcommand=scrollbar.set)
        self.table_3.pack(fill=tk.Y, side=tk.LEFT, padx=10, pady=(20, 10))
        scrollbar.config(command=self.table_3.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(20, 10))
        

        for column in columns_:
            if column == 'آیدی':
                self.table_3.column(column, width=50, anchor='center')
                self.table_3.heading(column, text=column, anchor='center')
            else:
                self.table_3.column(column, width=100, anchor='center')
                self.table_3.heading(column, text=column, anchor='center')
        
        self.show_borrow_table()

    def tab_back_book(self):

        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='برگشت کتاب')

        # -------- Table
        frame_2 = ttk.Frame(tab)
        frame_2.pack(padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame_2)

        columns_ = ['آیدی', 'عضو', 'کتاب', 'تاریخ امانت', 'تاریخ برگشت']
        self.table_4 = ttk.Treeview(frame_2, columns=columns_, show='headings', height=12, yscrollcommand=scrollbar.set)
        self.table_4.pack(fill=tk.Y, side=tk.LEFT, padx=10, pady=(20, 10))
        scrollbar.config(command=self.table_4.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(20, 10))
        

        for column in columns_:
            if column == 'آیدی':
                self.table_4.column(column, width=50, anchor='center')
                self.table_4.heading(column, text=column, anchor='center')
            else:
                self.table_4.column(column, width=100, anchor='center')
                self.table_4.heading(column, text=column, anchor='center')
        
        self.show_back_book_table()
        ttk.Button(tab, text='برگشت امانت', width=45, command=self.back_book_).pack(padx=10, pady=10)

    # ---------------------- database settings
    # -------- Tab Members
    def add_member(self):
        name, email, phone = self.member_name.get(), self.member_email.get(), self.member_phone.get()
        if name != '' and email != '' and phone != '':
            db_s.add_members(name, email, phone)
            messagebox.showinfo('Success', 'عضو اضافه شد')
            self.member_name.delete(0, tk.END)
            self.member_email.delete(0, tk.END)
            self.member_phone.delete(0, tk.END)
            self.show_member_table()

        else:
            messagebox.showerror('Error', 'لطفا موارد خواسته شده را وارد کنید')
    
    def show_member_table(self):
        self.table_1.delete(*self.table_1.get_children())
        items = db_s.show_members_for_table()
        for item in items:
            self.table_1.insert('', tk.END, values=item)
    
    def delete_members(self):
        selection_ = self.table_1.selection()
        if selection_:
            ques = messagebox.askyesno('Ques', 'از حذف این مورد مطمئنی؟')
            if ques:
                id_member_ = self.table_1.item(selection_)['values'][0]
                db_s.delete_members(id_member_)
                self.show_member_table()
    
    # -------- Tab Books
    def add_book(self):
        title, author, isbn = self.title_book.get(), self.author_book.get(), self.isbn_book.get()
        if title != '' and author != '' and isbn != '':
            db_s.add_books(title, author, isbn)
            messagebox.showinfo('Success', 'کتاب اضافه شد')
            self.title_book.delete(0, tk.END)
            self.author_book.delete(0, tk.END)
            self.isbn_book.delete(0, tk.END)
            self.show_book_table()

        else:
            messagebox.showerror('Error', 'لطفا موارد خواسته شده را وارد کنید')
    
    def show_book_table(self):
        self.table_2.delete(*self.table_2.get_children())
        items = db_s.show_books_for_table()
        for item in items:
            item = list(item)
            if item[-1]:
                item[-1] = 'قابل دسترسی'
            else:
                item[-1] = 'غیرقابل دسترسی'
            self.table_2.insert('', tk.END, values=item)
    
    def delete_books(self):
        selection_ = self.table_2.selection()
        if selection_:
            ques = messagebox.askyesno('Ques', 'از حذف این مورد مطمئنی؟')
            if ques:
                id_book_ = self.table_2.item(selection_)['values'][0]
                db_s.delete_books(id_book_)
                self.show_book_table()

    # ----------- Tab Borrow
    def add_borrowings(self):
        id_member = self.member_name_borrow.get().split('.')[0]
        id_book = self.title_book_borrow.get().split('.')[0]
        borrow_date = self.borrow_date.get_date()
        return_date = self.return_date.get_date()

        if id_member != '' and id_book != '':
            count_date = datetime.datetime(return_date.year, return_date.month, return_date.day)-datetime.datetime(borrow_date.year, borrow_date.month, borrow_date.day)
            if count_date.days >= 1:
                result = db_s.add_borrow(id_member, id_book, borrow_date, return_date)
                if result[0]:
                    messagebox.showinfo("seccuessfully", result[1])
                    self.show_borrow_table()
                    self.show_book_table()
                    self.show_back_book_table()
                else:
                    messagebox.showerror('Error', result[1])
            else:
                messagebox.showerror('Error', 'تعداد روز امانت باید بیشتر از یک روز باشد')
        else:
            messagebox.showerror('Error', 'لطفا تمام موارد را وارد کنید')
    
    def show_borrow_table(self):
        self.table_3.delete(*self.table_3.get_children())
        items = db_s.show_borrow_for_table()
        for item in items:
            self.table_3.insert('', tk.END, values=item)
    
    def delete_borrow_table(self):
        selection_ = self.table_3.selection()
        if selection_:
            ques = messagebox.askyesno('Ques', 'از حذف این مورد مطمئنی؟')
            if ques:
                borrow_id = self.table_3.item(selection_)['values'][0]
                db_s.delete_borrow_(borrow_id)
                messagebox.showinfo('Successfully', 'امانت با موفقیت حذف شد')
                self.show_borrow_table()
                self.show_book_table()
                self.show_back_book_table()
    
    # ---------------- Tab Back Book
    def show_back_book_table(self):
        self.table_4.delete(*self.table_4.get_children())
        items = db_s.show_borrow_for_table()
        for item in items:
            self.table_4.insert('', tk.END, values=item)
    
    def back_book_(self):
        selection_ = self.table_4.selection()
        if selection_:
            ques = messagebox.askyesno('Ques', 'از برگشت این کتاب مطمئنی؟')
            if ques:
                borrow_id = self.table_4.item(selection_)['values'][0]
                db_s.delete_borrow_(borrow_id)
                messagebox.showinfo('Successfully', 'امانت با موفقیت برگشت داده شد')
                self.show_borrow_table()
                self.show_book_table()
                self.show_back_book_table()


if __name__ == '__main__':
    app = LibraryApp()
    app.mainloop()