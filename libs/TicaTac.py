'''
@name: tic tac toe with dynamic matrix, task completed for Luka Giorgobiani
@file: responsible for tictoc game logic
@AUTHOR: DATO BARBAKADZE
@IDEA: MARINE DATA SCRAPER - SHIPS
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
from threading import Thread

class TicTacLogic:

    def __init__(self):
        self.graph_length = 3
        self.graph = [[None for i in range(self.graph_length)] for j in range(self.graph_length)]
        self.tik_val = 1
        self.tok_val = 0
        self.draw_val = 2

        self.mainWinner = None

        self.direction_h = 0
        self.direction_v = 1
        self.direction_dy_l = 2
        self.direction_dy_r = 3

        self.thread_list = list()

        self.tok_win_count = 0
        self.tik_win_count = 0
        self.move_count = 0

        self.turn = self.tik_val
    def clear_graph(self):
        self.graph = [[None for i in range(self.graph_length)] for j in range(self.graph_length)]
        for i in range(self.graph_length):
            for j in range(self.graph_length):
                self.graph[i][j] = None
        self.turn = self.tik_val



    def increase_win_count(self,side):
        if side == self.tik_val:
            self.tik_win_count+=1
        elif side == self.tok_val:
            self.tok_win_count+=1

    def coordinates(self,number):
        coord_difiner = 0
        for y in range(self.graph_length):
            for x in range(self.graph_length):
                if number == coord_difiner:
                    return y,x
                elif number>=(self.graph_length*self.graph_length):
                    return None
                else:
                    coord_difiner+=1

    def fill(self,y,x,val):
        if self.graph[y][x] != None:
            return False
        self.graph[y][x] = val
        return True

    # TODO merge tik and tok functions
    def tic_tac(self,position):
        try:
            position = int(position)
        except:
            return False
        coordinates = self.coordinates(position)
        if coordinates ==None:
            return False
        y, x = coordinates
        if self.turn==1:
            if self.fill(y, x, self.tik_val) == False:
                return False
            self.turn = self.tok_val
        elif self.turn==0:
            if self.fill(y, x, self.tok_val) == False:
                return False
            self.turn = self.tik_val
        else:
            return False
        self.move_count+=1
        if self.move_count >=(self.graph_length+(self.graph_length-1)):
            self.run_check()
        # self.print_matrix()
    def check(self,axis=None,direction=None):
        '''
        function for checking the winner
        :param axis: static value for y or x axis
        :param direction: 0 = horizontal, 1 = vertical, 2 = dyagonal_left, 3 = dyagonal_right
        :return:
        '''
        winner = None;
        for i in range(self.graph_length):
            if direction==self.direction_h:
                el = self.graph[axis][i]
            elif direction==self.direction_v:
                el = self.graph[i][axis]
            elif direction==self.direction_dy_l:
                el = self.graph[i][i]
            elif direction==self.direction_dy_r:
                el = self.graph[i][(self.graph_length-1)-i]
            if el != None:
                if i != 0:
                    if el != winner:
                        winner = None
                        break
                else:
                    winner = el
            else:
                winner = None
                break

        return winner

    def check_x_axis(self):
        for y in range(self.graph_length):
            winner = self.check(y,self.direction_h)
            if winner != None:
                return winner
            else:
                continue
        return None

    def check_y_axis(self):
        for x in range(self.graph_length):
            winner = self.check(x,self.direction_v)
            if winner != None:
                return winner
            else:
                continue
        return None

    def check_dyagonal_left(self):

        winner = self.check(None, self.direction_dy_l)

        if winner != None:
            return winner
        else:
            return None

    def check_dyagonal_right(self):
        winner = self.check(None, self.direction_dy_r)
        if winner != None:
            return winner
        else:
            return None

    def run_check(self):
        x_check = self.check_x_axis()
        if x_check != None:
            self.mainWinner = x_check

        y_check = self.check_y_axis()
        if y_check != None:
            self.mainWinner = y_check

        dy_l_check = self.check_dyagonal_left()
        if dy_l_check != None:
            self.mainWinner = dy_l_check

        dy_r_check = self.check_dyagonal_right()
        if dy_r_check != None:
            self.mainWinner = dy_r_check

        if self.graph_fill_check() == True:
            self.mainWinner = self.draw_val

    def graph_fill_check(self):
        for y in range(self.graph_length):
            for x in range(self.graph_length):
                if self.graph[y][x] == None:
                    return False
        return True









if __name__ == "__main__":
    print("run program from gui side")
