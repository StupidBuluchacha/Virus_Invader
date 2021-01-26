import pgzrun
import random

#设定窗口大小
HEIGHT = 700
WIDTH = 900

#绘制背景图和选手形象
bg1 = Actor("pavement")
player1 = Actor("doctor")
player1.x = WIDTH / 2
player1.y = HEIGHT - 20

enemies = []
NUM_ENEMIES = 3
enemies_speed = []

lasers = []
score = 0
lives = 3
GAMETIME = 60
timer = GAMETIME
level = 1
gameover = False

def updateTimer():
    global timer
    timer -= 1
    
clock.schedule_interval(updateTimer,1.0)

#设置病毒
for i in range(NUM_ENEMIES):
    enemy1 = Actor("virus")
    enemy1.y = 20
    enemy1.x = random.randrange(0,WIDTH)
    enemies.append(enemy1)
    enemies_speed.append(random.randrange(1,3))


#每次刷新窗口时，会自动调用此draw函数
def draw():
    global score
    global gameover
    
    screen.clear()
    
    if (timer > 0) and (level == 1):
        bg1.draw()
        screen.draw.text("Score: "+str(score),(10,15),color="white")
        screen.draw.text("Lives: "+str(lives),(10,35),color="white")
        screen.draw.text("Timer: "+str(timer),(10,55),color="blue")
        player1.draw()
        
        for i in range(NUM_ENEMIES):
            enemies[i].draw()
            
        for i in range(len(lasers)):
            lasers[i].draw()
    else:
        screen.draw.text("GAME OVER",fontsize=60,center=(WIDTH/2,HEIGHT/2),color="white")
        screen.draw.text("Score = "+str(score),fontsize=40,center=(WIDTH/2,HEIGHT/2+50),color="white")
        screen.draw.text("Type 'p' to play again",fontsize=40,center=(WIDTH/2,HEIGHT/2+100),color="white")
        gameover = True
        
#每一帧都自动调用此update函数
def update():
    global score
    global lives
    global gameover
    global timer
    
    if keyboard.p and gameover:
        timer = GAMETIME
        score = 0
        gameover = False
    
    for i in range(NUM_ENEMIES):
        enemies[i].y += enemies_speed[i]
        
        if (enemies[i].y > HEIGHT):
            enemies[i].y = 0
            enemies[i].x = random.randrange(0,WIDTH)
            
        if (enemies[i].collidepoint(player1.pos)):
            lives -= 1
            enemies[i].y = 0
            enemies[i].x = random.randrange(0,WIDTH)            
    
    for i in range(len(lasers)):
        lasers[i].y -= 5
        
        for j in range(NUM_ENEMIES):
            if lasers[i].collidepoint(enemies[j].pos):
                enemies[j].y = 0
                enemies[j].x = random.randrange(0,WIDTH)
                lasers[i].y = 0
                score += 1
                
    
#鼠标移动时调用这个函数
def on_mouse_move(pos):
    player1.x = pos[0]

#鼠标点击时调用这个函数（发射来攻击病毒）
def on_mouse_down(pos):
    laser1 = Actor("injector")
    laser1.x = player1.x
    laser1.y = player1.y - 20
    lasers.append(laser1)
    sounds.laser5.play()

pgzrun.go()