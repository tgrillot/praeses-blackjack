from deck import Deck
from player import Player
import click
from os.path import isfile
import json

class Pbj:

##################
#   Game Setup   #
##################

    def __init__(self,newgame=False):
        if not isfile('state.json') or newgame:
            data = {}
            data['prog'] = "New"
            with open('state.json', 'w') as f:
                json.dump(data,f)
        self._read_state()

    def _generate_players(self, pcount):
        players = []
        for i in range(pcount):
            player = Player()
            players.append(player)
        return players

    def _deal_cards(self):
        click.echo('Dealing cards...')
        deal = 0
        while deal < 2:
            for player in self.players:
                player.hand.append(self.deck.draw_card())
            self.dealer.hand.append(self.deck.draw_card())
            deal += 1

##################
#   Game State   #
##################

    def _read_state(self):
        with open('state.json', 'r') as f:
            state = json.load(f)
        if state["prog"] == "New" or state["prog"] == "End":
            self.prog = "New"
            self.deck = Deck()
            self.dealer = Player()
            self.turn = 0
            return
        self.turn = state["turn"]
        self.prog = state["prog"]
        self.deck = Deck(state["deck"]["deck"])
        self.dealer = Player(state["dealer"])
        self.players = []
        for player in state["players"]:
            self.players.append(Player(player))
        
    def _write_state(self):
        with open('state.json', 'w') as f:
            json.dump(self, f, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def _display_state(self):
        self._eval_player_nat()
        click.echo("------------------ Praeses Blackjack ------------------")
        click.echo()
        click.echo("Dealer's Hand:")
        click.echo(self.dealer.get_hand_ascii("d",self.turn,len(self.players)))
        if self.prog == "End":
            click.echo("Hand Value: " + str(self.dealer.total))
        if self.dealer.nat == True:
            click.echo("Natural 21!")
        if self.dealer.bust == True:
            click.echo("Bust!")
        click.echo()

        for player_id, player in enumerate(self.players):
            click.echo(f"Player {player_id + 1}'s Hand:")
            click.echo(player.get_hand_ascii("p",self.turn,len(self.players)))
            click.echo("Hand Value: " + str(player.total))
            if player.nat == True:
                click.echo("Natural 21!")
            if player.bust == True:
                click.echo("Bust!")
            click.echo()

        if self.prog == "Cont":
            click.echo(f"It's Player {self.turn}'s turn. Please choose whether to hit or stand.")
        elif self.prog == "End":
            self._eval_endgame()
        click.echo()
    
#######################
#   Game Evaluation   #
#######################

    def _eval_hands(self):
        click.echo("Evaluating hands...")
        self.dealer.evaluate()
        if self.dealer.nat == True:
            self.prog = "End"
        for player in self.players:
            player.evaluate()

    def _eval_player_nat(self):
        if self.prog == "Cont":
            if self.players[self.turn - 1].nat:
                self.turn += 1
                self._eval_game()

    def _eval_game(self):
        if self.turn > len(self.players):
            self._dealer_play()
            self.prog = "End"
        self._write_state()
        self._display_state()

    def _eval_endgame(self):
        click.echo("Endgame:")

        if self.dealer.nat == True:
            click.echo("The house wins with a natural 21.")
            for player in self.players:
                if player.nat == True:
                    click.echo("Player " + str(self.players.index(player)+1) + " ties the house with a natural 21.")
                else:
                    click.echo("Player " + str(self.players.index(player)+1) + " loses.")
            return
        elif self.dealer.bust == True:
            click.echo("The house loses with a bust.")
        
        for player in self.players:
            if player.bust == True:
                click.echo("Player " + str(self.players.index(player)+1) + " loses with a bust.")
            elif player.total > self.dealer.total and player.total <= 21 or self.dealer.bust and not player.bust:
                click.echo("Player " + str(self.players.index(player)+1) + " beats the house.")
            elif player.total == self.dealer.total and player.total <= 21:
                click.echo("Player " + str(self.players.index(player)+1) + " ties the house.")
            elif player.total < self.dealer.total and player.total <= 21:
                click.echo("The house beats Player " + str(self.players.index(player)+1) + ".")

#################
#   Game Play   #
#################

    def _dealer_play(self):
        if self.dealer.total >= 17:
            return
        self.dealer.hand.append(self.deck.draw_card())
        self.dealer.evaluate()
        self._dealer_play()

    def play(self, pcount, ):
        if self.prog == "Cont":
            self._display_state()
            return
        click.echo('Lets play some blackjack.')
        self.players = self._generate_players(pcount)
        self.deck.shuffle()    
        self._deal_cards()
        self.prog = "Cont"
        self.turn = 1
        self._eval_hands()
        self._eval_game()

    def hit(self):
        if self.prog in ["End","New"]:
            click.echo("Please use the 'play' command to start a new game.")
            return
        pi = self.turn - 1
        self.players[pi].hand.append(self.deck.draw_card())
        self.players[pi].evaluate()
        if self.players[pi].total >= 21:
            self.turn += 1
        self._eval_game()
    
    def stand(self):
        if self.prog in ["End","New"]:
            click.echo("Please use the 'play' command to start a new game.")
            return
        self.turn += 1
        self._eval_game()