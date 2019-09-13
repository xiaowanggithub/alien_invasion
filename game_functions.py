
import sys

import pygame

from bullet import Bullet

from alien import Alien
from ship import Ship
from time import sleep

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,
                        bullets):
    '''响应按键和鼠标事件'''
    #监视鼠标和电脑事件
    for event in pygame.event.get():
        
        if event.type==pygame.QUIT:#鼠标点击关闭窗口
            filename='hight_score.txt'
            with open(filename,'w')as file_object:
                file_object.write(str(stats.high_score))
                
            sys.exit()#退出程序
            
            #监测按键
        elif event.type==pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, sb,screen, ship,aliens,stats, bullets)
                
               #监测松键
        elif event.type==pygame.KEYUP: 
            check_keyup_events(event,ship)
        
                #检测点击屏幕
        elif event.type==pygame.MOUSEBUTTONDOWN:#点击屏幕行为
            mouse_x,mouse_y=pygame.mouse.get_pos()#它返回一个元组，其中包含玩家单击时鼠标的x 和y 坐标
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,
                        bullets,mouse_x,mouse_y)
                        
def check_keydown_events(event, ai_settings, sb,screen, ship,aliens,stats, bullets):
    '''响应按键'''
                
                #按下右键时，飞船连续移动开关打开
    if event.key==pygame.K_RIGHT:
        ship.moving_right=True
                
                #按下左键时，飞船连续移动开关打开
    elif event.key==pygame.K_LEFT:
        ship.moving_left=True
        
    elif event.key==pygame.K_UP:
        ship.moving_top=True
        
    elif event.key==pygame.K_DOWN:
        ship.moving_bottom=True
        
    elif event.key==pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    
    elif event.key==pygame.K_q:
        filename='hight_score.txt'
        #记录最高分
        with open(filename,'w')as file_object:
            file_object.write(str(stats.high_score))
        
        sys.exit() 
           
    elif event.key==pygame.K_p:
        start_game(stats,sb,aliens,bullets,ai_settings,screen,ship)

    
def check_keyup_events(event,ship):
    '''响应松开'''
     #松开右键时，飞船连续移动开关关闭
    if  event.key==pygame.K_RIGHT:
        ship.moving_right=False
    #松开左键时，飞船连续移动开关关闭
    if  event.key==pygame.K_LEFT:
        ship.moving_left=False
        
    if event.key==pygame.K_UP:
        ship.moving_top=False
        
    if event.key==pygame.K_DOWN:
        ship.moving_bottom=False

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,
                        bullets,mouse_x,mouse_y):
    '''在玩家单击play按钮时开始新游戏'''
    #测试点是否在矩形内，前面需要一个rect对象，检测点是否在其内
    button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active: #如果游戏在运行点击play区域也不会重置信息                   
        start_game(stats,sb,aliens,bullets,ai_settings,screen,ship)



def start_game(stats,sb,aliens,bullets,ai_settings,screen,ship):
    '''开始游戏'''
        #隐藏光标
    pygame.mouse.set_visible(False)
        #重置游戏统计信息   
    ai_settings.initialize_dynamic_settings()
    stats.reset_stats()
    stats.game_active=True  
    
    #重置记分牌图像
    sb.prep_images()
        
        #清空外星人和子弹列表
    aliens.empty()
    bullets.empty()
        
        #创建一群外星人并让飞船居中
    create_fleet(ai_settings,screen,ship,aliens)
    #将底部飞船复位
    reset_ship(ship)
    
                    
  
def fire_bullet(ai_settings,screen,ship,bullets):
    '''如果子弹还没达到上限，就再发一颗子弹'''
    if len(bullets)<=ai_settings.bullets_allowed:
        new_bullet=Bullet(ai_settings, screen, ship)
        #创建一颗子弹并加入编组bullets中
        bullets.add(new_bullet)
        

            
def update_screen(ai_settings,screen,stats, sb, ship,aliens, 
            bullets,play_button):
    '''更新屏幕上的图像并切换到新屏幕'''
   
    #每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    check_aliens_died(bullets,aliens,stats,sb,ai_settings)
    #背景色填充屏幕
    #在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():#方法bullets.sprites() 返回一个列表，其中包含编组
                            #bullets 中的所有精灵的surface和rect。为在屏幕上绘制发射的所有子弹
        bullet.draw_bullet()#精灵对象用draw画
    
    ship.blitme()
    
    aliens.draw(screen)#在屏幕上绘制编组的每个外星人
    
    #显示得分
    sb.show_score()
    
    #如果活动处于非活动状态，就绘制play按钮
    if not stats.game_active:
        play_button.draw_button()#为了让按钮处于屏幕顶层，绘制完其他元素再绘制按钮
        
        
    #让最近绘制的屏幕可见
    pygame.display.flip()
    
def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    '''更新子弹位置，删除已消失的子弹'''
    #更新子弹位置
    bullets.update()
    
    #删除已消失子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom<=0:
            bullets.remove(bullet)
    checke_bullet_anlien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)
 
