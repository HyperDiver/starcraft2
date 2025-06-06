import pygame
import sys

#-----------------------------------------初始化
pygame.init()
isbuild=False
canatk=False
money=50
bd=None
scv=None
TR=None

WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("星海爭霸簡化版 - 圖片顯示")
clock = pygame.time.Clock()
#資料庫-------------------------------------------------------------
atkcd={"太空工程車":1000,"陸戰隊":400,"坦克":500,"幽靈戰機":800,"戰巡艦":1000}
ranges={"太空工程車":1,"陸戰隊":4,"坦克":8,"幽靈戰機":5,"戰巡艦":6}
damages={"太空工程車":5,"陸戰隊":5,"坦克":15,"幽靈戰機":10,"戰巡艦":50}
costs={"太空工程車":50,"陸戰隊":50,"坦克":200,"幽靈戰機":250,"戰巡艦":600,"訓練營":150}
hps={"太空工程車":50,"陸戰隊":50,"坦克":300,"幽靈戰機":200,"戰巡艦":600,"基地":500,"訓練營":300}
unit_names = ["scv", "base", "bu","marine","mine","trainer","ghost","tank","battle"]
speeds={"太空工程車":2,"陸戰隊":2,"坦克":2,"幽靈戰機":4,"戰巡艦":3}
# 載入圖片------------------------------------------
unit_size=[(40,40),(80,80),(160,100),(40,40),(40,40),(60,60),(40,40),(60,60),(80,80)]
unit_images = {}

for us,name in zip(unit_size,unit_names):
    ux,uy=us
    path = f"{name}.png"
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, (ux,uy))
    unit_images[name] = image
mine_rect = unit_images["mine"].get_rect(midbottom=(100,100))

#---------------------文字--------------------------
pygame.font.init()
font = pygame.font.Font(None, 36)    
text_content=""
minec="50"
text_color=(50,50,0)

#------------------------------------------------
class button:
    def __init__(self, x, y, image,ty,te):
        self.image = image
        self.enable=False
        self.rect = self.image.get_rect(center=(x, y))
        self.selected = False
        self.typ=ty
        self.text = te
        self.font = font
        self.text_color = text_color
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        
    def update(self):pass
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        screen.blit(self.text_surface, self.text_rect)
        
        if self.selected:
            pygame.draw.rect(surface, (255, 255, 0), self.rect, 2)
class building:
    def __init__(self, x, y, image,ty,teamm):
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.selected = False
        self.target = None
        self.typ=ty
        self.hp=hps[self.typ]
        self.otime=pygame.time.get_ticks()
        self.blink_time=0
        self.team=teamm
    def update(self):
        pass

    def attacked(self, damage):
        global text_content
        self.hp -= damage
        self.blink_time = pygame.time.get_ticks()
        self.blink(screen)
        if self.hp <= 0:
            self.destroy()
    def create(self,tp):
        global money
        if(money>=costs[tp]):
            money-=costs[tp]
        else: 
            return
        if(tp=="太空工程車"):
            x,y=self.rect.centerx+60,self.rect.centery
            while(1):
                for c in canselect:
                    out=True
                    dx = c.rect.centerx - x
                    dy = c.rect.centery - y
                    dist = dis(dx, dy)
                    if dist < 40:
                        x+=40
                        out=False
                if out:
                  break
            units.append(Unit(x, y, unit_images["scv"],"太空工程車",True))
        elif(tp=="陸戰隊"):
            x,y=self.rect.centerx+90,self.rect.centery+90
            while(1):
                for c in canselect:
                    out=True
                    dx = c.rect.centerx - x
                    dy = c.rect.centery - y
                    dist = dis(dx, dy)
                    if dist < 40:
                        x+=40
                        y+=40
                        out=False
                if out:
                  break
            units.append(Unit(x, y, unit_images["marine"],"陸戰隊",True))
        elif(tp=="坦克"):
            x,y=self.rect.centerx+90,self.rect.centery+90
            while(1):
                for c in canselect:
                    out=True
                    dx = c.rect.centerx - x
                    dy = c.rect.centery - y
                    dist = dis(dx, dy)
                    if dist < 40:
                        x+=40
                        y+=40
                        out=False
                if out:
                  break
            units.append(Unit(x, y, unit_images["tank"],"坦克",True))
        elif(tp=="幽靈戰機"):
            x,y=self.rect.centerx+90,self.rect.centery+90
            while(1):
                for c in canselect:
                    out=True
                    dx = c.rect.centerx - x
                    dy = c.rect.centery - y
                    dist = dis(dx, dy)
                    if dist < 40:
                        x+=40
                        y+=40
                        out=False
                if out:
                  break
            units.append(Unit(x, y, unit_images["ghost"],"幽靈戰機",True))
        elif(tp=="戰巡艦"):
            x,y=self.rect.centerx+90,self.rect.centery+90
            while(1):
                for c in canselect:
                    out=True
                    dx = c.rect.centerx - x
                    dy = c.rect.centery - y
                    dist = dis(dx, dy)
                    if dist < 40:
                        x+=40
                        y+=40
                        out=False
                if out:
                  break
            units.append(Unit(x, y, unit_images["battle"],"戰巡艦",True))
    def destroy(self):
        for lst in [canselect, units]:
            if self in lst:
                lst.remove(self)
        for u in units:
            if u.enemy == self:
                u.enemy = None
                u.attacking = False
    def draw(self, surface):
       
        surface.blit(self.image, self.rect)
       
        bar_width = self.rect.width
        bar_height = 5
        bar_x = self.rect.left
        bar_y = self.rect.top - bar_height - 2

        pygame.draw.rect(surface, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        
        
        hp_ratio = max(self.hp / hps[self.typ], 0)
        hp_width = int(bar_width * hp_ratio)

    
        pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, hp_width, bar_height))
    
  
        if self.selected:
            pygame.draw.rect(surface, (255, 255, 0), self.rect, 2)
    def blink(self, surface):
        current_time = pygame.time.get_ticks()
        if current_time - self.blink_time<= 100:  # 顯示 0.3 秒
            pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)
