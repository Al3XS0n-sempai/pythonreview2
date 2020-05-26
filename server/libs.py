from random import shuffle

LIMIT = 21


class Deck:
    def __init__(self):
        self.data = []
        self.to_num = {}
        self.char_cards = ['J', 'Q', 'K', 'A']
        self.possible_cards = []
        self.possible_cards.extend(self.char_cards)
        self.possible_cards.extend([str(i) for i in range(2, 11)])
        for i in self.possible_cards:
            if not (i in self.char_cards):
                self.to_num[i] = int(i)
            elif i == 'A':
                self.to_num[i] = 1
            else:
                self.to_num[i] = 10

    def add_card(self, card):
        if not(isinstance(card, str) and self.possible_cards.count(card)):
            raise TypeError('Wrong type of card!')
        self.data.append(card)

    def get_card(self):
        return self.data.pop()

    def shuffle_deck(self):
        shuffle(self.data)

    def clear_deck(self):
        self.data = []

    def get_sum(self):
        result = 0
        count_of_one = 0
        for i in self.data:
            if i != 'A':
                result += self.to_num[i]
            else:
                count_of_one += 1
        min_result = result + count_of_one
        max_result = result + 11 * (count_of_one > 0) + max(count_of_one - 1, 0)
        if max_result > 21:
            return min_result
        return max_result

    def fill_deck(self):
        self.clear_deck()
        self.data = 4 * self.possible_cards


class Dealer:
    def __init__(self):
        self.deck = Deck()

    def get_deck(self):
        return self.deck.data

    def take_card(self, card):
        self.deck.add_card(card)


class Player:
    def __init__(self, start_balance=10000):
        self.deck = Deck()
        self.balance = start_balance
        self.bet = 0
        self.in_game = False

    def update_bet(self, new_bet):
        if not isinstance(new_bet, int):
            raise TypeError
        if new_bet > self.balance:
            raise ValueError
        self.balance += self.bet
        self.bet = new_bet
        self.balance -= self.bet

    def get_deck(self):
        return self.deck.data

    def take_card(self, card):
        self.deck.add_card(card)
