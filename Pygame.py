#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!pip install numpy
#!pip install pygame


# In[1]:


import pygame
import random
import time
from concurrent.futures import ThreadPoolExecutor


# In[2]:


def line(p1,p2):
    x1, y1 = p1
    x2, y2 = p2      
    l = (y2-y1)/(x2-x1) #直線方程式斜率
    tmp = []
    i = 0
    flag = 1 if x2-x1>0 else 0
    p = 30
    add = int(abs(x2-x1)/p)
    if flag:
        while i<=abs(x2-x1):
            tmp.append((x1+i, y1+i*l))
            i+=add
    else:
        while abs(i)<=abs(x2-x1):
            tmp.append((x1+i, y1+i*l))
            i-=add
    return tmp


# In[3]:


w, h = (2000, 3000)
points = [(972,368),(424,1956),(56,2364),(1472,2020),(1804,2424),(524,2364),(525,2792),(1396,2792),(1397,2424),(1808,2424)]
line1 = line(points[0],points[1])
line2 = line(points[1],points[2])
line3 = line(points[0],points[3])
line4 = line(points[3],points[4])
edgeTop = points[0][1] 
edgeLeft_ = line1+line2
edgeRight_ = line3+line4
edgeRight_.pop()
None


# In[4]:


class Player(pygame.sprite.Sprite):
    def __init__(self,speedx,speedy,bspeedy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r"element/太空船.png").convert_alpha()
        self.height = 450
        self.scale = self.height/self.image.get_height()
        self.width = self.image.get_width()*self.scale
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        #self.image = pygame.Surface((50,40))
        #self.image.fill(color='pink')
        self.rect = self.image.get_rect()
        self.rect.x = 320
        self.rect.y = 240 
        self.rect.center=(width/2,height/2)
        self.speedx = speedx
        self.speedy = speedy
        self.bspeedy = bspeedy
    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.top+edgeTop*self.scale,self.bspeedy)    
        bully.append(bullet)
        all_sprites.add(bullet)    #將子彈加入sprites群組中
    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x-=self.speedx
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speedy
        if key_pressed[pygame.K_UP]:
            self.rect.y-= self.speedy
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.top < 0:
            self.rect.top = 0
        if key_pressed[pygame.K_SPACE]:
            self.shoot()
        if key_pressed[pygame.K_ESCAPE] or bloom<0:
            global running
            running = False
    def draw(self, screen):
        screen.blit(self.image, self.rect)


# In[5]:


class Rock(pygame.sprite.Sprite):
    def __init__(self,minx,maxx,miny,maxy):
        pygame.sprite.Sprite.__init__(self)
        self.size = 50
        self.image = pygame.Surface((self.size,self.size))
        self.image.fill((255,0,0))
        self.textSurf = pygame.font.Font("element/kaiu.ttf", self.size).render("草", 0, (0,0,0))
        self.image.blit(self.textSurf, [-18,0])
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,width)
        self.rect.y = random.randrange(-150,-41)
        self.minx = minx
        self.maxx = maxx+1
        self.miny = miny
        self.maxy = maxy+1
        self.init()
    def init(self):
        self.tend = random.randrange(1,101)
        self.tend = 0 if self.tend<25 else 1 if self.tend<50 else -1 if self.tend<75 else 2
        if self.tend==2 :
            self.real_tend = random.randrange(1,101)
            self.real_tend = 1 if self.real_tend<50 else -1
    def update(self):
        if self.rect.top>height  or self.rect.left>width or self.rect.right<0:
            self.rect.x = random.randrange(0,width)
            self.rect.y = random.randrange(-100,-41)
        if int(time.time())%5==0:
            self.init()
        if self.tend==2 :
            if random.randrange(1,101)<3 :
                self.real_tend*=-1
            random.randrange(1,4)*self.real_tend
        else:
            random.randrange(1,4)*self.tend
        self.rect.x += random.randrange(self.minx,self.maxx)*self.tend
        self.rect.y += random.randrange(self.miny,self.maxy)
    def draw(self, screen):
        screen.blit(self.image, self.rect)


