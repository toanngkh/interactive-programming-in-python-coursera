# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
player_pos = [80, 400]
dealer_pos = [80, 160]

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        s = "hand contains "
        for card in self.hand:
            s += str(card) + " "
        return s

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        sum = 0
        ace = 0	
        for card in self.hand:
            if card.get_rank() == "A":
                ace += 1
            for key, value in VALUES.items():
                if card.get_rank() == key:
                    sum += value
        if ace == 0:
            return sum
        else:
            if sum + 10 <= 21:
                sum += 10
        return sum
    
    def draw(self, canvas, pos):
        self.pos = pos
        i = 0
        for card in self.hand:
            card.draw(canvas, [self.pos[0] + i, self.pos[1]])
            i += 100
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        card_deal = random.choice(self.deck)
        i = self.deck.index(card_deal)
        return self.deck.pop(i)
    
    def __str__(self):
        s = "Deck contains "
        for card in self.deck:
            s += str(card) + " "
        return s

player_hand = Hand()
dealer_hand = Hand()
new_deck = Deck()
    
#define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, dealer_hand, new_deck, score
    if in_play:
        score -= 1
    outcome = "Hit or stand?"
    # create new players and deck
    player_hand = Hand()
    dealer_hand = Hand()
    new_deck = Deck()
    new_deck.shuffle()
    # deal cards to deck
    for i in xrange(2):
        player_hand.add_card(new_deck.deal_card())
        dealer_hand.add_card(new_deck.deal_card())
    
    in_play = True
    
        
def hit():
    global in_play, player_value, score, outcome
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(new_deck.deal_card())
        player_value = player_hand.get_value()
        if player_value > 21:
            outcome = "You LOST! New deal?"
            score -= 1
            in_play = False
    
def stand():
    global in_play, dealer_hand, score, outcome
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        dealer_value = dealer_hand.get_value()
        while dealer_value < 17:
            dealer_hand.add_card(new_deck.deal_card())
            dealer_value = dealer_hand.get_value()
        if dealer_value > 21:
            outcome = "You WON! New deal?"
            score += 1
        elif 21 >= dealer_value >= player_value:
            outcome = "You LOST! New deal?"
            score -= 1
        else:
            outcome = "You WON! New deal?"
            score += 1
        in_play = False
            
# draw handler    
def draw(canvas):
    canvas.draw_text("Blackjack", (100, 80), 72, "cyan")
    canvas.draw_text("Dealer", (80, 130), 36, "black")
    canvas.draw_text("Player", (80, 370), 36, "black")
    canvas.draw_text(outcome, (220, 370), 36, "black")
    canvas.draw_text("Score", (450, 80), 36, "black")
    canvas.draw_text(str(score), (540, 80), 36, "black")
    
    player_hand.draw(canvas, player_pos)     
    dealer_hand.draw(canvas, dealer_pos)
    # draw card back while in_play
    if in_play:	
        loc = [dealer_pos[0] + CARD_BACK_CENTER[0], dealer_pos[1] + CARD_BACK_CENTER[1]]
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, loc, CARD_BACK_SIZE)
        
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric