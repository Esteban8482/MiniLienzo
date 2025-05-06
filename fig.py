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

# --- Colores (por si se necesitan aquí, aunque vienen de main) ---
BLACK = (0, 0, 0)

# --- Clase Base para Figuras ---
class Shape:
    def __init__(self, color, width=1):
        self.color = color
        self.width = width

    def draw(self, surface):
        """Método abstracto que debe ser implementado por las subclases."""
        raise NotImplementedError("Cada figura debe implementar su propio método draw.")

# --- Clases Concretas para Cada Figura ---

class Line(Shape):
    def __init__(self, start_pos, end_pos, color, width=1):
        super().__init__(color, width)
        self.start_pos = start_pos
        self.end_pos = end_pos

    def draw(self, surface):
        """Dibuja la línea usando pygame.draw.line."""
        pygame.draw.line(surface, self.color, self.start_pos, self.end_pos, self.width)

class Rectangle(Shape):
    def __init__(self, rect, color, width=1):
        super().__init__(color, width)
        # Normalizar el rect para asegurar ancho/alto positivos
        self.rect = pygame.Rect(rect)
        self.rect.normalize()

    def draw(self, surface):
        """Dibuja el rectángulo usando pygame.draw.rect."""
        pygame.draw.rect(surface, self.color, self.rect, self.width)

    @staticmethod
    def from_points(p1, p2, color, width=1):
        """Constructor alternativo desde dos puntos."""
        x = min(p1[0], p2[0])
        y = min(p1[1], p2[1])
        w = abs(p1[0] - p2[0])
        h = abs(p1[1] - p2[1])
        return Rectangle(pygame.Rect(x, y, w, h), color, width)

class Circle(Shape):
    def __init__(self, center, radius, color, width=1):
        super().__init__(color, width)
        self.center = center
        # Asegurar radio mínimo si hay grosor
        self.radius = max(int(radius), width)

    def draw(self, surface):
        """Dibuja el círculo usando pygame.draw.circle."""
        pygame.draw.circle(surface, self.color, self.center, self.radius, self.width)

    @staticmethod
    def from_points(p1, p2, color, width=1):
        """Constructor alternativo desde centro y punto en borde."""
        center = p1
        radius = math.dist(p1, p2)
        return Circle(center, radius, color, width)

class Ellipse(Shape):
    def __init__(self, rect, color, width=1):
        super().__init__(color, width)
        self.rect = pygame.Rect(rect)
        self.rect.normalize()

    def draw(self, surface):
        """Dibuja la elipse usando pygame.draw.ellipse."""
        # pygame.draw.ellipse necesita ancho > 0
        if self.rect.width >= 1 and self.rect.height >= 1:
             pygame.draw.ellipse(surface, self.color, self.rect, self.width)

    @staticmethod
    def from_points(p1, p2, color, width=1):
        """Constructor alternativo desde dos puntos."""
        x = min(p1[0], p2[0])
        y = min(p1[1], p2[1])
        w = abs(p1[0] - p2[0])
        h = abs(p1[1] - p2[1])
        return Ellipse(pygame.Rect(x, y, w, h), color, width)

class Triangle(Shape):
    def __init__(self, points, color, width=1):
        super().__init__(color, width)
        if len(points) != 3:
            raise ValueError("Triangle requiere exactamente 3 puntos.")
        self.points = points

    def draw(self, surface):
        """Dibuja el triángulo usando pygame.draw.polygon."""
        pygame.draw.polygon(surface, self.color, self.points, self.width)

class Polygon(Shape):
    def __init__(self, points, color, width=1):
        super().__init__(color, width)
        if len(points) < 3:
            raise ValueError("Polygon requiere al menos 3 puntos.")
        self.points = points

    def draw(self, surface):
        """Dibuja el polígono usando pygame.draw.polygon."""
        pygame.draw.polygon(surface, self.color, self.points, self.width)

class BezierCurve(Shape):
    def __init__(self, control_points, color, width=1, steps=20):
        super().__init__(color, width)
        if len(control_points) != 4:
            raise ValueError("BezierCurve requiere exactamente 4 puntos de control.")
        self.control_points = control_points
        self.steps = steps
        self._calculate_points() # Calcular los puntos de la línea al crear

    def _calculate_points(self):
        """Calcula los puntos de la línea que aproximan la curva."""
        self.points = []
        cp = self.control_points
        for i in range(self.steps + 1):
            t = i / self.steps
            inv_t = 1 - t
            x = ( inv_t**3 * cp[0][0] +
                  3 * inv_t**2 * t * cp[1][0] +
                  3 * inv_t * t**2 * cp[2][0] +
                  t**3 * cp[3][0] )
            y = ( inv_t**3 * cp[0][1] +
                  3 * inv_t**2 * t * cp[1][1] +
                  3 * inv_t * t**2 * cp[2][1] +
                  t**3 * cp[3][1] )
            self.points.append((int(x), int(y)))

    def draw(self, surface):
        """Dibuja la curva (aproximada) usando pygame.draw.lines."""
        if len(self.points) > 1:
            pygame.draw.lines(surface, self.color, False, self.points, self.width)
