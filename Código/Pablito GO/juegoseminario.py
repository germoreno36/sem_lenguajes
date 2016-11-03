import pygame, sys
import random
from datetime import datetime
from pygame.locals import *


class  Cursor(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self,0,0,1,1)
    def update(self):
        self.left,self.top=pygame.mouse.get_pos()
        
class boton(pygame.sprite.Sprite):
    def __init__(self,imagen1,imagen2,x=200,y=200):
         self.imagen_normal=imagen1
         self.imagen_seleccion=imagen2
         self.imagen_actual=self.imagen_normal
         self.rect=self.imagen_actual.get_rect()
         self.rect.left,self.rect.top=(x,y)
         
    def update(self,PANTALLA,cursor):
        if cursor.colliderect(self.rect):
            self.imagen_actual=self.imagen_seleccion
        else: self.imagen_actual=self.imagen_normal
        PANTALLA.blit(self.imagen_actual,self.rect)
        
# ------------------------------------------------------------------------Resolucion pantalla
ancho = 800
alto = 600
pygame.init()
PANTALLA = pygame.display.set_mode((ancho,alto))                                    #Setear resolucion de pantalla
pygame.display.set_caption('PABLITO GO')                                            #Nombre del juego en la ventana

jugar = pygame.image.load("botones/jugar1.gif")                                      #BOTONES
jugar1 = pygame.image.load("botones/jugar2.gif")

gameplay = pygame.image.load("botones/gameplay1.gif")
gameplay1 = pygame.image.load("botones/gameplay2.gif")

#verpuntos = pygame.image.load("botones/puntajes1.gif")
#verpuntos1 = pygame.image.load("botones/puntajes2.gif")

salirjuego = pygame.image.load("botones/salir1.gif")
salirjuego1 = pygame.image.load("botones/salir2.gif")

menuinicial =  pygame.image.load("botones/inicio1.gif")
menuinicial1= pygame.image.load("botones/inicio2.gif")
       
boton_jugar = boton(jugar,jugar1,100,312)
boton_gameplay = boton(gameplay,gameplay1,125,362)
#boton_ver_puntos = boton(verpuntos,verpuntos1,150,412)
boton_salir_juego = boton(salirjuego,salirjuego1,175,462)
boton_menu_inicial = boton(menuinicial,menuinicial1,650,508)
cursor=Cursor()

musica_inicio_gameplay = True
estado_app = 1                                                                      #Estado applicacion
puntuacion_obtenida = 0                                                             #Conservar puntuacion

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
while estado_app !=7:                                                               # 7 = Salir
    if musica_inicio_gameplay == True:
        pygame.mixer.music.load("musica/(11) Showdown.mp3")
        pygame.mixer.music.play(-1,0.0)
    while estado_app == 1:                                                          # 1 = Menu Inicio
        menuF = pygame.image.load("fondos/Pablito GO Menu.jpg")
        Fx=0
        Fy=0
        for event in pygame.event.get():
                 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cursor.colliderect(boton_jugar.rect):
                    estado_app = 2

                if cursor.colliderect(boton_gameplay.rect):
                    estado_app = 3
                    
                #if cursor.colliderect(boton_ver_puntos.rect):
                #    estado_app = 4
                          
                if cursor.colliderect(boton_salir_juego.rect):
                    estado_app = 7
                          
               
        PANTALLA.blit(menuF,(Fx,Fy))              
        boton_jugar.update(PANTALLA,cursor)
        boton_gameplay.update(PANTALLA,cursor)
        #boton_ver_puntos.update(PANTALLA,cursor)
        boton_salir_juego.update(PANTALLA,cursor)
        cursor.update()
        pygame.display.update()

