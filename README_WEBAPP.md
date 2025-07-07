# Premium Blackjack Web Application

A modern, sleek blackjack game with a premium matte black design and clean user interface.

## Features

- **Modern UI**: Clean, matte black design with smooth animations
- **Full Blackjack Gameplay**: Hit, Stand, Double Down, and Split (coming soon)
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Real-time Updates**: Instant game state updates with beautiful card animations
- **Professional Feel**: Premium casino experience with elegant typography and effects

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python app.py
   ```

3. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## How to Play

1. **Start Game**: Enter your buy-in amount (minimum $10) and click "Start Game"
2. **Place Bet**: Choose your bet amount using the input field or quick bet buttons
3. **Play Your Hand**: Use Hit, Stand, or Double Down to play your cards
4. **Win or Lose**: The game will automatically calculate results and update your balance
5. **New Hand**: Click "New Hand" to continue playing

## Game Rules

- **Blackjack**: 21 with your first two cards (pays 3:2)
- **Bust**: Going over 21 loses automatically
- **Dealer Rules**: Dealer must hit on 16 and stand on 17
- **Double Down**: Double your bet and receive exactly one more card
- **Split**: Split identical cards into two hands (coming soon)

## Technical Details

- **Backend**: Flask (Python)
- **Frontend**: Vanilla JavaScript with modern CSS
- **Session Management**: Server-side game state management
- **Responsive**: Mobile-first design with CSS Grid and Flexbox

## File Structure

```
Blackjack/
├── app.py              # Main Flask application
├── templates/
│   └── index.html      # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css   # Modern CSS styling
│   └── js/
│       └── game.js     # Game logic and interactions
├── requirements.txt    # Python dependencies
└── README_WEBAPP.md   # This file
```

## Browser Support

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## Development

To modify the game:

1. **Backend Logic**: Edit `app.py` for game rules and API endpoints
2. **Frontend Styling**: Edit `static/css/style.css` for visual changes
3. **Game Interactions**: Edit `static/js/game.js` for UI behavior
4. **Layout**: Edit `templates/index.html` for structure changes

## License

This project is open source and available under the MIT License.

---

Enjoy your premium blackjack experience! 🎰 