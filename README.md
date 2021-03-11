# HangMan 

A basic implementation of the game HangMan Python <br>

## Update
- New commands added. Check [Game Commands](#game-commands) for more details

## Setup Instruction
Create a file called hangman.txt, where wordlist will be stored <br>
For each line, write a word and a hint associated with that word, both of which are separated by the character '|' <br>
    e.g: "apple | a red fruit" <br>
Compile and execute hangman.py <br>
Enjoy the game <br>

## Game Instruction
Players will be given 5 chances to guess the secret word <br>
For each turn, players will enter a character that they believe will exist in the secret word <br>
After guessing, system will give out verdict of the answer <br>
If the character does not exist in the secret word, "wrong" verdict will be shown and players will lose 1 chance <br>
If the character exists, all occurences of that character will be revealed to that player <br>
Game will end when either players used up all their chances or all the letters are revealed <br>

## Game Commands:
**!hint**: Show hint (if provided) of the secret word <br>
**!forfeit**: Give up <br>
**!answer**: Submit answer before all letters are revealed <br>

