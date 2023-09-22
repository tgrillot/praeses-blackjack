import click
from pbj import Pbj

@click.group()

def cli():
    """
        Praeses Blackjack
    """

@cli.command()
@click.option('-p','--players',type=int,default=1,prompt='Enter the number of blackjack players:\n> ', help='The number players. Can be 1 to 4.')
@click.option('-n','--newgame',is_flag=True, default=False, help='Start a new game if there is a current game in progress.')
def play(players,newgame):
    game = Pbj(newgame)
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