# In[6]:


class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,speedy):                             #子彈的X跟Y是由傳入的太空船X座標決定的
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((200,51))   
        self.image.fill((255,255,0))                   
        self.rect = self.image.get_rect()         #將圖片框起來
        self.rect.centerx = x                     #子彈的X跟Y是由傳入的太空船X座標決定的
        self.rect.bottom = y                    #子彈的X跟Y是由傳入的太空船X座標決定的
        self.speedy = speedy
    def update(self):
        self.rect.y -= self.speedy ; return
    def draw(self, screen):
        screen.blit(self.image, self.rect)


# In[7]:


def rockReset(rock):
    rock.rect.x = random.randrange(0,width)
    rock.rect.y = random.randrange(-100,-41)


# In[8]:


def get_text_center(font,text,color,size):
    font = pygame.font.Font(font, size)
    text = font.render(text, (0,0,0), color)
    return text


# In[9]:


# esc = lambda : False if pygame.key.get_pressed()[pygame.K_ESCAPE] else True


# In[10]:


#必須先調用pygame.event.get()，才可使用pygame.key.get_pressed()、pygame.mouse.get_pos()


# In[11]:


def screen2():
    global running, esc, mouse, events, MousePressed
    if esc :return
    running = True
    text1 = pygame.font.Font("element/kaiu.ttf", 100).render("Best Score : "+str(data["score"]), 0, (0,0,0))
    text = pygame.font.Font("element/kaiu.ttf", 100).render("Score : "+str(score), 0, (0,0,0))
    stm = time.time()
    
    def end():
        global esc, running
        esc = 1
        running = 0
        
    def restart():
        global esc, running
        esc = 0
        running = 0
    
    buttons = [
        Buttons("結束",    1500,100, *mc, end  , x=None, y=550),
        Buttons("重新開始",1500,100, *mc,restart, x=None, y=850),
    ]
    
    while running:
        clock.tick(fps)
        screen.fill((156,148,123))
        screen.blit(text1, (600,100))
        screen.blit(text, (600,200))
        events = list(pygame.event.get())
        mouse = pygame.mouse.get_pos()
        MousePressed = pygame.mouse.get_pressed()
        for b in buttons : b.update()
        if pygame.key.get_pressed()[pygame.K_ESCAPE] and (time.time()-stm>0.5):running=False; esc=1;
        pygame.display.update()


# In[12]:


class TextBox():
    def __init__(self,text,w,h,color,clicked_color,fontSize=50,padding=25,x=None,y=None, name=0):
        self.name = name
        self.width = w
        self.height = h
        self.center = ()
        self.color = color
        self.clicked_color = clicked_color
        self.fontSize = fontSize
        self.padding = padding
        self.text = text
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        if x!=None :
            self.rect.x = x
        else :
            self.rect.centerx = width/2
        if y!=None :
            self.rect.y = y
        else :
            self.rect.centery = height/2
        self.get_image(self.color)
    
    def get_image(self, color):
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255,255,255,int(255*0.3)))
        pygame.draw.lines(self.image, color, True, [
            (0,0), (self.width,0), (self.width,self.height), (0,self.height)
        ], width=self.padding)
        self.textSurf = pygame.font.Font("element/kaiu.ttf", self.fontSize).render(self.text, 0, (0,0,0))
        self.image.blit(self.textSurf, (self.padding/2,(self.height-self.fontSize)/2))
        self.center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = self.center
    
    def update(self):
        global screen, events, mouse, focus, KEYDOWN_BACKSPACE, KEYDOWN_NOT_BACKSPACE, EventUnicode
        if (self.text!="" and self.text[-1]=="|"): self.text=self.text[:-1]
        
        if focus==self.name :
            if KEYDOWN_BACKSPACE:    self.text = self.text[:-1];
            if KEYDOWN_NOT_BACKSPACE: self.text += EventUnicode;
            if (int(time.time()*10)%10)>=5 :
                self.text = self.text +"|"
            elif self.text!="" and self.text[-1]=="|":
                self.text = self.text[:-1]
            self.get_image(self.clicked_color)
        elif self.rect.collidepoint(*mouse):
            self.get_image(self.clicked_color)
        else :
            self.get_image(self.color)
        
        self.draw(screen)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def get_text(self):
        if (self.text!="" and self.text[-1]=="|"): return self.text[:-1]
        return self.text


