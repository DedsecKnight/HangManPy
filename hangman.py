from random import randint
from sys import stdout

class HangMan:

    GUESS_FLAG = "GUESS_FLAG"
    REQUEST_FLAG = "REQUEST_FLAG"

    HINT_COMMAND = "hint"
    ANSWER_COMMAND = "answer"
    FORFEIT_COMMAND = "forfeit"

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
        for dot in self.word_status: 
            stdout.write(dot + " ")
        stdout.write('\n\n')

    # Show hint
    def show_hint(self):
        print(f"Hint: {self.hint}")

    def invalid_input(self):
        print('Invalid input. Please try again')
    
    def submit_answer(self, answer):
        if (answer == self.word_list[self.word_idx][0]):
            self.remain_letter = 0
        else:
            self.chances = 0
    
    def confirm_action(self):
        while (True):
            prompt = input('Are you sure you want to do this action? This action is irreversible. (Y/N) ')
            
            if (prompt.lower() == 'y'):
                return True
            
            if (prompt.lower() == 'n'): 
                return False
            
            self.invalid_input()

    def get_final_answer(self):
        while (True):
            final_answer = input('Enter your final answer: ')
            if (self.confirm_action()):
                self.submit_answer(final_answer)
                return
    
    def forfeit(self):
        if (self.confirm_action()): self.chances = 0

    # Process request command from user
    def process_request(self, request):
        if (request == self.HINT_COMMAND):
            self.show_hint()
        elif (request == self.ANSWER_COMMAND):
            if (self.confirm_action()):
                self.get_final_answer()
        elif (request == self.FORFEIT_COMMAND):
            self.forfeit()
        else:
            self.invalid_input()
    
    def valid_character(self, guess_input):
        if (len(guess_input) != 1): return False
        return ord(guess_input) in range(65, 91) or ord(guess_input) in range(97, 123)

    # Get character input from player
    def get_character(self):
        guess_input = ''
        while (True):
            guess_input = input('Enter your guess: ')
            
            if (guess_input[0] == '!'):
                return (self.REQUEST_FLAG, guess_input[1:])
            
            if (not self.valid_character(guess_input)):
                self.invalid_input()
                continue
            
            guess_input = guess_input.lower()
            guess_ascii = ord(guess_input) - 97
            
            if (self.guessed[guess_ascii]):
                print('You have already guessed this character. Please try again\n')
                continue
            
            return (self.GUESS_FLAG, guess_input.lower())

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
            print(f"\nYou lose. The answer is {self.word_list[self.word_idx][0]}")

        self.play_again()
    
    # Ask whether player wants to play again
    def play_again(self):
        prompt_new_game = ""
        while (True):
            prompt_new_game = input('Do you want to play again? ')
            if (prompt_new_game.lower() == 'y' or prompt_new_game.lower() == 'n'): break
            self.invalid_input()
        
        if (prompt_new_game.lower() == 'n'): 
            exit(0)
            
        self.new_game()

    # Start game
    def new_game(self):
        self.reset()
        self.choose_word()

        while (self.chances and self.remain_letter):
            self.show_status()

            flag, data = self.get_character()

            if (flag == self.GUESS_FLAG):
                current_ascii = ord(data) - 97
                if (not self.character_list[current_ascii]): 
                    self.wrong_answer()
                else: 
                    self.correct_answer(current_character=data, current_ascii=current_ascii)
                self.guessed[current_ascii] = True
            else:
                self.process_request(data)
                
        
        self.game_result()


if __name__ == "__main__":
    hangman = HangMan('hangman.txt')
    hangman.new_game()