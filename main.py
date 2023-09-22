import click
from pbj import Pbj

@click.group()

def cli():
    """
        Praeses Blackjack
    """

@cli.command()
@click.option('-p','--players',type=click.IntRange(2,7),default=2, help='The number players in the game, from 2 to 7. ')
@click.option('-n','--newgame',is_flag=True, default=False, help='Start a new game if there is a current game in progress.')
@click.option('-d','--decks',type=click.IntRange(1,8),default=1, help='The number of decks in the pack, from 1 to 8.' )
def play(players,newgame,decks):
    """Start or continue a game of blackjack."""
    game = Pbj(decks,newgame)
    game.play(players)

@cli.command()
def hit():
    game = Pbj()
    game.hit()

@cli.command()
def stand():
    game = Pbj()
    game.stand()

if __name__ == '__main__':
    cli()