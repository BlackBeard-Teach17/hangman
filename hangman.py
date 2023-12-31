import random
import string
import re

class Hangman:
    def __init__(self) -> None:
        self.MAX_INCORRECT_GUESSES = 6
        self.hints_remaining = 2
        self.word_list = set(
            word.strip() for word in open("words.txt", mode="r")
            )
        self.target_word = random.choice(list(self.word_list))
        self.guessed_letters = set()
        self.correct_guess = ""
        self.wrong_guesses = 0
        self.correct_word_list = ['_'] * len(self.target_word)

    def play(self):
        print("Welcome to Hangman!!")
        while not self.game_over():
            self.draw_hangman(self.wrong_guesses)
            if len(self.correct_guess) == 0:
                print("Your word is:" + '_' * len(self.target_word))
            else:
                print(f"Your word is: {self.correct_guess}")
                
            print(f"Current guessed letters: {''.join(sorted(self.guessed_letters))}\n")
            
            player_guess = self.get_player_input()

            if player_guess in self.target_word:
                self.correct_guess = self.build_word(player_guess)
                print("Great guess!")
            else:
                print("Oops, incorrect guess")
                self.wrong_guesses += 1
                
            self.guessed_letters.add(player_guess)

        self.draw_hangman(self.wrong_guesses)
        if self.wrong_guesses == self.MAX_INCORRECT_GUESSES:
            print("Game Over!! You lost")
        else:
            print("Congratulations, You won")

        print(f"Your word was: {self.target_word}")
    
    def build_word(self, player_guess):
        letter_index = self.find_letter(player_guess, self.target_word)

        if len(letter_index) > 0:
            for i in letter_index:
                self.correct_word_list[int(i)] = player_guess
        correct_word = "".join(self.correct_word_list)

        return correct_word
    
    def find_letter(self, player_guess, target_word):
        matches = re.finditer(player_guess, target_word)
        indexes = []
        for match in matches:
            indexes.append(match.start())
        return indexes


    def game_over(self):
        if self.wrong_guesses == self.MAX_INCORRECT_GUESSES:
            return True
        return set(self.target_word) <= self.guessed_letters

    def draw_hangman(self, wrong_guesses):
        hanged_man = [
            """
            ------
            |   |
            |
            |
            |
            |
            |
            ======
            """,
            """
            ------
            |   |
            |   O
            |
            |
            |
            |
            ======
            """,
            """
            ------
            |   |
            |   O
            |   -
            |
            |
            |
            ======
            """,
            """
            ------
            |   |
            |   O
            |  /-
            |
            |
            |
            ======
            """,
            """
            ------
            |   |
            |   O
            |  /-\\
            |
            |
            |
            ======
            """,
            """
            ------
            |   |
            |   O
            |  /-\\
            |  /
            |
            |
            ======
            """,
            """
            ------
            |   |
            |   O
            |  /-\\
            |  / \\
            |
            |
            ======
            """
        ]
        print(hanged_man[wrong_guesses])


    def get_player_input(self):
        while True:
            player_input = input("Guess a letter or type 'hint' for a hint: ").lower()

            if player_input == "hint":
                # Check if hints are still available
                if self.hints_remaining <= 0:
                    print("You have no hints remaining.")
                    continue

                # Get and display a hint
                self.get_hint()
                continue

            # Validate input as usual
            if self.validate_input(player_input):
                return player_input

            print("Invalid input. Please enter a single lowercase letter that you haven't guessed before, or type 'hint' for a hint.")


    def validate_input(self, player_input):
        return (
            len(player_input) == 1
            and player_input in string.ascii_lowercase
            and player_input not in self.guessed_letters
        )
    
    def get_hint(self):
       
       if self.hints_remaining <= 0:
           print("You have no hints remaining.")
           return
       
       hint_letter = random.choice(list(set(self.target_word) - self.guessed_letters))
       self.hints_remaining -= 1

       print(f"Hint: The letter '{hint_letter}' is in the word.")

        

    def select_difficulty(self):
        pass

if __name__ == "__main__":
    Hangman().play()