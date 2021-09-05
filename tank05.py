"""
v1.0
    完成类的创建
    实现游戏窗口的加载
"""
import pygame
from pygame.sprite import Sprite
import sys
import time
import random

# 窗口宽度
WINDOW_WIDTH = 800
# 窗口高度
WINDOW_HEIGHT = 550

COLOR_WHITE = pygame.color.Color('white')
COLOR_GREEN = pygame.color.Color('#000000')


# 定义一个精灵类
class BaseItem(Sprite):
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)


# 坦克父类
class BaseTank(BaseItem):
    # 定义类属性，所有坦克对象高和宽都是一样
    width = 60
    height = 60

    def __init__(self, left, top):
        self.direction = 'U'  # 坦克的方向默认向上
        # 存放图片的字典
        self.images = {
            'U': pygame.image.load('tank_img/p1tankU.gif'),
            'D': pygame.image.load('tank_img/p1tankD.gif'),
            'L': pygame.image.load('tank_img/p1tankL.gif'),
            'R': pygame.image.load('tank_img/p1tankR.gif')
        }
        self.image = self.images[self.direction]  # 坦克的图片由方向决定
        self.speed = 5  # 坦克的速度
        self.rect = self.image.get_rect()
        # 设置放置的位置
        self.rect.left = left
        self.rect.top = top
        self.stop = True  # 坦克是否停止
        self.live = True  # 决定坦克是否消灭了

        # 保持原来的位置
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top

    # 射击方法
    def shot(self):
        return Bullet(self)

    # 坦克的移动
    def move(self):
        # 保持原来的状态
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top
        # 判断坦克的移动方向
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < WINDOW_HEIGHT:
                self.rect.top += self.speed
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == 'R':
            if self.rect.left+self.rect.height < WINDOW_WIDTH:
                self.rect.left += self.speed

    # 加载坦克
    def displayTank(self):
        self.image = self.images[self.direction]
        MainGame.window.blit(self.image, self.rect)

    # 撞墙处理
    def hitWall(self):
        for wall in MainGame.wallList:
            if pygame.sprite.collide_rect(wall, self):
                self.stay()

    # 处理位置不变
    def stay(self):
        self.rect.left = self.oldLeft
        self.rect.top = self.oldTop


# 我方坦克
class HeroTank(BaseTank):
    def __init__(self, left, top):
        super().__init__(left, top)

    def myTank_hit_enemyTank(self):
        for enemyTank in MainGame.EnemyTankList:
            if pygame.sprite.collide_rect(enemyTank, self):
                self.stay()


# 敌方坦克
class EnemyTank(BaseTank):
    def __init__(self, left, top, speed):
        super(EnemyTank, self).__init__(left, top)
        self.images = {
            'U': pygame.image.load('tank_img/enemy1U.gif'),
            'D': pygame.image.load('tank_img/enemy1D.gif'),
            'L': pygame.image.load('tank_img/enemy1L.gif'),
            'R': pygame.image.load('tank_img/enemy1R.gif')
        }

        self.direction = self.RandomDirection()
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = speed
        self.step = 60
        self.enemy_flag = False

    # 坦克出生随机方向
    def RandomDirection(self):
        num = random.randint(1, 4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return 'L'
        else:
            return 'R'

    # 坦克随机移动
    def randomMove(self):
        if self.step < 0:
            self.direction = self.RandomDirection()
            self.step = 60
        else:
            self.move()
            self.step -= 1

    # 坦克射击
    def shot(self):
        num = random.randint(1, 100)
        if num < 4:
            return Bullet(self)

    # 敌方坦克碰撞我方坦克
    def enemyTank_hit_MyTank(self):
        for enemy in MainGame.EnemyTankList:
            if MainGame.my_tank and MainGame.my_tank.live:
                if pygame.sprite.collide_rect(MainGame.my_tank, enemy):
                    self.stay()


# 子弹类
class Bullet(BaseItem):
    def __init__(self, tank):
        self.image = pygame.image.load('tank_img/tankmissile.gif')
        self.direction = tank.direction
        self.rect = self.image.get_rect()
        # 根据坦克方向，生成子弹位置
        if self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height / 2 - self.rect.width / 2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.height / 2 - self.rect.width / 2

        # 子弹的速度
        self.speed = 6
        # 子弹状态
        self.live = True

    # 加载子弹
    def displayBullet(self):
        MainGame.window.blit(self.image, self.rect)

    # 子弹的移动
    def move(self):
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                self.live = False
        elif self.direction == 'R':
            if self.rect.left + self.rect.width < WINDOW_WIDTH:
                self.rect.left += self.speed
            else:
                self.live = False
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < WINDOW_HEIGHT:
                self.rect.top += self.speed
            else:
                self.live = False
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.live = False

    # 我方子弹击中敌方坦克
    def myBullet_hit_enemy(self):
        for enemytank in MainGame.EnemyTankList:
            if pygame.sprite.collide_rect(enemytank, self):
                enemytank.live = False
                self.live = False

                # 创建爆炸对象
                explode = Explode(enemytank)
                MainGame.explodeList.append(explode)

    # 敌方坦克击中我方坦克
    def enemyBullet_hit_myTank(self):
        if MainGame.my_tank and MainGame.my_tank.live:
            if pygame.sprite.collide_rect(MainGame.my_tank, self):
                MainGame.my_tank.live = False
                self.live = False

                # 创建爆炸对象
                explode = Explode(MainGame.my_tank)
                MainGame.explodeList.append(explode)

    # 射击墙壁
    def wall_bullet(self):
        for wall in MainGame.wallList:
            if pygame.sprite.collide_rect(wall, self):
                wall.hg -= 1
                self.live = False
                if wall.hg <= 0:
                    wall.live = False


# 墙壁类
class Wall:
    def __init__(self, left, top):
        self.image = pygame.image.load('tank_img/steels.gif')
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.live = True
        self.hg = 100000000000000

    def displayWall(self):
        if self.live:
            MainGame.window.blit(self.image, self.rect)


# 爆炸类
class Explode:
    def __init__(self, tank):
        # 爆炸的位置由坦克决定
        self.rect = tank.rect
        self.images = [
            pygame.image.load('tank_img/blast0.gif'),
            pygame.image.load('tank_img/blast1.gif'),
            pygame.image.load('tank_img/blast2.gif'),
            pygame.image.load('tank_img/blast3.gif'),
            pygame.image.load('tank_img/blast4.gif'),
            pygame.image.load('tank_img/blast5.gif'),
            pygame.image.load('tank_img/blast6.gif'),
            pygame.image.load('tank_img/blast7.gif')
        ]
        self.step = 0
        self.image = self.images[self.step]
        self.live = True

    # 加载爆炸类
    def displayExplode(self):
        if self.step < len(self.images):
            self.image = self.images[self.step]
            self.step += 1
            MainGame.window.blit(self.image, self.rect)
        else:
            self.live = False
            self.step = 0


# 游戏类
class MainGame:
    # 类属性
    window = None
    my_tank = None

    # 敌方坦克初始化
    EnemyTankList = []
    EnemyTankCount = 5

    # 存储我方子弹列表
    myBulleList = []
    # 存储敌方子弹的列表
    EnemyBulletList = []

    # 创建爆炸对象列表
    explodeList = []

    # 创建墙壁列表
    wallList = []

    # 游戏开始方法
    def start_game(self):
        # 初始化展示模块
        pygame.display.init()
        # 调用创建窗口的方法
        self.creat_window()
        # 设置游戏窗口标题
        pygame.display.set_caption('坦克大战')
        # 初始化我方坦克
        self.createMyTank()
        # 初始化敌方坦克
        self.creatEnemyTank()
        # 初始化墙壁
        self.creatWall()

        # 程序持续进行
        while True:
            # 更改背景颜色
            MainGame.window.fill(COLOR_GREEN)
            # 背景音乐

            # 获取事件
            self.getEvent()
            # 调用我方坦克进行显示
            if MainGame.my_tank and MainGame.my_tank.live:
                MainGame.my_tank.displayTank()
                if not MainGame.my_tank.stop:
                    MainGame.my_tank.move()
                    MainGame.my_tank.hitWall()
                    MainGame.my_tank.myTank_hit_enemyTank()
            else:
                del MainGame.my_tank
                MainGame.my_tank = None
            # 加载我方子弹
            self.biltMyBullet()
            # 显示敌方坦克
            self.biltEnemyTank()
            # 显示敌方子弹
            self.biltEnemyBullet()
            # 显示墙壁
            self.blitWall()
            # 显示爆炸效果
            self.blitExplode()

            self.put_more_enemytank()

            # 窗口持续刷新
            pygame.display.update()
            time.sleep(0.02)

    # 重复添加敌方坦克
    def put_more_enemytank(self):
        while len(MainGame.EnemyTankList) < 5:
            self.more()

    # 创建游戏窗口方法：
    def creat_window(self):
        if not MainGame.window:
            # 创建窗口
            MainGame.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        return MainGame.window

    # 创建我方坦克
    def createMyTank(self):
        MainGame.my_tank = HeroTank((WINDOW_WIDTH - HeroTank.width)/2, WINDOW_HEIGHT - HeroTank.height)
        music = Music('tank_img/start.wav')
        music.play()

    # 创建墙壁
    def creatWall(self):
        for i in range(60, WINDOW_WIDTH, 60):
            top = WINDOW_WIDTH // 3
            left = i
            wall = Wall(left, top)
            MainGame.wallList.append(wall)

    # 显示墙壁
    def blitWall(self):
        for b in MainGame.wallList:
            if b.live:
                b.displayWall()
            else:
                MainGame.wallList.remove(b)

    # 加载我方子弹
    def biltMyBullet(self):
        for bullet in MainGame.myBulleList:
            if bullet.live:
                bullet.displayBullet()
                bullet.move()
                bullet.myBullet_hit_enemy()
                bullet.wall_bullet()
            else:
                MainGame.myBulleList.remove(bullet)

    # 后续坦克的添加
    def more(self):
        top = 0
        for i in range(5 - len(MainGame.EnemyTankList)):
            left = random.randint(0, 750)
            speed = random.randint(1, 4)
            enemy = EnemyTank(left, top, speed)
            MainGame.EnemyTankList.append(enemy)

    # 创建敌方坦克
    def creatEnemyTank(self):
        top = 0
        for i in range(MainGame.EnemyTankCount):
            left = random.randint(0, 750)
            speed = random.randint(1, 4)
            enemy = EnemyTank(left, top, speed)
            MainGame.EnemyTankList.append(enemy)

    # 循环遍历显示敌方坦克
    def biltEnemyTank(self):
        for enemytank in MainGame.EnemyTankList:
            if enemytank.live:
                enemytank.displayTank()
                EnemyBullet = enemytank.shot()
                enemytank.randomMove()
                enemytank.hitWall()
                enemytank.enemyTank_hit_MyTank()

                # 存储敌方子弹
                if EnemyBullet:
                    MainGame.EnemyBulletList.append(EnemyBullet)
            else:
                MainGame.EnemyTankList.remove(enemytank)
                MainGame.EnemyTankCount -= 1

    # 加载敌方子弹
    def biltEnemyBullet(self):
        for bullet in MainGame.EnemyBulletList:
            if bullet.live:
                bullet.displayBullet()
                bullet.move()
                bullet.enemyBullet_hit_myTank()
                bullet.wall_bullet()

            else:
                MainGame.EnemyBulletList.remove(bullet)

    # 加载爆炸效果
    def blitExplode(self):
        for explode in MainGame.explodeList:
            if explode.live:
                explode.displayExplode()
            else:
                MainGame.explodeList.remove(explode)

    # 获取游戏中的所有事件
    def getEvent(self):
        # 获取游戏中的事件列表
        even_list = pygame.event.get()
        for e in even_list:
            # 点击窗口的叉号实现游戏结束
            if e.type == pygame.QUIT:
                sys.exit()

            # 通过上下左右键控制坦克的移动
            if e.type == pygame.KEYDOWN:
                if MainGame.my_tank and MainGame.my_tank.live:
                    if e.key == pygame.K_DOWN or e.key == pygame.K_s:
                        MainGame.my_tank.direction = 'D'
                        MainGame.my_tank.stop = False
                        print("按下向下的键，向下移动")
                    elif e.key == pygame.K_UP or e.key == pygame.K_w:
                        MainGame.my_tank.direction = 'U'
                        MainGame.my_tank.stop = False
                        print("按下向上的键，向上移动")
                    elif e.key == pygame.K_LEFT or e.key == pygame.K_a:
                        MainGame.my_tank.direction = 'L'
                        MainGame.my_tank.stop = False
                        print("按下向左的键，向左移动")
                    elif e.key == pygame.K_RIGHT or e.key == pygame.K_d:
                        MainGame.my_tank.direction = 'R'
                        MainGame.my_tank.stop = False
                        print("按下向右的键，向右移动")

                    elif e.key == pygame.K_SPACE:
                        print('发射子弹')
                        # 创建我方子弹
                        if len(MainGame.myBulleList) < 10:
                            mybullet = Bullet(MainGame.my_tank)
                            MainGame.myBulleList.append(mybullet)

                            # 射击音效
                            Shot_music = Music('tank_img/fire.wav')
                            Shot_music.play()

            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_UP or e.key == pygame.K_DOWN or e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT \
                        or e.key == pygame.K_w or e.key == pygame.K_s or e.key == pygame.K_a or e.key == pygame.K_d:
                    if MainGame.my_tank and MainGame.my_tank.live:
                        MainGame.my_tank.stop = True


class Music:
    def __init__(self,filename):
        self.filename = filename
        # 初始化音乐混合器
        pygame.mixer.init()
        pygame.mixer.music.load(filename)

    def play(self):
        pygame.mixer.music.play()


if __name__ == '__main__':
    game = MainGame()
    game.start_game()
