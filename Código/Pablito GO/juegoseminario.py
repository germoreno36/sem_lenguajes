import pygame, sys
import random
from datetime import datetime
from pygame.locals import *
 

# ------------------------------------------------------------------------ Resolucion pantalla
ancho = 800
alto = 600

# ------------------------------------------------------------------------ Divisiones para respawn
respawn_naves_ancho1 = 100
respawn_naves_ancho2 = 700
respawn_medio = 400

# ------------------------------------------------------------------------
ancho_medio_nave = 27                                                      #ancho nave = 54
alto_medio_nave = 32                                                       #alto nave = 68

ancho_medio_npc_nave = 30                                                  #ancho npc_nave = 60
alto_medio_npc_nave = 37                                                   #alto npc_nave = 53

ancho_medio_npc_boss = 100                                                 #ancho npc_boss = 200
alto_medio_npc_boss = 64                                                   #alto npc_boss = 123

disparo_npc_nave = 3
velocidad_respawn = 2

velocidad_npc_nave = 1                                                     #velocidad nave 1 y 2
velocidad_npc_nave3 = 3
velocidad_npc_bossX = 4
velocidad_npc_bossY = 2

hp_npc_nave = 2
hp_npc_nave2 = 2
hp_npc_nave3 = 3
hp_npc_boss = 5
hp_npc_boss_escudo = 3
# ------------------------------------------------------------------------ Colores
BLANCO = (255,255,255)
NEGRO = (0,0,0)
AZUL = (0,0,255)
ROJO = (255,0,0)
VERDE = (34,139,34)
NARANJA = (255,165,0)
ROSA = (255,192,203)
BORDO = (178,34,34)
MARRON = (139,69,19)

# ------------------------------------------------------------------------
puntuacion = 0                                                             #Contador puntuacion
rocas_destruidas = 0
naves_destruidas = 0                                                       #Contador naves destruidas
nivel = 0
# ------------------------------------------------------------------------
pygame.init()
PANTALLA = pygame.display.set_mode((ancho,alto))                           #Setear resolucion de pantalla
pygame.display.set_caption('PABLITO GO')                                   #Nombre del juego en la ventana
fuente1 = pygame.font.SysFont ("Calibri", 20, True, False)

SalirJuego= False
reloj = pygame.time.Clock()

# ------------------------------------------------------------------------
Nave = pygame.image.load("pj_nave.gif")
pj_nave = Nave.get_rect()
pj_nave.left = 400
pj_nave.top = 450

Disparo = pygame.image.load("PJ Disparo.gif") 
pj_disparo = Disparo.get_rect()        
disparoActivo = False


NaveNPC = pygame.image.load("npc_nave.gif")
npc_nave = NaveNPC.get_rect()
npc_nave.left = random.randint(100, 700)
npc_nave.top = -200
npc_nave_aparecer = False

DisparoNPCNave = pygame.image.load("NPC Disparo.gif")    
npc_nave_disparo = DisparoNPCNave.get_rect()        
disparoActivo_npc_nave = False


NaveNPC2 = pygame.image.load("npc_nave2.gif")
npc_nave2 = NaveNPC2.get_rect()
npc_nave2.left = random.randint(100, 700)
npc_nave2.top = -200
npc_nave2_aparecer = False

DisparoNPCNave2 = pygame.image.load("NPC Disparo.gif")    
npc_nave2_disparo = DisparoNPCNave2.get_rect()        
disparoActivo_npc_nave2 = False


NaveNPC3 = pygame.image.load("npc_nave.gif")
npc_nave3 = NaveNPC3.get_rect()
npc_nave3.left = random.randint(100, 700)
npc_nave3.top = -200
npc_nave3_aparecer = False

DisparoNPCNave3 = pygame.image.load("NPC Disparo.gif")    
npc_nave3_disparo = DisparoNPCNave3.get_rect()        
disparoActivo_npc_nave3 = False

EscudoNPCNave3 = pygame.image.load("NPC Escudo.gif")
npc_nave3_escudo = EscudoNPCNave3.get_rect()
npc_nave3_escudo.left = npc_nave3.left
npc_nave3_escudo.top = npc_nave3.top +alto_medio_npc_nave
npc_nave3_escudo_activo = False


