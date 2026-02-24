import sys
import pygame
from pygame.sprite import Group
from setting import settings
from ship import ship
from alien import Alien
import game_function as gf
from Bubble import Bubbles
from game_stats import Gamestats
from button import Button
from score_board import Score_board
def run_game() :
    #( الشرح بصفحة 274)
    #يستوعب اللعبة ويصنع واجهة اللعبة

    pygame.init()
    ai_setting=settings()
    screen=pygame.display.set_mode((ai_setting.screen_width ,ai_setting.screen_height))

    pygame.display.set_caption("biscuit team")
    play_button=Button(ai_setting,screen,"START")

    stats=Gamestats(ai_setting)
    sb=Score_board(ai_setting,screen,stats)
    #make ship
    my_ship = ship(screen)
    my_bullets=Group()

    my_aliens=Group()
    # my_bubbles=Bubbles(screen)

    gf.creat_fleet(ai_setting,screen,my_ship,my_aliens)

#*************************************************

    number_of_bubbles = 10
    bubbles = []
    for _ in range(number_of_bubbles):
        bubbles.append(Bubbles(screen))

    # ---------------------------------------
    # البدأ ب لووب اللعبة لأنه مهم
    while True:


        gf.chek_events(ai_setting,screen,stats,sb,play_button,my_ship,my_aliens,my_bullets)

        if stats.game_active:

            my_ship.update()
            gf.update_aliens(ai_setting,stats,screen,my_ship,my_aliens,my_bullets)
            gf.update_bullets(ai_setting,screen,stats,sb,my_ship,my_aliens,my_bullets)

        gf.update_screen(ai_setting,screen,stats,sb,my_ship,my_aliens,my_bullets,bubbles,play_button)





run_game()