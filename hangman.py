from random import randint
from sys import stdout

class HangMan:
    def __init__(self, filename):
        # Generate dictionary
        f = open(filename, 'r')
        self.word_list = [self.parse_line(line) for line in f]
        f.close()
    
    # Parse line from input file
    def parse_line(self, line):
        current_word = [word.strip() for word in line.strip().split('|')]
        if (len(current_word) == 1): current_word.append('')
        return tuple(current_word)

    # Choose a random word
    def choose_word(self):
        self.word_idx = randint(0, len(self.word_list)-1)
        word, hint = self.word_list[self.word_idx]
        self.remain_letter = len(word)
        if (hint): self.hint = hint
        for (i,c) in enumerate(word):
            character_ascii = ord(c.lower()) - 97
            self.character_list[character_ascii].append(i+1)
            self.word_status.append("_")
    
    # Reset game state
    def reset(self):
        self.word_idx = -1
        self.chances = 5
        self.word_status = []
        self.remain_letter = 0
        self.hint = "No hint available"
        self.character_list = [[] for i in range(26)]
        self.guessed = [False for i in range(26)]
    
    # Show guessed characters and remaining lives
    def show_status(self):
        print(f"{self.remain_letter} more letters to reveal the secret word. You have {self.chances} chance(s) remaining. ")
        print(f"Hint: {self.hint}")
        for dot in self.word_status: 
            stdout.write(dot + " ")
        stdout.write('\n\n')
    
    # Get character input from player
    def get_character(self):
        guess_input = ''
        while (True):
            guess_input = input('Enter your guess: ')
            if (len(guess_input) != 1):
                print("You entered more or less than 1 character. Please try again\n")
                continue
            if (ord(guess_input) not in range(65, 91) and ord(guess_input) not in range(97, 123)):
                print("You entered an invalid character. Please try again\n")
                continue
            guess_input = guess_input.lower()
            guess_ascii = ord(guess_input) - 97
            if (self.guessed[guess_ascii]):
                print('You have already guessed this character. Please try again\n')
                continue
            return (guess_input.lower(), ord(guess_input.lower()) - 97)

    # If given character does not exist in the secret word
    def wrong_answer(self):
        self.chances -= 1
        print('This character does not exist in the secret word. Please try again\n')
    
    # If given character exists in secret word
    def correct_answer(self, current_character, current_ascii):
        match_character = len(self.character_list[current_ascii])
        position_list = ", ".join([str(index) for index in self.character_list[current_ascii]])
        
        print(f'\nThere are {match_character} occurrences of {current_character.upper()} in position {position_list}\n')

        self.remain_letter -= match_character
        
        for position in self.character_list[current_ascii]:
            self.word_status[position-1] = current_character

    # Print game result
    def game_result(self):
        if (not self.remain_letter):
            print(f"\nCongratulation! You have found the word. The word is {self.word_list[self.word_idx][0]}")
        else:
            print(f"\nYou lose. The answer is {self.word_list[self.word_idx]}")

        self.play_again()
    
    # Ask whether player wants to play again
    def play_again(self):
        prompt_new_game = ""
        while (True):
            prompt_new_game = input('Do you want to play again? ')
            if (prompt_new_game.lower() == 'y' or prompt_new_game.lower() == 'n'): break
            print('Invalid input. Please try again')
        
        if (prompt_new_game.lower() == 'n'): 
            exit(0)
            
        self.new_game()

    # Start game
    def new_game(self):
        self.reset()
        self.choose_word()

        while (self.chances and self.remain_letter):
            self.show_status()
            current_guess, current_ascii = self.get_character()
            if (not self.character_list[current_ascii]): 
                self.wrong_answer()
            else: 
                self.correct_answer(current_character=current_guess, current_ascii=current_ascii)
            
            self.guessed[current_ascii] = True
        
        self.game_result()


if __name__ == "__main__":
    hangman = HangMan('hangman.txt')
    hangman.new_game()