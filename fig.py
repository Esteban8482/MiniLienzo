"""
Módulo de figuras para el graficador interactivo
-----------------------------------------------
Implementa las clases para dibujar diferentes figuras geométricas usando
algoritmos clásicos de gráficos por computadora (DDA, Bresenham, etc.).
Cada figura hereda de la clase base Shape y proporciona su propia implementación
del método draw().
"""
import pygame
import math

# --- Clase Base para Figuras ---
class Shape:
    """
    Clase base abstracta para todas las figuras.
    
    Attributes:
        color: Tupla RGB representando el color de la figura
        filled: Boolean indicando si la figura debe dibujarse rellena o solo el contorno
    """
    def __init__(self, color, filled=False):
        self.color = color
        self.filled = filled
    
    def draw(self, surface):
        """
        Método abstracto que debe ser implementado por las subclases.
        
        Args:
            surface: Superficie pygame donde se dibujará la figura
        """
        raise NotImplementedError("Cada figura debe implementar su propio método draw.")

# --- Clases herederas, concretas para Cada Figura ---
class Line(Shape):
    """
    Representa una línea entre dos puntos.
    Permite seleccionar entre varios algoritmos de rasterización.
    
    Attributes:
        start_pos: Punto inicial (x, y)
        end_pos: Punto final (x, y)
        algorithm: Algoritmo a usar ('pygame', 'dda', 'bresenham')
    """
    def __init__(self, start_pos, end_pos, color, filled=False, algorithm='pygame'):
        super().__init__(color, filled)
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.algorithm = algorithm

    def draw(self, surface):
        """
        Dibuja la línea usando el algoritmo seleccionado.
        
        Args:
            surface: Superficie pygame donde se dibujará la línea
        """
        if self.algorithm == 'dda':
            self._draw_dda(surface)
        elif self.algorithm == 'bresenham':
            self._draw_bresenham(surface)
        else:  # Por defecto o si se especifica 'pygame'
            pygame.draw.line(surface, self.color, self.start_pos, self.end_pos, 1)
            
    def _draw_dda(self, surface):
        """
        Implementa el algoritmo DDA (Digital Differential Analyzer) para dibujar líneas.
        Es un algoritmo de rasterización de líneas que trabaja con punto flotante.
        
        Args:
            surface: Superficie pygame donde se dibujará la línea
        """
        x1, y1 = self.start_pos
        x2, y2 = self.end_pos
        
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        
        if steps == 0:
            surface.set_at((int(x1), int(y1)), self.color)
            return
            
        x_increment = dx / steps
        y_increment = dy / steps
        
        x, y = x1, y1
        
        for _ in range(int(steps) + 1):
            surface.set_at((int(round(x)), int(round(y))), self.color)
            x += x_increment
            y += y_increment
    
    def _draw_bresenham(self, surface):
        """
        Implementa el algoritmo de Bresenham para dibujar líneas.
        Es un algoritmo de rasterización que solo utiliza aritmética de enteros.
        
        Args:
            surface: Superficie pygame donde se dibujará la línea
        """
        x1, y1 = self.start_pos
        x2, y2 = self.end_pos
        
        x1, y1 = int(x1), int(y1)
        x2, y2 = int(x2), int(y2)
        
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        
        steep = dy > dx
        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
            dx, dy = dy, dx
            sx, sy = sy, sx
        
        error = dx // 2
        y = y1
        
        points = []
        
        for x in range(x1, x2 + sx, sx):
            if steep:
                points.append((y, x))
            else:
                points.append((x, y))
            
            error -= dy
            if error < 0:
                y += sy
                error += dx
        
        for point in points:
            surface.set_at(point, self.color)
                
    @staticmethod
    def from_points(p1, p2, color, filled=False, algorithm='pygame'):
        """
        Constructor alternativo desde dos puntos.
        
        Args:
            p1: Punto inicial (x, y)
            p2: Punto final (x, y)
            color: Color de la línea
            filled: No se utiliza para líneas
            algorithm: Algoritmo de dibujo a utilizar
            
        Returns:
            Instancia de Line configurada
        """
        return Line(p1, p2, color, filled, algorithm)

