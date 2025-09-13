import random
import pygame
from pygame.locals import *
import math
import time
pygame.init()
#Play window
screen = pygame.display.set_mode((800, 600), RESIZABLE)
pygame.display.set_caption('UNO Game')
font = pygame.font.Font('freesansbold.ttf',35)
textx, texty = 0, 150
drtextx, drtexty = 200, 150
wtextx, wtexty = 200, 200
class Button():
    def __init__(self, x, y, image, scale, number):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.number = number
        self.clicked = False

    def draw(self):
        # mouse pos
        pos = pygame.mouse.get_pos()
        # check hover
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                return self.number
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image,(self.rect.x, self.rect.y))


class Scale():
    def __init__(self, image, x, y, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.cood = (x, y)

    def draw(self):
        screen.blit(self.image,(self.cood[0], self.cood[1]))


def show_cards(playerNo):
    x_pos = 0
    for i in players[playerNo - 1]:
        card_img = pygame.image.load(i + '.png')
        Scale(card_img, x_pos, 0, 0.3).draw()
        x_pos += 40

def card_chosen(playerNo):
    x_pos = 0
    n = 1
    for i in players[playerNo - 1]:
        card_img = pygame.image.load(i + '.png')
        card = Button(x_pos, 0,card_img, 0.3, n).draw()
        try:
            if not math.isnan(card):
                return card
            break
        except:
            pass
        x_pos += 40
        n += 1


def deck():
    deck = []
    colors = ['Red', 'Blue', 'Green', 'Yellow']
    vals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 'Reverse', 'DrawTwo', 'Skip']
    for color in colors:
        for val in vals:
            car = '{} {}'.format(color, val)
            deck.append(car)
            deck.append(car)
    random.shuffle(deck)
    return deck


def dealcard(amount, playerNo):
    for i in range(amount):
        players[playerNo - 1].append(Deck.pop(0))


def playerhand(playerNo):
    print(f"Player{playerNo}'s cards")
    count = 0
    for i in players[playerNo - 1]:
        count += 1
        print(f'{count}) {i}')


def color_choice():
    colors = ['Red', 'Blue', 'Green', 'Yellow']
    x = 1
    for i in range(4):
        print(f'{x}) {colors[i]}')
        x += 1
    chosen_color = int(input('Which color would you like to choose?: '))
    new_color = colors[chosen_color - 1]
    return new_color


def start_turn(color, val, playerno):
    # This will not allow a player to play, if the last card they have is a special card
    if len(players[playerno - 1]) == 1:
        if 'Wild' in players[playerno - 1][0] or 'Reverse' in players[playerno - 1][0] or 'DrawTwo' in players[playerno - 1][0] or 'Skip' in players[playerno - 1][0]:
            return False
        else:
            for card in players[playerno - 1]:
                if 'Wild' in card:
                    return True
                elif color in card:
                    return True
                elif val in card:
                    return True
            return False
    else:
        for card in players[playerno - 1]:
            if 'Wild' in card:
                return True
            elif color in card:
                return True
            elif val in card:
                return True
        return False


def can_play(chosen, playerNo, color, val):
    if 'Wild' in color:
        return True
    elif color in players[playerNo - 1][chosen - 1]:
        return True
    elif val in players[playerNo - 1][chosen - 1]:
        return True
    elif 'Wild' in players[playerNo - 1][chosen - 1]:
        return True
    else:
        return False

# this function tells if the card is a special or not
def game_start(card):
    if 'Wild' in card or 'Reverse' in card or 'DrawTwo' in card or 'Skip' in card:
        return False
    else:
        return True

def uno(declare, playerNo):
    if 'uno' in declare:
        pass
    else:
        dealcard(2,playerNo)
        print('You have not declared uno. Therefore you have drawn two cards')


def show_playerturn(x, y):
    turn = font.render(f'player {player_turn}', True, (0, 0, 0))
    screen.blit(turn, (x, y))


def drawn(x, y):
    dr = font.render('Drawn', True, (0, 0, 0))
    screen.blit(dr, (x, y))


def won(x, y):
    w = font.render(f'Player{player_turn} Won', True, (0, 0, 0))
    screen.blit(w, (x, y))

Deck = deck()
players = [[], []]
dealcard(7, 1)
dealcard(7, 2)
played = []
# This will ensure no special card will be drawn from the deck at the start
while not game_start(Deck[0]):
    Deck.append(Deck.pop(0))

played.append(Deck.pop(0))
player_turn = 1
play_direction = 1

played_split = played[0].split(' ', 1)
played_color_split = played_split[0]
if 'Wild' in played_color_split:
    played_val_split = 'any'
else:
    played_val_split = played_split[1]

playing = True

while playing:
    deck_img = pygame.image.load(played[-1] + '.png')
    screen.fill((0, 69, 69))
    show_playerturn(textx, texty)
    Scale(deck_img, 250, 250, 0.5).draw()
    show_cards(player_turn)
    pygame.display.update()
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            playing = False
        elif i.type == VIDEORESIZE:
            screen.blit(pygame.transform.scale(deck_img, i.dict['size']), (0, 0))
            pygame.display.update()
        elif i.type == VIDEOEXPOSE:  # handles window minimising/maximising
            screen.fill((0, 0, 0))
            screen.blit(pygame.transform.scale(deck_img, screen.get_size()), (0, 0))
            pygame.display.update()
        if start_turn(played_color_split, played_val_split, player_turn):
            if i.type == pygame.MOUSEBUTTONDOWN:
                chosen_card = card_chosen(player_turn)
                if not can_play(chosen_card, player_turn, played_color_split, played_val_split):
                    continue
                played.append(players[player_turn - 1].pop(chosen_card - 1))
                if len(players[player_turn - 1]) == 0:
                    playing = False
                    print(f'----------------------------------------Player{player_turn} Won----------------------------------------')
                    won(wtextx, wtexty)
                    pygame.display.update()
                    time.sleep(5)

                played_split = played[-1].split(' ', 1)
                played_color_split = played_split[0]
                played_val_split = played_split[1]

                if 'Wild' in played_color_split:
                    if 'color' in played_val_split:
                        played_color_split = color_choice()
                    else:
                        played_color_split = color_choice()
                        player_turn += play_direction
                        if player_turn == 3:
                            player_turn = 1
                        elif player_turn == 0:
                            player_turn = 2
                        dealcard(4, player_turn)
                elif 'Reverse' in played_val_split:
                    if len(players) == 2:
                        continue
                    else:
                        play_direction *= -1
                elif 'DrawTwo' in played_val_split:
                    player_turn += play_direction
                    if player_turn == 3:
                        player_turn = 1
                    elif player_turn == 0:
                        player_turn = 2
                    dealcard(2, player_turn)
                elif 'Skip' in played_val_split:
                    player_turn += play_direction
                    if player_turn > 2:
                        player_turn = 1
                    elif player_turn < 0:
                        player_turn = 2

                player_turn += play_direction
                if player_turn > 2:
                    player_turn = 1
                elif player_turn < 0:
                    player_turn = 2
        else:
            drawn(drtextx, drtexty)
            pygame.display.update()
            dealcard(1, player_turn)
            player_turn += play_direction
            time.sleep(1)
            if player_turn > 2:
                player_turn = 1
            elif player_turn < 0:
                player_turn = 2
