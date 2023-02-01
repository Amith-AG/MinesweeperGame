import re
import random
class MineSweeper():
    def __init__(self,dem_size,bomb):
        self.dem_size=dem_size
        self.bomb=bomb
        self.board=self.make_board()
        self.assign_value_to_board()
        self.dug=set()
    def make_board(self):
        board=[[None for i in range(self.dem_size)] for i in range(self.dem_size)]
        bomb_planted=0
        while bomb_planted<self.bomb:
            loc=random.choice([i for i in range(0,self.dem_size**2-1)])
            row=loc//self.dem_size
            col=loc%self.dem_size
            if board[row][col]=='*':
                continue
            board[row][col]='*'
            bomb_planted+=1
        return board
    def assign_value_to_board(self):
        for r in range(self.dem_size):
            for c in range(self.dem_size):
                if self.board[r][c]=='*':
                    continue
                self.board[r][c]=self.neighbour_min(r,c)


    def neighbour_min(self,row,col):
        bomb_count=0
        for r in range(max(0,row-1),min(self.dem_size-1,(row+1)+1)):
            for c in range(max(0,col-1),min(self.dem_size-1,(col+1)+1)):
                if r==row and c==col:
                    continue
                if self.board[r][c]=='*':
                    bomb_count+=1
        return bomb_count
    def dig(self,row,col):
        self.dug.add((row,col))
        if self.board[row][col]=='*':
            return False
        if self.board[row][col]>0:
            return True
        for r in range(max(0,row-1),min(self.dem_size-1,(row+1)+1)):
            for c in range(max(0,col-1),min(self.dem_size-1,(col+1)+1)):
                if (r,c) in self.dug:
                    continue
                self.dig(r,c)
        return True
    def __str__(self):
        # this is a magic function where if you call print on this object,
        # it'll print out what this function returns!
        # return a string that shows the board to the player

        # first let's create a new array that represents what the user would see
        visible_board = [[None for _ in range(self.dem_size)] for _ in range(self.dem_size)]
        for row in range(self.dem_size):
            for col in range(self.dem_size):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
        
        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dem_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dem_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dem_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep
def play(dem_size=10,bomb=10):
    board=MineSweeper(dem_size,bomb)
    safe=True
    while len(board.dug)<board.dem_size**2-bomb:
        print(board)
        user_input=re.split(',(\\s)*',input('enter position where you want to dig,imput as [row,col]:'))
        row=int(user_input[0])
        col=int(user_input[-1])
        if row<0 or row>=dem_size or col<0 or col>=dem_size:
            print("invaid input try again")
            continue
        safe=board.dig(row,col)
        if not safe:
            break
    if safe:
        print("congragulation you won the game")
    else:
        print("Game Over")
        board.dug=[(r,c)for r in range(dem_size)for c in range(dem_size)]
        print(board)
if __name__=='__main__':
    play()