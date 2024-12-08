import random
import requests

class HangmanGame:
    def __init__(self):
        # backupwords
        self.words = ['python', 'hangman', 'challenge', 'programming', 'developer']
        
        try:
            # API Fetch for a random word
            url = "https://random-word-api.herokuapp.com/word"
            response = requests.get(url)

            if response.status_code == 200:
                self.word = response.json()[0].lower()
            else:
                # if API Fails
                self.word = random.choice(self.words)
        except Exception:
            # fallback
            self.word = random.choice(self.words)

        # init game 
        self.guessed_word = ['_' for _ in range(len(self.word))]
        self.attempts_left = 6
        self.wrong_guesses = 0
        self.hints_used = 0
        self.guessed_characters = []
        self.hint_available = False

        # ASCII art for game 
        self.hangman_stages = [
            r"""
             ------
             |    |
                  |
                  |
                  |
                  |
            ========
            """,
            r"""
             ------
             |    |
             O    |
                  |
                  |
                  |
            ========
            """,
            r"""
             ------
             |    |
             O    |
             |    |
                  |
                  |
            ========
            """,
            r"""
             ------
             |    |
             O    |
            /|    |
                  |
                  |
            ========
            """,
            r"""
             ------
             |    |
             O    |
            /|\   |
                  |
                  |
            ========
            """,
            r"""
             ------
             |    |
             O    |
            /|\   |
            /     |
                  |
            ========
            """,
            r"""
             ------
             |    |
             O    |
            /|\   |
            / \   |
                  |
            ========
            """
        ]

    def draw_hangman(self):
        """draw the current state of the hangman."""
        print(self.hangman_stages[self.wrong_guesses])

    def correct_guess(self, guess): 
        """update the guessed word with correctly guessed letters."""
        for i in range(len(self.word)):
            if self.word[i] == guess:
                self.guessed_word[i] = guess 

    def provide_hint(self):
        """provide a hint to the player."""
        # check if hint is available and hasn't been used before (only one hint per game pal)
        if self.wrong_guesses >= 3 and self.hints_used < 1:
            # Find unguessed letters
            unguessed_letters = [
                letter for letter in set(self.word) 
                if letter not in self.guessed_characters
            ]
            
            if unguessed_letters:
                # choose a random unguessed letter
                hint_letter = random.choice(unguessed_letters)
                
                # reveal all instances of this letter 
                self.correct_guess(hint_letter)
                
                self.hints_used += 1
                print(f"HINT: The letter '{hint_letter}' is in the word!")
                print(f"Updated word: {''.join(self.guessed_word)}")
            else:
                print("No more hints available. All letters are revealed!")
        elif self.hints_used >= 1:
            print("You have already used your hint!")
        else:
            print("Hints are only available after 3 wrong guesses.")

    def start_game(self):
        """Main game loop."""
        print("Welcome to Hangman!")
        print(f"The word has {len(self.word)} letters.")

        while self.attempts_left > 0:
            # draw current game state
            self.draw_hangman()
            print(f"Word: {''.join(self.guessed_word)}")
            print(f"Attempts left: {self.attempts_left}")
            print(f"Wrong guesses: {self.wrong_guesses}")
            print(f"Guessed letters: {', '.join(self.guessed_characters)}")

            # hint availability message
            if self.wrong_guesses >= 3 and self.hints_used == 0:
                print("\n Hint is now available! Type 'hint' to get help.")

            # grab player input
            guess = input("Guess a letter (or type 'hint'): ").lower()

            # input validation
            if not guess.isalpha() or len(guess) != 1 and guess != 'hint':
                print("Invalid input. Please enter a single letter.")
                continue

            # handle hint
            if guess == 'hint':
                self.provide_hint()
                continue

            # already guessed letter check
            if guess in self.guessed_characters:
                print("You already guessed that letter!")
                continue

            # add to guessed characters
            self.guessed_characters.append(guess)

            # guess logic
            if guess in self.word:
                self.correct_guess(guess)
                print(f"Correct guess! {''.join(self.guessed_word)}")
                
                # check for win condition
                if '_' not in self.guessed_word:
                    print(f"\n Congratulations! You've guessed the word: {self.word}")
                    break
            else:
                self.wrong_guesses += 1
                self.attempts_left -= 1
                print(f"Wrong guess! You have {self.attempts_left} attempts left.")

        # game over condition
        if self.attempts_left == 0:
            print(f"\n Game over! The word was: {self.word}")

def main():
    """Start a new game of Hangman."""
    while True:
        game = HangmanGame()
        game.start_game()
        
        # Ask if player wants to play again
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != 'yes':
            print("Thanks for playing Hangman!")
            break

if __name__ == "__main__":
    main()