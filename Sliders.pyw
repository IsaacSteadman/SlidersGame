"""
 * Use the w, a, s, and d keys to move your blue square around
 *   to move diagonally down left use a and s
 *   to move diagonally down right use d and s
 *   to move diagonally up right use a and w
 *   to move diagonally up left use d and w
 * Use the arrow keys to fire projectiles
 *   like the w, a, s, and d keys to fire on the diagonals
 *     use the two arrow keys that correspond to that diagonal
 *   to fire diagonally down left use LeftArrow and DownArrow
 *   to fire diagonally down right use RightArrow and DownArrow
 *   to fire diagonally up left use LeftArrow and UpArrow
 *   to fire diagonally up right use RightArrow and UpArrow
 *   The projectiles will impart a damage to any entity they hit,
 *   The projectiles will dissapear after their time is up or after they hit
 *     an entity (that includes both the boss and the player)
 * The Enemy/Boss entity will try to occupy the same space as the player,
 *   and in doing so kill the player
 *   The boss can only move horizontally or vertically, not both
 * F9 - Restart
 * Esc - Pause
"""
import pygame
import time
import random
import os

def StrToInt(Str, base):
    if type(base) != type(1):
        return "base must be a positive integer"
    if type(Str) != type("Str"):
        return "Str must be type: string"
    if base >= 16 or base <= 1:
        return "base must be less than 16 and greater than 1"
    c = 0
    Num = 0
    Power = base ** (len(Str) - 1)
    while c < len(Str):
        Ord = ord(Str[c])
        if Ord >= ord('A') and Ord <= ord('F'):
            Num += ((Ord - ord('A')) * Power)
        elif Ord >= ord('a') and Ord <= ord('f'):
            Num += ((Ord - ord('a')) * Power)
        elif Ord >= ord('0') and Ord <= ord('9'):
            Num += ((Ord - ord('0')) * Power)
        elif Str[c] == '-' and c == 0:
            Num *= -1
        else:
            return "non-number encountered at character " + str(c)
        Power = Power/base
        c += 1
    return Num
def IntToStr(Int, base):
    Num = Int
    if base < 1 or base > 16:
        return -1
    if Num < 0:
        Num *= -1
    Rtn = list()
    Digits = "0123456789ABCDEF"
    while Num > 0:
        Tmp = Num % base
        Rtn.insert(0, Digits[Tmp])
        Num -= Tmp
        Num /= base
    if Int < 0:
        Rtn.insert(0, '-')
    Rtn1 = str()
    c = 0
    while c < len(Rtn):
        Rtn1 = Rtn1 + Rtn[c]
        c += 1
    return Rtn1

def YesNo(Caption):
    Rtn = None
    while True:
        Rtn = raw_input(Caption + ": ")
        Rtn = Rtn.lower()
        if Rtn == "yes" or Rtn == "no" or Rtn == "n" or Rtn == "y":
            return Rtn[0] == 'y'
        else:
            print "must be yes, no, y or n"

def GetInt(Caption, base):
    NotValid = True
    Rtn = 0
    while NotValid:
        Str = raw_input(Caption + ": ")
        Rtn = StrToInt(Str, base)
        if type(Rtn) == type(1):
            return Rtn
        else:
            print "Not a valid integer. Please try again"
def GetIntBounds(Caption, base, a, b):
    Rtn = GetInt(Caption, base)
    while Rtn < a or Rtn > b:
        print "Must be a valid integer between " + str(a) + " and " + str(b)
        Rtn = GetInt(Caption, base)
    return Rtn
def GetIntGreaterThan(Caption, base, a):
    Rtn = GetInt(Caption, base)
    while Rtn < a:
        print "must be a valid integer greater than " + str(a)
        Rtn = GetInt(Caption, base)
    return Rtn
def IsComboSym(Ch):
    return Ch == '~' or Ch == '+' or Ch == '-' or Ch == '=' or Ch == '!' or Ch == '@' or Ch == '#' or Ch == '$' or Ch == '%' or Ch == '^' or Ch == '&' or Ch == '*' or Ch == '|' or Ch == '<' or Ch == '>' or Ch == '/'
