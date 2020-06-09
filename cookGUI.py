from tkinter import *
import tkinter as tk
import PIL.Image, PIL.ImageTk
import time
import cooksearch2
import cooksearch3

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, *kwargs)
        self.title('Cook me')
        self.geometry('800x600')
        
        self.grid_rowconfigure(0, weight=1) #0行目の縦の長さが1
        self.grid_columnconfigure(0, weight=1) #0列目の横の長さが1

#----------------------------------------------------------------------------------------
        #main_frame
        self.main_frame = tk.Frame()
        self.main_frame.grid(column=0, row=0, sticky='nsew')

        self.main_frame_label = tk.Label(self.main_frame, text="COOK♪ME♪♪にログイン",font=("",24), height=2,
            foreground='red') #fontの大きさを64に設定する(よく分からない)
        self.main_frame_label.pack(fill='both')

        self.main_frame_label2 = tk.Label(self.main_frame, text='user',
            font=('', 16))
        self.main_frame_label2.pack(fill='both', padx=300)

        self.main_frame_entry = tk.Entry(self.main_frame, text='', font=('', 16),
            width=20)
        self.main_frame_entry.pack(fill='both', padx=300)

        self.main_frame_label3 = tk.Label(self.main_frame, text='password',
            font=('', 16))
        self.main_frame_label3.pack(fill='both', padx=300)

        self.main_frame_entry2 = tk.Entry(self.main_frame, text='', font=('', 16),
            width=20)
        self.main_frame_entry2.pack(fill='both', padx=300)

        self.main_frame_button = tk.Button(self.main_frame, text='login', font=('Helvetica', '16'),
            background='red', command=lambda:self.change_page(self.frame1))
        self.main_frame_button.pack(fill='both', padx=300)
        

#-----------------------------------------------------------------------------------------
        #frame1
        self.frame1 = tk.Frame()
        self.frame1.grid(column=0, row=0, sticky='nsew')
        
        #frame1(cook meを表示)
        self.frame1_label = tk.Label(self.frame1, text="COOK♪ME♪♪",font=("",64), height=2,
            foreground='red') #fontの大きさを64に設定する(よく分からない)
        self.frame1_label.pack()

        #frame1(お気に入りのボタン)
        self.frame1_button = tk.Button(self.frame1, text="お気に入り", font=('Helvetica', '16'),
            background='red', command=lambda:self.change_page(self.frame3))
        self.frame1_button.pack(fill='both', padx=200, side='top')

        #frame1('材料やレシピ、調理時間を入力'を表記)
        self.frame1_label2 = tk.Label(self.frame1, text='材料を入力',
            font=("", 16), height=2)
        self.frame1_label2.pack(side='top')

        #frame1(材料名を入力するテキストボックス)
        self.frame1_entry = tk.Entry(self.frame1, text='', font=("", 16),
            width=20)
        self.frame1_entry.pack(pady=20, side='top')

        #frame1('調理時間を入力'を表記)
        self.frame1_label3 = tk.Label(self.frame1, text='調理時間を入力',
            font=("", 16), height=2)
        self.frame1_label3.pack(side='top')

        #frame1(調理時間を入力するテキストボックス)
        self.frame1_entry2 = tk.Entry(self.frame1, text='', font=("", 16),
            width=20)
        self.frame1_entry2.pack(pady=20, side='top')

        #frame1(検索ボタン)
        self.frame1_button2 = tk.Button(self.frame1, text='search', 
            font=('Helvetica', 16), foreground='red', width=20, 
            command=lambda:self.change_page(self.frame2))
        self.frame1_button2.pack(pady=20, side='top')

        #frame1(ログアウト)
        self.frame1_button3 = tk.Button(self.frame1, text='logout', 
            font=('Helvetica', 16), foreground='blue', 
            command=lambda:self.change_page(self.main_frame))
        self.frame1_button3.pack(padx=20, pady=20, side='right')

