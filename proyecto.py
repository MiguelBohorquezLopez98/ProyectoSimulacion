# Mini-project #6 - Blackjack

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import random
from time import sleep

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
message = ''
messageop = ''
victorias = 0
derrotas = 0
sumajug = 0
sumaop = 0
deck = None
player_hand = None
dealer_hand = None

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
            print ("Carta invalida: ", suit, rank)

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
        self.cards = []

    def __str__(self):
        rep = 'Hand contains'
        
        for card in self.cards:
            rep += ' ' + str(card)
        
        return rep

    def add_card(self, card):
        self.cards.append(card)
        
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        
        has_ace = False
        
        for card in self.cards:
            value += VALUES[card.get_rank()]
            
            if card.get_rank() == 'A':
                has_ace = True
                
        if has_ace and value + 10 <= 21:
            value += 10
            
        return value
    pass	# calcula el valor de la mano
   
    def draw(self, canvas, pos):
        c = 0
        for card in self.cards:
            card.draw(canvas, [pos[0] + CARD_SIZE[0] * c, pos[1]])
                               
            c += 1

 
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        # add cards back to deck and shuffle
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()
    
    def __str__(self):
        rep = 'Deck contains'
        
        for card in self.cards:
            rep += ' ' + str(card)
            
        return rep

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, message, messageop
    global dealer_hand, player_hand, sumajug

  

    # your code goes here
    deck = Deck()
    deck.shuffle()
    
    player_hand, dealer_hand = Hand(), Hand()
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    in_play = True
    outcome = "Pedir o Quedarte?"
    message = ''
    messageop = ''
    sumajug = player_hand.get_value()
    
      
    

    

def hit():
    # if the hand is in play, hit the player
    global outcome, in_play, message, messageop, sumajug, sumaop, derrotas
    sumajug = player_hand.get_value()

    if not in_play:
        return
    
    if player_hand.get_value() <= 21:
        
        player_hand.add_card(deck.deal_card())
        sumajug = player_hand.get_value()

    
    # if busted, assign a message to outcome, update in_play and score
    if player_hand.get_value() > 21:

        outcome = "Nueva Mano?"
        message = "Te pasaste!!"
        derrotas += 1
        sumajug = player_hand.get_value()
        sumaop = dealer_hand.get_value()
        messageop = "Mano: " + str(sumaop)
        in_play = False
        
    
       
def stand():
    global outcome, in_play, message, sumajug, sumaop, messageop, derrotas, victorias
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if not in_play:
        return
    
    if player_hand.get_value() > 21:
        message = "Te pasaste!!"
        derrotas += 1
        sumajug = player_hand.get_value()
        sumaop = dealer_hand.get_value()
        messageop = "Mano: " + str(sumaop)
        in_play = False
        return
    
    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(deck.deal_card())
        
    if dealer_hand.get_value() > 21:
        message = "El oponente se paso!!"
        victorias += 1
        sumajug = player_hand.get_value()
        sumaop = dealer_hand.get_value()
        messageop = "Mano: " + str(sumaop)
        
    else:
        if player_hand.get_value() <= dealer_hand.get_value():
            message = "El oponente gano!!!"
            derrotas += 1
            sumajug = player_hand.get_value()
            sumaop = dealer_hand.get_value()
            messageop = "Mano: " + str(sumaop)
        else:
            message = "Tu ganaste!!!"
            victorias += 1
            sumajug = player_hand.get_value()
            sumaop = dealer_hand.get_value()
            messageop = "Mano: " + str(sumaop)
     
    # assign a message to outcome, update in_play and score
    outcome = "Nueva Mano?"
    in_play = False

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    canvas.draw_text("Juego del 21!!", (25, 50), 40, "Red", "monospace")
    canvas.draw_text(outcome, (250, 350), 25, "Black", "monospace")
    
    canvas.draw_text("Jugador", (75, 350), 25, "Black", "monospace")
    canvas.draw_text("Oponente", (75, 100), 25, "Black", "monospace")
    canvas.draw_text(messageop, (275, 125), 25, "Black", "monospace")
    
    canvas.draw_text(message, (250, 150), 25, "Black", "monospace")
    
    
    canvas.draw_text("Victorias: " + str(victorias), (350, 550), 30, "Black", "monospace")
    canvas.draw_text("Derrotas: " + str(derrotas), (350, 585), 30, "Black", "monospace")
    
    canvas.draw_text("Mano Jugador: " + str(sumajug), (10, 575), 30, "Black", "monospace")
    
    player_hand.draw(canvas, [75, 400])
    dealer_hand.draw(canvas, [75, 200])
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                          [75 + CARD_BACK_CENTER[0],
                           200 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
                                     

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Mano", deal, 200)
frame.add_button("Pedir",  hit, 200)
frame.add_button("Quedarte", stand, 200)
frame.set_draw_handler(draw)


deal()

# get things rolling
frame.start()


# remember to review the gradic rubric