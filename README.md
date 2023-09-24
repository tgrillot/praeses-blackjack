# Praeses Blackjack (PBJ)

A simple command line Blackjack game written in Python and utilizing the [Click Framework](https://click.palletsprojects.com/en/8.1.x/).

## Installation Instructions
1. Ensure that python 3.11.5 is installed on your system.
2. Clone this repo to a working directory on your system.
3. Open a terminal in the repo directory.
4. Create a Python virtual environment by running `python -m venv venv`.
5. Activate the virtual environment by running `venv\scripts\activate`.
6. Run `pip install --editable .` (don't leave out the period).
7. Run `pbj` to view the main help file.

## Additional Features
* **Multiplayer**: Supports 2 to 7 players.
* **Multideck Game**: May be played with from 1 to 8 decks of cards.
* **Deck Cut**: In games with more than one deck, a random player will be prompted to cut the deck by entering a float value between 0 and 5 which results in a cut card being place in the deck approximately 19% to 24% before the end of the deck.
* **Reshuffle**: When the cut card is reached, the dealer will reshuffle the deck, prompt for another cut, and continue play.
* **Multiple Game Rounds**: Games may be continued beyond one round, allowing the same players to play with the same deck of cards.
* **Betting**: Games may be initiated with or without betting, and player winnings will be tracked accross rounds. Bets must be in whole dollar amounts from $2 to $500.

## Commands
The main command is `pbj`. Each command below must be run as a subcommand of pbj. eg. `pbj play` or `pbj hit`.

|Command|Switch|Description|Default|
|---|---|---|---|
|play||Start a new game or continue an existing one.||
||-p|Specify the number players in a new game, from 2 to 7.|2|
||-d|Specify the number of decks in the pack of a new game, from 1 to 8.|1|
||-b|Enable betting in a new game.|False|
||-n|Start a new game if there is a current game in progress.|False|
||-c|Continue the previous game with a new round.|False|
|hit||Indicate the current player would like to hit.||
|stand||Indicate the current player would like to stand.||

### Examples:
* `pbj play` Start a new game with 2 players, 1 deck, and betting turned off. Or if a round is in progress, display the state of the current round.  
* `pbj play -nbp 3 -d 4` Start a new game with 3 players, 4 decks and betting enabled.  
* `pbj play -c` Start a new round in a running game.  
* `pbj hit` Deal a card to the current player.
* `pbj stand` Progress play to the next player.

## Other Notes
* In the case when either a player or dealer scores 21 either naturally or note, play progresses to the next player automatically without the player scoring 21 needing to hit or stand.
* PBJ has been tested only on Windows 11. It has not been tested on MacOS or Linux.
* PBJ looks best, especially at higher numbers of players, when run in a maximized standalone terminal.