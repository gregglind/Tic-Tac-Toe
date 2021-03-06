#!/usr/bin/env python 
'''
INVINCITRON, an opponent that can win *all games* with 100% certainty [1]

Note [1]: current implementation only plays tic-tac-toe, future versions will expand on this.

LICENSE:  BSD, with attribution
AUTHOR:  Gregg Lind <gregg.lind@gmail.com>


'''

'''
Intructions:
1. Fork this repo on github.
2. Create an app that can interactively play the game of Tic Tac Toe against another player and never lose.
3. Commit early and often, with good messages.
4. Push your code back to github and send me a pull request.
'''


'''
Strategy (from Wikipedia)

A player can play perfect tic-tac-toe (win or draw) given they move according to the highest possible move from the following table.[4]
Win: If the player has two in a row, play the third to get three in a row.
Block: If the opponent has two in a row, play the third to block them.
Fork: Create an opportunity where you can win in two ways.
Block opponent's fork:
Option 1: Create two in a row to force the opponent into defending, as long as it doesn't result in them creating a fork or winning. For example, if "X" has a corner, "O" has the center, and "X" has the opposite corner as well, "O" must not play a corner in order to win. (Playing a corner in this scenario creates a fork for "X" to win.)
Option 2: If there is a configuration where the opponent can fork, block that fork.
Center: Play the center.
Opposite corner: If the opponent is in the corner, play the opposite corner.
Empty corner: Play in a corner square.
Empty side: Play in a middle square on any of the 4 sides.
The first player, whom we shall designate "X", has 3 possible positions to mark during the first turn. Superficially, it might seem that there are 9 possible positions, corresponding to the 9 squares in the grid. However, by rotating the board, we will find that in the first turn, every corner mark is strategically equivalent to every other corner mark. The same is true of every edge mark. For strategy purposes, there are therefore only three possible first marks: corner, edge, or center. Player X can win or force a draw from any of these starting marks; however, playing the corner gives the opponent the smallest choice of squares which must be played to avoid losing.[5]
The second player, whom we shall designate "O", must respond to X's opening mark in such a way as to avoid the forced win. Player O must always respond to a corner opening with a center mark, and to a center opening with a corner mark. An edge opening must be answered either with a center mark, a corner mark next to the X, or an edge mark opposite the X. Any other responses will allow X to force the win. Once the opening is completed, O's task is to follow the above list of priorities in order to force the draw, or else to gain a win if X makes a weak play.

'''

import itertools
import random

# ttt has small state, so we can throw it around.  

triples = [
    (0,1,2),
    (3,4,5),
    (6,7,8),
    (0,3,6),
    (1,4,7),
    (2,5,8),
    (0,4,8),
    (2,4,6)
]

corners = {0:8,2:6,6:2,8:0}
sides = {1:7,3:5,5:3,7:1}


def opponent(player):
    return 'XO'[player=='X']

def won(game):
    ''' return play who wins the game, or False 

    >>> print won(['X','X','X'] + [None,]*6)
    X
    >>> print won([None,]*9)
    None

    # 2 ways for x to win
    >>> print won(['O', 'O', 'X', 'O', 'X', 'O', 'X', 'X', 'X'])
    X

    '''
    winners = set()
    for p in (('O','O','O'),('X','X','X')):
        for (a,b,c) in triples:
            run = (game[a],game[b],game[c]) 
            if run == p:
                winners.add(p[0])
            else:
                pass
                #print run, p[0]

    l = len(winners)
    if l == 0:
        return None
    elif l == 1:
        return list(winners)[0]
    else:
        raise Exception('more than one winner!?  oops!')

def tie(game):
    '''

    >>> g = ['O', 'X', 'O', 'X', 'O', 'X', 'X', 'O', 'X']
    >>> tie(g)
    True
    '''
    return (not won(game)) and None not in game
    


## all of these are brute force.  We could save state along the way.
def can_win(game,player):
    ''' in some triple, there is a None, and two 'player' tokens. 

    >>> can_win(['X','X'] + [None,]*7,'X')
    2
    '''
    for t in triples:
        run = (game[t[0]],game[t[1]],game[t[2]])
        if None in run and sorted([None,player,player]) == sorted(run):
             for k in t:
                if game[k] is None: return k

    return None

def can_block(game,player):
    # block the enemy
    return can_win(game,opponent(player))

def can_fork(game,player):
    return None

def block_fork(game,player):
    return None

def center(game,player):
    '''

    >>> center([None,]*9,'X')
    4
    >>> w = [None,]*9
    >>> w[4] = 'O'
    >>> print center(w,'X')
    None
    '''
    if game[4] is None:
        return 4
    else:
        return None

def opposite_corner(game,player):
    move = None
    for k,v  in corners.iteritems():
        if game[k] is None and game[v] == opponent(player):
            move = k
            break

    return move

def empty_corner(game,player):
    moves = [x for x in corners if game[x] is None]
    if moves:
        return random.choice(moves)
    else:
        return None

def empty_side(game,player):
    moves = [x for x in sides if game[x] is None]
    if moves:
        return random.choice(moves)
    else:
        return None

def random_move(game,player):
    moves = [ii for (ii,x) in enumerate(game) if x is None]
    #print "NEXT_MOVE:", game, player, moves
    return random.choice(moves)

def suggest_optimal_move(game,player):
    move = None
    move_fns = (can_win,can_block,can_fork,
        block_fork,center,
        opposite_corner, empty_corner,
        empty_side)
     
    for move_fn in move_fns:
        move = move_fn(game,player)
        #print move, move_fn.__name__
        if move is not None:  
            break
    
    return move

def play_game(player1,player2):
    '''
    Play an interactive tic-tac-toe game.

    Args:
        player1, player2: 'players'
            that have a 'get_move(game,player)'
            method.  

    Returns:
        game, winner, moves
    '''
    game = [None,]*9
    moves = []
    players = itertools.cycle([('X',player1),('O',player2)])
    while not (won(game) or tie(game)):
        s, p = players.next()
        move = p.next_move(game,s)
        if move is None:
            raise Exception, "no move chosen! %r %r %r" % (s,game,moves)
        game[move] = s
        moves.append(move)
        # should have some exceptions here for illegal moves.  
    
    if tie(game):
        winner = "TIE"
    else:
        winner = won(game)
    
    return winner,game,moves



class GoodPlayer(object):
    def next_move(self,game,player):
        return suggest_optimal_move(game,player)

class RandomPlayer(object):
    def next_move(self,game,player):
        return random_move(game,player)

def format(game):
    g = [(x,'_')[x is None] for x in game]  
    a = ('''%s %s %s  1 2 3 \n'''
         '''%s %s %s  4 5 6 \n'''
         '''%s %s %s  7 8 9 \n''' % 
        (g[0],g[1],g[2],g[3],g[4],g[5],g[6],g[7],g[8])
        )
    return a

class LivePlayer(object):
    def next_move(self,game,player):
        print format(game)
        moves = dict([(str(ii+1),ii) for (ii,x) in enumerate(game) if x is None])
        while True:
            provisional = raw_input("your move? choose from [%s] " % " ".join(sorted(moves))).strip()
            if provisional not in moves:
                print "%s: not a valid move, try again" % (provisional)
            else:
                return moves[provisional]

if __name__ == '__main__':
    ans = raw_input("X or 0? ").strip().upper()
    X = 'X' in ans
    players = (LivePlayer(),GoodPlayer())
    if X:
        print "you are X"
    else:
        print "you are O"
        players = players[::-1]

    winner,game,moves =  play_game(*players)
    print "winner", winner
    print "game board:"
    print format(game)
    print "move sequeunce:", moves









