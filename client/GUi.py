import pygame
from pygame.locals import *
import requests
import argparse
import libs

pygame.init()


def create_main_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', default=8888, type=int)

    return parser


def input_value(screen):
    current_bet = ''
    flag = True
    while flag:
        screen.fill((0, 0, 0))
        title_font = pygame.font.Font(None, 36)
        text_font = pygame.font.SysFont('Calibri', 20)
        title = title_font.render('Enter your bet', 1, (255, 255, 255))
        bet = text_font.render(str(current_bet), 1, (255, 255, 255))
        screen.blit(title, (330, 10))
        screen.blit(bet, (20, 50))
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                exit()
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_1:
                    current_bet += '1'
                elif i.key == pygame.K_2:
                    current_bet += '2'
                elif i.key == pygame.K_3:
                    current_bet += '3'
                elif i.key == pygame.K_4:
                    current_bet += '4'
                elif i.key == pygame.K_5:
                    current_bet += '5'
                elif i.key == pygame.K_6:
                    current_bet += '6'
                elif i.key == pygame.K_7:
                    current_bet += '7'
                elif i.key == pygame.K_8:
                    current_bet += '8'
                elif i.key == pygame.K_9:
                    current_bet += '9'
                elif i.key == pygame.K_0:
                    current_bet += '0'
                elif i.key == pygame.K_BACKSPACE:
                    current_bet = current_bet[:-1]
                elif i.key == pygame.K_RETURN:
                    flag = False
        pygame.display.update()
    if current_bet == '':
        return '0'
    return current_bet


def error_text(screen, message):
    text_font = pygame.font.SysFont('Calibri', 20)
    text = text_font.render(message, 1, (255, 0, 0))
    screen.blit(text, (40, 700))


def info_text(screen, message):
    text_font = pygame.font.SysFont('Calibri', 20)
    text = text_font.render(message, 1, (0, 255, 0))
    screen.blit(text, (340, 500))


def print_info(screen, address):
    text_font = pygame.font.SysFont('Calibri', 20)
    balance = requests.get(address + '/get_balance').text
    current_bet = requests.get(address + '/get_bet').text
    status = requests.get(address + '/get_status').text
    my_deck = requests.get(address + '/view_cards', params={'target': 'player'}).text
    dealer_deck = requests.get(address + '/view_cards', params={'target': 'dealer'}).text

    balance_text = text_font.render('Balance: ' + balance, 1, (255, 255, 255))
    bet_text = text_font.render('Bet: ' + current_bet, 1, (255, 255, 255))
    status_text = text_font.render('In game: ' + status, 1, (255, 255, 255))
    my_text = text_font.render('Your deck: ' + str(my_deck), 1, (255, 255, 255))
    dealer_text = text_font.render('Dealer_deck: ' + str(dealer_deck), 1, (255, 255, 255))
    screen.blit(balance_text, (300, 50))
    screen.blit(bet_text, (300, 70))
    screen.blit(status_text, (300, 90))
    screen.blit(my_text, (300, 110))
    screen.blit(dealer_text, (300, 130))


def main():
    main_parser = create_main_parser()
    server_args = main_parser.parse_args()
    address = f'http://{server_args.host}:{server_args.port}'
    screen = pygame.display.set_mode((800, 800))
    error_message = ''
    game_result = ''
    while True:
        title_font = pygame.font.Font(None, 36)
        text_font = pygame.font.SysFont('Calibri', 20)

        title = title_font.render('Black Jack', 1, (255, 255, 255))
        screen.fill((0, 0, 0))
        screen.blit(title, (330, 10))
        print_info(screen, address)

        change_bet = libs.Button()
        place_bet = libs.Button()
        all = libs.Button()
        more = libs.Button()
        double = libs.Button()

        screen = change_bet.create_button(
                                            screen, (255, 255, 255),
                                            20, 50,
                                            100, 30, 5,
                                            'Change bet', (0, 0, 0))
        screen = place_bet.create_button(
                                            screen, (255, 255, 255),
                                            20, 100,
                                            100, 30, 5,
                                            'Place bet', (0, 0, 0))
        screen = all.create_button(
                                    screen, (255, 255, 255),
                                    20, 150,
                                    100, 30, 5,
                                    'All', (0, 0, 0))
        screen = more.create_button(
                                    screen, (255, 255, 255),
                                    20, 200,
                                    100, 30, 5,
                                    'More', (0, 0, 0))
        screen = double.create_button(
                                    screen, (255, 255, 255),
                                    20, 250,
                                    100, 30, 5,
                                    'Double', (0, 0, 0))

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                exit()
            if i.type == MOUSEBUTTONDOWN:
                if change_bet.pressed(pygame.mouse.get_pos()):
                    res = input_value(screen)
                    result = requests.post(address + '/change_bet', params={'new_bet': res}).text
                    if result != 'success':
                        error_message = result
                    else:
                        error_message = ''
                elif place_bet.pressed(pygame.mouse.get_pos()):
                    result = requests.post(address + '/place_bet').text
                    if result != 'success':
                        error_message = result
                    else:
                        error_message = ''
                    game_result = ''
                elif all.pressed(pygame.mouse.get_pos()):
                    result = requests.post(address + '/all').text
                    if result == 'You are not in game!':
                        error_message = result
                        game_result = ''
                    else:
                        game_result = result
                        error_message = ''
                elif more.pressed(pygame.mouse.get_pos()):
                    result = requests.post(address + '/more').text
                    if result != 'success':
                        if result == 'You are not in game!':
                            error_message = result
                            game_result = ''
                        else:
                            error_message = ''
                            game_result = result
                    else:
                        error_message = ''
                elif double.pressed(pygame.mouse.get_pos()):
                    result = requests.post(address + '/double').text
                    if result[0] == 'Y':
                        error_message = result
                        game_result = ''
                    else:
                        game_result = result
                        error_message = ''

        if game_result != '':
            info_text(screen, game_result)
        if error_message != '':
            error_text(screen, error_message)
        pygame.display.update()


if __name__ == '__main__':
    main()