# In[13]:


class Rect():
    def __init__(self, w, h, color=(230,230,230), x=None, y=None):
        self.x = x
        self.y = y
        self.image = pygame.Surface((w,h))
        self.image.fill(color)
    
    def update(self):
        global screen
        self.draw(screen)
    
    def draw(self, screen):
        screen.blit(self.image, (self.x,self.y))


# In[14]:


class Button():
    def __init__(self,text,w,h,color,clickFunction=lambda:1,x=None,y=None,mode="mouseon",size=50,ix=None,iy=None):
        self.mode = mode
        self.clickFunction = clickFunction
        self.image = pygame.Surface((w,h))
        self.image.fill((230,230,230))
        self.scale = 25
        self.innerImage = pygame.Surface((w-self.scale,h-self.scale))
        self.innerImage.fill(color)
        self.image.blit(self.innerImage, [self.scale/2,self.scale/2])
        self.size = size
        self.textSurf = pygame.font.Font("element/kaiu.ttf", self.size).render(text, 0, (0,0,0))
        self.ix = (w-len(text)*self.size)/2 if ix==None else ix 
        self.iy = self.iy = (h-self.size)/2 if iy==None else iy
        self.image.blit(self.textSurf, [self.ix,self.iy])
        self.rect = self.image.get_rect()
        if x!=None :
            self.rect.x = x
        else :
            self.rect.centerx = width/2
        self.rect.y = y
    def update(self):
        global mouse,screen,MousePressed
        if self.rect.collidepoint(*mouse) and self.mode=="mouseon":
            self.draw(screen)
            if MousePressed[0]: self.clickFunction()
        if not(self.rect.collidepoint(*mouse)) and self.mode=="mouseoff":self.draw(screen)
    def draw(self,screen):
        screen.blit(self.image, self.rect)


# In[15]:


def init_(dict_):
    for e in dict_.keys(): globals()[e]=dict_[e]


# In[16]:


class Text():
    def __init__(self, text, FontSize=50, x=None, y=None, color=(0,0,0)):
        self.FontSize = FontSize
        self.x = x
        self.y = y
        self.text = text
        self.textSurf = pygame.font.Font("element/kaiu.ttf", self.FontSize).render(self.text, 0, color)
        self.color = color
    def update(self):
        global screen
        self.draw(screen)
    
    def draw(self, screen):
        screen.blit(self.textSurf, (self.x,self.y))
    
    def init(self):
        self.textSurf = pygame.font.Font("element/kaiu.ttf", self.FontSize).render(self.text, 0, self.color)


# In[17]:


class Text_with_border(Text):
    def __init__(self, text, FontSize=50, border={"padding":1,"color":(255,255,255),"terminal":(10,10)}, x=None, y=None, color=(0,0,0)):
        super().__init__(text, FontSize, x, y, color)
        self.border = border
        # border["terminal"] : ("width", "height")
    
    def update(self):
        global screen
        self.draw(screen)
        pygame.draw.lines(screen, self.border["color"], True, [
            (self.x, self.y),
            (self.x+self.border["terminal"][0], self.y),
            (self.x+self.border["terminal"][0], self.y+self.border["terminal"][1]),
            (self.x, self.y+self.border["terminal"][1])
        ], width=self.border["padding"])


# In[18]:


