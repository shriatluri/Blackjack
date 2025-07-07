class BlackjackGame {
    constructor() {
        this.gameState = {
            balance: 0,
            gameStarted: false,
            handInProgress: false
        };
        
        this.initializeElements();
        this.bindEvents();
    }
    
    initializeElements() {
        // Welcome screen elements
        this.welcomeScreen = document.getElementById('welcomeScreen');
        this.gameTable = document.getElementById('gameTable');
        this.buyInInput = document.getElementById('buyIn');
        this.startGameBtn = document.getElementById('startGameBtn');
        
        // Game elements
        this.balanceDisplay = document.getElementById('balance');
        this.dealerCards = document.getElementById('dealerCards');
        this.playerCards = document.getElementById('playerCards');
        this.dealerScore = document.getElementById('dealerScore');
        this.playerScore = document.getElementById('playerScore');
        this.gameMessage = document.getElementById('gameMessage');
        
        // Betting elements
        this.bettingSection = document.getElementById('bettingSection');
        this.betAmountInput = document.getElementById('betAmount');
        this.placeBetBtn = document.getElementById('placeBetBtn');
        
        // Action buttons
        this.actionButtons = document.getElementById('actionButtons');
        this.hitBtn = document.getElementById('hitBtn');
        this.standBtn = document.getElementById('standBtn');
        this.doubleBtn = document.getElementById('doubleBtn');
        this.splitBtn = document.getElementById('splitBtn');
        this.newHandBtn = document.getElementById('newHandBtn');
    }
    
    bindEvents() {
        this.startGameBtn.addEventListener('click', () => this.startGame());
        this.placeBetBtn.addEventListener('click', () => this.placeBet());
        this.hitBtn.addEventListener('click', () => this.hit());
        this.standBtn.addEventListener('click', () => this.stand());
        this.doubleBtn.addEventListener('click', () => this.double());
        this.splitBtn.addEventListener('click', () => this.split());
        this.newHandBtn.addEventListener('click', () => this.newHand());
        
        // Enter key support
        this.buyInInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.startGame();
        });
        
        this.betAmountInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.placeBet();
        });
    }
    
    async startGame() {
        const buyIn = parseInt(this.buyInInput.value);
        
        if (buyIn < 10) {
            this.showMessage('Minimum buy-in is $10', 'error');
            return;
        }
        
        try {
            const response = await fetch('/start_game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ balance: buyIn })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.gameState.balance = data.balance;
                this.gameState.gameStarted = true;
                this.updateBalance(data.balance);
                this.showGameTable();
                this.showMessage(data.message);
            } else {
                this.showMessage(data.message, 'error');
            }
        } catch (error) {
            this.showMessage('Error starting game. Please try again.', 'error');
        }
    }
    
    async placeBet() {
        const bet = parseInt(this.betAmountInput.value);
        
        if (bet <= 0) {
            this.showMessage('Please enter a valid bet amount', 'error');
            return;
        }
        
        if (bet > this.gameState.balance) {
            this.showMessage('Insufficient balance for this bet', 'error');
            return;
        }
        
        try {
            const response = await fetch('/place_bet', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ bet: bet })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.updateGameState(data);
                this.gameState.handInProgress = true;
                this.hideBettingSection();
                
                if (!data.game_over) {
                    this.showActionButtons();
                }
                
                this.updateButtonStates(data);
            } else {
                this.showMessage(data.message, 'error');
            }
        } catch (error) {
            this.showMessage('Error placing bet. Please try again.', 'error');
        }
    }
    
    async hit() {
        try {
            const response = await fetch('/hit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.updateGameState(data);
                this.updateButtonStates(data);
                
                if (data.game_over) {
                    this.endHand();
                }
            } else {
                this.showMessage(data.message, 'error');
            }
        } catch (error) {
            this.showMessage('Error hitting. Please try again.', 'error');
        }
    }
    
    async stand() {
        try {
            const response = await fetch('/stand', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.updateGameState(data);
                this.endHand();
            } else {
                this.showMessage(data.message, 'error');
            }
        } catch (error) {
            this.showMessage('Error standing. Please try again.', 'error');
        }
    }
    
    async double() {
        try {
            const response = await fetch('/double', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.updateGameState(data);
                this.endHand();
            } else {
                this.showMessage(data.message, 'error');
            }
        } catch (error) {
            this.showMessage('Error doubling. Please try again.', 'error');
        }
    }
    
    async split() {
        // Split functionality would be implemented here
        // For now, show a message that it's not implemented
        this.showMessage('Split functionality coming soon!', 'info');
    }
    
    async newHand() {
        try {
            const response = await fetch('/new_hand', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.resetForNewHand();
                this.showMessage(data.message);
                this.updateBalance(data.balance);
            } else {
                this.showMessage(data.message, 'error');
            }
        } catch (error) {
            this.showMessage('Error starting new hand. Please try again.', 'error');
        }
    }
    
    updateGameState(data) {
        if (data.player_hand) {
            this.displayCards(this.playerCards, data.player_hand);
            this.playerScore.textContent = data.player_score;
        }
        
        if (data.dealer_hand) {
            this.displayCards(this.dealerCards, data.dealer_hand);
            this.dealerScore.textContent = data.dealer_score;
        }
        
        if (data.balance !== undefined) {
            this.gameState.balance = data.balance;
            this.updateBalance(data.balance);
        }
        
        if (data.message) {
            this.showMessage(data.message, this.getMessageType(data.message));
        }
    }
    
    displayCards(container, cards) {
        container.innerHTML = '';
        
        cards.forEach((card, index) => {
            setTimeout(() => {
                const cardElement = this.createCardElement(card);
                container.appendChild(cardElement);
            }, index * 200);
        });
    }
    
    createCardElement(card) {
        const cardDiv = document.createElement('div');
        cardDiv.className = 'card';
        
        const suit = card.suit;
        const value = card.value;
        const symbol = this.getCardSymbol(suit);
        const color = this.getCardColor(suit);
        
        cardDiv.innerHTML = `
            <div class="card-value ${color}">${value}</div>
            <div class="card-suit ${color}">${symbol}</div>
            <div class="card-value-bottom ${color}">${value}</div>
        `;
        
        return cardDiv;
    }
    
    createCardBack() {
        const cardDiv = document.createElement('div');
        cardDiv.className = 'card card-back';
        return cardDiv;
    }
    
    getCardSymbol(suit) {
        const symbols = {
            'Hearts': '♥',
            'Diamonds': '♦',
            'Clubs': '♣',
            'Spades': '♠'
        };
        return symbols[suit] || suit;
    }
    
    getCardColor(suit) {
        return (suit === 'Hearts' || suit === 'Diamonds') ? 'red' : 'black';
    }
    
    getMessageType(message) {
        const lowerMessage = message.toLowerCase();
        if (lowerMessage.includes('win') || lowerMessage.includes('blackjack')) {
            return 'win';
        } else if (lowerMessage.includes('lose') || lowerMessage.includes('bust')) {
            return 'lose';
        } else if (lowerMessage.includes('push') || lowerMessage.includes('tie')) {
            return 'push';
        }
        return 'info';
    }
    
    showMessage(message, type = 'info') {
        this.gameMessage.textContent = message;
        this.gameMessage.className = `message ${type}`;
    }
    
    updateBalance(balance) {
        this.balanceDisplay.textContent = `$${balance.toLocaleString()}`;
    }
    
    showGameTable() {
        this.welcomeScreen.style.display = 'none';
        this.gameTable.style.display = 'grid';
    }
    
    hideBettingSection() {
        this.bettingSection.style.display = 'none';
    }
    
    showBettingSection() {
        this.bettingSection.style.display = 'flex';
    }
    
    showActionButtons() {
        this.actionButtons.style.display = 'flex';
    }
    
    hideActionButtons() {
        this.actionButtons.style.display = 'none';
    }
    
    updateButtonStates(data) {
        this.hitBtn.disabled = !data.can_hit;
        this.doubleBtn.disabled = !data.can_double;
        this.splitBtn.style.display = data.can_split ? 'block' : 'none';
    }
    
    endHand() {
        this.gameState.handInProgress = false;
        this.hideActionButtons();
        this.newHandBtn.style.display = 'block';
        
        // Check if player is out of money
        if (this.gameState.balance <= 0) {
            this.showMessage('Game Over! You\'re out of money.', 'lose');
            setTimeout(() => {
                this.resetGame();
            }, 3000);
        }
    }
    
    resetForNewHand() {
        this.playerCards.innerHTML = '';
        this.dealerCards.innerHTML = '';
        this.playerScore.textContent = '0';
        this.dealerScore.textContent = '0';
        this.showBettingSection();
        this.newHandBtn.style.display = 'none';
        this.gameState.handInProgress = false;
    }
    
    resetGame() {
        this.gameState = {
            balance: 0,
            gameStarted: false,
            handInProgress: false
        };
        
        this.welcomeScreen.style.display = 'block';
        this.gameTable.style.display = 'none';
        this.buyInInput.value = '1000';
        this.betAmountInput.value = '50';
        this.balanceDisplay.textContent = '$0';
    }
}

// Utility functions
function setBet(amount) {
    document.getElementById('betAmount').value = amount;
}

// Initialize the game when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new BlackjackGame();
});

// Add some visual effects
document.addEventListener('DOMContentLoaded', () => {
    // Add subtle animations to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', () => {
            button.style.transform = 'translateY(-2px)';
        });
        
        button.addEventListener('mouseleave', () => {
            button.style.transform = 'translateY(0)';
        });
    });
    
    // Add click effects
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            button.style.transform = 'translateY(0) scale(0.95)';
            setTimeout(() => {
                button.style.transform = 'translateY(-2px) scale(1)';
            }, 100);
        });
    });
}); 