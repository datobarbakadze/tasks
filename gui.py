'''
@name: tic tac toe with dynamic matrix, task completed for Luka Giorgobiani
@file: responsible for tictoc game gui
@AUTHOR: DATO BARBAKADZE
@begin date/time: Saturday August 22, year 2020 / 8.36pm
  ██████  ▒█████   ██▀███   ▄████▄  ▓█████  ██▀███  ▓█████  ██▀███
▒██    ▒ ▒██▒  ██▒▓██ ▒ ██▒▒██▀ ▀█  ▓█   ▀ ▓██ ▒ ██▒▓█   ▀ ▓██ ▒ ██▒
░ ▓██▄   ▒██░  ██▒▓██ ░▄█ ▒▒▓█    ▄ ▒███   ▓██ ░▄█ ▒▒███   ▓██ ░▄█ ▒
  ▒   ██▒▒██   ██░▒██▀▀█▄  ▒▓▓▄ ▄██▒▒▓█  ▄ ▒██▀▀█▄  ▒▓█  ▄ ▒██▀▀█▄
▒██████▒▒░ ████▓▒░░██▓ ▒██▒▒ ▓███▀ ░░▒████▒░██▓ ▒██▒░▒████▒░██▓ ▒██▒
▒ ▒▓▒ ▒ ░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░░ ░▒ ▒  ░░░ ▒░ ░░ ▒▓ ░▒▓░░░ ▒░ ░░ ▒▓ ░▒▓░
░ ░▒  ░ ░  ░ ▒ ▒░   ░▒ ░ ▒░  ░  ▒    ░ ░  ░  ░▒ ░ ▒░ ░ ░  ░  ░▒ ░ ▒░
░  ░  ░  ░ ░ ░ ▒    ░░   ░ ░           ░     ░░   ░    ░     ░░   ░
      ░      ░ ░     ░     ░ ░         ░  ░   ░        ░  ░   ░
                           ░
'''