class Rectangle(Shape):
    """
    Representa un rectángulo definido por su posición, ancho y alto.
    
    Attributes:
        rect: Objeto pygame.Rect que define la posición y dimensiones
    """
    def __init__(self, rect, color, filled=False):
        super().__init__(color, filled)
        self.rect = pygame.Rect(rect)
        self.rect.normalize()

    def draw(self, surface):
        """
        Dibuja el rectángulo usando líneas con el algoritmo de Bresenham.
        
        Args:
            surface: Superficie pygame donde se dibujará el rectángulo
        """
        x, y, w, h = self.rect.x, self.rect.y, self.rect.width, self.rect.height
        
        if self.filled:
            for row in range(y, y + h):
                line = Line((x, row), (x + w - 1, row), self.color, False, 'bresenham')
                line.draw(surface)
        else:
            top_line = Line((x, y), (x + w - 1, y), self.color, False, 'bresenham')
            right_line = Line((x + w - 1, y), (x + w - 1, y + h - 1), self.color, False, 'bresenham')
            bottom_line = Line((x, y + h - 1), (x + w - 1, y + h - 1), self.color, False, 'bresenham')
            left_line = Line((x, y), (x, y + h - 1), self.color, False, 'bresenham')
            
            top_line.draw(surface)
            right_line.draw(surface)
            bottom_line.draw(surface)
            left_line.draw(surface)

    @staticmethod
    def from_points(p1, p2, color, filled=False):
        """
        Constructor alternativo desde dos puntos (esquinas opuestas).
        
        Args:
            p1: Primera esquina (x, y)
            p2: Esquina opuesta (x, y)
            color: Color del rectángulo
            filled: Si es True, se rellena el rectángulo
            
        Returns:
            Instancia de Rectangle configurada
        """
        x = min(p1[0], p2[0])
        y = min(p1[1], p2[1])
        w = abs(p1[0] - p2[0])
        h = abs(p1[1] - p2[1])
        return Rectangle(pygame.Rect(x, y, w, h), color, filled)

class Circle(Shape):
    """
    Representa un círculo definido por su centro y radio.
    
    Attributes:
        center: Punto central (x, y)
        radius: Radio del círculo
        algorithm: Algoritmo a usar ('pygame', 'bresenham')
    """
    def __init__(self, center, radius, color, filled=False, algorithm='pygame'):
        super().__init__(color, filled)
        self.center = center
        self.radius = int(radius)
        self.algorithm = algorithm

    def draw(self, surface):
        """
        Dibuja el círculo usando el algoritmo seleccionado.
        
        Args:
            surface: Superficie pygame donde se dibujará el círculo
        """
        if self.algorithm == 'bresenham':
            self._draw_bresenham(surface)
        else:
            width = 0 if self.filled else 1
            pygame.draw.circle(surface, self.color, self.center, self.radius, width)
    
    def _draw_bresenham(self, surface):
        """
        Implementa el algoritmo de Bresenham para círculos.
        
        Args:
            surface: Superficie pygame donde se dibujará el círculo
        """
        x0, y0 = int(self.center[0]), int(self.center[1])
        radius = int(self.radius)
        
        if radius <= 0:
            surface.set_at((x0, y0), self.color)
            return
            
        x = 0
        y = radius
        d = 3 - 2 * radius
        
        if self.filled:
            while x <= y:
                Line((x0 - x, y0 + y), (x0 + x, y0 + y), self.color, False, 'bresenham').draw(surface)
                Line((x0 - y, y0 + x), (x0 + y, y0 + x), self.color, False, 'bresenham').draw(surface)
                Line((x0 - y, y0 - x), (x0 + y, y0 - x), self.color, False, 'bresenham').draw(surface)
                Line((x0 - x, y0 - y), (x0 + x, y0 - y), self.color, False, 'bresenham').draw(surface)
                
                if d < 0:
                    d = d + 4 * x + 6
                else:
                    d = d + 4 * (x - y) + 10
                    y -= 1
                x += 1
        else:
            while x <= y:
                # Dibujar puntos en los 8 octantes
                surface.set_at((x0 + x, y0 + y), self.color)
                surface.set_at((x0 + y, y0 + x), self.color)
                surface.set_at((x0 + y, y0 - x), self.color)
                surface.set_at((x0 + x, y0 - y), self.color)
                surface.set_at((x0 - x, y0 - y), self.color)
                surface.set_at((x0 - y, y0 - x), self.color)
                surface.set_at((x0 - y, y0 + x), self.color)
                surface.set_at((x0 - x, y0 + y), self.color)
                
                if d < 0:
                    d = d + 4 * x + 6
                else:
                    d = d + 4 * (x - y) + 10
                    y -= 1
                x += 1

    @staticmethod
    def from_points(p1, p2, color, filled=False, algorithm='pygame'):
        """
        Constructor alternativo desde el centro y un punto en la circunferencia.
        
        Args:
            p1: Centro del círculo (x, y)
            p2: Punto en la circunferencia (x, y)
            color: Color del círculo
            filled: Si es True, se rellena el círculo
            algorithm: Algoritmo de dibujo a utilizar
            
        Returns:
            Instancia de Circle configurada
        """
        center = p1
        radius = math.dist(p1, p2)
        return Circle(center, radius, color, filled, algorithm)

