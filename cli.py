import click
from pbj import Pbj

@click.group()
def cli():
    """
        Preses Blackjack
    """

@cli.command()
@click.option('-p','--players',type=int,default=1,prompt='Enter the number of blackjack players:\n> ', help='The number players. Can be 1 to 4.')
def playpbj(players):
    if players > 4:
        click.echo('Too many players, please enter a smaller number:\n> ')
    elif players < 1:
        click.echo('Not enough players to play. Game over.')
        return
    pbj = Pbj(players)


if __name__ == '__main__':
    cli()