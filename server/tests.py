import unittest
import libs


class TestClasses(unittest.TestCase):
    def test_add_wrong_card(self):
        deck = libs.Deck()
        with self.assertRaises(TypeError):
            deck.add_card('g')
        with self.assertRaises(TypeError):
            deck.add_card(123)

    def test_add_card(self):
        deck = libs.Deck()
        deck.add_card('1')
        self.assertEqual(deck.data, ['1'])

    def test_get_card(self):
        deck = libs.Deck()
        deck.add_card('1')
        card = deck.get_card()
        self.assertEqual(card, '1')

    def test_shuffle_deck(self):
        deck1 = libs.Deck()
        deck2 = libs.Deck()
        deck1.add_card('1')
        deck1.add_card('2')
        deck1.shuffle_deck()
        deck2.add_card('1')
        deck2.add_card('2')
        self.assertEqual(set(deck1.data), set(deck2.data))

    def test_clear_deck(self):
        deck = libs.Deck()
        deck.add_card('K')
        deck.add_card('1')
        deck.add_card('1')
        deck.clear_deck()
        self.assertEqual(deck.data, [])

    def test_get_sum(self):
        deck = libs.Deck()
        deck.add_card('1')
        self.assertEqual(deck.get_sum(), 11)
        deck.add_card('K')
        self.assertEqual(deck.get_sum(), 21)

    def test_dealer_take_card(self):
        deck = libs.Deck()
        deck.add_card('J')
        dealer = libs.Dealer()
        dealer.take_card('J')
        self.assertEqual(deck.data, dealer.deck.data)

    def test_dealer_take_bad_card(self):
        dealer = libs.Dealer()
        dealer.take_card('J')
        with self.assertRaises(TypeError):
            dealer.take_card('g')

    def test_dealer_get_deck(self):
        dealer = libs.Dealer()
        dealer.take_card('J')
        self.assertEqual(dealer.deck.data, dealer.get_deck())

    def test_player_update_bet1(self):
        player = libs.Player()
        player.balance = 100
        player.update_bet(50)
        self.assertEqual(player.bet, 50)

    def test_player_update_bet2(self):
        player = libs.Player()
        player.balance = 100
        player.update_bet(50)
        self.assertEqual(player.balance, 50)

    def test_player_update_bad_bet1(self):
        player = libs.Player()
        player.balance = 100
        with self.assertRaises(TypeError):
            player.update_bet('123')

    def test_player_update_bad_bet2(self):
        player = libs.Player()
        player.balance = 100
        with self.assertRaises(ValueError):
            player.update_bet(123)

    def test_player_take_card(self):
        deck = libs.Deck()
        deck.add_card('J')
        player = libs.Player()
        player.take_card('J')
        self.assertEqual(deck.data, player.deck.data)

    def test_player_take_bad_card(self):
        player = libs.Player()
        player.take_card('J')
        with self.assertRaises(TypeError):
            player.take_card('g')

    def test_player_get_deck(self):
        player = libs.Player()
        player.take_card('J')
        self.assertEqual(player.deck.data, player.get_deck())
