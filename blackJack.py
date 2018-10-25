import random

#defining all of the values
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

#Listing out all of the classes that are going to be used. 
class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.rank + " of " + self.suit

class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return "The deck has " +deck_comp

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        single_card = self.deck.pop()
        return single_card
class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        #card passed in comes from our Deck.deal()
        self.cards.append(card)
        self.value += values[card.rank]
        
        #track aces
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_ace(self):
        #If the total value is greater than 21 and I still have an Ace, Then it changes the ace to a one. 
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips:
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

#Listing out all of the functions that are going to be used for the blackjack game
def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except ValueError:
            print("Please provide an acceptable amount")
        else:
            if chips.bet > chips.total:
                print("sorry you do not have enough chips. Your bet can only be {}".format(chips.total))
            else:
                break
def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    while True:
        x = input('Hit or stand? Enter H or S')
        
        if x[0].lower() == 'h':
            hit(deck,hand)
        elif x[0].lower() == 's':
                print("Player Stands. It is now the dealer's turn")
                playing = False
        else:
            print("Sorry I did not understand that. Please enter an H or S")
            continue
        break

def show_some(player,dealer):
    print("\nDealer's Hand:")
    print("<<card hidden>>")
    print('',dealer.cards[1])
    print("\nPlayer's", *player.cards, sep = '\n')
    
    
def show_all(player,dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's", *player.cards, sep = '\n')
    print("Player's Hand =",player.value)

def player_busts(player,dealer,chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("Player Wins!!")
    chips.win_bet()


def dealer_bust(player,dealer,chips):
    print("Dealer busts!")
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print("Dealer wins!")
    chips.lose_bet()
    
    
def push():
    print("Dealer and player Tie. Push!")

playing = True

while True:
    # Print an opening statement
    print("Welcome to my Blackjack game!")
    deck = Deck()
    deck.shuffle()
    
    # Create & shuffle the deck, deal two cards to each player
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
        
    # Set up the Player's chips
    player_chips = Chips()
    
    # Prompt the Player for their bet
    take_bet(player_chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand)
        
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)

            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:
        
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)
    
        # Show all cards
        show_all(player_hand, dealer_hand)
        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_bust(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        else:
            push()
    
    # Inform Player of their chips total 
    print("\nPlayers total chips are at: ",player_chips.total)
    # Ask to play again
    new_game = input("Would you like to play another game? y/n")
    
    if new_game[0].lower() == 'y':
        playing = True
    else:
        print("Thank you for playing!")
        

        break
