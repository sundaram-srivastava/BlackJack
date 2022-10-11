#!/usr/bin/env python

# blackjack.py
# from Complete-Python-3-Bootcamp Udemy course
# Pierian Data International by Jose Portilla

# IMPORT STATEMENTS AND VARIABLE DECLARATIONS:

import random

suits = ('?', '?', '?', '?')
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8,
            '9':9, '10':10, 'J':10, 'Q':10, 'K':10, 'A':11}

playing = True

# CLASS DEFINTIONS:

class Card:

    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + self.suit


class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

    def __str__(self):
        deck_comp = ''  # start with an empty string
        for card in self.deck:
            deck_comp += '\n '+card.__str__() # add each Card object's print string
        return 'The deck has:' + deck_comp

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
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1  # add to self.aces

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


# FUNCTION DEFINITIONS:

def take_bet(chips):

    while True:
        try:
            chips.bet = int(input(f'You have {chips.total} chips. Your bet? '))
        except ValueError:
            continue
        else:
            if chips.bet <= 0:
                continue
            elif chips.bet > chips.total:
                print("Your bet can't exceed",chips.total)
            else:
                break

def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing

    while True:
        x = input("[H]it or [S]tand? ")

        if x == '':
            continue

        elif x[0].lower() == 'h':
            hit(deck,hand)  # hit() function defined above

        elif x[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            playing = False

        else:
            continue
        break


def show_some(player,dealer):
    print("\nDealer's hand:")
    print(" <card hidden>")
    print('',dealer.cards[1])
    print("\nPlayer's hand:", *player.cards, sep='\n ')
    print("\n(total = " + str(player_hand.value) + ")")

def show_all(player,dealer):
    print("\nDealer's hand:", *dealer.cards, sep='\n ')
    print("Dealer's hand =",dealer.value)
    print("\nPlayer's hand:", *player.cards, sep='\n ')
    print("Player's hand =",player.value)

def player_busts(player,dealer,chips):
    print("\nPLAYER BUSTS")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("\nPLAYER WINS")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("\nDEALER BUSTS")
    chips.win_bet()

def dealer_wins(player,dealer,chips):
    print("\nDEALER WINS")
    chips.lose_bet()

def push(player,dealer):
    print("PUSH. Dealer and Player tie.")

# GAMEPLAY!
print('\nWelcome to Blackjack!\nGet as close to 21 as you can without going over. Aces count as 1 or 11.\n')

# Set up the Player's chips
player_chips = Chips()  # remember the default value is 100

while True:

    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Prompt the Player for their bet:
    take_bet(player_chips)

    # Show the cards:
    show_some(player_hand,dealer_hand)

    while playing:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand)
        show_some(player_hand,dealer_hand)

        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break

    # If Player hasn't busted, play Dealer's hand
    if player_hand.value <= 21:

        # "soft 17" variant (Dealer hits until he reaches 17. No tie/push)
        #while dealer_hand.value < 17:
        while dealer_hand.value < player_hand.value:
            hit(deck,dealer_hand)

        # Show all cards
        show_all(player_hand,dealer_hand)

        # Test different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)

        else:
            push(player_hand,dealer_hand)

    if player_chips.total == 0:
        print("\nGame over. You lost all chips!")
        break
    else:
        # Inform Player of their chips total
        print("\nPlayer's winnings stand at",player_chips.total)

# FIXME
    # Ask to play again
    new_game = input("Play another hand? [y/n] ")
    if new_game[0].lower()=='y':
        playing=True
        continue
    elif new_game[0].lower()=='n':
        print("Thanks for playing!")
        break