def checke_bullet_anlien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
    '''检查子弹和外星人的碰撞'''
    #检查是否有子弹击中了外星人
    #如果有，就删除相应的子弹和外星人
    collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)
    
    #与外星人碰撞的子弹都是字典collisions 中的一个键；而与每颗子弹相关的值都是一个列表，其中包含该子弹撞到的外星 人。
    if collisions:
        for aliens in collisions.values():#优化一颗子弹同时打到多个外星人记分
            stats.score+=ai_settings.alien_points* len(aliens)#为什么要乘外星人数量
            sb.prep_score()
            
        check_high_score(stats,sb)
        
    '''这行代码遍历编组bullets 中的每颗子弹，再遍历编组aliens 中的每个外星人。每当有子弹和外星人
    #的rect 重叠时，groupcollide() 就在它返回的字典中添加一 个键-值对。两个实参True 告诉
    #Pygame删除发生碰撞的子弹和外星人。（要模拟能够穿行到屏幕顶端的高能子弹——消灭它击中的每个外星
    #人，可将第一个布尔实参设置 为False ，并让第二个布尔实参为True 。这样被击中的外星人将消失，
    #但所有的子弹都始终有效，直到抵达屏幕顶端后消失。）'''
    if len(aliens)==0:
        #删除现有子弹
        bullets.empty()#方法empty（）删除编组余下所有精灵
        
        #整群外星人被消灭，提升等级
        start_new_level(sb,stats,ai_settings)
        #新建一群外星人
        create_fleet(ai_settings,screen,ship,aliens)

def start_new_level(sb,stats,ai_settings):
    '''提升游戏等级'''
    stats.level+=1
    sb.prep_level()
    #加快游戏节奏
    ai_settings.increase_speed()
            
def get_number_aliens_x(ai_settings,alien_width):
    '''计算每行可容纳多少外星人'''
    availble_space_x=ai_settings.screen_width-2*alien_width
    number_aliens_x=int(availble_space_x/(2*alien_width))#!!!!不打里面的括号会卡死
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    '''计算屏幕可容纳多少行外星人'''
    availble_space_y=(ai_settings.screen_height-(3*alien_height)-ship_height)
    number_rows=int(availble_space_y/(5*alien_height))#!!!!不打里面的括号会卡死
    return number_rows
    
def creat_alien(ai_settings,screen,aliens,alien_number,row_number):
    '''创建一个外星人并放在当前行'''
    alien=Alien(ai_settings,screen)

    alien_width=alien.rect.width
    alien.x=alien_width+2*alien.rect.width*alien_number#计算当前外星人，在x轴上的位置
    alien.rect.x=alien.x #把位置传递给rect目标
    alien.rect.y=3*alien.rect.height+3*alien.rect.height*row_number
    
    aliens.add(alien)#加当前外星人入外星人组
    
    
def create_fleet(ai_settings, screen, ship, aliens):
    '''创建外星人群'''
    #创建一个外星人，并计算一行可以容纳多少个外星人
    #外星人间距为外星人宽度
    alien=Alien(ai_settings,screen)
    number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows=get_number_rows(ai_settings, ship.rect.height,
        alien.rect.height)
    
    #创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
        #创建一个外星人并加入当前行
            creat_alien(ai_settings,screen,aliens,alien_number,row_number)

    #暂停
    sleep(1)

def check_fleet_edges(ai_settings, aliens):
    """如果有外星人到达边缘，请做出适当的反应."""
    for alien in aliens.sprites():
        if alien.check_edges(ai_settings):
            change_fleet_direction(ai_settings, aliens)
            break
        
def change_fleet_direction(ai_settings, aliens):
    """下移整个舰队，改变舰队的方向."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
        
    ai_settings.fleet_direction *= -1
            

def update_aliens(ai_settings,aliens,sb,screen,ship,stats,bullets):
    '''检查是否有外星人位于屏幕边缘，并更新外星人群中所有外星人的位置'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    #调用类的方法
    #实例名.方法名()
    
def anlens_ship_collision(ship,aliens,ai_settings,stats,screen,bullets,sb):
    '''检测外星人和飞船之间的碰撞'''
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets)#方法spritecollideany() 接受两个实参：一个精灵和一个编组。
                            #它检查编组是否有成员与精灵发生了碰撞，没有碰撞返回NONE，if不会执行
    check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets)
    
def ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets):
    '''响应被外星人撞到的飞船'''
    #r如果还有飞船
    if stats.ships_left>0:
        #将ship_left减1
        stats.ships_left-=1
        
        #更新记分牌
        sb.prep_ships()
    
    #清空外星人和子弹列表
        aliens.empty()
        bullets.empty()
    
    #创建一群新的外星人
        create_fleet(ai_settings,screen,ship,aliens)
    
    #将底部飞船复位
        reset_ship(ship)
    else:
        stats.game_active=False
        pygame.mouse.set_visible(True)#鼠标可见

def reset_ship(ship):
    '''将底部飞船复位'''
    ship.center_ship()
    ship.update()
    ship.blitme()
    
    
    
def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets):
    '''检查是否有外星人到达了屏幕底端'''
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():#一定要注意遍历精灵要加.sprites()
        if alien.rect.bottom>=screen_rect.bottom:
            #像被飞船撞到一样处理
            ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
            break
            
def check_high_score(stats,sb):
    '''检查是否诞生了新的最高分'''
    if stats.score>stats.high_score:
        stats.high_score=stats.score
        sb.prep_high_score()
    

def check_aliens_died(bullets,aliens,stats,sb,ai_settings):
    """检测杀死了多少个外星人，并计数"""
    if stats.level==5 :
        ai_settings.ship_speed_factor=28 #飞船的初始速度
        ai_settings.bullet_speed_factor=28  #子弹的初始速度
        ai_settings.alien_speed_factor=12
        
        
        sb.award_time()
        
    if stats.level==6 :
        ai_settings.ship_speed_factor=21 #飞船的初始速度
        ai_settings.bullet_speed_factor=21 #子弹的初始速度
        ai_settings.alien_speed_factor=7
        
        
        
        
                

    
    
    

    