def IsSingleSym(Ch):
    return Ch == '(' or Ch == ')' or Ch == '[' or Ch == ']' or Ch == '{' or Ch == '}'
def ParseStr(Str):
    Rtn = list()
    for Ch in Str:
        if Ch == ' ' or Ch == '\n' or Ch == '\t':
            Rtn.append("")
        elif Ch.isalnum() or Ch == '_':
            if len(Rtn) > 0 and len(Rtn[-1]) > 0 and (Rtn[-1][-1].isalnum() or Rtn[-1][-1] == '_'):
                Rtn[-1] += Ch
            else:
                Rtn.append(Ch)
        elif IsComboSym(Ch):
            if len(Rtn) > 0 and (len(Rtn[-1]) == 0 or IsComboSym(Rtn[-1][-1])):
                Rtn[-1] += Ch
            else:
                Rtn.append(Ch)
        elif IsSingleSym(Ch):
            if len(Rtn) > 0 and len(Rtn[-1]) == 0:
                Rtn[-1] = Ch
                Rtn.append("")
            else:
                Rtn.append(Ch)
                Rtn.append("")
        else:
            Rtn.append(Ch)
    while True:
        try:
            Rtn.remove("")
        except:
            break
    return Rtn
def ToColor(Str):
    LstTokens = ParseStr(Str)
    Rtn = list()
    if (LstTokens[0] == '(' or LstTokens[0] == '[') and LstTokens[2] == ',' and LstTokens[4] == ',' and (LstTokens[6] == ']' or LstTokens[6] == ')'):
        Num1, Num2, Num3 = StrToInt(LstTokens[1], 10), StrToInt(LstTokens[3], 10), StrToInt(LstTokens[5], 10)
        if type(Num1) == type(str()) or type(Num2) == type(str()) or type(Num3) == type(str()):
            return "Error: invalid number supplied"
        Rtn.append(Num1)
        Rtn.append(Num2)
        Rtn.append(Num3)
    else:
        return "Error: Invalid syntax"
    return Rtn
def GetColor():
    Rtn = ToColor(raw_input("enter the color in the format [r, g, b] or (r, g, b): "))
    while type(Rtn) == type(str()):
        print Rtn + ". Please try again."
        Rtn = ToColor(raw_input("enter the color in the format [r, g, b] or (r, g, b): "))
    return (Rtn[0], Rtn[1], Rtn[2])
def GetKey():
    if YesNo("Do you want to press the key to bind?\n"):
        return True
    else:
        Rtn = raw_input("type the name of the key: ")
        while len(Rtn) != 1 and ( not Rtn.isalnum()):
            print "must be a single letter or digit"
            Rtn = raw_input("type the name of the key: ")
        return Rtn.lower()
DebugLvl = 0

