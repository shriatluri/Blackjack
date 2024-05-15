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
