
class tictactoegame:

    def __init__(self):
        self.board = [ '-' for i in range(0,9) ]
        self.lastmoves = []
        self.winner = None

    def print_board(self):
        '''Print the current game board'''
        
        print ("\nCurrent board:")
        print(" %s | %s | %s" %(self.board[0], self.board[1], self.board[2]))
        print("-------------")
        print(" %s | %s | %s" %(self.board[3], self.board[4], self.board[5]))
        print("-------------")
        print(" %s | %s | %s" %(self.board[6], self.board[7], self.board[8]))
        print("-------------")
        print ("\n",)

    #get the free positions 
    def get_free_positions(self):
        moves = []
        for i,v in enumerate(self.board):
            if v=='-':
                moves.append(i)
        return moves

        
    # marking positions for player1 and player2
    def mark(self,marker,pos):
        self.board[pos] = marker
        self.lastmoves.append(pos)
    #Reset the last player move
    def revert_last_move(self):
        self.board[self.lastmoves.pop()] = '-'
        self.winner = None
    
    # check whether the game is over or not
    def is_gameover(self):
        
        win_positions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6),(1,4,7),(2,5,8), (0,4,8), (2,4,6)]

        for i,j,k in win_positions:
            if self.board[i] == self.board[j] == self.board[k] and self.board[i] != '-':
                self.winner = self.board[i]
                return True

        if '-' not in self.board:
            self.winner = '-'
            return True

        return False

    #Execute the game
    def play(self,player1,player2):
        

        self.p1 = player1
        self.p2 = player2
    
        for i in range(9):

            self.print_board()
            
            if i%2==0:
                if self.p1.type == 'H':
                    print ("\t\t[Human's Chance]")
                else:
                    print ("\t\t[Computer's Chance]")

                self.p1.move(self)
            else:
                if self.p2.type == 'H':
                    print ("\t\t[Human's Chance]")
                else:
                    print ("\t\t[Computer's Chance]")

                self.p2.move(self)

            if self.is_gameover():
                self.print_board()
                if self.winner == '-':
                    print ("\nGame Draw")
                else:
                    print("\nWinner : %s" %self.winner)
                return

class Human:
    '''Class for Human player'''

    def __init__(self,marker):
        self.marker = marker
        self.type = 'H'
    
    def move(self, gameinstance):

        while True:
        
            m = input("Input position:")

            try:
                m = int(m)
            except:
                m = -1
        
            if m not in gameinstance.get_free_positions():
                print ("Invalid move. Retry")
            else:
                break
    
        gameinstance.mark(self.marker,m)


#Class for Computer Player   
class AI:
    

    def __init__(self, marker):
        self.marker = marker
        self.type = 'C'

        if self.marker == 'X':
            self.opponentmarker = 'O'
        else:
            self.opponentmarker = 'X'

    def move(self,gameinstance):
        move_position,score = self.maximized_move(gameinstance)
        gameinstance.mark(self.marker,move_position)


    # Find maximized move
    def maximized_move(self,gameinstance):
            
        bestscore = None
        bestmove = None

        for m in gameinstance.get_free_positions():
            gameinstance.mark(self.marker,m)
        
            if gameinstance.is_gameover():
                score = self.get_score(gameinstance)
            else:
                move_position,score = self.minimized_move(gameinstance)
        
            gameinstance.revert_last_move()
            
            if bestscore == None or score > bestscore:
                bestscore = score
                bestmove = m

        return bestmove, bestscore

    # Find the minimized move
    def minimized_move(self,gameinstance):
        

        bestscore = None
        bestmove = None

        for m in gameinstance.get_free_positions():
            gameinstance.mark(self.opponentmarker,m)
        
            if gameinstance.is_gameover():
                score = self.get_score(gameinstance)
            else:
                move_position,score = self.maximized_move(gameinstance)
        
            gameinstance.revert_last_move()
            
            if bestscore == None or score < bestscore:
                bestscore = score
                bestmove = m

        return bestmove, bestscore

    def get_score(self,gameinstance):
        if gameinstance.is_gameover():
            if gameinstance.winner  == self.marker:
                return 1 # Won

            elif gameinstance.winner == self.opponentmarker:
                
                return -1 # Opponent won

        return 0 # Draw
        

        

if __name__ == '__main__':
    game=tictactoegame()     
    player1 = Human("X")
    player2 = AI("O")
    game.play( player1, player2)