class Entity:
    DmgTickTime = 10
    def __init__(self, Health, Name = "Unnamed", x = 0, y = 0):
        self.Name = Name
        self.x = x
        self.y = y
        self.Speed = 1
        self.Health = [Health, Health]
        self.Life = True
        self.Func = None
        self.Target = [None, None]
        self.Size = (8, 8)
        self.DrawFunc = None
        self.UpdateFunc = None
        self.DmgTick = 0
    def Update(self, Params = None):
        if self.DmgTick > 0:
            self.DmgTick -= 1
        if self.Target[0] != None:
            if abs(self.Target[0] - self.x) <= self.Speed:
                self.x = self.Target[0]
                self.Target[0] = None
            elif self.Target[0] < self.x:
                self.x -= self.Speed
            elif self.Target[0] > self.x:
                self.x += self.Speed
            else:
                self.x = Target[0]
                Target[0] = None
        if self.Target[1] != None:
            if abs(self.Target[1] - self.y) <= self.Speed:
                self.y = self.Target[1]
                self.Target[1] = None
            elif self.Target[1] < self.y:
                self.y -= self.Speed
            elif self.Target[1] > self.y:
                self.y += self.Speed
            else:
                self.y = Target[1]
                Target[1] = None
        if self.UpdateFunc != None:
            if Params == None:
                self.UpdateFunc(self)
            else:
                self.UpdateFunc(self, Params)
    def SetDrawFunc(self, Func):
        self.DrawFunc = Func
    def Draw(self, Surf, Params = None):
        if self.DrawFunc == None:
            return None
        if Params == None:
            self.DrawFunc(self, Surf)
        else:
            self.DrawFunc(self, Surf, Params)
    def Damage(self, Dmg = 1):
        if self.DmgTick > 0 or not self.Life:
            return self.Life
        else:
            self.DmgTick = Entity.DmgTickTime
        self.Health[0] -= Dmg
        if self.Health <= 0:
            self.Life = False
        if DebugLvl > 2:
            print "Entity " + str(self.Name) + " Took\n " + str(Dmg) + " points of damage: " + str(self.Health[0]) + "/" + str(self.Health[1])
        return self.Life
    def Heal(self, Amt = 1):
        self.Health[0] += Amt
        if self.Health[0] > self.Health[1]:
            self.Health[0] = self.Health[1]
    def SetTickFunc(self, Func):
        self.Func = Func
    def SetUpdateFunc(self, Func):
        self.UpdateFunc = Func
    def Tick(self, Params = None):
        if self.Func == None:
            return None
        if Params == None:
            self.Func(self)
        else:
            self.Func(self, Params)
    def IsInSpace(self, x, y):
        return x >= (self.x - self.Size[0]) and x <= (self.x + self.Size[0]) and y >= (self.y - self.Size[1]) and y <= (self.y + self.Size[1])



GlobalSpeed = 10
ProjMul = 1.2

# BossHealth = 900
BossHealth = 90
#PlayerHealth = ((BossHealth + 3)/4) + 1
PlayerHealth = 20

Fps = 50
TickRate = 20

WinBkgr = False


class Projectile:
    def __init__(self, x , y, DirX, DirY, Damage, Time, Speed):
        self.x = x
        self.y = y
        self.Speed = Speed
        self.Dir = (DirX, DirY)
        self.Dmg = Damage
        self.Time = Time
        self.Dead = False
    def Tick(self, Ents, Width, Height):
        for c in range(len(Ents)):
            TmpX = self.x
            TmpY = self.y
            for i in range(int(self.Speed)):
                if Ents[c].IsInSpace(TmpX, TmpY):
                    Ents[c].Damage(self.Dmg)
                    self.Dead = True
                    return False
                TmpX += self.Dir[0]
                TmpY += self.Dir[1]
        self.x += self.Dir[0] * self.Speed
        self.y += self.Dir[1] * self.Speed
        self.Time -= 1
        if len(Ents) > 0:
            for c in range(len(Ents)):
                if Ents[c].IsInSpace(self.x, self.y):
                    Ents[c].Damage(self.Dmg)
                    self.Dead = True
        if not self.Dead:
            if self.Time <= 0:
                self.Dead = True
            elif self.x < 0 or self.x > Width:
                self.Dead = True
            elif self.y < 0 or self.y > Height:
                self.Dead = True
        return not self.Dead
    def Draw(self, Surf):
        pygame.draw.rect(Surf, (191, 191, 0), pygame.rect.Rect(self.x - 4, self.y - 4, 8, 8))
    def PrintInfo(self):
        print "projectile Info:"
        print " x: " + str(self.x)
        print " y: " + str(self.y)
        print " DirX: " + str(self.Dir[0])
        print " DirY: " + str(self.Dir[1])
        print " damage: " + str(self.Dmg)
        print " Time: " + str(self.Time)
        print " IsDead: " + str(self.Dead)
def SliderTick(This, Player):
    DiffX = abs(This.x - Player.x)
    DiffY = abs(This.y - Player.y)
    if DiffY > DiffX:
        This.Target[1] = Player.y
        if DiffX < This.Size[0] and DiffY < This.Size[1]:
            Player.Damage((This.Health[0] + 3) / 4)
    elif DiffX > DiffY:
        This.Target[0] = Player.x
        if DiffX < This.Size[0] and DiffY < This.Size[1]:
            Player.Damage((This.Health[0] + 3) / 4)
    elif random.randint(0, 1) == 0:
        This.Target[1] = Player.y
        if DiffX < This.Size[0] and DiffY < This.Size[1]:
            Player.Damage((This.Health[0] + 3) / 4)
    else:
        This.Target[0] = Player.x
        if DiffX < This.Size[0] and DiffY < This.Size[1]:
            Player.Damage((This.Health[0] + 3) / 4)
