# -*- coding: utf-8 -*-

import io

import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
import pygame.font
from ship import Ship
from pygame.sprite import Group

class Scoreboard():
    '''显示得分信息的类'''
    
    def __init__(self,ai_settings,screen,stats):
        '''初始化显示得分涉及的属性'''
        self.screen=screen
        self.screen_rect=screen.get_rect()
        self.ai_settings=ai_settings
        self.stats=stats
        
        #显示得分信息时使用的字体设置
        self.text_color=(30,30,30)
        self.font=pygame.font.Font("C:/Windows/Fonts/simkai.ttf",32)#实例化一个字体对象
        
        #准备最高分和当前得分,等级，剩余飞船图像
        self.prep_images()
        
    def prep_images(self):
        '''准备最高分和当前得分,等级，剩余飞船图像'''
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.award_time()

        
    def award_time(self):
        '''奖励语句转换为图像'''
        self.font_t=pygame.font.Font("C:/Windows/Fonts/simkai.ttf",48)#实例化一个字体对象
        
        score_str1='亲爱的勇士 你已经消灭了210个外星人'
        score_str2='可获小汪线下奖励棒棒糖一根 继续游戏吧!'
        #使用了一个字符串格式设置指令，它让Python将数值转换为字符串时在其中插入逗号，例如，输出1,000,000 而不是1000000 。
        self.award_image1=self.font_t.render(score_str1,True,(255,31,57),
            self.ai_settings.bg_color)#创建一个具有指定文本的新surface
        self.award_image2=self.font_t.render(score_str2,True,(255,31,57),
            self.ai_settings.bg_color)#创建一个具有指定文本的新surface
            
        #将字放在屏幕中间
        self.award_rect1=self.award_image1.get_rect()#获取图像的rect位置
        self.award_rect1.y = 380
        self.award_rect1.centerx = self.screen_rect.centerx
        
        self.award_rect2=self.award_image2.get_rect()
        self.award_rect2.top = self.award_rect1.bottom
        self.award_rect2.centerx = self.screen_rect.centerx
        
        #显示语句
        self.screen.blit(self.award_image1,self.award_rect1)
        self.screen.blit(self.award_image2,self.award_rect2)
        

    def prep_score(self):
        '''将得分转换为一幅渲染的图像'''
        rounded_score=round(self.stats.score,-1)
        #函数round() 通常让小数精确到小数点后多少位，其中小数位数是由第二个实参指定的。然而，如
        #果将第二个实参指定为负数，round() 将圆整到最近的10(-1)、100(-2)、1000(-3)等整 数倍。
        score_str='当前分{:,}'.format(rounded_score)
        #使用了一个字符串格式设置指令，它让Python将数值转换为字符串时在其中插入逗号，例如，输出1,000,000 而不是1000000 。
        self.score_image=self.font.render(score_str,True,self.text_color,
            self.ai_settings.bg_color)#创建一个具有指定文本的新surface
        
        #将得分放在屏幕右上角
        self.score_rect=self.score_image.get_rect()#获取图像的rect位置
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top=20
        
    def prep_high_score(self):
        '''将最高得分转换为渲染的图像'''
        high_score=round(self.stats.high_score,-1)
        high_score_str='最高分{:,}'.format(high_score)
        self.high_score_image=self.font.render(high_score_str,True,self.text_color,
            self.ai_settings.bg_color)
            
        #将最高分放在屏幕顶端中央
        self.high_score_rect=self.high_score_image.get_rect()
        self.high_score_rect.centerx=self.screen_rect.centerx
        self.high_score_rect.top=self.score_rect.top
        
        
    def show_score(self):
        '''在屏幕上显示当前得分,最高分，等级'''
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        #绘制剩余数量飞船
        self.ships.draw(self.screen)
        
    def prep_level(self):
        '''将等级转换为渲染的图像'''
        self.level_image=self.font.render("等级:"+str(self.stats.level),True,self.text_color,
            self.ai_settings.bg_color)
        
        #将等级放在得分下方
        self.level_rect=self.level_image.get_rect()#获取图像的rect位置
        self.level_rect.right = self.score_rect.right 
        self.level_rect.top=self.score_rect.bottom+10
            
    def prep_ships(self):
        '''显示还剩下多少飞船'''
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
            

