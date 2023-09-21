class Player:
    def __init__(self, pre=None):
        if pre == None:
            self.hand = []
        else:
            self.hand = pre["hand"]

    def get_hand_ascii(self):
        ascii = [""] * 7
        for card in self.hand:
            ascii[0] += "┌───────┐ "
            ascii[1] += f"│ {card['abrev']:^2}    │ "
            ascii[2] += "│       │ "
            ascii[3] += f"│   {card['suit'][0]:<1}   │ "
            ascii[4] += "│       │ "
            ascii[5] += f"│    {card['abrev']:>2} │ "
            ascii[6] += "└───────┘ "
        ascii = "\n".join(ascii) + "\n"
        return ascii