class Ellipse(Shape):
    """
    Representa una elipse definida por su rectángulo contenedor.
    
    Attributes:
        rect: Objeto pygame.Rect que define la posición y dimensiones
    """
    def __init__(self, rect, color, filled=False):
        super().__init__(color, filled)
        self.rect = pygame.Rect(rect)
        self.rect.normalize()

    def draw(self, surface):
        """
        Dibuja la elipse usando algoritmos específicos según sea contorno o relleno.
        
        Args:
            surface: Superficie pygame donde se dibujará la elipse
        """
        if self.rect.width < 1 or self.rect.height < 1:
            return
            
        xc = self.rect.x + self.rect.width // 2
        yc = self.rect.y + self.rect.height // 2
        rx = self.rect.width // 2
        ry = self.rect.height // 2
        
        if rx <= 0 or ry <= 0:
            surface.set_at((xc, yc), self.color)
            return
            
        if self.filled:
            self._draw_filled(surface, xc, yc, rx, ry)
        else:
            self._draw_bresenham_ellipse(surface, xc, yc, rx, ry)
    
    def _draw_bresenham_ellipse(self, surface, xc, yc, rx, ry):
        """
        Implementa el algoritmo de Bresenham para elipses (contorno).
        
        Args:
            surface: Superficie pygame donde se dibujará la elipse
            xc, yc: Coordenadas del centro de la elipse
            rx, ry: Radios de la elipse en X e Y
        """
        xc, yc, rx, ry = int(xc), int(yc), int(rx), int(ry)
        
        # Región 1
        x, y = 0, ry
        
        d1 = (ry * ry) - (rx * rx * ry) + (0.25 * rx * rx)
        dx = 2 * ry * ry * x
        dy = 2 * rx * rx * y
        
        def draw_points(x, y):
            """Dibuja 4 puntos simétricos respecto al centro"""
            surface.set_at((xc + x, yc + y), self.color)
            surface.set_at((xc - x, yc + y), self.color)
            surface.set_at((xc + x, yc - y), self.color)
            surface.set_at((xc - x, yc - y), self.color)
        
        # Procesamiento en la región 1
        while dx < dy:
            draw_points(x, y)
            
            if d1 < 0:
                x += 1
                dx += 2 * ry * ry
                d1 += dx + ry * ry
            else:
                x += 1
                y -= 1
                dx += 2 * ry * ry
                dy -= 2 * rx * rx
                d1 += dx - dy + ry * ry
        
        # Región 2
        d2 = ((ry * ry) * ((x + 0.5) * (x + 0.5))) + \
             ((rx * rx) * ((y - 1) * (y - 1))) - \
             (rx * rx * ry * ry)
        
        # Procesamiento en la región 2
        while y >= 0:
            draw_points(x, y)
            
            if d2 > 0:
                y -= 1
                dy -= 2 * rx * rx
                d2 += rx * rx - dy
            else:
                y -= 1
                x += 1
                dx += 2 * ry * ry
                dy -= 2 * rx * rx
                d2 += dx - dy + rx * rx
    
    def _draw_filled(self, surface, xc, yc, rx, ry):
        """
        Dibuja una elipse rellena usando líneas horizontales.
        
        Args:
            surface: Superficie pygame donde se dibujará la elipse
            xc, yc: Coordenadas del centro de la elipse
            rx, ry: Radios de la elipse en X e Y
        """
        for y in range(yc - ry, yc + ry + 1):
            if ry == 0:
                continue
                
            dy = y - yc
            dy_squared = dy * dy
            term = (1.0 - dy_squared / (ry * ry)) * (rx * rx)
            
            if term < 0:
                continue
                
            dx = int(math.sqrt(term))
            
            start_x = xc - dx
            end_x = xc + dx
            line = Line((start_x, y), (end_x, y), self.color, False, 'bresenham')
            line.draw(surface)

    @staticmethod
    def from_points(p1, p2, color, filled=False):
        """
        Constructor alternativo desde dos puntos (esquinas opuestas del rectángulo contenedor).
        
        Args:
            p1: Primera esquina (x, y)
            p2: Esquina opuesta (x, y)
            color: Color de la elipse
            filled: Si es True, se rellena la elipse
            
        Returns:
            Instancia de Ellipse configurada
        """
        x = min(p1[0], p2[0])
        y = min(p1[1], p2[1])
        w = abs(p1[0] - p2[0])
        h = abs(p1[1] - p2[1])
        return Ellipse(pygame.Rect(x, y, w, h), color, filled)

