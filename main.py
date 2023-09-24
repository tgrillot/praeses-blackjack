import click
from pbj import Pbj
from extend_click import MutExOption

@click.group()

def cli():
    """
        \u2665 \u2666 \u2663 \u2660 Praeses Blackjack \u2665 \u2666 \u2663 \u2660

        Play Blackjack in the command line.
    """

@cli.command()
@click.option('-p','--players',type=click.IntRange(2,7),default=2, help='The number players in the game, from 2 to 7.')
@click.option('-d','--decks',type=click.IntRange(1,8),default=1,help='The number of decks in the pack, from 1 to 8.' )
@click.option('-b','--enable_betting',is_flag=True,default=False,help='Enable betting in a new game.')
@click.option('-n','--newgame',is_flag=True,default=False,cls=MutExOption,mut_ex=["continue"],help='Start a new game if there is a current game in progress.')
@click.option('-c','--continue_game',is_flag=True,default=False,cls=MutExOption,mut_ex=["newgame"], help='Continue the previous game with a new round.')
def play(players,newgame,decks,continue_game,enable_betting):
    """
    Start or continue a game of blackjack.

    A game round in progress will be continued automatically with no options. If a game round has ended, a new game will be started by default if the continue_game argument is not used. In the case of either continuing a round, or continuing a game with a new round, the players, decks, and enable_betting options will not have any effect as these will have been already set for the current game.    
    """
    game = Pbj(decks,newgame,continue_game,enable_betting)
    game.play(players,continue_game)

@cli.command()
def hit():
    """Indicate the current player would like to hit."""
    game = Pbj()
    game.hit()

@cli.command()
def stand():
    """Indicate the current player would like to stand."""
    game = Pbj()
    game.stand()

if __name__ == '__main__':
    cli()