class Unit:
    def __init__(self, x, y, image,ty,teamm):
        #default setting
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        
        self.typ=ty
        self.speed = speeds[self.typ]
        self.team=teamm
        self.rg=ranges[self.typ]
        self.dmg=damages[self.typ]
        self.hp=hps[self.typ]
        self.cd=atkcd[self.typ]
        self.otime=pygame.time.get_ticks()
        self.blink_time=0
        #change by time,check it for every movement
        self.enemy = None
        self.attacking=False
        self.selected = False
        self.target = None
        self.atime=pygame.time.get_ticks()
    def update(self):
        mtime=pygame.time.get_ticks()
        ax = 50 - self.rect.centerx
        ay = 50 - self.rect.centery
        dists = dis(ax, ay)
        if(dists<40):
            if(mtime-self.atime>1000):
                self.atime=pygame.time.get_ticks()
                global money
                money+=5
        if self.target:
            dx = self.target[0] - self.rect.centerx
            dy = self.target[1] - self.rect.centery
            dist = dis(dx, dy)
            if dist > self.speed:
                self.rect.centerx += int(self.speed * dx / dist)
                self.rect.centery += int(self.speed * dy / dist)
            else:
                self.target = None
        if self.enemy:
            dx = self.enemy.rect.centerx - self.rect.centerx
            dy = self.enemy.rect.centery - self.rect.centery
            dist = dis(dx, dy)
            if dist < self.rg * 20:
                self.attacking = True
                self.target=None
            else:
                self.attacking = False
        else:
            if self.target == None:
                md = 1000
                closest_enemy = None
                for u in units + buildings:
                    dx = u.rect.centerx - self.rect.centerx
                    dy = u.rect.centery - self.rect.centery
                    dist = dis(dx, dy)
                    if dist < md and dist < self.rg * 20 and u.team != self.team:
                        md = dist
                        closest_enemy = u
                if closest_enemy:
                    self.enemy = closest_enemy
                    self.attacking = True
                else:
                    self.attacking = False
                    self.enemy = None

        if self.attacking and self.enemy:
            ntime = pygame.time.get_ticks()
            if ntime - self.otime > self.cd:
                self.otime = ntime
                self.enemy.attacked(self.dmg)
    def create(self,tp):
        global money
        if(money>=costs[tp]):
            money-=costs[tp]
        else:
            return
        if(tp=="訓練營"):
            x,y=self.rect.centerx+60,self.rect.centery
            while(1):
                for c in canselect:
                    out=True
                    dx = c.rect.centerx - x
                    dy = c.rect.centery - y
                    dist = dis(dx, dy)
                    if dist < 40:
                        x+=40
                        out=False
                if out:
                  break
            buildings.append(building(x, y, unit_images["trainer"],"訓練營",True))
       
    def enemyiscome(self,en):
        self.enemy=en
        self.attacking=True
    def attacked(self, damage):
        global text_content
        self.hp -= damage
        self.blink_time = pygame.time.get_ticks()
        self.blink(screen)
        if self.hp <= 0:
            self.destroy()

    def destroy(self):
        for lst in [canselect, units]:
            if self in lst:
                lst.remove(self)
        for u in units:
            if u.enemy == self:
                u.enemy = None
                u.attacking = False
    def draw(self, surface):
   
        surface.blit(self.image, self.rect)
        
      
        bar_width = self.rect.width
        bar_height = 5
        bar_x = self.rect.left
        bar_y = self.rect.top - bar_height - 2

        pygame.draw.rect(surface, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        
      
        hp_ratio = max(self.hp / hps[self.typ], 0)
        hp_width = int(bar_width * hp_ratio)

        pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, hp_width, bar_height))
    
         
        if self.selected:
            pygame.draw.rect(surface, (255, 255, 0), self.rect, 2)
    def blink(self, surface):
        current_time = pygame.time.get_ticks()
        if current_time - self.blink_time<= 100:  
            pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)

