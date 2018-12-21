# implementation of card game - Memory

import simplegui
import random

record = 0
game = 0

# helper function to initialize globals
def new_game():
    global card_deck, turns, exposed, exposed_cards, game
    card_deck = list(range(8))*2
    random.shuffle(card_deck)
    exposed_cards = [False] * 16	# card is exposed or not
    exposed = []	# temporary list of exposed cards
    turns = 0
    game += 1
     
# define event handlers
def mouseclick(pos):
    global turns
    if pos[0] % 50 != 0 and pos[1] % 120 != 0: # not click on grid lines
        cell = pos[0] // 50
        if not exposed_cards[cell]:	# if the cell isn't exposed
            exposed_cards[cell] = True	# expose the card in that cell
            exposed.append([cell, card_deck[cell]])	# save as temporary list of exposed cards
            if len(exposed) == 3:
                if exposed[0][1] != exposed[1][1]:	# if 2 cards doesn't match
                    exposed_cards[exposed[0][0]] = False  # flip the cards
                    exposed_cards[exposed[1][0]] = False
                turns += 1
                exposed.pop(0)	# remove the 1st 2 cards in exposed cards list
                exposed.pop(0)
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global record
    for i in xrange(16):
        if not exposed_cards[i]:
            canvas.draw_polygon([[i*50, 0], [50*(i+1), 0], [50*(i+1), 120], [i*50, 120]], 2, "yellow", "green")
        else:
            canvas.draw_text(str(card_deck[i]), (14 + 50*i, 75), 48, "white")
    # numbers of games
    str_game = "Game: %d" %(game)
    label1.set_text(str_game)
    # numbers of turns
    str_turns = "Turns = %d" %(turns)
    label2.set_text(str_turns)
    # record of best performance
    if exposed_cards.count(False) == 0:
        if record == 0:
            record = turns
        elif record > turns:
            record = turns
        str_record = "Your record: %d" %(record)
        label3.set_text(str_record)
   
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 120)
frame.add_button("Reset", new_game)
label1 = frame.add_label("Game: 0")
label2 = frame.add_label("Turns = 0")
label3 = frame.add_label("Your record: -")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()