class Player:
    def __init__(self, pre=None):
        if pre == None:
            self.hand = []
            self.bust = False
            self.nat = False
            self.total = 0
            self.bet = 0
            self.winnings = 0
            self.losings = 0
        else:
            self.hand = pre["hand"]
            self.bust = pre["bust"]
            self.nat = pre["nat"]
            self.total = pre["total"]
            self.bet = pre["bet"]
            self.winnings = pre["winnings"]
            self.losings = pre["losings"]

    def evaluate(self):
        total = 0
        aces = 0
        for card in self.hand:
            if card["rank"] == 'A':
                aces += 1
            else:
                total += card["value"]
        while aces > 0:
            if total + 11 <=21:
                total += 11
            else:
                total += 1
            aces -= 1
        self.total = total
        if total > 21:
            self.bust = True
        if len(self.hand) == 2 and total == 21:
            self.nat = True

    def get_hand_ascii(self, ptype, turn, pcount):
        hidden = False
        if ptype == "d" and turn <= pcount:
            hidden = True
        ascii = [""] * 7
        for card in self.hand:
            if self.hand.index(card) > 0 and hidden and not self.nat:
                suit = "?"
                rank = " "
            else:
                suit = card['suit']
                rank = card['rank']
            ascii[0] += "┌───────┐ "
            ascii[1] += f"│ {rank:^2}    │ "
            ascii[2] += "│       │ "
            ascii[3] += f"│   {suit}   │ "
            ascii[4] += "│       │ "
            ascii[5] += f"│    {rank:>2} │ "
            ascii[6] += "└───────┘ "
        ascii = "\n".join(ascii)
        return ascii