#--------------------------函式--------------------
def dis(x,y):
    dist = (x**2 + y**2) ** 0.5
    return dist
def render_text(text):
    return font.render(text, True, text_color)


units = [Unit(100, 100, unit_images["scv"],"太空工程車",True)]
units.append(Unit(100,500,unit_images["marine"],"陸戰隊",True))
buildings=[building(100,200,unit_images["base"],"基地",True)]
units.append(Unit(900,290,unit_images["battle"],"戰巡艦",False))
units.append(Unit(820,290,unit_images["tank"],"坦克",False))
buildings.append(building(900,200,unit_images["base"],"基地",False))
for i in range(5):
    units.append(Unit(800,100+i*20,unit_images["marine"],"陸戰隊",False))
buttons=[]
canselect=units+buildings+buttons
rtime=pygame.time.get_ticks()
running = True
while running:
    rtime2=pygame.time.get_ticks()
    if(rtime2-rtime>6000):
        rtime=pygame.time.get_ticks()
        units.append(Unit(800,400,unit_images["marine"],"陸戰隊",False))
        units.append(Unit(800,450,unit_images["marine"],"陸戰隊",False))
        units.append(Unit(800,550,unit_images["marine"],"陸戰隊",False))
        units.append(Unit(800,650,unit_images["marine"],"陸戰隊",False))
        units.append(Unit(800,600,unit_images["marine"],"陸戰隊",False))
    screen.fill((255, 255, 255))  
    canselect=units+buildings+buttons
    screen.blit(unit_images["mine"], (50,50))
    minec="Money:"+str(money)
    for b in buildings:
        if b.typ=="基地" and b.hp<=0:
            text_content="You Win the game! Congrete"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            
            if event.button == 1:  
                selected_unit = None
                for c in canselect:
                    c.selected = c.rect.collidepoint(mx, my)
                    if c.selected and isinstance(c, Unit):
                        bd=None
                        scv=None
                        buttons.clear()
                    if c.selected and isinstance(c, Unit) and c.team: 
                        selected_unit = c
                        if c.typ=="太空工程車":
                            scv=c
                            buttons.append(button(1040,620,unit_images["bu"],"訓練營","Trainer"))
                    elif c.selected and isinstance(c,button):
                        if bd != None:
                            bd.create(c.typ)
                        if scv!=None:
                            scv.create(c.typ)
                    elif c.selected and isinstance(c,building):
                        bd=c
                        scv=None
                        buttons.clear()
                        if(c.typ=="基地"):
                            buttons.append(button(1040,620,unit_images["bu"],"太空工程車","SCV"))
                        if(c.typ=="訓練營"):
                            buttons.append(button(1040,620,unit_images["bu"],"陸戰隊","marine"))
                            buttons.append(button(1040,500,unit_images["bu"],"戰巡艦","BattleCruiser"))
                            buttons.append(button(1040,560,unit_images["bu"],"坦克","Tank"))
                            buttons.append(button(1040,440,unit_images["bu"],"幽靈戰機","Ghost"))



            elif event.button == 3:  
                if selected_unit and isinstance(selected_unit,Unit):
                    selected_unit.enemy=None
                for u in units+buildings:
                    if u.rect.collidepoint(mx, my) and not u.team:  # 敵人
                        if selected_unit:
                            selected_unit.enemyiscome(u)
                            u.blink_time=pygame.time.get_ticks()
                            u.blink(screen)
                if selected_unit and isinstance(selected_unit,Unit):
                    selected_unit.target = (mx, my)

                    
                
    for c in canselect:
        c.update()
        c.draw(screen)
    for u in units:
      u.blink(screen) 
    #-----文字
    text_surface = render_text(text_content)
    text_surface2 = render_text(minec)
    screen.blit(text_surface, (400, 300))
    screen.blit(text_surface2, (1000, 30))
    pygame.display.flip()
    clock.tick(60)
