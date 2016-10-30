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
ancho_medio_nave = 32                                                      #ancho nave = 63
alto_medio_nave = 31                                                       #alto nave = 61
velocidad_npc_nave = 2

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
naves_destruidas = 0                                                       #Contador naves destruidas

# ------------------------------------------------------------------------
pygame.init()
PANTALLA = pygame.display.set_mode((ancho,alto))                           #Setear resolucion de pantalla
pygame.display.set_caption('PABLITO GO')                                   #Nombre del juego en la ventana
fuente1 = pygame.font.SysFont ("Calibri", 20, True, False)

SalirJuego= False
reloj = pygame.time.Clock()

# ------------------------------------------------------------------------
Nave = pygame.image.load("Nave.gif")
pj_nave = Nave.get_rect()
pj_nave.left = 400
pj_nave.top = 450

Disparo = pygame.image.load("Disparo.gif")    
pj_disparo = Disparo.get_rect()        
disparoActivo = False


NaveNPC = pygame.image.load("npc_nave.gif")
npc_nave = NaveNPC.get_rect()
npc_nave.left = random.randint(100, 700)
npc_nave.top = -200
npc_nave_aparecer = False

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
     
# ------------------------------------------------------------------------ Movimiento de la roca
#     npc_roca.left += velocidadX                  
#     npc_roca.top += velocidadY                   
#     if npc_roca.left < 0 or npc_roca.right > ancho:
#           velocidadX = -velocidadX                          
#     if npc_roca.top < 0 or npc_roca.bottom > alto:
#           velocidadY = -velocidadY
     velocidadX1 = random.randint(1, 3)
     velocidadY1 = random.randint(1, 2)
     npc_roca.left += velocidadX1
     npc_roca.top += velocidadY1

# ------------------------------------------------------------------------ Movimiento de la roca2
     velocidadX2 = random.randint(1, 3)
     velocidadY2 = random.randint(1, 2)
     npc_roca2.left += -velocidadX2
     npc_roca2.top += velocidadY2
           
# ------------------------------------------------------------------------ Disparo
     if keys[K_SPACE] and not disparoActivo:      
        disparoActivo = True                      
        pj_disparo.left = pj_nave.left + 23  
        pj_disparo.top = pj_nave.top - 25

     if disparoActivo:             
        pj_disparo.top -= 4         
        if pj_disparo.top <= 0 or pj_disparo.colliderect(npc_roca) or pj_disparo.colliderect(npc_roca2): 
          disparoActivo = False     

# ------------------------------------------------------------------------ Respawn roca1

     if npc_roca.left > 950 or npc_roca.top > 750:
          npc_roca.left = random.randint(-700, respawn_medio/2)
          npc_roca.top = random.randint(-200, -10)

# ------------------------------------------------------------------------ Respawn roca2

     if npc_roca2.left < -150 or npc_roca2.top > 750:
          npc_roca2.left = random.randint((respawn_medio+respawn_medio/2), 1200)
          npc_roca2.top = random.randint(-200, -10)

# ------------------------------------------------------------------------ Colision disparo-roca
     if pj_disparo.colliderect(npc_roca):
          puntuacion += 1
          npc_roca.left = random.randint(-700, respawn_medio/2)
          npc_roca.top = random.randint(-200, -10)
          pj_disparo.left = 1000
          pj_disparo.top = 1000
          
# ------------------------------------------------------------------------ Colision disparo-roca2
     if pj_disparo.colliderect(npc_roca2):
          puntuacion += 1
          npc_roca2.left = random.randint(-700, respawn_medio/2)
          npc_roca2.top = random.randint(-200, -10)
          pj_disparo.left = 2000
          pj_disparo.top = 2000

# ------------------------------------------------------------------------ Nave enemiga
     if puntuacion == 5:
          npc_nave_aparecer = True
          if npc_nave_aparecer == True and npc_nave.top < 100:
               npc_nave.top += velocidad_npc_nave
     if npc_nave.top == 100:
          if npc_nave.left < pj_nave.left:
               npc_nave.left += velocidad_npc_nave
          if npc_nave.left > pj_nave.left:
               npc_nave.left -= velocidad_npc_nave
                    
# ------------------------------------------------------------------------ Mostrar en pantalla

     PANTALLA.blit(fondo,(fondox,fondoy))
     PANTALLA.blit(Roca,npc_roca)
     PANTALLA.blit(Roca2,npc_roca2)
     PANTALLA.blit(Nave,pj_nave)
     if disparoActivo:
        PANTALLA.blit(Disparo, pj_disparo)
     PANTALLA.blit(NaveNPC, npc_nave)
     
     tiempo_seg = pygame.time.get_ticks()/1000                             #Tiempo transcurrido
     tiempo_seg = str(tiempo_seg)                                          #
     contador_tiempo = fuente1.render(tiempo_seg, 0, BLANCO)               #
     PANTALLA.blit(contador_tiempo,(760,580))                              #

     puntuacion_str = str(puntuacion)                                      #Puntuacion
     contador_puntuacion = fuente1.render(puntuacion_str, 0, BLANCO)       #
     PANTALLA.blit(contador_puntuacion,(760, 15))                          #
     texto_puntuacion = fuente1.render("Puntuacion:",0,BLANCO)             #
     PANTALLA.blit(texto_puntuacion,(650,15))                              #
     
# ------------------------------------------------------------------------     
     pygame.display.update()                                               #Actualizar juego       
reloj.tick(40)
pygame.quit()                                                            
quit()