class Bloom(Text_with_border):
    def __init__(
        self, FontSize=50, 
        border={"padding":1,"color1":(0,255,0),"color2":(255,0,0),"terminal":(10,10)}, 
        x=None, y=None, color=(0,0,0)
    ):
        global bloom
        text = "█"*bloom
        border["color"] = border["color2"]
        super().__init__(text, FontSize, border, x, y, color)
        self.update_ = self.update
        
        def update():
            global bloom
            self.text = "█"*int(bloom) if bloom>0 else ""
            self.init()
            self.border["color"] = self.border["color2"] if int(bloom)>1 else self.border["color1"]
            self.update_()
        
        self.update = update


# In[19]:


# class Test():
#     print("Here I Run 1.")
    
#     def __init__(self):
#         print("Here I Run Init.")
    
#     def I_AM_A_FUNCTION(AAA):
#         print("I am", end=" ")
#         print(AAA)
    
#     print("Here I Run 2.")
    
#     I_AM_A_FUNCTION(101)

# print(Test)
# print(Test())
# print(dir(Test()))
# Test.I_AM_A_FUNCTION(202)


# In[20]:


class Setting():
    def __init__(self):
        global data
        t = [
            data["score"],
            data["player"]["speedx"],
            data["player"]["speedy"],
            data["rock"]["value"],
            data["rock"]["speedx"]["min"],
            data["rock"]["speedx"]["max"],
            data["rock"]["speedy"]["min"],
            data["rock"]["speedy"]["max"],
            data["bullet"]["speedy"]
        ]
        t = list(map(str,t))
        self.enable = False
        self.textboxes = [
            TextBox(t[0],350,100,(230,230,230),(230,0,230),fontSize=50,padding=10,x=600,y=100,name="best score"),
            TextBox(t[1],200,100,(230,230,230),(230,0,230),fontSize=50,padding=10,x=730,y=250,name="player speedx"),
            TextBox(t[2],200,100,(230,230,230),(230,0,230),fontSize=50,padding=10,x=1100,y=250,name="player speedy"),
            TextBox(t[3],200,100,(230,230,230),(230,0,230),fontSize=50,padding=10,x=600,y=400,name="rock value"),
            TextBox(t[4],100,100,(230,230,230),(230,0,230),fontSize=50,padding=10,x=730,y=550,name="rock speedx min"),
            TextBox(t[5],100,100,(230,230,230),(230,0,230),fontSize=50,padding=10,x=880,y=550,name="rock speedx max"),
            TextBox(t[6],100,100,(230,230,230),(230,0,230),fontSize=50,padding=10,x=1150,y=550,name="rock speedy min"),
            TextBox(t[7],100,100,(230,230,230),(230,0,230),fontSize=50,padding=10,x=1300,y=550,name="rock speedy max"),
            TextBox(t[8],200,100,(230,230,230),(230,0,230),fontSize=50,padding=10,x=730,y=700,name="bullet speedy"),
        ]
        
        self.elements = [
            Rect(1840,900, color=(166,158,133), x=40, y=90),
            Text("設", FontSize=100, x=10, y=125,color=(255,255,255)),
            Text("定", FontSize=100, x=64, y=230,color=(255,255,255)),
            Text("最高分數 : ", FontSize=50, x=300, y=125),
            Text("分", FontSize=50, x=980, y=125),
            Text("太空船速度 : ", FontSize=50, x=300, y=275),
            Text("水平", FontSize=50, x=600, y=275),
            Text("垂直", FontSize=50, x=970, y=275),
            Text("像素/幀 (FPS:60)", FontSize=50, x=1350, y=275),
            Text("草的數量 : ", FontSize=50, x=300, y=425),
            Text("個", FontSize=50, x=800, y=425),
            Text("草的速度 : ", FontSize=50, x=300, y=575),
            Text("水平", FontSize=50, x=600, y=575),
            Text("~", FontSize=100, x=830, y=555),
            Text("垂直", FontSize=50, x=1020, y=575),
            Text("~", FontSize=100, x=1250, y=555),
            Text("像素/幀 (FPS:60)", FontSize=50, x=1420, y=575),
            Text("黃色光束的速度 : ", FontSize=50, x=300, y=725),
            Text("像素/幀 (FPS:60)", FontSize=50, x=980, y=725),
            Buttons("確定",150,100, *mc, self.check, x=760, y=835, ix=0),
            Buttons("取消",150,100, *mc, self.cancel, x=980, y=835, ix=0),
            Text("", FontSize=50, x=-1000, y=-1000)
        ]

    def cancel(self):
        self.enable = False
    
    def check(self):
        global data
        set_succesful = 1
        tmp = []
        try:
            for e in self.textboxes:
                tmp.append(int(e.get_text()))
        except:
            self.elements[-1] = Text("設定失敗，僅能輸入零以上的整數", FontSize=45, x=18, y=850, color=(255,0,0))
            set_succesful = 0
        
        if set_succesful: 
            data["score"], data["player"]["speedx"], data["player"]["speedy"],             data["rock"]["value"], data["rock"]["speedx"]["min"], data["rock"]["speedx"]["max"],             data["rock"]["speedy"]["min"], data["rock"]["speedy"]["max"], data["bullet"]["speedy"] = tmp 
            with open("element/data", "w",encoding="utf8") as f: f.write(str(data))
            self.enable = False
    
    def update(self):
        if self.enable: self.update_()
    
    def update_(self):
        global KEYDOWN_BACKSPACE, KEYDOWN_NOT_BACKSPACE, EventUnicode, mouse, focus, MousePressed
        KEYDOWN_BACKSPACE, KEYDOWN_NOT_BACKSPACE= [False]*2
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    MousePressed = list(MousePressed)
                    MousePressed[0]=False
                    focus = -1
                if event.key == pygame.K_BACKSPACE:
                    KEYDOWN_BACKSPACE = True
                else :
                    KEYDOWN_NOT_BACKSPACE = True
                    if event.unicode=="|": event.unicode="!"
                    if event.unicode=='\x1b': event.unicode=""
                    EventUnicode = event.unicode
                break
        if MousePressed[0]:
            focus = -1
            for t in self.textboxes:
                if t.rect.collidepoint(*mouse): focus=t.name
        for e in self.elements: e.update()
        for t in self.textboxes: t.update()