def SliderUpdate(This, Player):
    DiffX = abs(This.x - Player.x)
    DiffY = abs(This.y - Player.y)
    if DiffX < This.Size[0] and DiffY < This.Size[1]:
        Player.Damage((This.Health[0] + 3) / 4)
def PlayerTick(This, Params):
    MyW = Params[0]
    MyH = Params[1]
    MyKeys = Params[2]
    if MyKeys[ord('w')] == True and MyKeys[ord('s')] == None:
        This.y -= This.Speed
    elif MyKeys[ord('s')] == True and MyKeys[ord('w')] == None:
        This.y += This.Speed
    if MyKeys[ord('d')] == True and MyKeys[ord('a')] == None:
        This.x += This.Speed
    elif MyKeys[ord('a')] == True and MyKeys[ord('d')] == None:
        This.x -= This.Speed
    if This.y < 0:
        This.y = 0
    elif This.y >= MyH:
        This.y = (MyH - 1)
    if This.x < 0:
        This.x = 0
    elif This.x >= MyW:
        This.x = (MyW - 1)
    ProjX = 0
    ProjY = 0
    if MyKeys[pygame.K_UP] == True:
        ProjY -= 1
    if MyKeys[pygame.K_DOWN] == True:
        ProjY += 1
    if MyKeys[pygame.K_LEFT] == True:
        ProjX -= 1
    if MyKeys[pygame.K_RIGHT] == True:
        ProjX += 1
    if ProjX != 0 or ProjY != 0:
        Params[3].append(Projectile(This.x + (This.Size[0] * ProjX) + ProjX, This.y + (This.Size[1] * ProjY) + ProjY, ProjX, ProjY, (This.Health[0] + 3) / 4, This.Health[0] * 2, GlobalSpeed * ProjMul))
        if DebugLvl > 4:
            Params[3][-1].PrintInfo()
def EntityDraw(This, Surf, Params = None):
    Color1 = (63, 63, 63)
    if This.Name.lower() == "player":
        Color1 = (31, 31, 191)
    if Entity.DmgTickTime > 1 and This.DmgTick > 0:
        Color1 = (Color1[0] + int(This.DmgTick * (float(255.0 - Color1[0])/float(Entity.DmgTickTime))), Color1[1], Color1[2])
    Level = (This.Health[0] * This.Size[0] * 2) / This.Health[1]
    if This.Health[0] > 0:
        pygame.draw.rect(Surf, (127, 127, 127), pygame.rect.Rect(This.x - This.Size[0], This.y - (This.Size[1] + 8), 2 * This.Size[0], 4))
        pygame.draw.rect(Surf, (191, 0, 0), pygame.rect.Rect(This.x - This.Size[0], This.y - (This.Size[1] + 8), Level, 4))
    pygame.draw.rect(Surf, Color1, pygame.rect.Rect(This.x - This.Size[0], This.y - This.Size[1], 2 * This.Size[0], 2 * This.Size[1]))
def SetKeys(Dest, Src):
    for k, v in dict.iteritems():
        Dest[k] = v
from pygame.locals import *

PygMods = (pygame.display, pygame.font, pygame.joystick, pygame.scrap, pygame.mixer, pygame.cdrom)



#pygame needs to be initialized

#pygame.init()
#pygame.mixer.quit()

PygMods[0].init()
PygMods[1].init()
PygMods[2].init()

MonWidth = pygame.display.Info().current_w
MonHeight = pygame.display.Info().current_h

GameFont = pygame.font.SysFont("Times New Roman", 64)