#--------------------------------------------------------------------------------------
        #frame2(食材や調理時間を検索した後のフレーム)
        self.frame2 = tk.Frame()
        self.frame2.grid(column=0, row=0, sticky='nsew')

        self.frame2_label = tk.Label(self.frame2, text='以下の検索候補から1つ選択してください',
            font=('', 20), foreground='blue')
        self.frame2_label.pack()

        self.frame2_scrollbar = tk.Scrollbar(self.frame2, orient='vertical')
        self.frame2_scrollbar.pack(fill='y', side='right')

        self.frame2_listbox = tk.Listbox(self.frame2, height=30,
            yscrollcommand=self.frame2_scrollbar.set)
        self.frame2_listbox.pack(fill='both')
        self.frame2_scrollbar.config(command=self.frame2_listbox.yview)

        self.frame2_button = tk.Button(self.frame2, text='back', 
            font=('Helvetica', 16), foreground='blue',
            command=lambda:self.FromFrame2ToFrame1(self.frame1))
        self.frame2_button.pack(side='right', padx=30)

        self.frame2_button2 = tk.Button(self.frame2, text='search', 
            font=('Helvetica', 16), foreground='red',
            command=lambda:self.change_page(self.frame4))
        self.frame2_button2.pack(side='right', padx=30)


#--------------------------------------------------------------------------------------
        #frame3(お気に入りを押した後のフレーム)
        self.frame3 = tk.Frame()
        self.frame3.grid(column=0, row=0, sticky='nsew')

        self.frame3_label = tk.Label(self.frame3, text='テストです')
        self.frame3_label.pack()

        self.frame3_button = tk.Button(self.frame3, text='back', 
            font=('Helvetica', 16), foreground='blue',
            command=lambda:self.change_page(self.frame1))
        self.frame3_button.pack()

#---------------------------------------------------------------------------------------
        #frame4:(材料や時間を出力するフレーム)
        self.frame4 = tk.Frame()
        self.frame4.grid(column=0, row=0, sticky='nsew')

        self.frame4_label = tk.Label(self.frame4, text='', font=('', 20))
        self.frame4_label.pack(fill='both', padx=100)

        self.frame4_button = tk.Button(self.frame4, text='back', 
            font=('Helvetica', 16), foreground='blue',
            command=lambda:self.change_page(self.frame2))
        self.frame4_button.pack(side='right', padx=100)

        self.frame4_button2 = tk.Button(self.frame4, text='お気に入りに登録', 
            font=('Helvetica', 16), foreground='green',
            command=lambda:self.change_page(self.frame5))
        self.frame4_button2.pack(side='right', padx=100)

#--------------------------------------------------------------------------------------
        #frame5
        self.frame5 = tk.Frame()
        self.frame5.grid(column=0, row=0, sticky='nsew')

        self.frame5_label = tk.Label(self.frame5, text='お気に入りに登録されました',
            font=("", 12))
        self.frame5_label.pack(fill='both')

#------------------------------------------------------------------------------------------

        self.main_frame.tkraise()

    def change_page(self, page):
        page.tkraise()
        if page == self.frame1:
            self.main_frame_entry.delete(0, tk.END)
            self.main_frame_entry2.delete(0, tk.END)

        if page == self.frame2:
            titleGroup = cooksearch2.selectTitle(self.frame1_entry.get())
            for searchTitle in titleGroup:
                self.frame2_listbox.insert('end', searchTitle)
            self.frame1_entry.delete(0, tk.END)

        if page == self.frame4:
            for i in self.frame2_listbox.curselection():
                print(self.frame2_listbox.get(i))
                self.frame4_label['text'] = cooksearch3.searchTitle(self.frame2_listbox.get(i))

    def FromFrame2ToFrame1(self, page):
        page.tkraise()
        self.frame2_listbox.delete(0, tk.END)


if __name__ == '__main__':
    app = App()
    app.mainloop()


