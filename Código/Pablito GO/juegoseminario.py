import pygame, sys
import random
from pygame.locals import *
 
# ------------------------------------------------------------------------ Definir colores

ancho = 800
alto = 600
respawn_naves_ancho1 = 100
respawn_naves_ancho2 = 700
ancho_medio_nave = 32                                                      #ancho nave = 63
alto_medio_nave = 31                                                       #alto nave = 61
velocidadX = 1
velocidadY = 1
  

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
pygame.init()
PANTALLA = pygame.display.set_mode((800,600))                              #Resolución
pygame.display.set_caption('PABLITO GO')                                   #Nombre del juego en la ventana
SalirJuego= False
reloj = pygame.time.Clock()

Nave = pygame.image.load("Nave.gif")
pj_nave = Nave.get_rect()
pj_nave.left = 400
pj_nave.top = 450

Roca = pygame.image.load("moustro.png")
npc_roca = Roca.get_rect()
npc_roca.left = random.randint(respawn_naves_ancho1, respawn_naves_ancho2)
npc_roca.top = 100

Disparo = pygame.image.load("Disparo.gif")    
pj_disparo = Disparo.get_rect()        
disparoActivo = False                               
 
fondo = pygame.image.load("Fondo.jpg")
fondox=0
fondoy=0
# ------------------------------------------------------------------------ Musica del juego
pygame.mixer.music.load("melodyloops-adrenaline.mp3")
pygame.mixer.music.play(-1,0.0)
# ------------------------------------------------------------------------ Eventos del juego

while not SalirJuego:
     for event in pygame.event.get():                                      #recorremos los eventos de pygame
        if event.type== pygame.QUIT:
               SalirJuego=True
               
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and pj_nave.left >= ancho_medio_nave:
                    pj_nave.move_ip(-30,0)
            if event.key == pygame.K_RIGHT and pj_nave.right <= ancho - ancho_medio_nave:
                    pj_nave.move_ip(30,0)
            if event.key == pygame.K_UP and pj_nave.top >= alto_medio_nave:
                    pj_nave.move_ip(0,-30)
            if event.key == pygame.K_DOWN and pj_nave.top <= alto - alto_medio_nave*3:
                    pj_nave.move_ip(0,30)

                    
     keys = pygame.key.get_pressed()  
 
# ------------------------------------------------------------------------ Movimiento de la roca
     npc_roca.left += velocidadX                  
     npc_roca.top += velocidadY                   
     if npc_roca.left < 0 or npc_roca.right > ancho:
           velocidadX = -velocidadX                          
     if npc_roca.top < 0 or npc_roca.bottom > alto:
           velocidadY = -velocidadY

     if keys[K_SPACE] and not disparoActivo:      
        disparoActivo = True                      
        pj_disparo.left = pj_nave.left + 23  
        pj_disparo.top = pj_nave.top - 25
# ------------------------------------------------------------------------

     if disparoActivo:             
        pj_disparo.top -= 4         
        if pj_disparo.top <= 0:     
            disparoActivo = False     

        
 
 
# ------------------------------------------------------------------------dibujos y personajes del juego

     PANTALLA.fill(NEGRO)
     PANTALLA.blit(fondo,(fondox,fondoy))
     PANTALLA.blit(Roca,npc_roca)
     PANTALLA.blit(Nave,pj_nave)
     if disparoActivo:                     
        PANTALLA.blit(Disparo, pj_disparo)
     pygame.display.update()                                          #actualiza el juego       
reloj.tick(40)
pygame.quit()                                                            
quit()
