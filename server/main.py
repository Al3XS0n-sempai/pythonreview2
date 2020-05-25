from flask import Flask
from flask import request
import configparser
import argparse
import libs

app = Flask('BlackJack')
deck = libs.Deck()
dealer = libs.Dealer()
player = libs.Player()
config = configparser.ConfigParser()
config.read('settings.ini')


def create_main_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='::')
    parser.add_argument('--port', default=8888, type=int)
    return parser


@app.route('/change_bet', methods=['POST'])
def change_bet():
    arg = int(request.args['new_bet'])
    try:
        new_bet = int(arg)
    except ValueError:
        return 'Wrong value!'
    if player.balance + player.bet < new_bet:
        return 'You do not have enough money!'
    player.update_bet(new_bet)
    return 'success'


@app.route('/place_bet', methods=['POST'])
def place_bet():
    start_game()
    return 'success'


@app.route('/view_cards', methods=['GET'])
def view_cards():
    target = request.args['target']
    if target == 'dealer':
        return str(dealer.get_deck())
    elif target == 'player':
        return str(player.get_deck())
    else:
        return 'Wrong target!'


@app.route('/get_balance', methods=['GET'])
def get_balance():
    return str(player.balance)


@app.route('/get_status', methods=['GET'])
def get_status():
    return str(player.in_game)


@app.route('/get_bet', methods=['GET'])
def get_bet():
    return str(player.bet)


@app.route('/double', methods=['POST'])
def double():
    if not player.in_game:
        return 'You are not in game!'
    if player.balance < player.bet:
        return 'You do not have enough money!'
    player.update_bet(2 * player.bet)
    card = deck.get_card()
    player.take_card(card)
    return 'Doubled! ' + all_in_game()


@app.route('/more', methods=['POST'])
def more():
    if not player.in_game:
        return 'You are not in game!'
    card = deck.get_card()
    player.deck.add_card(card)
    if player.deck.get_sum() > libs.LIMIT:
        return all_in_game()
    return 'success'


@app.route('/all', methods=['POST'])
def all_in_game():
    if player.in_game:
        result = who_is_win()
    else:
        result = 'You are not in game!'
    return result


def start_game():
    player.in_game = True
    player.deck.clear_deck()
    dealer.deck.clear_deck()
    deck.fill_deck()
    deck.shuffle_deck()
    for i in range(2):
        dealer_card = deck.get_card()
        player_card = deck.get_card()
        player.take_card(player_card)
        dealer.take_card(dealer_card)


def answer(res):
    return config.get('Phrases', res)


def who_is_win():
    dealer_sum = dealer.deck.get_sum()
    player_sum = player.deck.get_sum()
    config.set('Phrases', 'player_sum', str(player_sum))
    config.set('Phrases', 'dealer_sum', str(dealer_sum))
    with open('settings.ini', 'w') as config_file:
        config.write(config_file)
    if player_sum > libs.LIMIT:
        if dealer_sum <= libs.LIMIT:
            lost()
            return answer('win')
        else:
            draw()
            return answer('draw')
    else:
        if dealer_sum > libs.LIMIT or dealer_sum < player_sum:
            win()
            return answer('win')
        elif dealer_sum == player_sum:
            draw()
            return answer('draw')
        else:
            lost()
            return answer('lost')


def lost():
    player.in_game = False
    player.bet = 0


def win():
    player.in_game = False
    player.balance += 2 * player.bet
    player.bet = 0


def draw():
    player.in_game = False
    player.balance += player.bet
    player.bet = 0


def main():
    main_parser = create_main_parser()
    current_server = main_parser.parse_args()
    app.run(current_server.host, port=current_server.port)


if __name__ == '__main__':
    main()
