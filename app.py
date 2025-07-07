from flask import Flask, render_template, request, jsonify, session
import random
import uuid

app = Flask(__name__)
app.secret_key = 'blackjack_secret_key_2024'

# Game logic functions from the original files
def create_deck():
    suits = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
    values = ['2','3','4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    return [{'value': v, 'suit': s} for s in suits for v in values] * 6

def deal_card(deck):
    return deck.pop()

def calc_scores(hand):
    values = {'2': 2,'3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
    score = 0
    aces = 0
    for card in hand:
        card_key = card['value']
        score += values[card_key]
        if card_key == 'Ace':
            aces += 1
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score

def can_split(hand):
    return len(hand) == 2 and hand[0]['value'] == hand[1]['value']

def is_blackjack(hand):
    return calc_scores(hand) == 21 and len(hand) == 2

def get_card_symbol(suit):
    symbols = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}
    return symbols.get(suit, suit)

def get_card_color(suit):
    return 'red' if suit in ['Hearts', 'Diamonds'] else 'black'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    data = request.json
    balance = data.get('balance', 1000)
    
    # Initialize game state
    deck = create_deck()
    random.shuffle(deck)
    
    game_state = {
        'deck': deck,
        'balance': balance,
        'bet': 0,
        'player_hand': [],
        'dealer_hand': [],
        'game_over': False,
        'message': '',
        'can_hit': True,
        'can_double': True,
        'can_split': False,
        'insurance_offered': False,
        'insurance_bet': 0
    }
    
    session['game_state'] = game_state
    
    return jsonify({
        'success': True,
        'balance': balance,
        'message': 'Game started! Place your bet to begin.'
    })

@app.route('/place_bet', methods=['POST'])
def place_bet():
    data = request.json
    bet = data.get('bet', 0)
    
    game_state = session.get('game_state', {})
    
    if bet > game_state['balance']:
        return jsonify({
            'success': False,
            'message': 'Insufficient balance for this bet.'
        })
    
    if bet <= 0:
        return jsonify({
            'success': False,
            'message': 'Please enter a valid bet amount.'
        })
    
    # Deal initial cards
    deck = game_state['deck']
    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]
    
    game_state.update({
        'bet': bet,
        'player_hand': player_hand,
        'dealer_hand': dealer_hand,
        'can_double': game_state['balance'] >= bet,
        'can_split': can_split(player_hand) and game_state['balance'] >= bet,
        'insurance_offered': dealer_hand[0]['value'] == 'Ace'
    })
    
    # Check for blackjacks
    player_blackjack = is_blackjack(player_hand)
    dealer_blackjack = is_blackjack(dealer_hand)
    
    if player_blackjack and dealer_blackjack:
        game_state['message'] = 'Both have Blackjack! Push.'
        game_state['game_over'] = True
    elif dealer_blackjack:
        game_state['message'] = 'Dealer has Blackjack! Dealer wins.'
        game_state['balance'] -= bet
        game_state['game_over'] = True
    elif player_blackjack:
        game_state['message'] = 'Blackjack! You win!'
        game_state['balance'] += int(bet * 1.5)
        game_state['game_over'] = True
    
    session['game_state'] = game_state
    
    return jsonify({
        'success': True,
        'player_hand': player_hand,
        'dealer_hand': [dealer_hand[0]] if not game_state['game_over'] else dealer_hand,
        'player_score': calc_scores(player_hand),
        'dealer_score': calc_scores([dealer_hand[0]]) if not game_state['game_over'] else calc_scores(dealer_hand),
        'balance': game_state['balance'],
        'message': game_state['message'],
        'game_over': game_state['game_over'],
        'can_hit': not game_state['game_over'],
        'can_double': game_state['can_double'] and not game_state['game_over'],
        'can_split': game_state['can_split'] and not game_state['game_over'],
        'insurance_offered': game_state['insurance_offered'] and not game_state['game_over']
    })

@app.route('/hit', methods=['POST'])
def hit():
    game_state = session.get('game_state', {})
    
    if game_state['game_over']:
        return jsonify({'success': False, 'message': 'Game is over'})
    
    deck = game_state['deck']
    player_hand = game_state['player_hand']
    
    player_hand.append(deal_card(deck))
    player_score = calc_scores(player_hand)
    
    game_state['can_double'] = False
    game_state['can_split'] = False
    
    if player_score > 21:
        game_state['message'] = 'Bust! You lose.'
        game_state['balance'] -= game_state['bet']
        game_state['game_over'] = True
        game_state['can_hit'] = False
    
    session['game_state'] = game_state
    
    return jsonify({
        'success': True,
        'player_hand': player_hand,
        'player_score': player_score,
        'balance': game_state['balance'],
        'message': game_state['message'],
        'game_over': game_state['game_over'],
        'can_hit': game_state['can_hit'],
        'can_double': False,
        'can_split': False
    })