class Triangle(Shape):
    """
    Representa un triángulo definido por tres puntos.
    
    Attributes:
        points: Lista de tres puntos (x, y) que definen los vértices
    """
    def __init__(self, points, color, filled=False):
        super().__init__(color, filled)
        if len(points) != 3:
            raise ValueError("Triangle requiere exactamente 3 puntos.")
        self.points = points

    def draw(self, surface):
        """
        Dibuja el triángulo como contorno o relleno según corresponda.
        
        Args:
            surface: Superficie pygame donde se dibujará el triángulo
        """
        if self.filled:
            self._draw_filled(surface)
        else:
            for i in range(3):
                start_point = self.points[i]
                end_point = self.points[(i + 1) % 3]
                line = Line(start_point, end_point, self.color, False, 'bresenham')
                line.draw(surface)
    
    def _draw_filled(self, surface):
        """
        Implementa el algoritmo de relleno por escaneo de líneas para triángulos.
        
        Args:
            surface: Superficie pygame donde se dibujará el triángulo
        """
        sorted_points = sorted(self.points, key=lambda p: p[1])
        
        x1, y1 = sorted_points[0]
        x2, y2 = sorted_points[1]
        x3, y3 = sorted_points[2]
        
        if x1 == x2 == x3:
            for y in range(int(y1), int(y3) + 1):
                surface.set_at((int(x1), y), self.color)
            return
            
        # Calcular pendientes de los lados
        # Para evitar división por cero al calcular pendientes
        slope_1_3 = (x3 - x1) / (y3 - y1) if y3 != y1 else 0
        slope_1_2 = (x2 - x1) / (y2 - y1) if y2 != y1 else 0
        slope_2_3 = (x3 - x2) / (y3 - y2) if y3 != y2 else 0
        
        # Escanear la parte superior del triángulo
        x_left = x_right = x1
        
        # Escanear desde el punto superior hasta el medio
        for y in range(int(y1), int(y2) + 1):
            # Calcular intersecciones con el scanline
            if y2 != y1:
                x_right = x1 + (y - y1) * slope_1_2
            if y3 != y1:
                x_left = x1 + (y - y1) * slope_1_3
                
            # Asegurar que x_left <= x_right
            if x_left > x_right:
                x_left, x_right = x_right, x_left
                
            # Dibujar línea horizontal entre intersecciones
            line = Line((int(x_left), y), (int(x_right), y), self.color, False, 'bresenham')
            line.draw(surface)
        
        # Escanear la parte inferior del triángulo
        # Reiniciar x_left o x_right dependiendo de qué lado cambia en el punto medio
        if y3 != y2:
            if x2 < x3:
                x_left = x2
            else:
                x_right = x2
                
        # Escanear desde el punto medio hasta el inferior
        for y in range(int(y2) + 1, int(y3) + 1):
            # Calcular intersecciones con el scanline
            if y3 != y1:
                x_left = x1 + (y - y1) * slope_1_3
            if y3 != y2:
                x_right = x2 + (y - y2) * slope_2_3
                
            # Asegurar que x_left <= x_right
            if x_left > x_right:
                x_left, x_right = x_right, x_left
                
            # Dibujar línea horizontal entre intersecciones
            line = Line((int(x_left), y), (int(x_right), y), self.color, False, 'bresenham')
            line.draw(surface)