BossNPC = pygame.image.load("npc_boss.gif")
npc_boss = BossNPC.get_rect()
npc_boss.left = (ancho/2)- ancho_medio_npc_boss/2
npc_boss.top = -200
npc_boss_aparecer = False
npc_boss_respawn = False

EscudoNPCBoss = pygame.image.load("Escudo NPC Boss.gif")
npc_boss_escudo = EscudoNPCBoss.get_rect()
npc_boss_escudo.left = npc_boss.left
npc_boss_escudo.top = npc_boss.top
npc_boss_escudo_activo = False

DisparoNPCBoss = pygame.image.load("NPC Disparo.gif")    
npc_boss_disparo = DisparoNPCBoss.get_rect()        
disparoActivo_npc_boss = False

Disparo2NPCBoss = pygame.image.load("NPC Disparo.gif")    
npc_boss_disparo2 = Disparo2NPCBoss.get_rect()        
disparo2Activo_npc_boss = False


Roca = pygame.image.load("Roca1.gif")
npc_roca = Roca.get_rect()
npc_roca.left = random.randint(-700, respawn_medio/2)
npc_roca.top = random.randint(-200, -10)

Roca2 = pygame.image.load("Roca2.gif")
npc_roca2 = Roca2.get_rect()
npc_roca2.left = random.randint((respawn_medio+respawn_medio/2), 1200)
npc_roca2.top = random.randint(-200, -10)                       

 
fondo = pygame.image.load("Fondo.jpg")
fondox=0
fondoy=0
# ------------------------------------------------------------------------ Musica del juego
pygame.mixer.music.load("melodyloops-adrenaline.mp3")
pygame.mixer.music.play(-1,0.0)
# ------------------------------------------------------------------------ Eventos del juego

while not SalirJuego:
     for event in pygame.event.get():                                      #recorrer eventos de pygame
        if event.type== pygame.QUIT:
               SalirJuego=True
     keys = pygame.key.get_pressed()  
# ------------------------------------------------------------------------ Movimiento de la nave               
#     if event.type == pygame.KEYDOWN:                                      #Movimiento por teclado
#      if keys[K_LEFT]and pj_nave.left >= ancho_medio_nave :
#             pj_nave.left -= 4
#      if keys[K_RIGHT]and pj_nave.right <= ancho - ancho_medio_nave :
#             pj_nave.left += 4
#      if keys[K_UP] and pj_nave.top >= alto_medio_nave:
#              pj_nave.top -= 4  
#      if keys[K_DOWN]and pj_nave.top <= alto - alto_medio_nave*3:
#                pj_nave.top += 4

     pj_nave.left, pj_nave.top = pygame.mouse.get_pos()                    #Movimiento por mouse
     pj_nave.left -= ancho_medio_nave
     pj_nave.top -= alto_medio_nave

# ------------------------------------------------------------------------ Disparo
     if keys[K_SPACE] and not disparoActivo:      
        disparoActivo = True                      
        pj_disparo.left = pj_nave.left + 23  
        pj_disparo.top = pj_nave.top - 25

     if disparoActivo:             
        pj_disparo.top -= 4         
        if pj_disparo.top <= 0 or pj_disparo.colliderect(npc_roca) or pj_disparo.colliderect(npc_roca2): 
          disparoActivo = False     

# ------------------------------------------------------------------------ Movimiento de la roca

     velocidadX1 = random.randint(1, 3)
     velocidadY1 = random.randint(1, 2)
     npc_roca.left += velocidadX1
     npc_roca.top += velocidadY1

# ------------------------------------------------------------------------ Movimiento de la roca2
     velocidadX2 = random.randint(1, 3)
     velocidadY2 = random.randint(1, 2)
     npc_roca2.left += -velocidadX2
     npc_roca2.top += velocidadY2
           
# ------------------------------------------------------------------------ Respawn roca

     if npc_roca.left > 950 or npc_roca.top > 750:
          npc_roca.left = random.randint(-700, respawn_medio/2)
          npc_roca.top = random.randint(-200, -10)