@app.route('/stand', methods=['POST'])
def stand():
    game_state = session.get('game_state', {})
    
    if game_state['game_over']:
        return jsonify({'success': False, 'message': 'Game is over'})
    
    deck = game_state['deck']
    dealer_hand = game_state['dealer_hand']
    
    # Dealer draws until 17 or higher
    while calc_scores(dealer_hand) < 17:
        dealer_hand.append(deal_card(deck))
    
    dealer_score = calc_scores(dealer_hand)
    player_score = calc_scores(game_state['player_hand'])
    bet = game_state['bet']
    
    if dealer_score > 21:
        game_state['message'] = 'Dealer busts! You win!'
        game_state['balance'] += bet
    elif dealer_score < player_score:
        game_state['message'] = 'You win!'
        game_state['balance'] += bet
    elif dealer_score > player_score:
        game_state['message'] = 'Dealer wins.'
        game_state['balance'] -= bet
    else:
        game_state['message'] = 'Push! It\'s a tie.'
    
    game_state['game_over'] = True
    game_state['can_hit'] = False
    
    session['game_state'] = game_state
    
    return jsonify({
        'success': True,
        'dealer_hand': dealer_hand,
        'dealer_score': dealer_score,
        'balance': game_state['balance'],
        'message': game_state['message'],
        'game_over': True,
        'can_hit': False,
        'can_double': False,
        'can_split': False
    })

@app.route('/double', methods=['POST'])
def double():
    game_state = session.get('game_state', {})
    
    if game_state['game_over'] or not game_state['can_double']:
        return jsonify({'success': False, 'message': 'Cannot double'})
    
    bet = game_state['bet']
    if game_state['balance'] < bet:
        return jsonify({'success': False, 'message': 'Insufficient balance to double'})
    
    deck = game_state['deck']
    player_hand = game_state['player_hand']
    
    # Double the bet and deal one card
    game_state['bet'] *= 2
    player_hand.append(deal_card(deck))
    player_score = calc_scores(player_hand)
    
    if player_score > 21:
        game_state['message'] = 'Bust! You lose.'
        game_state['balance'] -= game_state['bet']
        game_state['game_over'] = True
        session['game_state'] = game_state
        return jsonify({
            'success': True,
            'player_hand': player_hand,
            'player_score': player_score,
            'balance': game_state['balance'],
            'message': game_state['message'],
            'game_over': True,
            'can_hit': False,
            'can_double': False,
            'can_split': False
        })
    
    # Automatically stand after doubling
    dealer_hand = game_state['dealer_hand']
    while calc_scores(dealer_hand) < 17:
        dealer_hand.append(deal_card(deck))
    
    dealer_score = calc_scores(dealer_hand)
    
    if dealer_score > 21:
        game_state['message'] = 'Dealer busts! You win!'
        game_state['balance'] += game_state['bet']
    elif dealer_score < player_score:
        game_state['message'] = 'You win!'
        game_state['balance'] += game_state['bet']
    elif dealer_score > player_score:
        game_state['message'] = 'Dealer wins.'
        game_state['balance'] -= game_state['bet']
    else:
        game_state['message'] = 'Push! It\'s a tie.'
    
    game_state['game_over'] = True
    session['game_state'] = game_state
    
    return jsonify({
        'success': True,
        'player_hand': player_hand,
        'dealer_hand': dealer_hand,
        'player_score': player_score,
        'dealer_score': dealer_score,
        'balance': game_state['balance'],
        'message': game_state['message'],
        'game_over': True,
        'can_hit': False,
        'can_double': False,
        'can_split': False
    })

@app.route('/new_hand', methods=['POST'])
def new_hand():
    game_state = session.get('game_state', {})
    
    # Reset for new hand
    game_state.update({
        'bet': 0,
        'player_hand': [],
        'dealer_hand': [],
        'game_over': False,
        'message': '',
        'can_hit': True,
        'can_double': True,
        'can_split': False,
        'insurance_offered': False,
        'insurance_bet': 0
    })
    
    # Check if deck needs reshuffling
    if len(game_state['deck']) < 20:
        game_state['deck'] = create_deck()
        random.shuffle(game_state['deck'])
    
    session['game_state'] = game_state
    
    return jsonify({
        'success': True,
        'balance': game_state['balance'],
        'message': 'Place your bet for the next hand.'
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False) 