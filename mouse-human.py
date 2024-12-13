import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
width, height = 1200, 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dibujar desplazamiento")

# Colores
green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)

# Función para generar posiciones aleatorias dentro de la pantalla
def random_position():
    return (random.randint(50, width - 50), random.randint(50, height - 50))

# Función para generar un color aleatorio, excluyendo el rojo y colores derivados
def random_color_excluding_red():
    while True:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        # Excluir colores con el componente rojo muy alto (por ejemplo, > 200)
        if color[0] < 150:  # Si el componente rojo es menor a 200, no es un color rojo o derivado
            return color

# Puntos inicial y final aleatorios
start_point = random_position()
end_point = random_position()

# Variables para el seguimiento
drawing = False
trajectory = []
all_trajectories = []  # Almacena todas las trayectorias previas
all_colors = []  # Almacena los colores de las trayectorias

# Fuente de texto
font = pygame.font.Font(None, 36)

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Iniciar el dibujo al hacer clic en el punto A
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(start_point[0] - 10, start_point[1] - 10, 20, 20).collidepoint(event.pos):
                drawing = True
                trajectory = [start_point]

        # Finalizar el dibujo al soltar el botón
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                drawing = False
                # Almacenar la trayectoria y su color
                all_trajectories.append(trajectory[:])  # Guardar una copia de la trayectoria
                all_colors.append(random_color_excluding_red())  # Guardar un color aleatorio (excepto rojo)
                trajectory = []  # Reiniciar para la siguiente línea

        # Registrar la posición del mouse
        if event.type == pygame.MOUSEMOTION and drawing:
            trajectory.append(event.pos)

    # Limpiar la pantalla (fondo blanco) para dibujar una nueva línea
    screen.fill(white)

    # Dibujar puntos inicial y final
    pygame.draw.circle(screen, green, start_point, 10)
    pygame.draw.circle(screen, red, end_point, 10)

    # Dibujar etiquetas
    screen.blit(font.render("Inicio", True, black), (start_point[0] - 30, start_point[1] - 30))
    screen.blit(font.render("Final", True, black), (end_point[0] - 30, end_point[1] - 30))

    # Dibujar todas las trayectorias acumuladas con colores estables
    for i, traj in enumerate(all_trajectories):
        if len(traj) > 1:
            pygame.draw.lines(screen, all_colors[i], False, traj, 2)  # Usar el color correspondiente a cada trayectoria

    # Dibujar la trayectoria actual en curso con un color aleatorio (excepto rojo)
    if len(trajectory) > 1:
        pygame.draw.lines(screen, random_color_excluding_red(), False, trajectory, 2)

    # Actualizar la pantalla
    pygame.display.flip()

    # Guardar la imagen final después de completar una trayectoria
    if not drawing and len(trajectory) == 0 and len(all_trajectories) > 0:
        # Guardar la imagen solo si hay trayectorias acumuladas
        pygame.image.save(screen, "mouse-displacement-human.jpg")
        print("Imagen final guardada como mouse-displacement-human.jpg")

# Salir de Pygame
pygame.quit()
sys.exit()
