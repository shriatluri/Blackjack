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

#play_hand is a recursive function which is needed to efficiency with the split function
#Recursive due to individual split hands, multiple split hands, etc.
def play_hand(deck, bet, balance):
    #the player and dealers hands
    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]
    #players hand
    print("Your cards: ", display(player_hand))
    #Dealers first card, second not revealed
    print("Dealer's first card: ", format(dealer_hand[0]))

    #Check for blackjack
    if is_blackjack(dealer_hand) and is_blackjack(player_hand):
        print("Both dealer and you have Blackjack. It's a push.")
        return balance
    elif is_blackjack(dealer_hand):
        #Display both cards of dealers
        print("Dealer's cards: ", display(dealer_hand))
        print("Dealer has a Blackjack! Dealer wins.")
        return balance - bet
    elif is_blackjack(player_hand):
        print("You have a Blackjack! You win.")
        balance += bet * 1.5
        return balance

    #insurance bet
    if dealer_hand[0]['value'] == 'Ace':
        insurance_option = input('The dealer\'s first care is an Ace! Do you want insurance? (yes/no)')
        if insurance_option.lower() == 'yes':
            insurance_bet = min(bet/ 2, balance)
            #update balance
            balance -= insurance_bet
            print(f"Insurance bet placed: {insurance_bet}")
    
    while True:
        #hit, stay, double, and split applications
        action = input('Would you like to hit, stay, double or split (if possible)? ')

        #hit application
        if action.lower() == 'hit':
            player_hand.append(deal_card(deck))
            print("Your cards are: ", display(player_hand))
            if calc_scores(player_hand) > 21:
                print("You Bust! You lose!")
                return balance - bet
            
        #double application
        elif action.lower() == 'double':
            if balance >= bet:
                balance -= bet
                bet *= 2
                player_hand.append(deal_card(deck))
                print("Your cards after doubling: ", display(player_hand))
                #deal with result right away
                if calc_scores(player_hand) > 21:
                    print("You Bust! You lose!")
                    return balance
                break
            else:
                print('Your balance is not high enough to double?')

        #split application
        elif action.lower() == 'split' and can_split[player_hand]:
            #is player wants to split and they have the balance to split
            if balance >= 2 * bet:
                balance -= bet
                #both split hands
                split_hand_1 = [player_hand[0], deal_card(deck)] # type: ignore
                split_hand_2 = [player_hand[1], deal_card(deck)] # type: ignore
                #display them in a neat format and balance update after each split_hand
                print('Hand 1: ', display(split_hand_1))
                balance = play_hand(deck, bet, balance, split_hand_1)
                print('Hand 2: ', display(split_hand_2))
                balance = play_hand(deck, bet, balance, split_hand_2)
                return balance
            else: 
                print("Balance is not enough to split")

        #stay application
        elif action.lower() == 'stay':
            break

    #dealer hand applications; keep drawing until 17 or over or bust
    while calc_scores(dealer_hand) < 17:
        dealer_hand.append(deal_card(deck))
    #show the dealers cards
    print("Dealer's Cards: ", display(dealer_hand))
    dealer_score = calc_scores(dealer_hand)
    player_score = calc_scores(player_hand)

    if dealer_score > 21:
        print('Dealer Busts! Congrats, you win!')
        return balance + bet
    elif dealer_score < player_score:
        print('Congrants, you win!')
        return balance + bet
    elif dealer_score > player_score:
        print("Dealer wins.")
        return balance - bet
    else:
        print("Push. It's a tie.")
        return balance
        
#function to play blackjack
def play_blackjack():
    #shoedeck
    deck = create_deck()
    #shuffle
    random.shuffle(deck)
    #balance input statement
    balance = int(input('Welcome, how much would you like to buy-in for? '))

    while balance > 0:
        bet = int(input('Enter your bet amount for this hand: '))
        if bet > balance:
            print("Your balance is not sufficient to make this bet, please choose a smaller amount. Your balance is: ", balance)
            continue

        #call the play_hand function for the hand to be played and obtain the balance
        balance = play_hand(deck, bet, balance)

        print('Your balance is ', balance)
        if balance <= 0:
            print('Your balance is empty! Game over!')
            break

        if input("Do you want to reload your balance? (yes/no) ").lower() == 'yes':
            additional_balance = int(input("How much would you like to add? "))
            balance += additional_balance

#enjoy!
play_blackjack()
