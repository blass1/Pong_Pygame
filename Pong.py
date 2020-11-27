#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
# Módulos
import sys, pygame
from pygame.locals import *
 
# Constantes
WIDTH = 640
HEIGHT = 480
 
# Clases
# ---------------------------------------------------------------------
# Crea la clase Bola que hereda los métodos de la clase pygame.sprite.Sprite contiene métodos necesarios para el manejo de Sprite
class Bola(pygame.sprite.Sprite):
    # Constructor
    def __init__(self):
        # Invoca al método init de la clase heredada
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen y True porque la pelota si tiene zonas transparentes
        self.image = load_image("img/ball.png", True)
        # Obtiene un rectangulo con las dimensiones y posición de la imagen (en este caso self.image) y se lo asignamos a self.rect
        self.rect = self.image.get_rect()
        #  usamos las propiedades de rect y con centerx y centery definimos el centro de la pelota en el centro de la pantalla
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        # Define la velocidad que queremos para la pelota, Una lista con la velocidad en el eje X y la velocidad en el eje Y
        self.speed = [0.5, -0.5]

    def actualizar(self, time, pala_jug, pala_cpu, puntos):
        
        # Espacio es igual a la velocidad por el tiempo (e = v*t)
        # El centro de nuestro rectangulo en x es el valor que tenía (self.rect.centerx) más (+=) la velocidad a la
        # que se mueve en el eje x (self.speed[0]) por (*) el tiempo transcurrido (time)
        self.rect.centerx += self.speed[0] * time
        self.rect.centery += self.speed[1] * time
 		
 		# El controlador de puntos verifica cuando la parte izquierda de la pelota toca el el borde izquierdo de la ventana
 		# y los puntos del cpu aumentan en 1 sumando a los puntos[1], el mismo pasa con los puntos del jugador [0]
        if self.rect.left <= 0:
            puntos[1] += 1
        if self.rect.right >= WIDTH:
            puntos[0] += 1
 		
 		# El rebote de la pelota en los bordes
 		# Si el borde izq es 0 o el borde derecho es el ancho de pantalla, cambia su velocidad inversamente
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
        # Lo mismo con el eje Y
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed[1] = -self.speed[1]
            self.rect.centery += self.speed[1] * time
 		
 		# Rebote contra las palas, comprueba si el rectángulo del Sprite del obj pelota está en contacto con 
 		# el rectángulo de obj2 pala del jugador	
        if pygame.sprite.collide_rect(self, pala_jug):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
 		# Lo mismo con la pala del cpu
        if pygame.sprite.collide_rect(self, pala_cpu):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
 
        return puntos


