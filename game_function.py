import sys
import pygame
from ship import ship
from setting import settings
from bullet import Bullet
from alien import Alien
from Bubble import Bubbles
from time import sleep



ai_setting=settings()
screen=pygame.display.set_mode((ai_setting.screen_width ,ai_setting.screen_height))
my_ship=ship(screen)

# my_bubbles=bubbles(screen)


#----------------------------------------------


def chek_keydown_events(event,ai_setting,screen,my_ship,my_bullets):
    # event from keybord, moving pos x and y (keydown) " make my code tidy and obvious
            if event.key==pygame.K_RIGHT:
                my_ship.moving_right=True

            elif event.key==pygame.K_LEFT:
                my_ship.moving_left=True

            elif event.key==pygame.K_UP:
                my_ship.moving_up=True

            elif event.key==pygame.K_DOWN:
                my_ship.moving_down=True

            elif event.key==pygame.K_SPACE:
               fire_bullet(ai_setting,screen,my_ship,my_bullets)

            elif event.key == pygame.K_q:
                sys.exit()

def fire_bullet(ai_setting,screen,my_ship,my_bullets):
    if len(my_bullets) < ai_setting.bullet_allowed:
        new_bullet = Bullet(ai_setting, screen, my_ship)
        my_bullets.add(new_bullet)


#------------------------------------------------
def chek_keyup_events(event,my_ship):

     if event.key == pygame.K_RIGHT:
         my_ship.moving_right = False

     elif event.key == pygame.K_LEFT:
         my_ship.moving_left = False

     elif event.key == pygame.K_UP:
         my_ship.moving_up = False

     elif event.key == pygame.K_DOWN:
         my_ship.moving_down = False





 #-----------------------------------------------


def chek_events(ai_setting,screen,stats,sb,play_button,my_ship,my_aliens,my_bullets):

    #respond to keypresses and mouse events
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        #event from keybord, moving pos x and y (keydown)
        elif event.type==pygame.KEYDOWN:
            chek_keydown_events(event,ai_setting,screen,my_ship,my_bullets)


        # event from keybord, moving pos x and y (keyup)
        elif event.type==pygame.KEYUP:
            chek_keyup_events(event,my_ship)

        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(ai_setting,screen,stats,sb,play_button,my_ship,my_aliens,my_bullets,mouse_x,mouse_y)

def check_play_button(ai_setting,screen,stats,sb,play_button,my_ship,my_aliens,my_bullets,mouse_x,mouse_y):

        button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)

        if button_clicked and not stats.game_active:
            ai_setting.initialize_dynamic_settings()
            pygame.mouse.set_visible(False)
            stats.reset_stats()
            stats.game_active=True

            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()

            my_ship.center_ship()

            my_aliens.empty()
            my_bullets.empty()

            creat_fleet(ai_setting,screen,my_ship,my_aliens)


#----------------------------------------------------


def update_screen(ai_setting,screen,stats,sb,my_ship,my_aliens,my_bullets,bubbles,play_button):
    #update images on the screen during each pass though the loop
    screen.fill(ai_setting.bg_color)
    sb.show_score()
    for bubble in bubbles:
        bubble.draw_bubble()

    my_ship.blitme()
    my_aliens.draw(screen)


    #redraw all bullets behind ship and aliens
    for bullet in my_bullets.sprites(): #404
        bullet.draw_bullet()


    if not stats.game_active:#****
        play_button.draw_button()

    pygame.display.flip()


def update_bullets(ai_sitting,screen,stats,sb,my_ship,my_aliens,my_bullets):
    my_bullets.update()

    # make the bullets disappeard

    for bullet in my_bullets.copy():
        if bullet.rect.bottom <= 0:
            my_bullets.remove(bullet)

    chek_bullet_alien_collisions(ai_sitting,screen,stats,sb,my_ship,my_aliens,my_bullets)

def chek_bullet_alien_collisions(ai_sitting,screen,stats,sb,my_ship,my_aliens,my_bullets):
    collisions=pygame.sprite.groupcollide(my_bullets,my_aliens,True,True)
    if len(my_aliens)==0:
        my_bullets.empty()
        ai_setting.increase_speed()
        creat_fleet(ai_sitting,screen,my_ship,my_aliens)
        stats.level+=1
        sb.prep_level()

    if collisions:
        for my_aliens in collisions.values():
            stats.score +=ai_setting.alien_points * len(my_aliens)
            sb.prep_score()
        chek_high_score(stats,sb)

#--------------------------------------------------
def chek_high_score(stats,sb):
    if stats.score>stats.high_score:
        stats.high_score=stats.score
        sb.prep_high_score()
def get_number_aliens_x(ai_setting,alien_width):
    avalibale_space_x = ai_setting.screen_width - 3* alien_width#here $
    number_aliens_x = int(avalibale_space_x / (2* alien_width))# and here
    return number_aliens_x

def creat_alien(ai_setting,screen,my_aliens,alien_number,row_number):
    alien = Alien(ai_setting, screen)
    alien_width=alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number #here
    alien.rect.x = alien.x
    alien.rect.y=alien.rect.height+1 *alien.rect.height*row_number #here to$
    my_aliens.add(alien)

def creat_fleet(ai_setting,screen,my_ship,my_aliens):
    alien=Alien(ai_setting,screen)
    number_aliens_x=get_number_aliens_x(ai_setting,alien.rect.width)
    number_rows=get_number_rows(ai_setting,my_ship.rect.height,alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
             creat_alien(ai_setting,screen,my_aliens,alien_number,row_number)

def get_number_rows(ai_setting,ship_height,alien_height):
     available_space_y=(ai_setting.screen_height-(3*alien_height)-ship_height)
     number_rows=int(available_space_y/(2*alien_height))
     return  number_rows


def change_fleet_direction(ai_setting,my_aliens):
    for alien in my_aliens.sprites():
        alien.rect.y+=ai_setting.fleet_drop_speed
    ai_setting.fleet_direction *= -1


def check_aliens_bottom(ai_setting,stats,screen,my_ship,my_aliens,my_bullets):
    screen_rect=screen.get_rect()
    for alien in my_aliens.sprites():
        if alien.rect.bottom >=screen_rect.bottom:
            ship_hit(ai_setting, stats, screen, my_ship, my_aliens, my_bullets)
            break

def ship_hit(ai_setting,stats,screen,my_ship,my_aliens,my_bullets):

    if stats.ship_left >0:

        stats.ship_left-=1

        my_aliens.empty()
        my_bullets.empty()

        creat_fleet(ai_setting,screen, my_ship, my_aliens)
        my_ship.center_ship()

        sleep(0.5)

    else:
        stats.game_active=False
        pygame.mouse.set_visible(True)
def update_aliens(ai_setting,stats,screen,my_ship,my_aliens,my_bullets):
    check_fleet_edges(ai_setting,my_aliens)
    my_aliens.update()

    if pygame.sprite.spritecollideany(my_ship,my_aliens):
        ship_hit(ai_setting,stats,screen,my_ship,my_aliens,my_bullets)
    check_aliens_bottom(ai_setting, stats, screen, my_ship, my_aliens, my_bullets)

def check_fleet_edges(ai_setting,my_aliens):
    for alien in my_aliens.sprites():
        if alien.check_edges():
             change_fleet_direction(ai_setting,my_aliens)
             break