# ------------------------------------------------------------------------        
    while estado_app == 2:                                                          # 2 = Juego
        
    # ------------------------------------------------------------------------ Divisiones para respawn
        respawn_naves_ancho1 = 100
        respawn_naves_ancho2 = 700
        respawn_medio = 400

    # ------------------------------------------------------------------------
        ancho_medio_nave = 27                                                       #ancho nave = 54
        alto_medio_nave = 32                                                        #alto nave = 68

        ancho_medio_npc_nave = 30                                                   #ancho npc_nave = 60
        alto_medio_npc_nave = 37                                                    #alto npc_nave = 53

        ancho_escudo = 84
        alto_escudo = 43

        ancho_medio_npc_boss = 100                                                  #ancho npc_boss = 200
        alto_medio_npc_boss = 64                                                    #alto npc_boss = 123

        disparo_npc_nave = 3
        velocidad_respawn = 2

        velocidad_npc_nave = 1                                                      #velocidad nave 1 y 2
        velocidad_npc_nave3 = 3
        velocidad_npc_bossX = 4
        velocidad_npc_bossY = 2

        hp_npc_nave = 2
        hp_npc_nave2 = 2
        hp_npc_nave3 = 3
        hp_npc_boss = 5
        hp_npc_boss_escudo = 3


        pj_nave_hp = 3
        escudo_inventario = 0
        pj_escudo_hp = 2

        # ------------------------------------------------------------------------
        puntuacion = 0                                                              #Contador puntuacion
        rocas_destruidas = 0
        naves_destruidas = 0                                                        #Contador naves destruidas
        nivel = 0
        
        # ------------------------------------------------------------------------ 
        fuente1 = pygame.font.SysFont ("Calibri", 20, True, False)

        SalirJuego= False
        reloj = pygame.time.Clock()
          
        # ------------------------------------------------------------------------
        Nave = pygame.image.load("imagenes/pj_nave.gif")                                     #PJ nave
        pj_nave = Nave.get_rect()
        pj_nave.left = 400
        pj_nave.top = 450

        Disparo = pygame.image.load("imagenes/PJ Disparo.gif")                               #PJ Disparo
        pj_disparo = Disparo.get_rect()        
        disparoActivo = False

        Escudo = pygame.image.load("imagenes/PJ Escudo.gif")                                 #PJ Escudo
        pj_escudo = Escudo.get_rect()
        pj_escudo.left = pj_nave.left
        pj_escudo.top = pj_nave.top - alto_medio_nave
        escudoActivo = False

        Vida = pygame.image.load("imagenes/pj_vida.gif")                                     #Vidas
        pj_vida = Vida.get_rect()
        pj_vida.left = 72
        pj_vida.top = 562
        vidaActiva = True

        Vida2 = pygame.image.load("imagenes/pj_vida.gif")
        pj_vida2 = Vida.get_rect()
        pj_vida2.left = 115
        pj_vida2.top = 562
        vida2Activa = True

        ItemEscudo = pygame.image.load ("imagenes/Escudo_Item.gif")                          #Item Escudo
        item_escudo = ItemEscudo.get_rect()
        item_escudo.left = random.randint(100,700)
        item_escudo.top = -200
        item_escudo_aparecer = False
        item_escudo_activo = False


        NaveNPC = pygame.image.load("imagenes/npc_nave.gif")                                 #NPC Nave
        npc_nave = NaveNPC.get_rect()
        npc_nave.left = random.randint(100, 700)
        npc_nave.top = -200
        npc_nave_aparecer = False

        DisparoNPCNave = pygame.image.load("imagenes/NPC Disparo.gif")    
        npc_nave_disparo = DisparoNPCNave.get_rect()        
        disparoActivo_npc_nave = False

        NaveNPCVida = pygame.image.load("imagenes/npc_barra_salud.gif")
        npc_nave_barra_salud = NaveNPCVida.get_rect()
        npc_nave_barra_salud.left = npc_nave.left + ancho_medio_npc_nave-12
        npc_nave_barra_salud.top = npc_nave.top + alto_medio_npc_nave/3
        npc_nave_barra_salud_aparecer = False

        NaveNPCVida2 = pygame.image.load("imagenes/npc_barra_salud.gif")
        npc_nave_barra_salud2 = NaveNPCVida2.get_rect()
        npc_nave_barra_salud2.left = npc_nave.left + ancho_medio_npc_nave-1
        npc_nave_barra_salud2.top = npc_nave.top + alto_medio_npc_nave/3
        npc_nave_barra_salud2_aparecer = False


        NaveNPC2 = pygame.image.load("imagenes/npc_nave2.gif")                               #NPC Nave2
        npc_nave2 = NaveNPC2.get_rect()
        npc_nave2.left = random.randint(100, 700)
        npc_nave2.top = -200
        npc_nave2_aparecer = False

        DisparoNPCNave2 = pygame.image.load("imagenes/NPC Disparo.gif")    
        npc_nave2_disparo = DisparoNPCNave2.get_rect()        
        disparoActivo_npc_nave2 = False

        NaveNPC2Vida = pygame.image.load("imagenes/npc_barra_salud.gif")
        npc_nave2_barra_salud = NaveNPC2Vida.get_rect()
        npc_nave2_barra_salud.left = npc_nave2.left + ancho_medio_npc_nave-12
        npc_nave2_barra_salud.top = npc_nave2.top + alto_medio_npc_nave/3

        NaveNPC2Vida2 = pygame.image.load("imagenes/npc_barra_salud.gif")
        npc_nave2_barra_salud2 = NaveNPC2Vida2.get_rect()
        npc_nave2_barra_salud2.left = npc_nave2.left + ancho_medio_npc_nave-1
        npc_nave2_barra_salud2.top = npc_nave2.top + alto_medio_npc_nave/3


        NaveNPC3 = pygame.image.load("imagenes/npc_nave.gif")                                #NPC Nave3
        npc_nave3 = NaveNPC3.get_rect()
        npc_nave3.left = random.randint(100, 700)
        npc_nave3.top = -200
        npc_nave3_aparecer = False

        DisparoNPCNave3 = pygame.image.load("imagenes/NPC Disparo.gif")
        npc_nave3_disparo = DisparoNPCNave3.get_rect()        
        disparoActivo_npc_nave3 = False

        NaveNPC3Vida = pygame.image.load("imagenes/npc_barra_salud.gif")
        npc_nave3_barra_salud = NaveNPC3Vida.get_rect()
        npc_nave3_barra_salud.left = npc_nave3.left + ancho_medio_npc_nave-17
        npc_nave3_barra_salud.top = npc_nave3.top + alto_medio_npc_nave/3

        NaveNPC3Vida2 = pygame.image.load("imagenes/npc_barra_salud.gif")
        npc_nave3_barra_salud2 = NaveNPC3Vida2.get_rect()
        npc_nave3_barra_salud2.left = npc_nave3.left + ancho_medio_npc_nave-6
        npc_nave3_barra_salud2.top = npc_nave3.top + alto_medio_npc_nave/3

        NaveNPC3Vida3 = pygame.image.load("imagenes/npc_barra_salud.gif")
        npc_nave3_barra_salud3 = NaveNPC3Vida3.get_rect()
        npc_nave3_barra_salud3.left = npc_nave3.left + ancho_medio_npc_nave+5
        npc_nave3_barra_salud3.top = npc_nave3.top + alto_medio_npc_nave/3

        EscudoNPCNave3 = pygame.image.load("imagenes/NPC Escudo.gif")                        #NPC Nave3 Escudo
        npc_nave3_escudo = EscudoNPCNave3.get_rect()
        npc_nave3_escudo.left = npc_nave3.left
        npc_nave3_escudo.top = npc_nave3.top + alto_medio_npc_nave
        npc_nave3_escudo_activo = True

        EscudoNPCNave3Vida = pygame.image.load("imagenes/npc_barra_salud2.gif")
        npc_nave3_escudo_barra_salud = EscudoNPCNave3Vida.get_rect()
        npc_nave3_escudo_barra_salud.left = npc_nave3.left + ancho_medio_npc_nave-6
        npc_nave3_escudo_barra_salud.top = npc_nave3.top + alto_medio_npc_nave/3+7


        BossNPC = pygame.image.load("imagenes/npc_boss.gif")                                 #NPC Boss
        npc_boss = BossNPC.get_rect()
        npc_boss.left = (ancho/2) - ancho_medio_npc_boss/2
        npc_boss.top = -200
        npc_boss_aparecer = False
        npc_boss_respawn = False

        DisparoNPCBoss = pygame.image.load("imagenes/NPC Disparo.gif")
        npc_boss_disparo = DisparoNPCBoss.get_rect()        
        disparoActivo_npc_boss = False

        Disparo2NPCBoss = pygame.image.load("imagenes/NPC Disparo.gif")    
        npc_boss_disparo2 = Disparo2NPCBoss.get_rect()        
        disparo2Activo_npc_boss = False

        BossNPCVida = pygame.image.load("imagenes/npc_barra_salud.gif")
        npc_boss_barra_salud = BossNPCVida.get_rect()
        npc_boss_barra_salud.left = npc_boss.left + ancho_medio_npc_boss-28
        npc_boss_barra_salud.top = npc_boss.top + alto_medio_npc_boss/3

        BossNPCVida2 = pygame.image.load("imagenes/npc_barra_salud.gif")
        npc_boss_barra_salud2 = BossNPCVida2.get_rect()
        npc_boss_barra_salud2.left = npc_boss.left + ancho_medio_npc_boss-17
        npc_boss_barra_salud2.top = npc_boss.top + alto_medio_npc_boss/3

        BossNPCVida3 = pygame.image.load("imagenes/npc_barra_salud.gif")
        npc_boss_barra_salud3 = BossNPCVida3.get_rect()
        npc_boss_barra_salud3.left = npc_boss.left + ancho_medio_npc_boss-6
        npc_boss_barra_salud3.top = npc_boss.top + alto_medio_npc_boss/3

        BossNPCVida4 = pygame.image.load("imagenes/npc_barra_salud.gif")
        npc_boss_barra_salud4 = BossNPCVida4.get_rect()
        npc_boss_barra_salud4.left = npc_boss.left + ancho_medio_npc_boss+5
        npc_boss_barra_salud4.top = npc_boss.top + alto_medio_npc_boss/3

        BossNPCVida5 = pygame.image.load("imagenes/npc_barra_salud.gif")
        npc_boss_barra_salud5 = BossNPCVida5.get_rect()
        npc_boss_barra_salud5.left = npc_boss.left + ancho_medio_npc_boss+16
        npc_boss_barra_salud5.top = npc_boss.top + alto_medio_npc_boss/3

        EscudoNPCBoss = pygame.image.load("imagenes/Escudo NPC Boss.gif")                    #NPC Boss Escudo
        npc_boss_escudo = EscudoNPCBoss.get_rect()
        npc_boss_escudo.left = npc_boss.left
        npc_boss_escudo.top = npc_boss.top
        npc_boss_escudo_activo = False

        EscudoNPCBossVida = pygame.image.load("imagenes/npc_barra_salud2.gif")
        npc_boss_escudo_barra_salud = EscudoNPCBossVida.get_rect()
        npc_boss_escudo_barra_salud.left = npc_boss.left + ancho_medio_npc_boss-17
        npc_boss_escudo_barra_salud.top = npc_boss.top + alto_medio_npc_boss/3+7

        EscudoNPCBossVida2 = pygame.image.load("imagenes/npc_barra_salud2.gif")
        npc_boss_escudo_barra_salud2 = EscudoNPCBossVida2.get_rect()
        npc_boss_escudo_barra_salud2.left = npc_boss.left + ancho_medio_npc_boss-6
        npc_boss_escudo_barra_salud2.top = npc_boss.top + alto_medio_npc_boss/3+7

        EscudoNPCBossVida3 = pygame.image.load("imagenes/npc_barra_salud2.gif")
        npc_boss_escudo_barra_salud3 = EscudoNPCBossVida3.get_rect()
        npc_boss_escudo_barra_salud3.left = npc_boss.left + ancho_medio_npc_boss+5
        npc_boss_escudo_barra_salud3.top = npc_boss.top + alto_medio_npc_boss/3+7

        Roca = pygame.image.load("imagenes/Roca1.gif")
        npc_roca = Roca.get_rect()
        npc_roca.left = random.randint(-700, respawn_medio/2)
        npc_roca.top = random.randint(-200, -10)

        Roca2 = pygame.image.load("imagenes/Roca2.gif")
        npc_roca2 = Roca2.get_rect()
        npc_roca2.left = random.randint((respawn_medio+respawn_medio/2), 1200)
        npc_roca2.top = random.randint(-200, -10)                       

           
        fondo = pygame.image.load("fondos/Fondo.jpg")
        fondox=0
        fondoy=0      

        # ------------------------------------------------------------------------ Estado puntos extra al ganar
        puntos_otorgados = False

        # ------------------------------------------------------------------------ Musica del juego
        pygame.mixer.music.load("musica/Melodyloops adrenaline.mp3")
        pygame.mixer.music.play(-1,0.0)
        
        # ------------------------------------------------------------------------ Eventos del juego

        while not SalirJuego:
            for event in pygame.event.get():                                        #recorrer eventos de pygame
                if event.type== pygame.QUIT:
                    SalirJuego=True
                    
            keys = pygame.key.get_pressed()
            
        # ------------------------------------------------------------------------ Movimiento de la nave               
        #        if event.type == pygame.KEYDOWN:                                    #Movimiento por teclado
        #        if keys[K_LEFT]and pj_nave.left >= ancho_medio_nave :
        #            pj_nave.left -= 4
        #        if keys[K_RIGHT]and pj_nave.right <= ancho - ancho_medio_nave :
        #            pj_nave.left += 4
        #        if keys[K_UP] and pj_nave.top >= alto_medio_nave:
        #            pj_nave.top -= 4  
        #        if keys[K_DOWN]and pj_nave.top <= alto - alto_medio_nave*3:
        #            pj_nave.top += 4

            pj_nave.left, pj_nave.top = pygame.mouse.get_pos()                      #Movimiento por mouse
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
                    npc_nave_disparo.top = -100
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
                    npc_nave2_disparo.top = -100
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
                    npc_nave3_disparo.top = -100
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
                         
        # ------------------------------------------------------------------------ Colisiones npc_disparos-pj_nave
            if npc_nave_disparo.colliderect(pj_nave) and npc_nave_aparecer == True:
                disparoActivo_npc_nave = False
                pj_nave_hp -= 1

            if npc_nave2_disparo.colliderect(pj_nave) and npc_nave2_aparecer == True:
                disparoActivo_npc_nave2 = False
                pj_nave_hp -= 1

            if npc_nave3_disparo.colliderect(pj_nave) and npc_nave3_aparecer == True:
                disparoActivo_npc_nave3 = False
                pj_nave_hp -= 1

            if npc_boss_disparo.colliderect(pj_nave) and npc_boss_aparecer == True:
                disparoActivo_npc_boss = False
                pj_nave_hp -= 1

            if npc_boss_disparo2.colliderect(pj_nave) and npc_boss_aparecer == True:
                disparo2Activo_npc_boss = False
                pj_nave_hp -= 1

        # ------------------------------------------------------------------------ Colisiones npc_disparos-pj_escudo
            if npc_nave_disparo.colliderect(pj_escudo) and escudoActivo == True:
                disparoActivo_npc_nave = False
                pj_escudo_hp -=1

            if npc_nave2_disparo.colliderect(pj_escudo) and escudoActivo == True:
                disparoActivo_npc_nave2 = False
                pj_escudo_hp -=1

            if npc_nave3_disparo.colliderect(pj_escudo) and escudoActivo == True:
                disparoActivo_npc_nave3 = False
                pj_escudo_hp -=1

            if npc_boss_disparo.colliderect(pj_escudo) and escudoActivo == True:
                disparoActivo_npc_boss = False
                pj_escudo_hp -=1

            if npc_boss_disparo2.colliderect(pj_escudo) and escudoActivo == True:
                disparo2Activo_npc_boss = False
                pj_escudo_hp -=1

        # ------------------------------------------------------------------------ Colisiones rocas,naves y escudos-pj_escudo
            if npc_roca.colliderect(pj_escudo) and escudoActivo == True:
                disparoActivo_npc_boss = False
                pj_escudo_hp = 0

            if npc_roca2.colliderect(pj_escudo) and escudoActivo == True:
                disparoActivo_npc_boss = False
                pj_escudo_hp = 0

            if npc_nave.colliderect(pj_escudo) and escudoActivo == True:
                disparoActivo_npc_boss = False
                pj_escudo_hp = 0

            if npc_nave2.colliderect(pj_escudo) and escudoActivo == True:
                disparoActivo_npc_boss = False
                pj_escudo_hp = 0

            if npc_nave3.colliderect(pj_escudo) and escudoActivo == True:
                disparoActivo_npc_boss = False
                pj_escudo_hp = 0

            if npc_nave3_escudo.colliderect(pj_escudo) and escudoActivo == True:
                disparoActivo_npc_boss = False
                pj_escudo_hp = 0

            if npc_boss.colliderect(pj_escudo) and escudoActivo == True:
                disparoActivo_npc_boss = False
                pj_escudo_hp = 0

            if npc_boss_escudo.colliderect(pj_escudo) and escudoActivo == True:
                disparoActivo_npc_boss = False
                pj_escudo_hp = 0
                    
        # ------------------------------------------------------------------------ Colisiones npc-pj_nave (Game Over instantaneo)
            if npc_roca.colliderect(pj_nave):
                pj_nave_hp = 0
            if npc_roca2.colliderect(pj_nave):
                pj_nave_hp = 0
            if npc_nave.colliderect(pj_nave):
                pj_nave_hp = 0
            if npc_nave2.colliderect(pj_nave):
                pj_nave_hp = 0
            if npc_nave3.colliderect(pj_nave):
                pj_nave_hp = 0
            if npc_nave3_escudo.colliderect(pj_nave):
                pj_nave_hp = 0
            if npc_boss.colliderect(pj_nave):
                pj_nave_hp = 0
            if npc_boss_escudo.colliderect(pj_nave):
                pj_nave_hp = 0

        # ------------------------------------------------------------------------ Item_escudo
            if puntuacion < 20 and puntuacion >= 15:
                item_escudo_aparecer = True

            if item_escudo_aparecer == True and item_escudo.top < 1000:
                item_escudo_activo = True
                item_escudo.top += velocidad_respawn

            if item_escudo.top == 1000:
                item_escudo_activo = False
                item_escudo_aparecer = False
                item_escudo.top = 1000
                
        # ------------------------------------------------------------------------ Colision Item_escudo-pj_nave
            if item_escudo.colliderect(pj_nave):
                escudo_inventario = 1
                item_escudo_activo = False
                item_escudo_aparecer = False
                item_escudo.top = 1000
                    
        # ------------------------------------------------------------------------ Uso item_escudo
            if keys[K_v] and escudo_inventario == 1:
                escudoActivo = True
                escudo_inventario = 0

        # ------------------------------------------------------------------------ Escudo activo
            if pj_escudo_hp <= 0:
                escudoActivo = False
                pj_escudo.left = 2000
                pj_escudo.top = 2000

        # ------------------------------------------------------------------------ Movimiento escudo
            pj_escudo.left, pj_escudo.top = pygame.mouse.get_pos()
            pj_escudo.left -= ancho_escudo/2
            pj_escudo.top -= alto_medio_nave*2 + alto_medio_nave/2

        # ------------------------------------------------------------------------ Naves enemigas
            if puntuacion == 5:                                                 #Respawn_nivel1
                nivel = 1
                    
            if nivel == 1:
                npc_nave_aparecer = True
                if npc_nave_aparecer == True and npc_nave.top < 70:
                    npc_nave.top += velocidad_respawn
                         
                if npc_nave.top == 70 and npc_nave_aparecer == True:            #Movimiento npc_nave
                    if npc_nave.left < pj_nave.left:
                        npc_nave.left += velocidad_npc_nave
                    if npc_nave.left > pj_nave.left:
                        npc_nave.left -= velocidad_npc_nave
                         

                if  npc_nave.top == 70 and not disparoActivo_npc_nave:          #Disparo npc_nave
                    disparoActivo_npc_nave = True
                    npc_nave_disparo.left = npc_nave.left + 23  
                    npc_nave_disparo.top = npc_nave.top + 25

                if disparoActivo_npc_nave == True:             
                    npc_nave_disparo.top += disparo_npc_nave         
                    if npc_nave_disparo.top >= 600:
                        disparoActivo_npc_nave = False

                if hp_npc_nave == 2:                                            #Movimiento npc_nave_barra_salud
                    npc_nave_barra_salud.left = npc_nave.left + ancho_medio_npc_nave-12
                    npc_nave_barra_salud.top = npc_nave.top + alto_medio_npc_nave/3
                    npc_nave_barra_salud2.left = npc_nave.left + ancho_medio_npc_nave-1
                    npc_nave_barra_salud2.top = npc_nave.top + alto_medio_npc_nave/3

                if hp_npc_nave == 1:
                    npc_nave_barra_salud.left = npc_nave.left + ancho_medio_npc_nave-12
                    npc_nave_barra_salud.top = npc_nave.top + alto_medio_npc_nave/3
                         
        # ------------------------------------------------------------------------
            if naves_destruidas == 1:                                           #Respawn_nivel2
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
                              

                if npc_nave2.top == 70 and not disparoActivo_npc_nave2:        #Disparo npc_nave2
                    disparoActivo_npc_nave2 = True
                    npc_nave2_disparo.left = npc_nave2.left + 23  
                    npc_nave2_disparo.top = npc_nave2.top + 25

                if disparoActivo_npc_nave2 == True:             
                    npc_nave2_disparo.top += disparo_npc_nave         
                    if npc_nave2_disparo.top >= 600:
                        disparoActivo_npc_nave2 = False

                if hp_npc_nave2 == 2:                                           #Movimiento npc_nave2_barra_salud
                    npc_nave2_barra_salud.left = npc_nave2.left + ancho_medio_npc_nave-12
                    npc_nave2_barra_salud.top = npc_nave2.top + alto_medio_npc_nave/3
                    npc_nave2_barra_salud2.left = npc_nave2.left + ancho_medio_npc_nave-1
                    npc_nave2_barra_salud2.top = npc_nave2.top + alto_medio_npc_nave/3

                if hp_npc_nave2 == 1:
                    npc_nave2_barra_salud.left = npc_nave2.left + ancho_medio_npc_nave-12
                    npc_nave2_barra_salud.top = npc_nave2.top + alto_medio_npc_nave/3


                if npc_nave3_aparecer == True and npc_nave3.top < 140:
                    npc_nave3.top += velocidad_respawn
                              
                if npc_nave3.top == 140 and npc_nave2_aparecer == True and hp_npc_boss > 0:#Movimiento npc_nave3
                    if npc_nave3.left < pj_nave.left:
                        npc_nave3.left += velocidad_npc_nave3
                    if npc_nave3.left > pj_nave.left:
                        npc_nave3.left -= velocidad_npc_nave3
                              

                if  npc_nave3.top == 140 and not disparoActivo_npc_nave3:       #Disparo npc_nave3
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

                if hp_npc_nave3 == 3:                                           #Movimiento npc_nave3_barra_salud
                    npc_nave3_barra_salud.left = npc_nave3.left + ancho_medio_npc_nave-17
                    npc_nave3_barra_salud.top = npc_nave3.top + alto_medio_npc_nave/3
                    npc_nave3_barra_salud2.left = npc_nave3.left + ancho_medio_npc_nave-6
                    npc_nave3_barra_salud2.top = npc_nave3.top + alto_medio_npc_nave/3
                    npc_nave3_barra_salud3.left = npc_nave3.left + ancho_medio_npc_nave+5
                    npc_nave3_barra_salud3.top = npc_nave3.top + alto_medio_npc_nave/3
                         
                if hp_npc_nave3 == 2:
                    npc_nave3_barra_salud.left = npc_nave3.left + ancho_medio_npc_nave-17
                    npc_nave3_barra_salud.top = npc_nave3.top + alto_medio_npc_nave/3
                    npc_nave3_barra_salud2.left = npc_nave3.left + ancho_medio_npc_nave-6
                    npc_nave3_barra_salud2.top = npc_nave3.top + alto_medio_npc_nave/3

                if hp_npc_nave3 == 1:
                    npc_nave3_barra_salud.left = npc_nave3.left + ancho_medio_npc_nave-17
                    npc_nave3_barra_salud.top = npc_nave3.top + alto_medio_npc_nave/3

                if npc_nave3_escudo_activo == True:                             #Movimiento npc_nave3_escudo_barra_salud
                    npc_nave3_escudo_barra_salud.left = npc_nave3.left + ancho_medio_npc_nave-6
                    npc_nave3_escudo_barra_salud.top = npc_nave3.top + alto_medio_npc_nave/3+6
                         
        # ------------------------------------------------------------------------
            if naves_destruidas == 3:                                           #Respawn_nivel3
                nivel = 3
                    
            if nivel == 3:
                npc_boss_aparecer = True
                npc_boss_escudo_activo = True
                    
                if npc_boss_aparecer == True and npc_boss.top < 20:
                    npc_boss.top += velocidad_respawn
                    npc_boss_respawn = True
                         

                if npc_boss_respawn == True and npc_boss_aparecer == True:      #Movimiento npc_boss
                    npc_boss.left += velocidad_npc_bossX
                    npc_boss.top += velocidad_npc_bossY
                    if npc_boss.left < 0 or npc_boss.right > ancho:
                        velocidad_npc_bossX = -velocidad_npc_bossX
                    if npc_boss.top < 20 or npc_boss.top > 250:
                        velocidad_npc_bossY = -velocidad_npc_bossY

                if npc_boss_escudo_activo == True and hp_npc_boss_escudo > 0:
                    npc_boss_escudo.left = npc_boss.left
                    npc_boss_escudo.top = npc_boss.top + alto_medio_npc_boss + 45


                if  hp_npc_boss > 0 and not disparoActivo_npc_boss:             #Disparo npc_boss
                    disparoActivo_npc_boss = True
                    npc_boss_disparo.left = npc_boss.left + ancho_medio_npc_boss - ancho_medio_npc_boss/2  
                    npc_boss_disparo.top = npc_boss.top + alto_medio_npc_boss

                if disparoActivo_npc_boss == True:             
                    npc_boss_disparo.top += disparo_npc_nave         
                    if npc_boss_disparo.top >= 600:
                        disparoActivo_npc_boss = False

                if  hp_npc_boss > 0 and not disparo2Activo_npc_boss:            #Disparo2 npc_boss
                    disparo2Activo_npc_boss = True
                    npc_boss_disparo2.left = npc_boss.left + ancho_medio_npc_boss + ancho_medio_npc_boss/2  
                    npc_boss_disparo2.top = npc_boss.top + alto_medio_npc_boss

                if disparo2Activo_npc_boss == True:             
                    npc_boss_disparo2.top += disparo_npc_nave         
                    if npc_boss_disparo2.top >= 600:
                        disparo2Activo_npc_boss = False

                if hp_npc_boss == 5:                                            #Movimiento npc_boss_barra_salud
                    npc_boss_barra_salud.left = npc_boss.left + ancho_medio_npc_boss-28
                    npc_boss_barra_salud.top = npc_boss.top + alto_medio_npc_boss/3
                    npc_boss_barra_salud2.left = npc_boss.left + ancho_medio_npc_boss-17
                    npc_boss_barra_salud2.top = npc_boss.top + alto_medio_npc_boss/3
                    npc_boss_barra_salud3.left = npc_boss.left + ancho_medio_npc_boss-6
                    npc_boss_barra_salud3.top = npc_boss.top + alto_medio_npc_boss/3
                    npc_boss_barra_salud4.left = npc_boss.left + ancho_medio_npc_boss+5
                    npc_boss_barra_salud4.top = npc_boss.top + alto_medio_npc_boss/3
                    npc_boss_barra_salud5.left = npc_boss.left + ancho_medio_npc_boss+16
                    npc_boss_barra_salud5.top = npc_boss.top + alto_medio_npc_boss/3

                if hp_npc_boss == 4:
                    npc_boss_barra_salud.left = npc_boss.left + ancho_medio_npc_boss-28
                    npc_boss_barra_salud.top = npc_boss.top + alto_medio_npc_boss/3
                    npc_boss_barra_salud2.left = npc_boss.left + ancho_medio_npc_boss-17
                    npc_boss_barra_salud2.top = npc_boss.top + alto_medio_npc_boss/3
                    npc_boss_barra_salud3.left = npc_boss.left + ancho_medio_npc_boss-6
                    npc_boss_barra_salud3.top = npc_boss.top + alto_medio_npc_boss/3
                    npc_boss_barra_salud4.left = npc_boss.left + ancho_medio_npc_boss+5
                    npc_boss_barra_salud4.top = npc_boss.top + alto_medio_npc_boss/3
                         
                if hp_npc_boss == 3:
                    npc_boss_barra_salud.left = npc_boss.left + ancho_medio_npc_boss-28
                    npc_boss_barra_salud.top = npc_boss.top + alto_medio_npc_boss/3
                    npc_boss_barra_salud2.left = npc_boss.left + ancho_medio_npc_boss-17
                    npc_boss_barra_salud2.top = npc_boss.top + alto_medio_npc_boss/3
                    npc_boss_barra_salud3.left = npc_boss.left + ancho_medio_npc_boss-6
                    npc_boss_barra_salud3.top = npc_boss.top + alto_medio_npc_boss/3
                         
                if hp_npc_boss == 2:
                    npc_boss_barra_salud.left = npc_boss.left + ancho_medio_npc_boss-28
                    npc_boss_barra_salud.top = npc_boss.top + alto_medio_npc_boss/3
                    npc_boss_barra_salud2.left = npc_boss.left + ancho_medio_npc_boss-17
                    npc_boss_barra_salud2.top = npc_boss.top + alto_medio_npc_boss/3

                if hp_npc_boss == 1:
                    npc_boss_barra_salud.left = npc_boss.left + ancho_medio_npc_boss-28
                    npc_boss_barra_salud.top = npc_boss.top + alto_medio_npc_boss/3

                if hp_npc_boss_escudo == 3:                                     #Movimiento npc_boss_escudo_barra_salud
                    npc_boss_escudo_barra_salud.left = npc_boss.left + ancho_medio_npc_boss-17
                    npc_boss_escudo_barra_salud.top = npc_boss.top + alto_medio_npc_boss/3+7
                    npc_boss_escudo_barra_salud2.left = npc_boss.left + ancho_medio_npc_boss-6
                    npc_boss_escudo_barra_salud2.top = npc_boss.top + alto_medio_npc_boss/3+7
                    npc_boss_escudo_barra_salud3.left = npc_boss.left + ancho_medio_npc_boss+5
                    npc_boss_escudo_barra_salud3.top = npc_boss.top + alto_medio_npc_boss/3+7

                if hp_npc_boss_escudo == 2:
                    npc_boss_escudo_barra_salud.left = npc_boss.left + ancho_medio_npc_boss-17
                    npc_boss_escudo_barra_salud.top = npc_boss.top + alto_medio_npc_boss/3+7
                    npc_boss_escudo_barra_salud2.left = npc_boss.left + ancho_medio_npc_boss-6
                    npc_boss_escudo_barra_salud2.top = npc_boss.top + alto_medio_npc_boss/3+7

                if hp_npc_boss_escudo == 1:
                    npc_boss_escudo_barra_salud.left = npc_boss.left + ancho_medio_npc_boss-17
                    npc_boss_escudo_barra_salud.top = npc_boss.top + alto_medio_npc_boss/3+7

        # ------------------------------------------------------------------------ Puntos extra al ganar
            if naves_destruidas == 4 and puntos_otorgados == False:
                if pj_nave_hp == 3:
                    puntuacion += 20
                if pj_nave_hp == 2:
                    puntuacion += 10
                puntos_otorgados = True
                puntuacion_obtenida = puntuacion ##############
                estado_app = 5 ##############
                SalirJuego = True ###############
                   

        # ------------------------------------------------------------------------ GAME OVER ###############
            if pj_nave_hp == 0: ###########
                puntuacion_obtenida = puntuacion ##############
                estado_app = 6 ############
                SalirJuego = True ###########
                             
        # ------------------------------------------------------------------------ Mostrar en pantalla
            PANTALLA.blit(fondo,(fondox,fondoy))
            PANTALLA.blit(Roca,npc_roca)
            PANTALLA.blit(Roca2,npc_roca2)
            PANTALLA.blit(Nave,pj_nave)
            if disparoActivo:
                PANTALLA.blit(Disparo, pj_disparo)
            PANTALLA.blit(NaveNPC, npc_nave)
            if escudoActivo == True:
                PANTALLA.blit(Escudo, pj_escudo)
               
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
            if item_escudo_activo == True:
                PANTALLA.blit(ItemEscudo, item_escudo)

            tiempo_seg = pygame.time.get_ticks()/1000                           #Tiempo transcurrido
            tiempo_seg = str(tiempo_seg)                                        #
            contador_tiempo = fuente1.render(tiempo_seg,0,BLANCO)               #
            #PANTALLA.blit(contador_tiempo,(760,575))                            #

            puntuacion_str = str(puntuacion)                                    #Puntuacion
            contador_puntuacion = fuente1.render(puntuacion_str,0,BLANCO)       #
            PANTALLA.blit(contador_puntuacion,(760,15))                         #
            texto_puntuacion = fuente1.render("Puntuacion:",0,BLANCO)           #
            PANTALLA.blit(texto_puntuacion,(650,15))                            #

            naves_destruidas_str = str(naves_destruidas)                        #Naves destruidas
            contador_naves_destruidas = fuente1.render(naves_destruidas_str,0,BLANCO)#
            PANTALLA.blit(contador_naves_destruidas,(165,15))                   #
            texto_naves_destruida2 = fuente1.render("Naves destruidas:",0,BLANCO)#
            PANTALLA.blit(texto_naves_destruida2,(15,15))                       #

            texto_vidas_restantes = fuente1.render("Vidas:",0,BLANCO)           #Vidas restantes
            PANTALLA.blit(texto_vidas_restantes,(15,575))                       #

            #salud_restante = str(pj_nave_hp)                                    #PRUEBA HP PJ NAVE
            #estado_salud_restante = fuente1.render(salud_restante,0,BLANCO)     #     
            #PANTALLA.blit(estado_salud_restante,(250,575))                      #
               
                # ------------------------------------------------------------------------ Barras HP
            if pj_nave_hp == 3:                                                 #
                PANTALLA.blit(Vida, pj_vida)                                    #
                PANTALLA.blit(Vida2, pj_vida2)                                  #
            if pj_nave_hp == 2:                                                 #
                PANTALLA.blit(Vida, pj_vida)                                    #

            if hp_npc_nave == 2:                                                #Salud npc_nave
                PANTALLA.blit(NaveNPCVida, npc_nave_barra_salud)                #
                PANTALLA.blit(NaveNPCVida2, npc_nave_barra_salud2)              #
            if hp_npc_nave == 1:                                                #
                PANTALLA.blit(NaveNPCVida, npc_nave_barra_salud)                #

            if hp_npc_nave2 == 2:                                               #Salud npc_nave2
                PANTALLA.blit(NaveNPC2Vida, npc_nave2_barra_salud)              #
                PANTALLA.blit(NaveNPC2Vida2, npc_nave2_barra_salud2)            #
            if hp_npc_nave2 == 1:                                               #
                PANTALLA.blit(NaveNPC2Vida, npc_nave2_barra_salud)              #

            if hp_npc_nave3 == 3:                                               #Salud npc_nave3
                PANTALLA.blit(NaveNPC3Vida, npc_nave3_barra_salud)              #
                PANTALLA.blit(NaveNPC3Vida2, npc_nave3_barra_salud2)            #
                PANTALLA.blit(NaveNPC3Vida3, npc_nave3_barra_salud3)            #
            if hp_npc_nave3 == 2:                                               #
                PANTALLA.blit(NaveNPC3Vida, npc_nave3_barra_salud)              #
                PANTALLA.blit(NaveNPC3Vida2, npc_nave3_barra_salud2)            #
            if hp_npc_nave3 == 1:                                               #
                PANTALLA.blit(NaveNPC3Vida, npc_nave3_barra_salud)              #
            if hp_npc_nave2 > 0:                                                #Salud npc_nave3_escudo
                PANTALLA.blit(EscudoNPCNave3Vida, npc_nave3_escudo_barra_salud) #

            if hp_npc_boss == 5:                                                #Salud npc_boss
                PANTALLA.blit(BossNPCVida5, npc_boss_barra_salud5)              #
                PANTALLA.blit(BossNPCVida4, npc_boss_barra_salud4)              #
                PANTALLA.blit(BossNPCVida3, npc_boss_barra_salud3)              #
                PANTALLA.blit(BossNPCVida2, npc_boss_barra_salud2)              #
                PANTALLA.blit(BossNPCVida, npc_boss_barra_salud)                #
            if hp_npc_boss == 4:                                                #
                PANTALLA.blit(BossNPCVida4, npc_boss_barra_salud4)              #
                PANTALLA.blit(BossNPCVida3, npc_boss_barra_salud3)              #
                PANTALLA.blit(BossNPCVida2, npc_boss_barra_salud2)              #
                PANTALLA.blit(BossNPCVida, npc_boss_barra_salud)                #
            if hp_npc_boss == 3:                                                #
                PANTALLA.blit(BossNPCVida3, npc_boss_barra_salud3)              #
                PANTALLA.blit(BossNPCVida2, npc_boss_barra_salud2)              #
                PANTALLA.blit(BossNPCVida, npc_boss_barra_salud)                #
            if hp_npc_boss == 2:                                                #
                PANTALLA.blit(BossNPCVida2, npc_boss_barra_salud2)              #
                PANTALLA.blit(BossNPCVida, npc_boss_barra_salud)                #
            if hp_npc_boss == 1:                                                #
                PANTALLA.blit(BossNPCVida, npc_boss_barra_salud)                #
            if hp_npc_boss_escudo == 3:                                         #Salud npc_boss_escudo
                PANTALLA.blit(EscudoNPCBossVida3, npc_boss_escudo_barra_salud3) #
                PANTALLA.blit(EscudoNPCBossVida2, npc_boss_escudo_barra_salud2) #
                PANTALLA.blit(EscudoNPCBossVida, npc_boss_escudo_barra_salud)   #
            if hp_npc_boss_escudo == 2:                                         #
                PANTALLA.blit(EscudoNPCBossVida2, npc_boss_escudo_barra_salud2) #
                PANTALLA.blit(EscudoNPCBossVida, npc_boss_escudo_barra_salud)   #
            if hp_npc_boss_escudo == 1:                                         #
                PANTALLA.blit(EscudoNPCBossVida, npc_boss_escudo_barra_salud)   #
                    
        # ------------------------------------------------------------------------     
            pygame.display.update()                                             #Actualizar juego       
        reloj.tick(40)

    # ------------------------------------------------------------------------
    while estado_app == 3:                                                      # 3 = Gameplay
        gameplay_img = pygame.image.load("fondos/Pablito GO Gameplay.jpg")
        gameplay_imgx=0
        gameplay_imgy=0
        
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                if cursor.colliderect(boton_menu_inicial.rect):
                    estado_app=1
                
        PANTALLA.blit(gameplay_img,(gameplay_imgx,gameplay_imgy))
        boton_menu_inicial.update(PANTALLA,cursor)
        pygame.display.update()
        cursor.update()
        musica_inicio_gameplay = False
        
    # ------------------------------------------------------------------------
    #while estado_app == 4:                                                      # 4 = Puntuaciones
    #    puntuaciones_img = pygame.image.load("fondos/Pablito GO Puntuajes.jpg")
    #    puntuaciones_imgx=0
    #    puntuaciones_imgy=0
    #    
    #    for event in pygame.event.get():
    #
    #        if event.type == pygame.MOUSEBUTTONDOWN:
    #            if cursor.colliderect(boton_menu_inicial.rect):
    #                estado_app=1
    #            
    #    PANTALLA.blit(puntuaciones_img,(puntuaciones_imgx,puntuaciones_imgy))
    #    boton_menu_inicial.update(PANTALLA,cursor)
    #    pygame.display.update()
    #    cursor.update()
    #    musica_inicio_gameplay = False
    
    # ------------------------------------------------------------------------
    while estado_app == 5:                                                      # 5 = Ganaste
        pygame.mixer.music.load("musica/(08) Nonhii  Feeling.mp3")
        pygame.mixer.music.play(-1,0.0)
        ganaste = pygame.image.load("fondos/Pablito GO You Win.jpg")
        ganastex=0
        ganastey=0
        salir_ganaste = False
            
        while salir_ganaste == False:
            for event in pygame.event.get():
                      
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if cursor.colliderect(boton_menu_inicial.rect):
                        estado_app=1
                        salir_ganaste = True

            PANTALLA.blit(ganaste,(ganastex,ganastey))
            boton_menu_inicial.update(PANTALLA,cursor)
            puntuacion_obtenida_str = str(puntuacion_obtenida)                      #Puntuacion
            textopuntuaciontotal = fuente1.render(puntuacion_obtenida_str,0,BLANCO) #
            PANTALLA.blit(textopuntuaciontotal,(405,339))                           #
            #texto_puntuacion_total = fuente1.render("PUNTUACIÓN TOTAL:",0,BLANCO)   #
            #PANTALLA.blit(texto_puntuacion_total,(50,15))                           #
            pygame.display.update()
            cursor.update()
        musica_inicio_gameplay = True
        
    # ------------------------------------------------------------------------            
    while estado_app == 6:                                                      # 6 = Perdiste   
        pygame.mixer.music.load("musica/(04) Conan's Dream.mp3")
        pygame.mixer.music.play(-1,0.0)
        perdiste = pygame.image.load("fondos/Pablito GO Game Over.jpg")
        perdistex=0
        perdistey=0
        salir_perdiste = False
            
        while salir_perdiste == False:
            for event in pygame.event.get():
                      
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if cursor.colliderect(boton_menu_inicial.rect):
                        salir_perdiste = True
                        estado_app=1
                    
            PANTALLA.blit(perdiste,(perdistex,perdistey))
            boton_menu_inicial.update(PANTALLA,cursor)
            puntuacion_obtenida_str = str(puntuacion_obtenida)                      #Puntuacion
            textopuntuaciontotal = fuente1.render(puntuacion_obtenida_str,0,BLANCO) #
            PANTALLA.blit(textopuntuaciontotal,(405,339))                           #
            #texto_puntuacion_total = fuente1.render("PUNTUACIÓN TOTAL:",0,BLANCO)   #
            #PANTALLA.blit(texto_puntuacion_total,(50,15))                           #
            pygame.display.update()
            cursor.update()
        musica_inicio_gameplay = True
        
    # ------------------------------------------------------------------------      
pygame.quit()                                                            
quit()
