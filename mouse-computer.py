import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
width, height = 1200, 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dibujar desplazamiento con interpolación lineal y curva de bezier")

# Colores
green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)

# Función para generar posiciones aleatorias dentro de la pantalla
def random_position():
    return (random.randint(50, width - 50), random.randint(50, height - 50))

# Métodos para generar trayectorias
def interpolate_points(start, end, steps=100):
    """Interpolación lineal."""
    points = []
    for t in range(steps + 1):
        x = start[0] + (end[0] - start[0]) * (t / steps)
        y = start[1] + (end[1] - start[1]) * (t / steps)
        points.append((int(x), int(y)))
    return points


def bezier_curve(start, end, steps=100):
    """Curva de Bézier cuadrática que se asemeja a un movimiento humano."""
    # Calculamos el punto de control con un pequeño ajuste aleatorio
    # El control estará cerca de la línea recta, pero ligeramente desplazado.
    control_x = (start[0] + end[0]) // 2 + random.randint(-50, 50)  # Desplazamiento aleatorio en X
    control_y = (start[1] + end[1]) // 2 + random.randint(-50, 50)  # Desplazamiento aleatorio en Y
    control = (control_x, control_y)

    points = []
    for t in range(steps + 1):
        t /= steps
        x = (1 - t) ** 2 * start[0] + 2 * (1 - t) * t * control[0] + t ** 2 * end[0]
        y = (1 - t) ** 2 * start[1] + 2 * (1 - t) * t * control[1] + t ** 2 * end[1]
        points.append((int(x), int(y)))
    return points

# Métodos de trayectorias
trajectory_methods = [
    ("Interpolación lineal", interpolate_points),
    ("Curva de Bézier", lambda start, end: bezier_curve(start, end)),
    ("Curva de Bézier", lambda start, end: bezier_curve(start, end)),
    ("Curva de Bézier", lambda start, end: bezier_curve(start, end)),
    ("Curva de Bézier", lambda start, end: bezier_curve(start, end)),
    ("Curva de Bézier", lambda start, end: bezier_curve(start, end)),
    ("Curva de Bézier", lambda start, end: bezier_curve(start, end)),
    ("Curva de Bézier", lambda start, end: bezier_curve(start, end)),
    ("Curva de Bézier", lambda start, end: bezier_curve(start, end)),
]

# Puntos inicial y final aleatorios
start_point = random_position()
end_point = random_position()

# Generar trayectorias con diferentes métodos
trajectories = [(name, func(start_point, end_point)) for name, func in trajectory_methods]

# Fuente de texto
font = pygame.font.Font(None, 36)

# Bucle principal (solo para mostrar el resultado)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Limpiar la pantalla (fondo blanco)
    screen.fill(white)

    # Dibujar puntos inicial y final
    pygame.draw.circle(screen, green, start_point, 10)
    pygame.draw.circle(screen, red, end_point, 10)

    # Dibujar etiquetas
    screen.blit(font.render("Inicio", True, black), (start_point[0] - 30, start_point[1] - 30))
    screen.blit(font.render("Final", True, black), (end_point[0] - 30, end_point[1] - 30))

    # Dibujar trayectorias
    for i, (name, trajectory) in enumerate(trajectories):
        if name == "Interpolación lineal":
            color = red  # La interpolación lineal será de color rojo
        else:
            color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))  # Colores aleatorios para las demás trayectorias
        
        if len(trajectory) > 1:
            pygame.draw.lines(screen, color, False, trajectory, 2)
        legend_text = font.render(name, True, color)
        screen.blit(legend_text, (10, 30 * i))

    # Actualizar la pantalla
    pygame.display.flip()

    # Guardar la imagen y salir automáticamente
    pygame.image.save(screen, "mouse-displacement-computer.jpg")
    print("Imagen final guardada como mouse-displacement-computer.jpg")
    running = False

# Salir de Pygame
pygame.quit()
sys.exit()