# ------------------------------------------------------------------------ Respawn roca2

     if npc_roca2.left < -150 or npc_roca2.top > 750:
          npc_roca2.left = random.randint((respawn_medio+respawn_medio/2), 1200)
          npc_roca2.top = random.randint(-200, -10)

# ------------------------------------------------------------------------ Colision disparo-roca
     if pj_disparo.colliderect(npc_roca):
          rocas_destruidas += 1
          puntuacion += 1
          npc_roca.left = random.randint(-700, respawn_medio/2)
          npc_roca.top = random.randint(-200, -10)
          pj_disparo.top = 2000
          disparoActivo = False
          
# ------------------------------------------------------------------------ Colision disparo-roca2
     if pj_disparo.colliderect(npc_roca2):
          rocas_destruidas += 1
          puntuacion += 1
          npc_roca2.left = random.randint(-700, respawn_medio/2)
          npc_roca2.top = random.randint(-200, -10)
          pj_disparo.top = 2000
          disparoActivo = False

# ------------------------------------------------------------------------ Colision disparo-npc_nave
     if pj_disparo.colliderect(npc_nave):
          hp_npc_nave -= 1
          if  hp_npc_nave == 0:
               naves_destruidas += 1
               puntuacion += 5
               npc_nave.left = 2000
               npc_nave.top = 2000
               npc_nave_aparecer = False
               disparoActivo_npc_nave = False
          pj_disparo.top = -1000

# ------------------------------------------------------------------------ Colision disparo-npc_nave2
     if pj_disparo.colliderect(npc_nave2):
          hp_npc_nave2 -= 1
          if  hp_npc_nave2 == 0:
               naves_destruidas += 1
               puntuacion += 5
               npc_nave2.left = 2000
               npc_nave2.top = 2000
               npc_nave2_aparecer = False
               npc_nave3_escudo.left = 2000
               npc_nave3_escudo.top = 2000
               npc_nave3_escudo_activo = False
               disparoActivo_npc_nave2 = False
          pj_disparo.top = -1000

# ------------------------------------------------------------------------ Colision disparo-npc_nave3
     if pj_disparo.colliderect(npc_nave3):
          hp_npc_nave3 -= 1
          if  hp_npc_nave3 == 0:
               naves_destruidas += 1
               puntuacion += 5
               npc_nave3.left = 2000
               npc_nave3.top = 2000
               npc_nave3_aparecer = False
               disparoActivo_npc_nave3 = False
          pj_disparo.top = -1000

# ------------------------------------------------------------------------ Colision disparo-npc_nave3_escudo
     if pj_disparo.colliderect(npc_nave3_escudo):
          pj_disparo.top = -1000

# ------------------------------------------------------------------------ Colision disparo-npc_boss
     if pj_disparo.colliderect(npc_boss):
          hp_npc_boss -= 1
          if  hp_npc_boss == 0:
               naves_destruidas += 1
               puntuacion += 20
               npc_boss.left = 2000
               npc_boss.top = 2000
               npc_boss_aparecer = False
               disparoActivo_npc_boss = False
               disparo2Activo_npc_boss = False
          pj_disparo.top = -1000
          
# ------------------------------------------------------------------------ Colision disparo-npc_boss_escudo
     if pj_disparo.colliderect(npc_boss_escudo):
          hp_npc_boss_escudo -= 1
          pj_disparo.top = -1000
          if hp_npc_boss_escudo == 0:
               npc_boss_escudo.left = 2000
               npc_boss_escudo.top = 2000
               npc_boss_escudo_aparecer = False
               npc_boss_escudo_activo = False
          
