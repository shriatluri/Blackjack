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
