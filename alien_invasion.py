# -*- coding: utf-8 -*-

import io

import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
import pygame

from settings import Settings

from ship import Ship

import game_functions as gf

from pygame.sprite import Group

from alien import Alien

from game_stats import GameStats

from button import Button

from scoreboard import Scoreboard
def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings=Settings()
    screen=pygame.display.set_mode(
    (ai_settings.screen_width,ai_settings.screen_height))#创建一个窗口
    pygame.display.set_caption('Alien Invasion')#窗口名
    
    #创建play按钮
    play_button=Button(ai_settings,screen,'play')
    
    #创建一个用于储存游戏统计信息的实例
    stats=GameStats(ai_settings)
    #创建一个记分牌
    sb=Scoreboard(ai_settings,screen,stats)
    #设置背景色
    bg_color=ai_settings.bg_color
    
    #创建一艘飞船
    ship=Ship(ai_settings, screen)
    
    bullets=Group()#这个编组是pygame.sprite.Group 类的一个实例；pygame.sprite.Group
                    #类似于列表，但提供了有助于开发游戏的额外功 能。
    aliens=Group()                
    
    #创建一群外星人
    gf.create_fleet(ai_settings, screen, ship, aliens)
    
    #开始游戏的主循环
    while True:
        
        #监视鼠标和电脑事件
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,
                        bullets)
        
        if stats.game_active:
            
            
        
        #更新子弹位置，删除已消失的子弹
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
        
        #更新外星人
            gf.update_aliens(ai_settings,aliens,sb,screen,ship,stats,bullets)
        #检测外星人碰到飞船，并作出反应
            gf.anlens_ship_collision(ship,aliens,ai_settings,stats,screen,bullets,sb)
            
            ship.update()
        #更新屏幕上的图像并切换到新屏幕        
        gf.update_screen(ai_settings,screen,stats, sb, ship,aliens, 
            bullets,play_button)
        
        #我们还需要不断更新屏幕，以便在等待玩家是否选择开始新游戏时能够修改屏幕。
        #游戏处于非活动状态时，我们不用更新 游戏元素的位置。
run_game() 
