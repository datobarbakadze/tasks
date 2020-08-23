'''
@name: tic tac toe with dynamic matrix, task completed for Luka Giorgobiani
@file: responsible for tictoc game logic
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
from threading import Thread

class TicTacLogic:

    def __init__(self):
        self.graph_length = 3
        self.graph = [[None for i in range(self.graph_length)] for j in range(self.graph_length)]  #create empty matrix
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
        '''
            ფუნქცია ასუბთავებს მატრიცას როცა ამის საჭიროება ხდება.
            მაგ: მოგების ან რესტარტის შემთხვევაში
        '''
        self.graph = [[None for i in range(self.graph_length)] for j in range(self.graph_length)]
        for i in range(self.graph_length):
            for j in range(self.graph_length):
                self.graph[i][j] = None
        self.turn = self.tik_val
        self.thread_list = list()

    def increase_win_count(self,side):
        '''
        ფუნქცია ზრდის ქულას მომგები მხარისას, იქნება ეს X(tic) თუ O(tac)

        :param side: ეს პარამეტრი განსაზღვრავს თუ რომელ მხარეს უნდა გაიზარდოს ქულა,
        მნიშვნელობა აუცილებლად უნდა უდრიდეს ან 1(X)-ს ან 0(O)-ს
        :return:
        '''
        if side == self.tik_val:
            self.tik_win_count+=1
        elif side == self.tok_val:
            self.tok_win_count+=1

    def coordinates(self,number):
        '''
        ფუნქციას გადმოეცემა რიცხვითი მნიშვნელობა რომელიც განსაზღვრავს მატრიცაში მნიშვნელობის მერამდენეობას.
        მაგ: 0 შეესაბამება [0,0], 1 - [0,1] და ა.შ

        :param number: რიცხვი რომელიც განსაზღვრავს თუ რომელი მატრიცის კოორდინატი უნდა დააბრუნოს ფუნქციამ

        '''
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
        '''
        ფუნქცია ანიჭებს val მნიშვნელობას მატრიცაში არსებულ სივრცეს კონკრეტულ კოორდინატებზე,
        ასევე ამოწმებს აქვს თუ არა ამ სივრცეს მნიშვნელობა მინიჭებული.

        :param y: ორდინატა (მატრიცის პირველი განზომილება)
        :param x: აბსცისა (მატრიცის მეორე განზომილება)
        :param val: მნიშვნელობა რომელიც უნდა იყოს ან 1 ან 0, შესაბამისად X-ისა და O-სა
        :rtype: bool
        '''
        if self.graph[y][x] != None:
            return False
        self.graph[y][x] = val
        return True

    # TODO merge tik and tok functions
    def tic_tac(self,position):
        '''
        მთავარი ფუნქცია რომელიც გამოიძახება მაშინ როცა ეჭირება ღილაკს X-ის ან O-ს ჩასაწერად

        :param position: რიცხვითი მნიშვნელობა რომელიც განსაზღვრას  coordinates ფუნქციის დახმარებით
        თუ რომელ ადგილას უნდა ჩაისვას მნიშვნელობა მატრიცაში
        '''
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

    def check(self,axis=None,direction=None):
        '''
        ფუნქცია რომელიც ამოწმებს დაფიქსირდა თუ არა მოგებული
        ეს ფუნქცია დამოკიდებულია ქვემოტ მოცემულ ოთხი ფუნქციაზე check_x_axis, check_y_axis, check_dyagonal_left, check_dyagonal_right

        :param axis: სტატიკური მნიშვნელობა რომელიც ასრულებს ხან x კოორდინატის როლს ხან კიდევ y isas
        :param direction: 0 = horizontal, 1 = vertical, 2 = dyagonal_left, 3 = dyagonal_right
        :return:winner | None
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
        '''
        ფუნქცია რომელიცა ამოწმებს ჰორიზონტალურ გამარჯვებას check ფუნქციის დახმარებით
        '''
        for y in range(self.graph_length):
            winner = self.check(y,self.direction_h)
            if winner != None:
                self.mainWinner = winner
            else:
                continue
        return None

    def check_y_axis(self):
        '''
        ფუნქცია რომელიცა ამოწმებს ვერტიკალურ გამარჯვებას check ფუნქციის დახმარებით
        '''
        for x in range(self.graph_length):
            winner = self.check(x,self.direction_v)
            if winner != None:
                self.mainWinner = winner
            else:
                continue
        return None

    def check_dyagonal_left(self):
        '''
        ფუნქცია რომელიცა ამოწმებს დიაგონალურ გამარჯვებას check ფუნქციის დახმარებით,
        ეს დიაგონალი იწყება კოორდინატიდან [0,0]
        '''
        winner = self.check(None, self.direction_dy_l)

        if winner != None:
            self.mainWinner = winner
        else:
            return None

    def check_dyagonal_right(self):
        '''
        ფუნქცია რომელიცა ამოწმებს დიაგონალურ გამარჯვებას check ფუნქციის დახმარებით,
        ეს დიაგონალი იწყება კოორდინატიდან [0,last_y]
        '''
        winner = self.check(None, self.direction_dy_r)
        if winner != None:
            self.mainWinner = winner
        else:
            return None

    def run_check(self):
        '''
        ფუნქცია უშვებს ყველა გამარჯვების შემამოწმებელ ფუნქციას, multi-threaded გარემოში,
        ასევე ყველა სრედის დამთავრების შემდეგ ამოწმებს ნიჩიას
        '''
        x_check = Thread(target=self.check_x_axis())
        self.thread_list.append(x_check)

        y_check = Thread(target=self.check_y_axis())
        self.thread_list.append(y_check)

        dy_l_check = Thread(target=self.check_dyagonal_left())
        self.thread_list.append(dy_l_check)

        dy_r_check = Thread(target=self.check_dyagonal_right())
        self.thread_list.append(dy_r_check)

        #start threads
        self.thread_join_start()
        self.thread_list = list()
        if self.graph_fill_check() == True:
            self.mainWinner = self.draw_val

    def thread_join_start(self):
        '''
        ფუნქცია ემსახურება, run_check ფუნქციაში შექმნილი სრედების ჩართვას და მართ დაჯოინებას
        '''
        for th in self.thread_list:
            th.start()
        for th in self.thread_list:
            th.join()

    def graph_fill_check(self):
        '''
        ფუნქცია ამოწმებს, შევსილია თუ არა მატრიცა ბოლომდე
        '''
        for y in range(self.graph_length):
            for x in range(self.graph_length):
                if self.graph[y][x] == None:
                    return False
        return True

if __name__ == "__main__":
    print("run program from gui side")
