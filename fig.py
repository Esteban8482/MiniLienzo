import pygame
import math

# Este archivo contendrá las funciones de dibujo.
# Inicialmente, usarán pygame.draw, pero luego se reemplazarán
# con implementaciones propias (DDA, Bresenham, etc.)

# --- Funciones de Dibujo (Placeholders usando pygame.draw) ---

def draw_line(surface, color, start_pos, end_pos, width=1):
    """Dibuja una línea usando pygame.draw.line."""
    pygame.draw.line(surface, color, start_pos, end_pos, width)

def draw_rectangle(surface, color, rect, width=1):
    """Dibuja un rectángulo usando pygame.draw.rect."""
    # Asegurarse de que el ancho y alto no sean negativos
    # Pygame puede manejarlo, pero es buena práctica normalizar
    normalized_rect = pygame.Rect(rect)
    normalized_rect.normalize()
    pygame.draw.rect(surface, color, normalized_rect, width)

def draw_circle(surface, color, center, radius, width=1):
    """Dibuja un círculo usando pygame.draw.circle."""
    if radius < width: radius = width # Evitar error si el radio es muy pequeño
    pygame.draw.circle(surface, color, center, int(radius), width)

def draw_ellipse(surface, color, rect, width=1):
    """Dibuja una elipse usando pygame.draw.ellipse."""
    normalized_rect = pygame.Rect(rect)
    normalized_rect.normalize()
    # pygame.draw.ellipse necesita ancho > 0
    if normalized_rect.width < 1 or normalized_rect.height < 1:
        return # No dibujar si es demasiado pequeño
    pygame.draw.ellipse(surface, color, normalized_rect, width)

def draw_triangle(surface, color, points, width=1):
    """Dibuja un triángulo usando pygame.draw.polygon."""
    if len(points) == 3:
        pygame.draw.polygon(surface, color, points, width)

def draw_polygon(surface, color, points, width=1):
    """Dibuja un polígono usando pygame.draw.polygon."""
    if len(points) > 2:
        pygame.draw.polygon(surface, color, points, width)

def draw_bezier_curve(surface, color, control_points, width=1, steps=20):
    """Dibuja una curva de Bézier cúbica (aproximada con líneas)."""
    if len(control_points) != 4:
        return # Necesita 4 puntos de control

    points = []
    for i in range(steps + 1):
        t = i / steps
        x = ( (1 - t) ** 3 * control_points[0][0] +
              3 * (1 - t) ** 2 * t * control_points[1][0] +
              3 * (1 - t) * t ** 2 * control_points[2][0] +
              t ** 3 * control_points[3][0] )
        y = ( (1 - t) ** 3 * control_points[0][1] +
              3 * (1 - t) ** 2 * t * control_points[1][1] +
              3 * (1 - t) * t ** 2 * control_points[2][1] +
              t ** 3 * control_points[3][1] )
        points.append((int(x), int(y)))

    if len(points) > 1:
        pygame.draw.lines(surface, color, False, points, width)

# --- Funciones de utilidad (ej. para calcular rect desde puntos) ---
def get_rect_from_points(p1, p2):
    """Calcula un pygame.Rect a partir de dos puntos (esquinas opuestas)."""
    x = min(p1[0], p2[0])
    y = min(p1[1], p2[1])
    width = abs(p1[0] - p2[0])
    height = abs(p1[1] - p2[1])
    return pygame.Rect(x, y, width, height)

def get_circle_params_from_points(p1, p2):
    """Calcula centro y radio a partir de dos puntos (centro y borde, o diámetro)."""
    # Asumiremos p1=centro, p2=punto en borde por simplicidad ahora
    center = p1
    radius = math.dist(p1, p2)
    return center, radius