# In[21]:


class Rules():
    def __init__(self):
        self.enable = False
        self.elements = [
            Rect(1840,900, color=(166,158,133), x=40, y=90),
            Text("1. 當血量小於零會停止遊戲，每撞到一個草會減一滴血。", FontSize=50, x=300, y=125),
            Text("2. 初始玩家會有六滴血，血量上限為六滴。", FontSize=50, x=300, y=235),
            Text("3. 超級模式不消耗血量、按esc可離開遊戲、按V鍵可暫停或繼續。", FontSize=50, x=300, y=345),
            Text("4. 點擊上下左右鍵可移動太空梭，按空白鍵可發射光束。", FontSize=50, x=300, y=455),
            Text("5. 血量會隨著時間恢復，頻率大約為5秒回復一次。", FontSize=50, x=300, y=565),
            Text("6. 光束每擊到一顆草字，能獲得一分。", FontSize=50, x=300, y=675),
            Buttons("確定",150,100, *mc, self.check, x=900, y=800, ix=0),
        ]
    
    def check(self):
        self.enable = False
    
    def update(self):
        if self.enable:
            for e in self.elements: e.update()


# In[22]:


def screen1():
    global running, esc, mouse, events, MousePressed
    if esc :return
    running = True
    
    def clicked(fun):
        def target():
            global running,esc
            esc=0
            running=False
            return fun()
        return target
    
    @clicked
    def normal(): global mode; mode="normal";
    
    @clicked
    def super_(): global mode; mode="super";
    
    def set_(): setting.enable=True;
    def rule(): rules.enable=True;
    def exit(): global esc, running; esc=1; running=0;
    
    text = pygame.font.Font("element/kaiu.ttf", 50).render("請選擇一個模式開始遊戲，按Esc結束。", 0, (0,0,0))
    setting = Setting()
    rules = Rules()
    
    elements = [
        Buttons("正常模式",1500,100,*mc, normal, x=None,y=400),
        Buttons("超級模式",1500,100,*mc, super_, x=None,y=700),
        Buttons("設定",150,100, *mc, set_, x=30, y=height-150, ix=0),
        Buttons("規則",150,100, *mc, rule, x=230, y=height-150, ix=12),
        Buttons("離開",150,100, *mc, exit, x=430, y=height-150, ix=25),
    ]
    
    while running:
        clock.tick(fps)
        screen.fill((156,148,123))
        screen.blit(text, (510,100))
        events = list(pygame.event.get())
        mouse = pygame.mouse.get_pos()
        MousePressed = pygame.mouse.get_pressed()
        if setting.enable:
            setting.update()
        elif rules.enable:
            rules.update()
        else:
            for e in elements : e.update()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:running=False; esc=1;
        pygame.display.update()