#making a display
PauseImg = None
LoseImg = GameFont.render("You Lost", 1, (191, 0, 0), (0, 0, 0))
LoseImg.set_colorkey((0, 0, 0))
WinImg = GameFont.render("You Won", 1, (0, 191, 0), (0, 0, 0))
WinImg.set_colorkey((0, 0, 0))
if not os.path.isfile(os.getcwd() + "/GamePaused.png"):
    FileStr = "E:/python/GamePaused.png"
    while not os.path.isfile(FileStr) and ord(FileStr[0]) <= ord('Z'):
        FileStr = chr(ord(FileStr[0]) + 1) + FileStr[1:]
    if ord(FileStr[0]) > ord('Z'):
        print "Give Me GamePaused.png"
        PauseImg = GameFont.render("Game Paused", 1, (0, 191, 191), (0, 0, 0))
        PauseImg.set_colorkey((0, 0, 0))
    else:
        PauseImg = pygame.image.load_extended(FileStr)
else:
    PauseImg = pygame.image.load_extended("GamePaused.png")
PausW, PausH = PauseImg.get_size()
PausOff = (PausW / 2, PausH / 2)
LoseW, LoseH = LoseImg.get_size()
LoseOff = (LoseW / 2, (LoseH / 2) + PausH)
WinW, WinH = WinImg.get_size()
WinOff = (WinW / 2, (WinH / 2) + PausH)

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0, 191, 0)
RED = (255, 0, 0)

OrigH = 640
OrigW = 640
CurrH = OrigH
CurrW = OrigW
Surface = pygame.display.set_mode((CurrW, CurrH))
pygame.display.set_caption("Sliders")
pygame.display.update()

Quit = False
Tmp = None
Color = [255, 255, 255]
Prevx, Prevy = pygame.mouse.get_pos()
IsFullScreen = False
Started = False
PlayerWin = False
GameOver = False
Paused = False


Projectiles = list()
PrevLen = 0

DEFAULT_K = {ord('w'):None, ord('a'):None, ord('s'):None, ord('d'):None,
        pygame.K_UP:None, pygame.K_LEFT:None,
        pygame.K_DOWN:None, pygame.K_RIGHT:None}
Keys = {ord('w'):None, ord('a'):None, ord('s'):None, ord('d'):None,
        pygame.K_UP:None, pygame.K_LEFT:None,
        pygame.K_DOWN:None, pygame.K_RIGHT:None}
#PlayerEnt = Entity(26, "Player", 320, 320)
PlayerEnt = Entity(PlayerHealth, "Player", 320, 320)
PlayerEnt.SetTickFunc(PlayerTick)
PlayerEnt.SetDrawFunc(EntityDraw)
PlayerEnt.Speed = GlobalSpeed
#BossEnt = Entity(100, "Like a Boss", 160, 160)
BossEnt = Entity(BossHealth, "Like a Boss", 160, 160)
BossEnt.SetTickFunc(SliderTick)
BossEnt.Size = (16, 16)
BossEnt.SetDrawFunc(EntityDraw)
BossEnt.Speed = GlobalSpeed

TICK_EVT = pygame.USEREVENT + 1
RENDER_EVT = pygame.USEREVENT + 2
RESTART_EVT = pygame.USEREVENT + 3


pygame.time.set_timer(TICK_EVT, 1000/TickRate)
pygame.time.set_timer(RENDER_EVT, 1000/Fps)

