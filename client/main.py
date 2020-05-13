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


def make_request(address, request_name, request_args={}):
    request = f'{address}/{request_name}'
    args = ''
    for arg_name, arg_value in request_args.items():
        args += f'{arg_name}={arg_value}'
    if args:
        request += '?' + args
    return request


def help_text():
    return ('Before game started:\n'
            'change_bet - change your bet\n' +
            'place_bet - confirm your bet\n' +
            'After game started:\n'
            'double - make Double\n' +
            'more - take one more card\n' +
            'view_my_cards - view your cards\n' +
            'view_dealer_cards - view dealer cards\n' +
            'all - enough cards\n' +
            'Always:\n' +
            'get_balance - find out the balance\n' +
            'get_bet - find out the bet\n' +
            'help - help\n' +
            'exit - exit from game'
            )


def main():
    main_parser = create_main_parser()
    server_args = main_parser.parse_args()
    address = make_address(server_args)

    while True:
        try:
            cmd = input('Enter command: ')
            status = requests.get(make_request(address, 'get_status')).text
            if cmd == 'help':
                print(help_text())
            elif cmd == 'get_balance':
                balance = requests.get(make_request(address, 'get_balance')).text
                print('Your balance: ' + balance)
            elif cmd == 'get_bet':
                current_bet = requests.get(make_request(address, 'get_bet')).text
                print('Your bet: ' + current_bet)
            elif cmd == 'exit':
                normal_exit()
            elif status == 'False':
                if cmd == 'change_bet':
                    new_bet = ask_value('Enter your new_bet: ')
                    if new_bet >= 0:
                        result = requests.post(make_request(address, 'change_bet', {'new_bet': new_bet})).text
                        if result != 'success':
                            print(result)
                elif cmd == 'place_bet':
                    result = requests.post(make_request(address, 'place_bet')).text
                    if result != 'success':
                        print(result)
                else:
                    print('Invalid command syntax. Enter help to get correct command syntax.')
            elif status == 'True':
                if cmd == 'view_dealer_cards':
                    dealer_deck = requests.get(make_request(address, 'view_cards', {'target': 'dealer'})).text
                    print(dealer_deck)
                elif cmd == 'view_my_cards':
                    my_deck = requests.get(make_request(address, 'view_cards', {'target': 'player'})).text
                    print(my_deck)
                elif cmd == 'double':
                    result = requests.post(make_request(address, 'double')).text
                    if result != 'success':
                        print(result)
                elif cmd == 'more':
                    result = requests.post(make_request(address, 'more')).text
                    if result != 'success':
                        print(result)
                elif cmd == 'all':
                    result = requests.post(make_request(address, 'all')).text
                    print(result)
                else:
                    print('Invalid command syntax. Enter help to get correct command syntax.')
        except KeyboardInterrupt:
            normal_exit()


if __name__ == '__main__':
    main()