class Polygon(Shape):
    """
    Representa un polígono definido por n puntos.
    
    Attributes:
        points: Lista de puntos (x, y) que definen los vértices
    """
    def __init__(self, points, color, filled=False):
        super().__init__(color, filled)
        if len(points) < 3:
            raise ValueError("Polygon requiere al menos 3 puntos.")
        self.points = points

    def draw(self, surface):
        """
        Dibuja el polígono como contorno o relleno según corresponda.
        
        Args:
            surface: Superficie pygame donde se dibujará el polígono
        """
        if self.filled:
            self._draw_filled(surface)
        else:
            num_points = len(self.points)
            for i in range(num_points):
                start_point = self.points[i]
                end_point = self.points[(i + 1) % num_points]
                line = Line(start_point, end_point, self.color, False, 'bresenham')
                line.draw(surface)
    
    def _draw_filled(self, surface):
        """
        Implementa el algoritmo de relleno por escaneo de líneas para polígonos.
        
        Args:
            surface: Superficie pygame donde se dibujará el polígono
        """
        min_y = min(p[1] for p in self.points)
        max_y = max(p[1] for p in self.points)
        
        for y in range(int(min_y), int(max_y) + 1):
            intersections = []
            num_points = len(self.points)
            
            for i in range(num_points):
                p1 = self.points[i]
                p2 = self.points[(i + 1) % num_points]
                
                if (p1[1] <= y < p2[1]) or (p2[1] <= y < p1[1]):
                    if p1[1] == p2[1]:
                        continue
                    
                    x = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])
                    intersections.append(int(x))
            
            intersections.sort()
            
            for i in range(0, len(intersections), 2):
                if i + 1 < len(intersections):
                    start_x = intersections[i]
                    end_x = intersections[i + 1]
                    line = Line((start_x, y), (end_x, y), self.color, False, 'bresenham')
                    line.draw(surface)

class BezierCurve(Shape):
    """
    Representa una curva de Bézier cúbica definida por 4 puntos de control.
    
    Attributes:
        control_points: Lista de 4 puntos de control (x, y)
        steps: Número de segmentos para aproximar la curva
        points: Lista de puntos calculados que componen la curva
    """
    def __init__(self, control_points, color, filled=False, steps=20):
        super().__init__(color, filled)
        if len(control_points) != 4:
            raise ValueError("BezierCurve requiere exactamente 4 puntos de control.")
        self.control_points = control_points
        self.steps = steps
        self._calculate_points()

    def _calculate_points(self):
        """
        Calcula los puntos de la línea que aproximan la curva usando
        la ecuación paramétrica de la curva de Bézier cúbica.
        """
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
        """
        Dibuja la curva de Bézier conectando los puntos calculados con líneas.
        
        Args:
            surface: Superficie pygame donde se dibujará la curva
        """
        if len(self.points) < 2:
            return
            
        for i in range(len(self.points) - 1):
            line = Line(self.points[i], self.points[i+1], self.color, False, 'bresenham')
            line.draw(surface)
