import cv2
import numpy as np

# Variables globales
start_point = None
end_point = None
drawing = False
manual_lines = []

# Callback para eventos del mouse
def draw(event, x, y, flags, param):
    global start_point, end_point, drawing, manual_lines

    if event == cv2.EVENT_LBUTTONDOWN:
        # Iniciar dibujo al hacer clic en "Inicio"
        if start_point and end_point:
            if abs(x - start_point[0]) < 10 and abs(y - start_point[1]) < 10:
                drawing = True
                manual_lines.append([start_point])

    elif event == cv2.EVENT_MOUSEMOVE:
        # Continuar dibujando mientras se arrastra el mouse
        if drawing:
            manual_lines[-1].append((x, y))

    elif event == cv2.EVENT_LBUTTONUP:
        # Finalizar dibujo al soltar en "Final"
        if drawing:
            if abs(x - end_point[0]) < 10 and abs(y - end_point[1]) < 10:
                manual_lines[-1].append(end_point)
            drawing = False

# Interpolación lineal
def linear_interpolation(p1, p2, num_points=100):
    x_vals = np.linspace(p1[0], p2[0], num_points)
    y_vals = np.linspace(p1[1], p2[1], num_points)
    return list(zip(x_vals.astype(int), y_vals.astype(int)))

# Generación de curvas de Bézier
def bezier_curve(p1, p2, num_curves=5, num_points=100):
    curves = []
    for _ in range(num_curves):
        control1 = (p1[0] + np.random.randint(-50, 50), p1[1] + np.random.randint(-50, 50))
        control2 = (p2[0] + np.random.randint(-50, 50), p2[1] + np.random.randint(-50, 50))

        t = np.linspace(0, 1, num_points)
        curve = []
        for t_val in t:
            x = (1 - t_val)**3 * p1[0] + 3 * (1 - t_val)**2 * t_val * control1[0] + 3 * (1 - t_val) * t_val**2 * control2[0] + t_val**3 * p2[0]
            y = (1 - t_val)**3 * p1[1] + 3 * (1 - t_val)**2 * t_val * control1[1] + 3 * (1 - t_val) * t_val**2 * control2[1] + t_val**3 * p2[1]
            curve.append((int(x), int(y)))
        curves.append(curve)
    return curves

# Main
if __name__ == "__main__":
    # Crear ventana y configurar eventos del mouse
    cv2.namedWindow("Draw")
    cv2.setMouseCallback("Draw", draw)

    # Crear lienzo blanco
    canvas = np.ones((500, 800, 3), dtype=np.uint8) * 255

    # Inicializar posiciones aleatorias para inicio y final
    start_point = (np.random.randint(100, 700), np.random.randint(100, 400))
    end_point = (np.random.randint(100, 700), np.random.randint(100, 400))

    while True:
        temp_canvas = canvas.copy()

        # Mostrar puntos inicio y final
        if start_point:
            cv2.putText(temp_canvas, "Inicio", (start_point[0] - 30, start_point[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            cv2.circle(temp_canvas, start_point, 10, (0, 0, 255), -1)
        if end_point:
            cv2.putText(temp_canvas, "Final", (end_point[0] - 30, end_point[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            cv2.circle(temp_canvas, end_point, 10, (0, 255, 0), -1)

        # Dibujar líneas manuales
        for line in manual_lines:
            for i in range(1, len(line)):
                cv2.line(temp_canvas, line[i - 1], line[i], (255, 0, 0), 2)

        cv2.imshow("Draw", temp_canvas)

        # Salir al presionar 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Dibujar interpolación lineal y curvas de Bézier
    if start_point and end_point:
        # Interpolación lineal
        linear_points = linear_interpolation(start_point, end_point)
        for point in linear_points:
            cv2.circle(canvas, point, 1, (0, 255, 255), -1)

        # Curvas de Bézier
        bezier_curves = bezier_curve(start_point, end_point)
        for curve in bezier_curves:
            for i in range(1, len(curve)):
                cv2.line(canvas, curve[i - 1], curve[i], (0, 255, 0), 1)

    # Guardar la imagen final
    cv2.imwrite("output.png", canvas)
    cv2.destroyAllWindows()