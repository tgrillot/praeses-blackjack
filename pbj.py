from deck import Deck
from player import Player
import click
from os.path import isfile
import json
from random import randint

class Pbj:

##################
#   Game Setup   #
##################

    def __init__(self,decks=None,newgame=False,continue_game=False,enable_betting=False):
        if not isfile('state.json') or newgame:
            data = {}
            data['prog'] = "New"
            data['decks'] = decks
            data['betting'] = enable_betting
            with open('state.json', 'w') as f:
                json.dump(data,f)
        self._read_state(continue_game)

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
                player.hand.append(self._eval_cut(self.deck.draw_card()))
            self.dealer.hand.append(self._eval_cut(self.deck.draw_card()))
            deal += 1

##################
#   Game State   #
##################

    def _read_state(self, continue_game=False):
        with open('state.json', 'r') as f:
            state = json.load(f)
        if state["prog"] == "New" or state["prog"] == "End" and not continue_game:
            self.prog = "New"
            self.decks = state["decks"]
            self.betting = state["betting"]
            self.deck = Deck(self.decks)
            self.dealer = Player()
            self.turn = 0
            self.round = 1
            return
        self.turn = state["turn"]
        self.prog = state["prog"]
        self.decks = state["decks"]
        self.betting = state["betting"]
        self.round = state["round"]
        self.deck = Deck(self.decks,state["deck"]["deck"])
        self.dealer = Player(state["dealer"])
        self.players = []
        for player in state["players"]:
            self.players.append(Player(player))
        if continue_game:
            self.prog = "Cont"
            self.round += 1
            self.turn = 0
            self.dealer.new_round_reset()
            for player in self.players:
                player.new_round_reset()

        
    def _write_state(self):
        with open('state.json', 'w') as f:
            json.dump(self, f, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def _finalize_bet_outcome(self):
        self._write_state()
        click.echo()
        click.echo("Player Winnings:")
        click.echo()
        for player in self.players:
            click.echo("Player " + str(self.players.index(player)+1) + " has won $" + str(int(player.winnings - player.losings)) + " in " + str(self.round) + " rounds.")

    def _display_state(self):
        if self._skip_if_player_nat():
            return
        click.echo("\u2665 \u2666 \u2663 \u2660 \u2665 \u2666 \u2663 \u2660 Praeses Blackjack \u2665 \u2666 \u2663 \u2660 \u2665 \u2666 \u2663 \u2660")
        click.echo()
        click.echo("Dealer's Hand:")
        click.echo(self.dealer.get_hand_ascii("d",self.turn,len(self.players)))
        if self.prog == "End":
            click.echo("Hand Value: " + str(self.dealer.total))
        if self.dealer.nat:
            click.echo("Blackjack!")
        if self.dealer.bust:
            click.echo("Bust!")
        click.echo()

        for player_id, player in enumerate(self.players):
            click.echo(f"Player {player_id + 1}'s Hand:")
            click.echo(player.get_hand_ascii("p",self.turn,len(self.players)))
            click.echo("Hand Value: " + str(player.total))
            if self.betting:
                click.echo("Bet: $" + str(player.bet))
            if player.nat:
                click.echo("Blackjack!")
            if player.bust:
                click.echo("Bust!")
            click.echo()

        
        if self.prog == "Cont":
            click.echo("Round " + str(self.round))
            click.echo(f"It's Player {self.turn}'s turn. Please choose whether to hit or stand.")
        elif self.prog == "End":
            click.echo("Round " + str(self.round) + " Outcome:")
            click.echo()
            self._eval_endgame()
        click.echo()
    
#######################
#   Game Evaluation   #
#######################

    def _eval_player_nat(self, player):
        if self.betting and player.nat and not self.dealer.nat:
            player.winnings += player.bet * 1.5
            click.echo("Player " + str(self.players.index(player)+1) + " scores a black jack and wins one and a half times the amount of their bet.")

    def _eval_hands(self):
        click.echo("Evaluating hands...")
        self.dealer.evaluate()
        if self.dealer.nat == True:
            self.prog = "End"
        for player in self.players:
            player.evaluate()
            self._eval_player_nat(player)

    def _skip_if_player_nat(self):
        if self.prog == "Cont":
            if self.players[self.turn - 1].nat:
                self.turn += 1
                self._eval_game()
                return True

    def _eval_game(self):
        if self.turn > len(self.players):
            self._dealer_play()
            self.prog = "End"
        self._write_state()
        self._display_state()

    def _eval_cut(self, card):
        if card["rank"] != 'C':
            return card
        click.echo("Cut card reached.")
        cards_in_Play = []
        for player in self.players:
            cards_in_Play += player.hand
        self.deck = Deck(self.decks)
        for in_play in cards_in_Play:
            self.deck.deck.pop(self.deck.deck.index(in_play))
        self.deck.shuffle()
        self.deck.cut(self._cut_prompt(),self.decks)
        card = self.deck.draw_card()
        return card

    def _eval_endgame(self):

        if self.dealer.nat == True:
            click.echo("The house wins with a Blackjack.")
            for player in self.players:
                bet_outcome = ""
                if player.nat == True:
                    if self.betting:
                        bet_outcome = " No chips are collected."
                    click.echo("Player " + str(self.players.index(player)+1) + " ties the house with a Blackjack." + bet_outcome)
                else:
                    if self.betting:
                        bet_outcome = " The house collects Player " + str(self.players.index(player)+1) + "'s bet."
                    click.echo("Player " + str(self.players.index(player)+1) + " loses." + bet_outcome)
                    player.losings += player.bet
            if self.betting:
                self._finalize_bet_outcome()
            return

        elif self.dealer.bust == True:
            click.echo("The house loses with a bust.")
        
        for player in self.players:
            bet_outcome = ""
            if player.bust == True:
                if self.betting:
                    bet_outcome = " The house collects Player " + str(self.players.index(player)+1) + "'s bet."
                click.echo("Player " + str(self.players.index(player)+1) + " loses with a bust." + bet_outcome)
                player.losings += player.bet
            elif player.total > self.dealer.total and player.total <= 21 or self.dealer.bust and not player.bust or player.nat and not self.dealer.nat:
                if self.betting and not player.nat:
                    bet_outcome = " The house pays Player " + str(self.players.index(player)+1) + " the value of their bet."
                elif self.betting and player.nat:
                    bet_outcome = " The house paid Player " + str(self.players.index(player)+1) + " one and a half times their bet when they scored a Blackjack."
                click.echo("Player " + str(self.players.index(player)+1) + " beats the house." + bet_outcome)
                if not player.nat:
                    player.winnings += player.bet
            elif player.total == self.dealer.total and player.total <= 21 and not player.nat:
                if self.betting:
                    bet_outcome = " No chips are collected."
                click.echo("Player " + str(self.players.index(player)+1) + " ties the house." + bet_outcome)
            elif player.total < self.dealer.total and player.total <= 21:
                if self.betting:
                    bet_outcome = " The house collects Player " + str(self.players.index(player)+1) + "'s bet."
                click.echo("The house beats Player " + str(self.players.index(player)+1) + "." + bet_outcome)
                player.losings += player.bet
        if self.betting:
            self._finalize_bet_outcome()

#################
#   Game Play   #
#################

    def _dealer_play(self):
        if self.dealer.total >= 17:
            return
        self.dealer.hand.append(self.deck.draw_card())
        self.dealer.evaluate()
        self._dealer_play()

    def _cut_prompt(self):
        cut = click.prompt('Dealer prompts player ' + str(randint(1,len(self.players))) + ' to cut the deck. Please enter a number between 0 and 5.',type=click.FloatRange(0,5))
        return cut

    def play(self, pcount, continue_game=False):
        if self.prog == "Cont" and not continue_game:
            self._display_state()
            return
        click.echo('Lets play some blackjack.')
        if not continue_game:
            self.players = self._generate_players(pcount)
            self.deck.shuffle()
            if self.decks > 1:
                self.deck.cut(self._cut_prompt(),self.decks)
        if self.betting:
            for player in self.players:
                player.bet = click.prompt('Dealer prompts player ' + str(self.players.index(player) + 1) + ' to place a bet.',type=click.IntRange(2,500))
        self._deal_cards()
        self.prog = "Cont"
        self.turn = 1
        self._eval_hands()
        self._eval_game()

    def hit(self):
        if self.prog in ["End","New"]:
            click.echo("Please use the 'play' command to start a new game or continue an existing one.")
            return
        pi = self.turn - 1
        self.players[pi].hand.append(self._eval_cut(self.deck.draw_card()))
        self.players[pi].evaluate()
        if self.players[pi].total >= 21:
            self.turn += 1
        self._eval_game()
    
    def stand(self):
        if self.prog in ["End","New"]:
            click.echo("Please use the 'play' command to start a new game or continue an existing one.")
            return
        self.turn += 1
        self._eval_game()