# In[23]:


def init(*args,**kargs):
    for e in args:
        if type(e)==str: globals()[e]=None
    
    for e in kargs.keys(): globals()[e]=kargs[e]
    
    pygame.init()
    pygame.display.set_caption("推しみこねこ")
    pygame.mixer.music.load("element/music.mp3")
    
    e = {
        "width":1920, "height":1080, "score":0, "bloom":6, "esc":0, "mode":"", "fps":60, "bully":[], "running":True,
        "mouse":[], "events":[], "focus":-1, "KEYDOWN_BACKSPACE":False, "KEYDOWN_NOT_BACKSPACE":False,
        "MousePressed":[], "EventUnicode":"", "lheight":60, "moc":(255,255,255), "mfc":(245,245,245),
        "love": pygame.image.load(r"element/love.png"), "paused":0, "s":0, "bombs":[]
    }
    
    init_(e)
    
    e = {
        "screen":pygame.display.set_mode((width,height), pygame.FULLSCREEN), ##screen = pygame.display.set_mode((width,height), pygame.FULLSCREEN)
        "image":pygame.transform.scale( pygame.image.load(r"element/background.jpg").convert_alpha(), (width, height)),
        "love": pygame.transform.scale(love, (love.get_width()*lheight/love.get_height(), lheight)),
        "clock":pygame.time.Clock(), "textX":(width/2)-150,
        "text" :get_text_center("element/kaiu.ttf","推しみこねこ",(0,255,0),50),
        "text3":get_text_center("element/kaiu.ttf","血量 : ",(0,255,0),45),
        "all_sprites":pygame.sprite.Group(), "player":Player(10,10,10),
        "rocks":[Rock(5,10,5,10) for i in range(5)],
        "mc":[moc,mfc]
    }
    
    init_(e)
    
    e = {
        "edgeLeft":[(e[0]*player.scale,e[1]*player.scale) for e in edgeLeft_],
        "edgeRight":[(e[0]*player.scale,e[1]*player.scale) for e in edgeRight_]
    }
    
    init_(e)


# In[32]:


