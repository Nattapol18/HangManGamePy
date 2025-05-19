"""
Enhanced Hangman Game with:
- Multiple difficulty levels
- Visual hangman display
- Word categories
- Score tracking
- Color interface
- Improved user experience
"""
import random
import os
import time
from collections import Counter
import json

# For colored text
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Word categories
word_categories = {
    'fruits': ['apple', 'banana', 'mango', 'strawberry', 'orange', 'grape', 'pineapple', 
               'apricot', 'lemon', 'coconut', 'watermelon', 'cherry', 'papaya', 'berry', 
               'peach', 'lychee', 'muskmelon', 'kiwi', 'pomegranate', 'dragonfruit'],
    'animals': ['elephant', 'giraffe', 'monkey', 'zebra', 'lion', 'tiger', 'bear', 
                'wolf', 'fox', 'deer', 'rabbit', 'squirrel', 'dolphin', 'whale', 
                'shark', 'eagle', 'hawk', 'snake', 'turtle', 'crocodile'],
    'countries': ['india', 'australia', 'japan', 'brazil', 'canada', 'mexico', 
                  'france', 'germany', 'italy', 'spain', 'egypt', 'china', 
                  'russia', 'kenya', 'nigeria', 'peru', 'chile', 'sweden', 'finland', 'norway'],
    'vegetables': ['carrot', 'potato', 'tomato', 'cabbage', 'spinach', 'broccoli', 
                   'cauliflower', 'cucumber', 'eggplant', 'pepper', 'celery', 
                   'lettuce', 'radish', 'onion', 'garlic', 'pumpkin', 'zucchini', 'squash']
}

# Difficulty levels
difficulty_levels = {
    'easy': {'max_wrong': 8, 'hint': True},
    'medium': {'max_wrong': 6, 'hint': True},
    'hard': {'max_wrong': 4, 'hint': False}
}