# A la clase pala le pasamos el parámetro X para usarlo en self.rect.centerx, una pala para el jugador y otra para el cpu 
# con la disncia X definimos a que distancia del eje X0 queremos colocar el Sprite
class Pala(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("img/pala.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = HEIGHT / 2
        self.speed = 0.5

    def mover(self, time, keys):
	    # Comprueban que la pala no se sale de la ventana
	    if self.rect.top >= 0:
	        # comprueba si la constante K_UP de keys es 1, lo que querría decir que tenemos presionada la tecla de la flecha hacia arriba del teclado
	        if keys[K_UP]:
	            # en caso de tener la tecla presionada disminuye el valor de centery haciendo que la pala se mueva hacia arriba
	            self.rect.centery -= self.speed * time
	    
	    # Comprueban que la pala no se sale de la ventana
	    if self.rect.bottom <= HEIGHT:
	        # hacen lo mismo, pero para abajo y aumentando el valor de centery
	        if keys[K_DOWN]:
	            self.rect.centery += self.speed * time

	# recibe como siempre self y time y aparte recibe ball que es la bola, es necesario pues el método necesita conocer donde está la bola
    def mover_ia(self, time, ball):
        if ball.speed[0] >= 0 and ball.rect.centerx >= WIDTH/2:
            if self.rect.centery < ball.rect.centery:
                self.rect.centery += self.speed * time
            if self.rect.centery > ball.rect.centery:
                self.rect.centery -= self.speed * time
# ---------------------------------------------------------------------
 
# Funciones
# ---------------------------------------------------------------------
# Funcion para cargar imagenes, recibe la nombre/ruta(filename) y si es transparente
def load_image(filename, transparent=False):
        # Intenta cargar la imagen, sino sale del sistema
        try: image = pygame.image.load(filename)
        except pygame.error:
                raise SystemExit
        # Convierte la imagen al tipo interno de Pygame que hace que sea mucho más eficiente
        image = image.convert()
        # Condicional que controla si el parámetro transparent es verdadero
        if transparent:
                # Obtiene el color del pixel (0, 0) de la imagen (esquina superior izquierda)
                color = image.get_at((0,0))
                # lo define como color transparente de la imagen. Es decir que si quieres una 
	                # imagen con transparencia, el color que actúa como transparente se toma del 
	                # pixel superior izquierdo, así que asegúrate que este color no está en la imagen.
                image.set_colorkey(color, RLEACCEL)
        return image

# Recibe el texto que aparece, la posicion del texto y una tupla con el color(Opcional, sino es blanco) 
def texto(texto, posx, posy, color=(255, 255, 255)):
    # Asignamos la tipografia
    fuente = pygame.font.Font("img/DroidSans.ttf", 25)
    # Convierte el texto a un Sprite, recibe Fuente, Texto, Antialias (verdadero o falso , con o sin antialias) y el color
    salida = pygame.font.Font.render(fuente, texto, 1, color)
    # Obtenemos el rect como si de un Sprite más se tratare y lo almacenamos en salida_rect
    salida_rect = salida.get_rect()
    # Modifican el centro del Sprite en función de los valores posx y posy
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect
 
# ---------------------------------------------------------------------
 
def main():
	# Creamos la ventana
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	# Le asignamos el titulo
	pygame.display.set_caption("Blasito Pong")

	# Cargamos la imagen del fondo
	background_image = load_image('img/fondo.png')
	# Creamos el objeto bola
	bola = Bola()
	# Creamos la pala, x = 30, esto quiere decir que centerx estará a 30 px del borde derecho de la ventana
	pala_jug = Pala(30)
	# La pala del cpu, con parametros WIDTH – 30, es decir a 30 píxeles del borde derecho
	pala_cpu = Pala(WIDTH - 30)

	# Creamos un reloj, esto es importante para el movimiento, pues sabemos cuanto tiempo a pasado desde 
	# la ultima actualización de la pelota y con ello poder situarla en el espacio.
	clock = pygame.time.Clock()

	puntos = [0, 0]

	# Bucle infinito que mantiene el juego ejecutandose
	while True:
		# El 60 que se le pasa como parámetro es el framerate, con él nos aseguramos de que el juego 
		# no va a más de la velocidad estipulada. Con ello conseguimos que el juego corra igual en todos lados
		time = clock.tick(60)
		# Que teclas se están pulsando creando la variable keys
		keys = pygame.key.get_pressed()
		
		for eventos in pygame.event.get():
			if eventos.type == QUIT:
				sys.exit(0)
		
		# Actualizar la posición de la bola antes de actualizarla en la ventana, es decir antes de los screen.blit
		# Y almacenamos el valor retornado por la funcion en la lista puntos
		puntos = bola.actualizar(time, pala_jug, pala_cpu, puntos)
		# debemos llamar al método mover en el bucle justo después de actualizar la bola
		pala_jug.mover(time, keys)
		# Actualizamos la cpu en cada ciclo
		pala_cpu.mover_ia(time, bola)
		
		# Crea dos Sprites con sus rects. Para mostrar
		p_jug, p_jug_rect = texto(str(puntos[0]), WIDTH/4, 40)
		p_cpu, p_cpu_rect = texto(str(puntos[1]), WIDTH-WIDTH/4, 40)

		#Todo lo que se actualizo se muetra en la ventana con BLIT
		screen.blit(background_image, (0, 0))
		# Agregamos la bola a la ventana
		screen.blit(bola.image, bola.rect)
		# Agregamos las palas con sus sprites a la pantalla del jugador y del cpu
		screen.blit(pala_jug.image, pala_jug.rect)
		screen.blit(pala_cpu.image, pala_cpu.rect)

		screen.blit(p_jug, p_jug_rect)
		screen.blit(p_cpu, p_cpu_rect)
		
		# Actualiza toda la ventana para que se muestren los cambios que han sucedido
		pygame.display.flip()
	return 0

if __name__ == '__main__':
	pygame.init()
	main()