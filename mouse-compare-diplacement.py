import cv2
import numpy as np

# Variables globales
start_point = None
end_point = None
drawing = False
manual_lines = []
show_text = True

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
def linear_interpolation(p1, p2, num_points=1000):
    x_vals = np.linspace(p1[0], p2[0], num_points)
    y_vals = np.linspace(p1[1], p2[1], num_points)
    return list(zip(x_vals.astype(int), y_vals.astype(int)))

# Generación de múltiples curvas de Bézier con curvatura suave y separación
def bezier_curves(p1, p2, num_curves=100, num_points=100, separation=10):
    curves = []
    for i in range(num_curves):
        # Desplazar aleatoriamente los puntos de control para que las curvas estén separadas
        control1 = (p1[0] + np.random.randint(-separation, separation), p1[1] + np.random.randint(-separation, separation))
        control2 = (p2[0] + np.random.randint(-separation, separation), p2[1] + np.random.randint(-separation, separation))

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
    cv2.namedWindow("Dibujar desplazamiento")
    cv2.setMouseCallback("Dibujar desplazamiento", draw)

    # Crear lienzo blanco
    canvas = np.ones((750, 1200, 3), dtype=np.uint8) * 255

    # Inicializar posiciones aleatorias para inicio y final
    start_point = (np.random.randint(100, 300), np.random.randint(450, 750))
    end_point = (np.random.randint(800, 1200), np.random.randint(0, 325))

    while True:
        temp_canvas = canvas.copy()
        # Agregar la leyenda para salir
        cv2.putText(canvas, "Presiona la letra 'q' para cerrar el programa", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1)

        # Mostrar puntos inicio y final
        if start_point:
            cv2.putText(temp_canvas, "Inicio", (start_point[0] - 30, start_point[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            cv2.circle(temp_canvas, start_point, 10, (0, 255, 0), -1)
        if end_point:
            cv2.putText(temp_canvas, "Final", (end_point[0] - 30, end_point[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            cv2.circle(temp_canvas, end_point, 10, (0, 0, 255), -1)

        # Dibujar líneas manuales
        for line in manual_lines:
            for i in range(1, len(line)):
                cv2.line(temp_canvas, line[i - 1], line[i], (255, 0, 0), 2)

        cv2.imshow("Dibujar desplazamiento", temp_canvas)

        # Salir al presionar 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Dibujar puntos de inicio y final en la imagen final
    if start_point:
        cv2.putText(canvas, "Inicio", (start_point[0] - 30, start_point[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        cv2.circle(canvas, start_point, 10, (0, 255, 0), -1)

    if end_point:
        cv2.putText(canvas, "Final", (end_point[0] - 30, end_point[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        cv2.circle(canvas, end_point, 10, (0, 0, 255), -1)

    # Dibujar interpolación lineal y múltiples curvas de Bézier
    if start_point and end_point:
        # Interpolación lineal
        linear_points = linear_interpolation(start_point, end_point)
        for point in linear_points:
            cv2.circle(canvas, point, 1, (0, 0, 255), 1)

        # Generar y dibujar múltiples curvas de Bézier
        bezier_curves_list = bezier_curves(start_point, end_point, num_curves=3, separation=40)
        for curve in bezier_curves_list:
            for i in range(1, len(curve)):
                cv2.line(canvas, curve[i - 1], curve[i], (0, 0, 0), 1)

    # Dibujar las líneas manuales en color verde
    for line in manual_lines:
        for i in range(1, len(line)):
            cv2.line(canvas, line[i - 1], line[i], (0, 255, 0), 1)  # Verde

    # Agregar la leyenda en la parte superior izquierda
    cv2.putText(canvas, "Interpolacion lineal", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    cv2.putText(canvas, "Curvas de Bezier", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(canvas, "Mouse controlado por un humano", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # Guardar la imagen final con los puntos de inicio, final, y las líneas manuales
    cv2.imwrite("mouse-displacement-compare.jpg", canvas)
    cv2.destroyAllWindows()
