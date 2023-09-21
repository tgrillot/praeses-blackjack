import click
from pbj import Pbj

@click.group()
@click.pass_context
def cli(ctx):
    """
        Preses Blackjack
    """

    ctx.obj = Pbj()

@cli.command("playpbj")
@click.option('-p','--players',type=int,default=1,prompt='Enter the number of blackjack players:\n> ', help='The number players. Can be 1 to 4.')
@click.pass_context
def playpbj(ctx, players):
    ctx.obj.play(players)

@cli.command("deckCount")
@click.pass_context
def deckCount(ctx):
    click.echo(str(ctx.obj.deck.remaining))

if __name__ == '__main__':
    cli()