from Sapir.enum import CardType


class Card:
    def __init__(self, card_type: CardType, color=None, number=None):
        self.card_type = card_type
        self.color = color
        self.number = number

    @classmethod
    def regular_card(cls, color, number):
        return cls(CardType.REGULAR_CARD, color, number)

    @classmethod
    def changes_color_card(cls):
        return cls(CardType.CHANGES_COLOR)

    @classmethod
    def stop_card(cls, color):
        return cls(CardType.STOP, color)

    @classmethod
    def changes_direction_card(cls, color):
        return cls(CardType.CHANGES_DIRECTION, color, None)

    @classmethod
    def plus_two_card(cls, color):
        return cls(CardType.PLUS_TWO, color, None)

    @classmethod
    def plus_card(cls, color):
        return cls(CardType.PLUS, color, None)

    def __eq__(self, card):
        return self.card_type == card.card_type and self.color == card.color and self.number == card.number

    def __str__(self):
        if self.card_type == CardType.REGULAR_CARD:
            return f'({self.color} {self.number})'
        elif not self.color:
            return f'({self.card_type.name})'
        else:
            return f'({self.color} {self.card_type.name})'