# ------------------------------------------------------------------------ Naves enemigas
     if puntuacion == 5:                                                   #Respawn_nivel1
          nivel = 1
          
     if nivel == 1:
          npc_nave_aparecer = True
          if npc_nave_aparecer == True and npc_nave.top < 70:
               npc_nave.top += velocidad_respawn
               
          if npc_nave.top == 70 and npc_nave_aparecer == True:             #Movimiento npc_nave
               if npc_nave.left < pj_nave.left:
                    npc_nave.left += velocidad_npc_nave
               if npc_nave.left > pj_nave.left:
                    npc_nave.left -= velocidad_npc_nave
               

          if  npc_nave.top == 70 and not disparoActivo_npc_nave:           #Disparo npc_nave
               disparoActivo_npc_nave = True
               npc_nave_disparo.left = npc_nave.left + 23  
               npc_nave_disparo.top = npc_nave.top + 25

          if disparoActivo_npc_nave == True:             
               npc_nave_disparo.top += disparo_npc_nave         
               if npc_nave_disparo.top >= 600:
                    disparoActivo_npc_nave = False
                    
# ------------------------------------------------------------------------
     if naves_destruidas == 1:                                             #Respawn_nivel2
          nivel = 2
          
     if nivel == 2:
          npc_nave2_aparecer = True
          npc_nave3_aparecer = True
          npc_nave3_escudo_activo = True
          
          if npc_nave2_aparecer == True and npc_nave2.top < 70:
                npc_nave2.top += velocidad_respawn
                    
          if npc_nave2.top == 70 and npc_nave2_aparecer == True:          #Movimiento npc_nave2
               if npc_nave2.left < pj_nave.left:
                    npc_nave2.left += velocidad_npc_nave
               if npc_nave2.left > pj_nave.left:
                    npc_nave2.left -= velocidad_npc_nave
                    

          if  npc_nave2.top == 70 and not disparoActivo_npc_nave2:        #Disparo npc_nave2
               disparoActivo_npc_nave2 = True
               npc_nave2_disparo.left = npc_nave2.left + 23  
               npc_nave2_disparo.top = npc_nave2.top + 25

          if disparoActivo_npc_nave2 == True:             
               npc_nave2_disparo.top += disparo_npc_nave         
               if npc_nave2_disparo.top >= 600:
                    disparoActivo_npc_nave2 = False



          if npc_nave3_aparecer == True and npc_nave3.top < 140:
                npc_nave3.top += velocidad_respawn
                    
          if npc_nave3.top == 140 and npc_nave2_aparecer == True and hp_npc_boss > 0:#Movimiento npc_nave3
               if npc_nave3.left < pj_nave.left:
                    npc_nave3.left += velocidad_npc_nave3
               if npc_nave3.left > pj_nave.left:
                    npc_nave3.left -= velocidad_npc_nave3
                    

          if  npc_nave3.top == 140 and not disparoActivo_npc_nave3:        #Disparo npc_nave3
               disparoActivo_npc_nave3 = True
               npc_nave3_disparo.left = npc_nave3.left + 23  
               npc_nave3_disparo.top = npc_nave3.top + 25

          if disparoActivo_npc_nave3 == True:             
               npc_nave3_disparo.top += disparo_npc_nave         
               if npc_nave3_disparo.top >= 600:
                    disparoActivo_npc_nave3 = False

          if npc_nave3_escudo_activo == True and npc_nave2.top == 70:
               npc_nave3_escudo.left = npc_nave3.left - 12
               npc_nave3_escudo.top = npc_nave3.top + 45

