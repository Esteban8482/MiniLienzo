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
    def __init__(self, start_pos, end_pos, color, width=1, algorithm='pygame'):
        super().__init__(color, width)
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.algorithm = algorithm  # 'pygame', 'dda' o 'bresenham'

    def draw(self, surface):
        """Dibuja la línea usando el algoritmo seleccionado."""
        if self.algorithm == 'dda':
            self._draw_dda(surface)
        elif self.algorithm == 'bresenham':
            self._draw_bresenham(surface)
        else:  # Por defecto o si se especifica 'pygame'
            pygame.draw.line(surface, self.color, self.start_pos, self.end_pos, self.width)
            
    def _draw_dda(self, surface):
        """Implementación del algoritmo DDA (Digital Differential Analyzer)."""
        x1, y1 = self.start_pos
        x2, y2 = self.end_pos
        
        # Calcular diferencias y número de pasos
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        
        # Si no hay pasos, dibujar un punto
        if steps == 0:
            if self.width <= 1:
                surface.set_at((int(x1), int(y1)), self.color)
            else:
                pygame.draw.circle(surface, self.color, (int(x1), int(y1)), self.width // 2)
            return
            
        # Calcular incrementos por paso
        x_increment = dx / steps
        y_increment = dy / steps
        
        # Dibujar píxeles
        x, y = x1, y1
        
        # Dibujar línea con grosor
        if self.width <= 1:
            # Dibujar píxel a píxel para width=1
            for _ in range(int(steps) + 1):
                surface.set_at((int(round(x)), int(round(y))), self.color)
                x += x_increment
                y += y_increment
        else:
            # Para grosores > 1, dibujar círculos en cada punto
            for _ in range(int(steps) + 1):
                pygame.draw.circle(surface, self.color, (int(round(x)), int(round(y))), self.width // 2)
                x += x_increment
                y += y_increment
    
    def _draw_bresenham(self, surface):
        """Implementación del algoritmo de Bresenham."""
        x1, y1 = self.start_pos
        x2, y2 = self.end_pos
        
        # Convertir a enteros
        x1, y1 = int(x1), int(y1)
        x2, y2 = int(x2), int(y2)
        
        # Calcular diferencias y sentido del movimiento
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        
        # Intercambiar si la pendiente es mayor a 1
        steep = dy > dx
        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
            dx, dy = dy, dx
            sx, sy = sy, sx
        
        # Inicializar variables de error
        error = dx // 2
        y = y1
        
        # Lista para almacenar puntos calculados
        points = []
        
        # Calcular puntos de la línea
        for x in range(x1, x2 + sx, sx):
            # Si se ha intercambiado, revertir las coordenadas
            if steep:
                points.append((y, x))
            else:
                points.append((x, y))
            
            error -= dy
            if error < 0:
                y += sy
                error += dx
        
        # Dibujar puntos
        if self.width <= 1:
            # Dibujar píxel a píxel
            for point in points:
                surface.set_at(point, self.color)
        else:
            # Dibujar círculos para grosores > 1
            for point in points:
                pygame.draw.circle(surface, self.color, point, self.width // 2)
                
    @staticmethod
    def from_points(p1, p2, color, width=1, algorithm='pygame'):
        """Constructor alternativo desde dos puntos, incluyendo el algoritmo."""
        return Line(p1, p2, color, width, algorithm)

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
    def __init__(self, center, radius, color, width=1, algorithm='pygame'):
        super().__init__(color, width)
        self.center = center
        # Asegurar radio mínimo si hay grosor
        self.radius = max(int(radius), width)
        self.algorithm = algorithm  # 'pygame' o 'bresenham'

    def draw(self, surface):
        """Dibuja el círculo usando el algoritmo seleccionado."""
        if self.algorithm == 'bresenham':
            self._draw_bresenham(surface)
        else:  # Por defecto o si se especifica 'pygame'
            pygame.draw.circle(surface, self.color, self.center, self.radius, self.width)
    
    def _draw_bresenham(self, surface):
        """Implementación del algoritmo de Bresenham para círculos."""
        x0, y0 = int(self.center[0]), int(self.center[1])
        radius = int(self.radius)
        
        # Si el radio es muy pequeño, simplemente dibujamos un punto
        if radius <= 0:
            surface.set_at((x0, y0), self.color)
            return
            
        # Inicializar valores
        x = 0
        y = radius
        d = 3 - 2 * radius
        
        # Función para dibujar píxeles en los 8 octantes
        def draw_circle_points(cx, cy, x, y):
            # Si el ancho es 1, dibujamos píxeles individuales
            if self.width == 1:
                surface.set_at((cx + x, cy + y), self.color)
                surface.set_at((cx + y, cy + x), self.color)
                surface.set_at((cx + y, cy - x), self.color)
                surface.set_at((cx + x, cy - y), self.color)
                surface.set_at((cx - x, cy - y), self.color)
                surface.set_at((cx - y, cy - x), self.color)
                surface.set_at((cx - y, cy + x), self.color)
                surface.set_at((cx - x, cy + y), self.color)
            else:
                # Para grosores > 1, dibujamos pequeños círculos en cada punto
                for dx, dy in [(cx + x, cy + y), (cx + y, cy + x), 
                               (cx + y, cy - x), (cx + x, cy - y),
                               (cx - x, cy - y), (cx - y, cy - x),
                               (cx - y, cy + x), (cx - x, cy + y)]:
                    pygame.draw.circle(surface, self.color, (dx, dy), self.width // 2)
        
        # Si es un círculo relleno
        if self.width == 0:
            # Dibujamos líneas horizontales entre los puntos
            while x <= y:
                # Dibujar líneas horizontales entre los puntos para rellenar
                pygame.draw.line(surface, self.color, (x0 - x, y0 + y), (x0 + x, y0 + y))
                pygame.draw.line(surface, self.color, (x0 - y, y0 + x), (x0 + y, y0 + x))
                pygame.draw.line(surface, self.color, (x0 - y, y0 - x), (x0 + y, y0 - x))
                pygame.draw.line(surface, self.color, (x0 - x, y0 - y), (x0 + x, y0 - y))
                
                # Actualizar valores usando el algoritmo de Bresenham
                if d < 0:
                    d = d + 4 * x + 6
                else:
                    d = d + 4 * (x - y) + 10
                    y -= 1
                x += 1
        else:
            # Algoritmo de Bresenham para círculos con contorno
            while x <= y:
                draw_circle_points(x0, y0, x, y)
                
                # Actualizar valores usando el algoritmo de Bresenham
                if d < 0:
                    d = d + 4 * x + 6
                else:
                    d = d + 4 * (x - y) + 10
                    y -= 1
                x += 1

    @staticmethod
    def from_points(p1, p2, color, width=1, algorithm='pygame'):
        """Constructor alternativo desde centro y punto en borde."""
        center = p1
        radius = math.dist(p1, p2)
        return Circle(center, radius, color, width, algorithm)

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
