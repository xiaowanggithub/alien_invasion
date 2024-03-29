import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''表示单个外星人的类'''
    
    def __init__(self,ai_settings,screen):
        '''初始化外星人并设置起始位置'''
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        screen_rect = self.screen.get_rect()
        #加载外星人图像
        self.image = pygame.image.load('images/UFO.bmp')#surface对象
        self.rect = self.image.get_rect()               #rect对象
        
        #每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        #我们将每个外星人的左边距都设置为外星人的宽度，
        #并将上边距设置为外星人的高度
        
        #储存外星人的准确位置
        self.x=float(self.rect.x)
        
    def blitme(self):
        '''在指定位置绘制外星人'''
        self.screen.blit(self.image,self.rect)#blit绘制图像draw绘制精灵
        
    def check_edges(self,ai_settings):
        '''如果外星人位于屏幕边缘，就返回True'''#这种带函数调用值不能用于条件判断，必须赋值
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:

            return True
        elif self.rect.left <= 0:
            return True       
        
    def update(self):
        '''向右移动外星人'''
        self.x += (self.ai_settings.alien_speed_factor *#可储存小数值
                        self.ai_settings.fleet_direction)
        self.rect.x = self.x
        
    
