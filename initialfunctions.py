import random

#function to create a deck of cards
def create_deck():
    suits = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
    values = ['2','3','4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    #we will make sure that the deck is a shoe, 6 decks put together
    return [{'value': v, 'suit': s} for s in suits for v in values] * 6
#function to deal a card
def deal_card(deck):
    #return the recent card from the shuffle
    return deck.pop()

#function to calculate score of hand, Ace will be either a 1 or an 11
def calc_scores(hand):
    values = {'2': 2,'3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
    score = 0
    aces = 0
    #Values of the cards in the users hand
    for card in hand:
        card_key = card['value']
        score += values[card_key]
        if card_key == 'Ace':
            aces += 1
    #if score is over 21 and ace is in hand, turn value into 1
    while score > 21 and aces:
        score -= 10
        aces -= 1

    return score

#function for clean formating of cards names
def format(card):
    #ex: "7 of Hearts"
    return f"{card['value']} of {card['suit']}"

#function to display the formated hand
def display(hand):
    #display with ,'s concatinated throughout the hand
    return ', '.join(format(card) for card in hand)

#function to check if it can be split; boolean
def can_split(hand):
    return len(hand) == 2 and hand[0]['value'] == hand[1]['value']

#check if hand is a blackjack
def is_blackjack(hand):
    return calc_scores(hand) == 21 and len(hand) == 2
