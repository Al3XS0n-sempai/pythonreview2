import requests
import argparse


def create_main_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', default=8888, type=int)

    return parser


def normal_exit():
    ans = input('Are really want to exit? Input Y to exit, or N to continue. ')
    if ans == 'Y':
        print('Bye Bye!')
        exit()
    elif ans == 'N':
        print('Continue')
    else:
        print('Wrong input, so continue')


def ask_value(text):
    value = input(text)
    try:
        return int(value)
    except ValueError:
        print('Wrong value!!!!')
        return -1


def make_address(server_args):
    address = f'http://{server_args.host}:{server_args.port}'
    return address


def help_text():
    seq = ('Before game started:',
           'change_bet - change your bet',
           'place_bet - confirm your bet',
           'After game started:',
           'double - make Double',
           'more - take one more card',
           'view_my_cards - view your cards',
           'view_dealer_cards - view dealer cards',
           'all - enough cards',
           'Always:',
           'get_balance - find out the balance',
           'get_bet - find out the bet',
           'help - help',
           'exit - exit from game')
    return "\n".join(seq)


def before_game(address, cmd):
    if cmd == 'change_bet':
        new_bet = ask_value('Enter your new_bet: ')
        if new_bet >= 0:
            result = requests.post(address + '/change_bet', params={'new_bet': new_bet}).text
            if result != 'success':
                print(result)
    elif cmd == 'place_bet':
        result = requests.post(address + '/place_bet').text
        if result != 'success':
            print(result)
    else:
        print('Invalid command syntax. Enter help to get correct command syntax.')


def in_game(address, cmd):
    if cmd == 'view_dealer_cards':
        dealer_deck = requests.get(address + '/view_cards', params={'target': 'dealer'}).text
        print(dealer_deck)
    elif cmd == 'view_my_cards':
        my_deck = requests.get(address + '/view_cards', params={'target': 'player'}).text
        print(my_deck)
    elif cmd == 'double':
        result = requests.post(address + '/double').text
        if result != 'success':
            print(result)
    elif cmd == 'more':
        result = requests.post(address + '/more').text
        if result != 'success':
            print(result)
    elif cmd == 'all':
        result = requests.post(address + '/all').text
        print(result)
    else:
        print('Invalid command syntax. Enter help to get correct command syntax.')


def main():
    main_parser = create_main_parser()
    server_args = main_parser.parse_args()
    address = make_address(server_args)

    while True:
        try:
            cmd = input('Enter command: ')
            status = requests.get(address + '/get_status').text
            if cmd == 'help':
                print(help_text())
            elif cmd == 'get_balance':
                balance = requests.get(address + '/get_balance').text
                print('Your balance: ' + balance)
            elif cmd == 'get_bet':
                current_bet = requests.get(address + '/get_bet').text
                print('Your bet: ' + current_bet)
            elif cmd == 'exit':
                normal_exit()
            elif status == 'False':
                before_game(address, cmd)
            elif status == 'True':
                in_game(address, cmd)
        except KeyboardInterrupt:
            normal_exit()


if __name__ == '__main__':
    main()