# ASCII art for hangman
hangman_pics = [
    '''
      +---+
          |
          |
          |
         ===''',
    '''
      +---+
      O   |
          |
          |
         ===''',
    '''
      +---+
      O   |
      |   |
          |
         ===''',
    '''
      +---+
      O   |
     /|   |
          |
         ===''',
    '''
      +---+
      O   |
     /|\\  |
          |
         ===''',
    '''
      +---+
      O   |
     /|\\  |
     /    |
         ===''',
    '''
      +---+
      O   |
     /|\\  |
     / \\  |
         ==='''
]

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_scores():
    """Load highscores from file"""
    try:
        with open('hangman_scores.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {'easy': 0, 'medium': 0, 'hard': 0}

def save_score(difficulty, score):
    """Save highscore if it's better than current"""
    scores = load_scores()
    if score > scores[difficulty]:
        scores[difficulty] = score
        with open('hangman_scores.json', 'w') as f:
            json.dump(scores, f)
        return True
    return False

def display_welcome():
    """Display welcome message and game rules"""
    clear_screen()
    print(f"{Colors.HEADER}{Colors.BOLD}WELCOME TO ENHANCED HANGMAN!{Colors.ENDC}")
    print(f"{Colors.CYAN}=========================={Colors.ENDC}")
    print(f"{Colors.BLUE}How to play:{Colors.ENDC}")
    print("1. Choose a category and difficulty level")
    print("2. Guess letters to reveal the hidden word")
    print("3. You win if you guess the word before the hangman is complete")
    print("4. You lose if the hangman is complete before you guess the word")
    print(f"{Colors.CYAN}=========================={Colors.ENDC}")
    print()
    input("Press Enter to continue...")

def select_category():
    """Let player select a word category"""
    clear_screen()
    print(f"{Colors.HEADER}Select a Word Category:{Colors.ENDC}")
    for i, category in enumerate(word_categories.keys(), 1):
        print(f"{i}. {category.capitalize()}")
    
    while True:
        try:
            choice = int(input("\nEnter your choice (1-4): "))
            if 1 <= choice <= len(word_categories):
                return list(word_categories.keys())[choice - 1]
            else:
                print(f"{Colors.WARNING}Invalid choice. Please enter a number between 1 and {len(word_categories)}.{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.WARNING}Please enter a valid number.{Colors.ENDC}")

def select_difficulty():
    """Let player select difficulty level"""
    clear_screen()
    print(f"{Colors.HEADER}Select Difficulty Level:{Colors.ENDC}")
    print(f"1. Easy (8 wrong guesses allowed, hints available)")
    print(f"2. Medium (6 wrong guesses allowed, hints available)")
    print(f"3. Hard (4 wrong guesses allowed, no hints)")
    
    while True:
        try:
            choice = int(input("\nEnter your choice (1-3): "))
            if choice == 1:
                return 'easy'
            elif choice == 2:
                return 'medium'
            elif choice == 3:
                return 'hard'
            else:
                print(f"{Colors.WARNING}Invalid choice. Please enter 1, 2, or 3.{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.WARNING}Please enter a valid number.{Colors.ENDC}")

def get_hint(word, guessed_letters):
    """Provide a hint (a letter not yet guessed)"""
    not_guessed = [letter for letter in word if letter not in guessed_letters]
    if not_guessed:
        return random.choice(not_guessed)
    return None

def display_game_state(word, guessed_letters, wrong_attempts, max_wrong, category):
    """Display current game state"""
    clear_screen()
    
    # Display hangman
    hangman_stage = min(wrong_attempts, len(hangman_pics) - 1)
    print(f"{Colors.BLUE}{hangman_pics[hangman_stage]}{Colors.ENDC}")
    
    # Display category and word status
    print(f"\n{Colors.CYAN}Category: {category.capitalize()}{Colors.ENDC}")
    print(f"Attempts remaining: {max_wrong - wrong_attempts}")
    
    # Display guessed letters
    if guessed_letters:
        print(f"Letters guessed: {', '.join(sorted(guessed_letters))}")
    
    # Display word with guessed letters revealed
    display_word = ""
    for letter in word:
        if letter in guessed_letters:
            display_word += f"{Colors.GREEN}{letter}{Colors.ENDC} "
        else:
            display_word += "_ "
    print(f"\nWord: {display_word}")

def calculate_score(difficulty, word_length, wrong_attempts):
    """Calculate score based on difficulty, word length and wrong attempts"""
    difficulty_multiplier = {'easy': 1, 'medium': 2, 'hard': 3}
    base_score = word_length * 10
    penalty = wrong_attempts * 5
    return max(0, base_score - penalty) * difficulty_multiplier[difficulty]

def play_hangman():
    """Main game function"""
    # Load gameplay options
    category = select_category()
    difficulty = select_difficulty()
    difficulty_settings = difficulty_levels[difficulty]
    
    # Select a random word from the chosen category
    word = random.choice(word_categories[category])
    
    # Game variables
    guessed_letters = set()
    wrong_attempts = 0
    max_wrong = difficulty_settings['max_wrong']
    game_over = False
    hint_used = False
    
    # Main game loop
    while not game_over:
        display_game_state(word, guessed_letters, wrong_attempts, max_wrong, category)
        
        # Check if player has won
        if all(letter in guessed_letters for letter in word):
            print(f"\n{Colors.GREEN}{Colors.BOLD}Congratulations! You guessed the word: {word}{Colors.ENDC}")
            score = calculate_score(difficulty, len(word), wrong_attempts)
            print(f"Your score: {score}")
            
            # Check if it's a new high score
            if save_score(difficulty, score):
                print(f"{Colors.BOLD}New high score for {difficulty} difficulty!{Colors.ENDC}")
            
            game_over = True
            break
        
        # Check if player has lost
        if wrong_attempts >= max_wrong:
            print(f"\n{Colors.FAIL}{Colors.BOLD}Game Over! The word was: {word}{Colors.ENDC}")
            game_over = True
            break
        
        # Get player's guess
        print("\nOptions:")
        print("- Enter a letter to guess")
        
        if difficulty_settings['hint'] and not hint_used:
            print("- Enter '?' for a hint (can be used once)")
        
        print("- Enter '!' to quit the game")
        
        guess = input("\nYour choice: ").lower()
        
        # Handle special commands
        if guess == '!':
            print(f"{Colors.WARNING}Game aborted. The word was: {word}{Colors.ENDC}")
            time.sleep(2)
            return
        
        if guess == '?' and difficulty_settings['hint'] and not hint_used:
            hint_letter = get_hint(word, guessed_letters)
            print(f"{Colors.CYAN}Hint: Try the letter '{hint_letter}'{Colors.ENDC}")
            hint_used = True
            time.sleep(2)
            continue
        
        # Validate guess
        if not guess.isalpha() or len(guess) != 1:
            print(f"{Colors.WARNING}Please enter a single letter.{Colors.ENDC}")
            time.sleep(1)
            continue
        
        if guess in guessed_letters:
            print(f"{Colors.WARNING}You've already guessed that letter.{Colors.ENDC}")
            time.sleep(1)
            continue
        
        # Process valid guess
        guessed_letters.add(guess)
        
        if guess in word:
            print(f"{Colors.GREEN}Good guess!{Colors.ENDC}")
        else:
            wrong_attempts += 1
            print(f"{Colors.FAIL}Wrong guess!{Colors.ENDC}")
        
        time.sleep(1)
    
    # Ask to play again after game ends
    time.sleep(2)
    return input("\nPlay again? (y/n): ").lower().startswith('y')

def display_high_scores():
    """Display high scores for each difficulty level"""
    clear_screen()
    scores = load_scores()
    
    print(f"{Colors.HEADER}{Colors.BOLD}HIGH SCORES{Colors.ENDC}")
    print(f"{Colors.CYAN}===================={Colors.ENDC}")
    
    for difficulty, score in scores.items():
        print(f"{difficulty.capitalize()}: {score}")
    
    print(f"{Colors.CYAN}===================={Colors.ENDC}")
    input("\nPress Enter to continue...")

def main_menu():
    """Display main menu and handle user choices"""
    while True:
        clear_screen()
        print(f"{Colors.HEADER}{Colors.BOLD}ENHANCED HANGMAN{Colors.ENDC}")
        print(f"{Colors.CYAN}===================={Colors.ENDC}")
        print("1. Play Game")
        print("2. View High Scores")
        print("3. Exit")
        print(f"{Colors.CYAN}===================={Colors.ENDC}")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            play_again = True
            while play_again:
                play_again = play_hangman()
        elif choice == '2':
            display_high_scores()
        elif choice == '3':
            clear_screen()
            print(f"{Colors.GREEN}Thanks for playing Enhanced Hangman! Goodbye!{Colors.ENDC}")
            break
        else:
            print(f"{Colors.WARNING}Invalid choice. Please enter 1, 2, or 3.{Colors.ENDC}")
            time.sleep(1)

if __name__ == '__main__':
    display_welcome()
    main_menu()