while True:
    Before = IsFullScreen
    x, y = pygame.mouse.get_pos()
    for Evt in pygame.event.get():
        Tmp = type(Evt)
        if Evt.type == pygame.QUIT:
            GameOver = True
            Quit = True
        elif Evt.type == pygame.KEYDOWN:
            if Evt.key == pygame.K_F4 and (Evt.mod & pygame.KMOD_ALT) != 0:
                if DebugLvl > 0:
                    print "Alt-F4"
                pygame.event.post(pygame.event.Event(pygame.QUIT, {}))
            elif Evt.key == pygame.K_F11:
                IsFullScreen = not IsFullScreen
            elif Evt.key == pygame.K_F9:
                pygame.event.post(pygame.event.Event(RESTART_EVT, {}))
            elif Evt.key == pygame.K_RETURN:
                Started = True
                if DebugLvl > 0:
                    print "Starting"
            elif Evt.key == 0x1B:
                #print "Dude stuff 0x1b"
                Paused = not Paused
                if Paused and DebugLvl > 0:
                    print "Paused"
                elif DebugLvl > 0:
                    print "Unpaused"
            else:
                Keys[Evt.key] = True
        elif Evt.type == TICK_EVT and Started and not Paused:
            PlayerEnt.Update()
            PlayerEnt.Tick([CurrW, CurrH, Keys, Projectiles])
            BossEnt.Update(PlayerEnt)
            DelLst = list()
            for Proj in Projectiles:
                if not Proj.Tick([PlayerEnt, BossEnt], CurrW, CurrH):
                    DelLst.append(Proj)
            for Elem in DelLst:
                try:
                    Projectiles.remove(Elem)
                except:
                    if DebugLvl > 0:
                        print "Exception"
            if len(Projectiles) != PrevLen:
                if DebugLvl > 3:
                    print "Len: " + str(len(Projectiles))
                PrevLen= len(Projectiles)
            if BossEnt.Target == [None, None] and not GameOver:
                BossEnt.Tick(PlayerEnt)
            if PlayerEnt.Health[0] <= 0 and not GameOver:
                GameOver = True
                PlayerWin = False
                print "You Lost  :("
                Surface.fill((255, 0, 0))
            elif BossEnt.Health[0] <= 0 and not GameOver:
                GameOver = True
                PlayerWin = True
                print "You won!  :)"
        elif Evt.type == RENDER_EVT:
            if GameOver and WinBkgr:
                if PlayerWin:
                    Surface.fill(GREEN)
                else:
                    Surface.fill(RED)
            elif GameOver:
                Surface.fill(BLACK)
                if PlayerWin:
                    Surface.blit(WinImg, pygame.rect.Rect((CurrW / 2) - WinOff[0], (CurrH / 2) - WinOff[1], WinW, WinH))
                else:
                    Surface.blit(LoseImg, pygame.rect.Rect((CurrW / 2) - LoseOff[0], (CurrH / 2) - LoseOff[1], LoseW, LoseH))
            else:
                Surface.fill(BLACK)
            PlayerEnt.Draw(Surface)
            BossEnt.Draw(Surface)
            for Proj in Projectiles:
                Proj.Draw(Surface)
            if Paused:
                Surface.blit(PauseImg, pygame.rect.Rect((CurrW / 2) - PausOff[0], (CurrH / 2) - PausOff[1], PausW, PausH))
            pygame.display.update()
        elif Evt.type == pygame.KEYUP:
            Keys[Evt.key] = None
        elif Evt.type == RESTART_EVT:
            Projectiles = list()
            PlayerEnt.x = 320
            PlayerEnt.y = 320
            PlayerEnt.Health[0] = PlayerEnt.Health[1]
            BossEnt.x = 160
            BossEnt.y = 160
            BossEnt.Target = [None, None]
            BossEnt.Health[0] = BossEnt.Health[1]
            Started = False
            GameOver = False
            PlayerWin = False
    if (Before != IsFullScreen):
        if IsFullScreen:
            Surf2 = pygame.display.set_mode((MonWidth, MonHeight), pygame.FULLSCREEN)
            Surf2.blit(Surface, Surface.get_rect())
            Surface = Surf2
            CurrH = MonHeight
            CurrW = MonWidth
        else:
            Surf2 = pygame.display.set_mode((OrigW, OrigH))
            Surf2.blit(Surface, Surf2.get_rect())
            Surface = Surf2
            CurrH = OrigH
            CurrW = OrigW
        pygame.display.update()
    if Quit:
        break
    Prevx, Prevy = x, y
pygame.quit()
"""if Evt.key == ord('w') or Evt.key == ord('a') or Evt.key == ord('s') or Evt.key == ord('d'):
                print "Released: " + chr(Evt.key)
            elif Evt.key == pygame.K_UP:
                print "Released: K_UP"
            elif Evt.key == pygame.K_LEFT:
                print "Released: K_LEFT"
            elif Evt.key == pygame.K_DOWN:
                print "Released: K_DOWN"
            elif Evt.key == pygame.K_RIGHT:
                print "Released: K_RIGHT"
"""