# ------------------------------------------------------------------------
     if naves_destruidas == 3:                                             #Respawn_nivel3
          nivel = 3
          
     if nivel == 3:
          npc_boss_aparecer = True
          npc_boss_escudo_activo = True
          
          if npc_boss_aparecer == True and npc_boss.top < 20:
               npc_boss.top += velocidad_respawn
               npc_boss_respawn = True
               

          if npc_boss_respawn == True and npc_boss_aparecer == True:       #Movimiento npc_boss
               npc_boss.left += velocidad_npc_bossX
               npc_boss.top += velocidad_npc_bossY
               if npc_boss.left < 0 or npc_boss.right > ancho:
                    velocidad_npc_bossX = -velocidad_npc_bossX
               if npc_boss.top < 20 or npc_boss.top > 250:
                    velocidad_npc_bossY = -velocidad_npc_bossY

          if npc_boss_escudo_activo == True and hp_npc_boss_escudo > 0:
               npc_boss_escudo.left = npc_boss.left
               npc_boss_escudo.top = npc_boss.top + alto_medio_npc_boss + 45


          if  hp_npc_boss > 0 and not disparoActivo_npc_boss:              #Disparo npc_boss
               disparoActivo_npc_boss = True
               npc_boss_disparo.left = npc_boss.left + ancho_medio_npc_boss - ancho_medio_npc_boss/2  
               npc_boss_disparo.top = npc_boss.top + alto_medio_npc_boss

          if disparoActivo_npc_boss == True:             
               npc_boss_disparo.top += disparo_npc_nave         
               if npc_boss_disparo.top >= 600:
                    disparoActivo_npc_boss = False

          if  hp_npc_boss > 0 and not disparo2Activo_npc_boss:             #Disparo2 npc_boss
               disparo2Activo_npc_boss = True
               npc_boss_disparo2.left = npc_boss.left + ancho_medio_npc_boss + ancho_medio_npc_boss/2  
               npc_boss_disparo2.top = npc_boss.top + alto_medio_npc_boss

          if disparo2Activo_npc_boss == True:             
               npc_boss_disparo2.top += disparo_npc_nave         
               if npc_boss_disparo2.top >= 600:
                    disparo2Activo_npc_boss = False
               
# ------------------------------------------------------------------------ Mostrar en pantalla

     PANTALLA.blit(fondo,(fondox,fondoy))
     PANTALLA.blit(Roca,npc_roca)
     PANTALLA.blit(Roca2,npc_roca2)
     PANTALLA.blit(Nave,pj_nave)
     if disparoActivo:
          PANTALLA.blit(Disparo, pj_disparo)
     PANTALLA.blit(NaveNPC, npc_nave)
     if disparoActivo_npc_nave:
          PANTALLA.blit(DisparoNPCNave, npc_nave_disparo)
     PANTALLA.blit(NaveNPC2, npc_nave2)
     if disparoActivo_npc_nave2:
          PANTALLA.blit(DisparoNPCNave2, npc_nave2_disparo)
     PANTALLA.blit(NaveNPC3, npc_nave3)
     if disparoActivo_npc_nave3:
          PANTALLA.blit(DisparoNPCNave3, npc_nave3_disparo)
     PANTALLA.blit(EscudoNPCNave3, npc_nave3_escudo)
     PANTALLA.blit(BossNPC, npc_boss)
     if disparoActivo_npc_boss:
          PANTALLA.blit(DisparoNPCBoss, npc_boss_disparo)
     if disparo2Activo_npc_boss:
          PANTALLA.blit(Disparo2NPCBoss, npc_boss_disparo2)
     PANTALLA.blit(EscudoNPCBoss, npc_boss_escudo)
     
     tiempo_seg = pygame.time.get_ticks()/1000                             #Tiempo transcurrido
     tiempo_seg = str(tiempo_seg)                                          #
     contador_tiempo = fuente1.render(tiempo_seg, 0, BLANCO)               #
     PANTALLA.blit(contador_tiempo,(760,580))                              #

     puntuacion_str = str(puntuacion)                                      #Puntuacion
     contador_puntuacion = fuente1.render(puntuacion_str, 0, BLANCO)       #
     PANTALLA.blit(contador_puntuacion,(760, 15))                          #
     texto_puntuacion = fuente1.render("Puntuacion:",0,BLANCO)             #
     PANTALLA.blit(texto_puntuacion,(650,15))                              #

     naves_destruidas_str = str(naves_destruidas)                          #Naves destruidas
     contador_naves_destruidas = fuente1.render(naves_destruidas_str, 0, BLANCO)#
     PANTALLA.blit(contador_naves_destruidas,(165, 15))                    #
     texto_naves_destruida = fuente1.render("Naves destruidas:",0,BLANCO)  #
     PANTALLA.blit(texto_naves_destruida,(15,15))    
     
# ------------------------------------------------------------------------     
     pygame.display.update()                                               #Actualizar juego       
reloj.tick(40)
pygame.quit()                                                            
quit()