class bomb(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = love.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.time_ = time.time()
    def update(self):
        if (time.time()*10-self.time_*10)>=2: self.kill()
    def Time(self):
        return (time.time()*10-self.time_*10)>=2
    def draw(self, screen):
        screen.blit(self.image, self.rect)


# In[40]:


class Logic(): #if you use this logic to judge,the bullet size should bigger than the rock size.
    def __init__(self):
        pass
    def playerRock(self):
        global score,running,bloom,esc,player
        if esc:return
        running = 1
        px = [w*player.scale for w in [56,524,1397,1808,525,1396]]
        py = [w*player.scale for w in [2364,2424,2792,368]]
        while running:
            time.sleep(0.01)
            for rock in rocks:
                pt,pb,pl,pr = [player.rect.top, player.rect.bottom, player.rect.left, player.rect.right]; rt,rb,rl,rr = [rock.rect.top, rock.rect.bottom, rock.rect.left, rock.rect.right]; x = [w+pl for w in px]; y = [w+pt for w in py]
                if (x[0]<=rl<=x[3] or x[0]<=rr<=x[3]) and (y[3]<=rt<=y[2] or y[3]<=rb<=y[2]):
                    for w in range(len(edgeLeft)): #偵測石頭是否砸中太空船
                        e = edgeLeft[w]; r = edgeRight[w]; x1 = pl+e[0]; x2 = pl+r[0]; y1 = pt+e[1]; y2 = pt+r[1]
                        if (rb>=y1 and rb>=y2) and ((rr>=x1 and rr<=x2) or (rl>=x1 and rl<=x2)) and ((x[0]<=rr<=x[1] and rt<=y[0]) or (x[2]<=rl<=x[3] and rt<=y[1]) or ((x[4]<=rl<=x[5] or x[4]<=rr<=x[5]) and rt<=y[2])):
                            bloom-=1 ; score -= 1; self.Bombs(rock); break
    def bullyRock(self):
        global score,running
        if esc:return
        running = 1
        while running:
            time.sleep(0.01)
            tmp = []
            for e in range(len(bully)): #當子彈的bottom已離開視窗，將子彈的從所有群組移除
                if bully[e].rect.bottom < 0 : bully[e].kill();tmp.append(e)
            if len(tmp)!=0 : tmp=sorted(tmp)[::-1] ; [bully.pop(e) for e in tmp]
            for rock in rocks:
                b=0
                for e in bully:  #偵測子彈是否與石頭發生碰撞
                    if e.rect.collidepoint(rock.rect.left,rock.rect.top) or e.rect.collidepoint(rock.rect.left,rock.rect.bottom) or e.rect.collidepoint(rock.rect.right,rock.rect.top) or e.rect.collidepoint(rock.rect.right,rock.rect.bottom):b=1;break
                if b:score += 1; self.Bombs(rock);
    def Bombs(self, rock):
        Bomb=bomb((rock.rect.left+rock.rect.right)/2,rock.rect.bottom);bombs.append(Bomb); all_sprites.add(Bomb);rockReset(rock)
    def bomb_update(self):
        global screen, running
        if esc:return
        running = 1
        while running:
            if not(paused):
                time.sleep(0.01);tmp = []
                for b in range(len(bombs)):
                    if bombs[b].Time(): tmp.append(b)
                if len(tmp)!=0 : tmp=sorted(tmp)[::-1] ; [bombs.pop(e) for e in tmp]


# In[26]:


class Buttons():
    def __init__(self,text,w,h,MouseOnColor,MouseOFFColor,clickFunction=lambda:1,x=None,y=None,size=50,ix=None,iy=None):
        self.button = [
            Button(text, w, h, MouseOnColor, clickFunction, x, y, "mouseon",size,ix,iy),
            Button(text, w, h, MouseOFFColor, clickFunction, x, y, "mouseoff",size,ix,iy)
        ]
        self.rect = self.button[0].rect
    def update(self):
        self.button[0].update(); self.button[1].update();
    
    def draw(screen):
        self.button[0].draw(screen); self.button[1].draw(screen);


# In[27]:


def event_update():
    global events, mouse, MousePressed, running
    events = list(pygame.event.get())
    mouse = pygame.mouse.get_pos()
    MousePressed = pygame.mouse.get_pressed()
    for event in events:
           if event.type == pygame.QUIT:
                running = False


# In[29]:


def main():
    global running,bloom,esc,paused #,clock,fps,all_sprites,screen,text1,score
    if esc==1 :return
    running = True
    
    def exit():
        global running,paused; running=False;paused=0
    
    def play():
        global paused, s
        if (time.time()-s)>0.2:
            s = time.time()
            elements[1] = Buttons("暫停",150,100, *mc, pause, x=(width-150), y=(height-210),ix=0)
            paused = 0
    
    def pause():
        global paused, s, screen
        if (time.time()-s)>0.2:
            s = time.time()
            paused = 1
            elements[1] = Buttons("繼續",150,100, *mc, play, x=(width-150), y=(height-210))
        while paused:
            event_update()
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:global running;running=False;paused=0
            clock.tick(fps)
            screen.fill((156,148,123))
            screen.blit(image, (0,0))
            screen.blit(text, (textX,0))
            text1 = get_text_center("element/kaiu.ttf","Score : "+str(score),(0,255,0),45)
            screen.blit(text1, (0,height-45))
            screen.blit(text3, (0,height-90))
            for e in elements: e.update()
            k = pygame.key.get_pressed()
            if k[pygame.K_v] : play()
            player.draw(screen)
            for r in rocks: r.draw(screen)
            for b in bully: b.draw(screen)
            for b in bombs[:]: b.draw(screen)
            pygame.display.update()
    
    def run():
        global bloom, mouse, MousePressed, events
        clock.tick(fps)
        all_sprites.update()
        if (int(time.time()%10)==0 and bloom<6):bloom+=(1/fps)
        screen.fill((156,148,123))
        screen.blit(image, (0,0))
        screen.blit(text, (textX,0))
        text1 = get_text_center("element/kaiu.ttf","Score : "+str(score),(0,255,0),45)
        event_update()
        for e in elements: e.update()
        k = pygame.key.get_pressed()
        if k[pygame.K_v] : pause()
        screen.blit(text1, (0,height-45))
        screen.blit(text3, (0,height-90))
        all_sprites.draw(screen)
        pygame.display.update()
    
    t301 = 0
    elements = [
        Buttons("離開",150,100, *mc, exit, x=(width-150), y=(height-100)),
        Buttons("暫停",150,100, *mc, pause, x=(width-150), y=(height-210),ix=0),
        Bloom(
            x=150, y=height-100,
            border={"padding":3,"color1":(230,0,0),"color2":(0,230,0),"terminal":(300,50)},
            color=(0,255,0),
        )
    ]
    
    for _ in range(3,0,-1):
        if t301 : break
        run()
        text_start = pygame.font.Font("element/kaiu.ttf", 300).render(str(_), 0, (0,255,0))
        screen.blit(text_start, (860,390))
        for i in range(fps):
            time.sleep(1/fps)
            pygame.display.update()
            list(pygame.event.get())
            k = pygame.key.get_pressed()
            if k[pygame.K_ESCAPE] :running,esc,t301=(False,1,1);break
    start = time.time()
    while running:
        run()


# In[38]:


def start():
    global bloom, score, player, bully, rocks, all_sprites, data, bombs
    with open("element/data", "r",encoding="utf8") as f: data=eval(f.read())
    screen1()
    bombs = []
    bloom = 6
    score = 0
    player.kill()
    for bu in bully: bu.kill()
    for rock in rocks : rock.kill()
    player = Player(data["player"]["speedx"], data["player"]["speedy"],data["bullet"]["speedy"])
    rd = [data["rock"]["speedx"]["min"],data["rock"]["speedx"]["max"],data["rock"]["speedy"]["min"],data["rock"]["speedy"]["max"]]
    rocks = [Rock(*rd) for i in range(data["rock"]["value"])]
    bully = []
    all_sprites.add(player)
    for rock in rocks : all_sprites.add(rock)
    logic=Logic()
    #main()
    with ThreadPoolExecutor(max_workers=4) as executor:
        if mode=="normal" : executor.submit(logic.playerRock)
        executor.submit(logic.bomb_update)
        executor.submit(logic.bullyRock)
        main()
    if score>data["score"]:
        data["score"] = score
        with open("element/data", "w",encoding="utf8") as f: f.write(str(data))
    screen2()


# In[41]:


if __name__=="__main__":
    init()
    pygame.mixer.music.play(loops=-1)
    while not(esc):
        start()
    pygame.mixer.music.stop()
    pygame.quit()


# In[ ]:




