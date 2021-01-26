import pgzrun
import random

#设定窗口大小
HEIGHT,WIDTH = 700,700


class Deadtreater():
    def __init__(self,dead):
        self.dead=dead
    def remove(self):
        data.treaters.remove(self)
class Data():
    #敌人类型：图片类型 最低速度 最高速度
    ENEMY_TYPES=[
        {'name':'virus','speed0':1,'speed1':3},
        {'name':'yellow virus','speed0':2,'speed1':4},
        {'name':'green virus','speed0':3,'speed1':5},
    ]
    STATUS_INIT='init'
    STATUS_SHOWING_BG='showing_bg'
    STATUS_NEXT_LEVEL='next_level'
    STATUS_PLAY='play'
    STATUS_GAME_OVER='game_over'
    STATUS_GAME_OK='game_ok'
    def __init__(self):
        self.status='init'#init showing_bg next_level play game_over game_ok
        self.score = 0
        self.lives = 3
        self.timer = 150
        self.level = -1
        self.showsupertext=False

        #三个级别：敌人数量，背景图片，时间（计时到多少秒时进入下一级） 提示词 
        self.levels=[
            {'enemies_num':3,'bg':'pavement','time':100,'text':'Infected by virus on the road!!!'},
            {'enemies_num':3,'bg':'hospital','time':50,'text':'Sent to the hospital!!!'},
            {'enemies_num':3,'bg':'surgery','time':0,'text':'Stick to the end!!!'},
        ]
        self.player1 = Actor("doctor")
        self.player1.x,self.player1.y = WIDTH / 2,HEIGHT - 20
        self.treaters=[]
    def isinit(self):
        return self.status==Data.STATUS_INIT
    def isshowingbg(self):
        return self.status==Data.STATUS_SHOWING_BG
    def isnextlevel(self):
        return self.status==Data.STATUS_NEXT_LEVEL
    def isplay(self):
        return self.status==Data.STATUS_PLAY
    def isgameover(self):
         return self.status==Data.STATUS_GAME_OVER
    def isgameok(self):
         return self.status==Data.STATUS_GAME_OK
    def startgame(self):
        self.nextlevel()

    def levelinfo(self):
        return self.levels[self.level]
    def nextlevel(self):
        #进入下一关
        if self.level+1==len(self.levels):return
        l=self.levels[self.level+1]
        self.level+=1
        self.bg = Actor(l['bg'])
        self.status=Data.STATUS_SHOWING_BG
        self.initenemy()
        self.bullets = []
        clock.schedule_unique(self.clockshowingbg,2.2)
       
    def clocktimer(self):
        #计时
        self.timer -= 1
        if self.timer==0:
            #游戏胜利
            self.status=Data.STATUS_GAME_OK
            return
        l=self.levels[self.level]
        if l['time']==self.timer:
            self.status=Data.STATUS_NEXT_LEVEL
            clock.unschedule(self.clocktimer)
    def clockshowingbg(self):
        self.status=Data.STATUS_PLAY
        clock.schedule_interval(self.clocktimer,0.8)

    def initenemy(self):
        #初始化敌人，随机种类
        l=self.levels[self.level]
        self.enemies=[]
        for i in range(l['enemies_num']):
            etype=random.choice(Data.ENEMY_TYPES[0:self.level+1])
            enemy1 = Actor(etype['name'])
            enemy1.__dict__['speed']=random.randrange(etype['speed0'],etype['speed1'])
            enemy1.y = 20
            enemy1.x = random.randrange(0,WIDTH)
            self.enemies.append(enemy1)
    
    def dead_enemy(self,enemy):
        #敌人被消灭
        dead = Actor('dead virus')
        dead.x,dead.y=enemy.x,enemy.y
        treater=Deadtreater(dead)
        self.treaters.append(treater)
        clock.schedule_unique(treater.remove,2)
    def gameover(self):
        #游戏结束
        clock.unschedule(self.clocktimer)
        self.status=Data.STATUS_GAME_OVER

    @staticmethod
    def resetenemy(enemy):
        #重新生成敌人
        enemy.y = 0
        enemy.x = random.randrange(0,WIDTH)
    def newbullet(self):
        #发射子弹
        b = Actor("injector")
        b.x = self.player1.x
        b.y = self.player1.y - 20
        self.bullets.append(b)
    def changeplayer(self):
        x,y=self.player1.x,self.player1.y
        self.player1 = Actor("super doctor")
        self.player1.x,self.player1.y=x,y
        self.showsupertext=True
        clock.schedule_unique(self.clockremovetext,3)
    def clockremovetext(self):
        self.showsupertext=False
data=Data()
data.startgame()
#每次刷新窗口时，会自动调用此draw函数
def draw():
    screen.clear()
    if data.isinit():
        #这个状态弃用了
        screen.draw.text("Type 's' to start game",fontsize=40,center=(WIDTH/2,HEIGHT/2+100),color="white")
    elif data.isshowingbg():
        #准备进入下一关
        l=data.levelinfo()
        screen.draw.text(l['text'],fontsize=60,center=(WIDTH/2,HEIGHT/2),color="white")
    elif data.isnextlevel():
        #上一关结束
        s='Congratulations!!!\nyou are tough!\npress p to continue.'
        screen.draw.text(s,fontsize=60,center=(WIDTH/2,HEIGHT/2),color="white")
    elif data.isplay():
        data.bg.draw()
        data.player1.draw()
        for enemy in data.enemies: enemy.draw()
        for tr in data.treaters:tr.dead.draw()
        for b in data.bullets: b.draw()
        screen.draw.text("Score: "+str(data.score),(10,15),color="white")
        screen.draw.text("Lives: "+str(data.lives),(10,35),color="white")
        screen.draw.text("Timer: "+str(data.timer),(10,55),color="blue")
        if data.showsupertext:
            screen.draw.text("Prof.Zhong Nanshan coming!!!",fontsize=60,center=(WIDTH/2,HEIGHT/2),color="red")
    elif data.isgameover():
        screen.draw.text("GAME OVER",fontsize=60,center=(WIDTH/2,HEIGHT/2),color="white")
        screen.draw.text("Score = "+str(data.score),fontsize=40,center=(WIDTH/2,HEIGHT/2+50),color="white")
        screen.draw.text("Type 'p' to play again",fontsize=40,center=(WIDTH/2,HEIGHT/2+100),color="white")
    elif data.isgameok():
        screen.draw.text("Congratulations!\nYou have killed all kinds of virus\nand saved countless lives!!! ",fontsize=60,center=(WIDTH/2,HEIGHT/2),color="white")
        
#每一帧都自动调用此update函数
def update():
    if not data.isplay():return 
    for enemy in data.enemies:
        enemy.y +=enemy.__dict__['speed']
        if (enemy.collidepoint(data.player1.pos)):#敌人击中玩家
            data.lives -= 1 #玩家减生命
            Data.resetenemy(enemy)#敌人被消耗
            if data.lives==1:
                data.changeplayer()#生命值为1，更换玩家角色
            elif data.lives==0:#生命值为0游戏结束
                data.gameover()
                return
        elif (enemy.y > HEIGHT):#敌人流失
            data.lives -= 1 #玩家减生命
            Data.resetenemy(enemy)#敌人被消耗
            if data.lives==1:
                data.changeplayer()#生命值为1，更换玩家角色
            elif data.lives==0:#生命值为0游戏结束
                data.gameover()
                return
    lost_bullets=set()
    for b in data.bullets:
        b.y -= 5
        if b.y<=0:
            lost_bullets.add(b)#子弹流失
            continue
        for enemy in data.enemies:
            if b.collidepoint(enemy.pos):
                data.dead_enemy(enemy)#死人被消灭
                Data.resetenemy(enemy)#生成新敌人
                lost_bullets.add(b)#子弹被消耗
                data.score += 1#累计积分
    if lost_bullets:
        for b in lost_bullets:
            data.bullets.remove(b)
            
    
#鼠标移动时调用这个函数
def on_mouse_move(pos):
    if data.isplay():
        data.player1.x = pos[0]

#鼠标点击时调用这个函数（发射来攻击病毒）
def on_mouse_down(pos):
    if data.isplay():
        data.newbullet()
        sounds.laser5.play()

def on_key_down(key, mod):
    global data
    
    if data.isnextlevel() and key == keys.P:
       data.nextlevel()
    elif data.isgameover() and key == keys.P:
        data=Data()
        data.startgame()
    #elif data.isinit() and key == keys.S:
    #   data.startgame()
pgzrun.go()