from tkinter import *
from tkinter import ttk
from libs.TicaTac import TicTacLogic as Logic
class TicTacGui(Logic):
    def __init__(self):
        self.main_bg = '#002c38'
        self.danger_color = '#990632'
        self.active_color = '#0099e6'
        super().__init__()
        windowWidth = 350
        windowHeight = 540
        self.button_list = list()
        self.border_list = list()
        self.root = Tk()  # main tkinter object
        # self.root.geometry(str(windowWidth) + 'x' + str(windowHeight))
        self.root.configure(bg=self.main_bg)
        self.root.resizable(False, False)
        self.root.title("Tic Tac Toe");
        self.root.iconbitmap(r'./images/tic.ico');

    def win(self):
        '''
        ფუნქცია პასუხისმგებელია გაუშვას ყველა საჭირო ფუნქცია, გამარჯვების ან ნიჩიის შემთხვევაშ
        '''
        if self.mainWinner == self.draw_val:
            self.win_message(self.mainWinner)

        if self.mainWinner == self.tik_val:
            self.win_message(self.mainWinner)
            self.increase_win_count(self.mainWinner)
        if self.mainWinner == self.tok_val:
            self.win_message(self.mainWinner)
            self.increase_win_count(self.mainWinner)
        self.mainWinner = None # გამარჯვებულის მნიშვნელობის საწყის პოზიციაში დაბრუნება
        self.graph_state(DISABLED) # მატრიცის ღილაკების გათიშვა, რესტარტამდე

    def win_message(self,side):
        '''
        ქმნის და აჩვენებს შეტყობინებას იმის შესახებ თუ ვინ გაიმარჯვა

        :param side: განსაზღვრავს გამარჯვებულის მხარეს
        '''
        if side == self.tik_val:
            self.gen_win_msg("Tic Won")
        elif side == self.tok_val:
            self.gen_win_msg("Tac Won")
        elif side == self.draw_val:
            self.gen_win_msg("Draw")

    def gen_win_msg(self,Msg):
        '''
        ქმნის label widget-ს რომელზეც წერია გამარჯვებულის მესიჯი

        :param Msg: მესიჯი რომელიც Label-ზე უნდა გამოჩნდეს
        :return:
        '''
        self.win_msg_label = Label(self.root,text=str(Msg),bg=self.danger_color, fg='white', font='Arial 15 bold',justify=CENTER,pady=10)
        self.win_msg_label.grid(row=(self.graph_length*self.graph_length)+6,sticky="we",columnspan=self.graph_length,ipady=10)

    def destroy_win_msg(self):
        '''
        ანადგურებს მესიჯს რომელიც გამარჯვების ან ნიჩიის შემთხვევაში გამოჩჰნდა,
        ძირითადად ამ ფუნქციას იძახებს რესტარტ ფუნქცია
        '''
        try:
            self.win_msg_label.destroy()
        except:
            pass

    def button_click(self,position):
        '''
        მნიშვნელობის ჩასაწერ ღილაკზე დაჭერა, ეს ღილაკებია ის კვადრატები რომელიც ჩანს ფანჯარაზე

        :param position: რომელ პოზიციაზე დააჭირა მოთამაშემ
        '''
        self.tic_tac(position)
        if self.turn == 0: # it should be compared to zero cause after tic or toc turn variable is changed
            self.button_list[position].configure({"text":"X"})
        if self.turn == 1:
            self.button_list[position].configure({"text": "O"})
        if self.mainWinner != None:
            self.win()
            self.update_wincount_label()

    def restart(self):
        '''
        ფუნქცია არესტარტებს თამაშს
        '''
        self.clear_graph()
        self.graph_state(NORMAL)
        self.destroy_win_msg()

        print(self.graph_length_entry.get())

    def graph_state(self,state):
        '''
        ფუნქცია აუქმებს კვადრატულ ღილაკებზე დაჭერის უფლებას ან პირიქით
        :param state: განსაძღვრავს ღილაკთა მდგომარეობს NORMAL ან DISABLED
        '''
        for btn in self.button_list:
            btn.configure(state=state)
            if state == NORMAL:
                btn.configure(text=' ')

    def update_wincount_label(self):
        '''
        ფუნქცია ანახლებს გამარჯვების მთვლელ მესიჯს, რომელიც ჩანს რესტარტ ღილაკის დაბლა
        '''
        try:
            self.wincountlabel.destroy()
        except:
            pass
        msg = "X: "+str(self.tik_win_count)+"       O: "+str(self.tok_win_count)
        self.wincountlabel = Label(self.root,text=str(msg),bg=self.main_bg, fg='white', font='Arial 11 bold',justify=CENTER)
        self.wincountlabel.grid(row=(self.graph_length*self.graph_length)+3,columnspan=self.graph_length)

    def reinitiate(self):
        '''
        ფუნქცია ანადგურებს მთელ ფანჯარას და ქმნის თავიდან,
        გამოიყენება იმ შემთხვევაში თუ იუზერი მოინდომებს მატრიცის ფართობის გაზრდას
        '''
        try:
            new_graph_length = self.graph_length_entry.get()
            self.graph_length = int(new_graph_length)
            self.clear_graph()
            for btn in self.button_list:
                btn.destroy()
            for br in self.border_list:
                br.destroy()
            self.button_list = list()
            self.border_list = list()
            self.restart_btn.destroy()
            self.tik_win_count = 0
            self.tok_win_count = 0
            try:
                self.wincountlabel.destroy()
            except:
                pass
            self.graph_length_entry.destroy()
            self.btn_reinitiate.destroy()

            self.create_elements()
            self.init_elements()

        except:
            pass

    def create_elements(self):
        '''
        ფუნქცია ქმნის 90% ელემენტებისას ანუ ვიჯეტებისას ანუ ობიექტებისას
        '''
        for i in range(self.graph_length*self.graph_length):
            Border = LabelFrame(self.root,bd=1, bg="#05f7eb", relief=FLAT)
            btn = Button(Border, activebackground=self.active_color,bd=0, text=' ', font='Arial 20 bold', bg=self.main_bg, fg='white', height=2,disabledforeground='white', width=6,command=lambda pos=i: self.button_click(pos))
            btn.pack()
            self.border_list.append(Border)
            self.button_list.append(btn)
        self.restart_btn = Button(self.root, padx=50, text='Restart', font='Arial 20 bold', bg='#207561', fg='white', height=1, width=8, command=lambda: self.restart())
        self.graph_length_entry = Entry(self.root,bg='white',width=30,justify=CENTER)
        self.btn_reinitiate = btn = Button(self.root, activebackground=self.active_color,bd=0, text='Change graph', font='Arial 15 bold', bg=self.danger_color, fg='white', height=2,disabledforeground='white', width=15,command=lambda: self.reinitiate())
        # self.wincount_lable = Label

    def init_elements(self):
        '''
        ფუნქცია აკეთებს ზემოთ შექმნილი ელემენტების ინიციალიზაციას ანუ გამოსახავს მათ მთავარ ფანჯარაში

        '''
        self.update_wincount_label()
        row_index=1
        column = 0
        for border in self.border_list:
            if column % self.graph_length ==0:
                row_index+=1
                column=0
            border.grid(row=row_index,column=column)
            column+=1
        self.restart_btn.grid(row=(self.graph_length*self.graph_length)+2,column=0,columnspan=self.graph_length,pady=7)
        self.graph_length_entry.grid(row=(self.graph_length*self.graph_length)+4,column=0,columnspan=self.graph_length,pady=5)
        self.btn_reinitiate.grid(row=(self.graph_length*self.graph_length)+5,column=0,columnspan=self.graph_length,pady=5)

    def run(self):
        '''
        აპლიკაციის გამშვები ფუნქცია
        '''
        self.create_elements()
        self.init_elements()
        self.root.mainloop()
        # print(self.print_matrix())

if __name__ == "__main__":
    tictacgui = TicTacGui()
    tictacgui.run()
