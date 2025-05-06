"""
Módulo de interfaz de usuario para el graficador interactivo
-----------------------------------------------------------
Implementa los componentes de la interfaz gráfica, incluyendo paneles, botones
y funciones para dibujar iconos. Gestiona la interacción del usuario con 
las herramientas y configuraciones del graficador.
"""
import pygame

# Definición de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (220, 220, 220)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

class Button:
    """
    Implementa un botón interactivo con soporte para iconos o texto.
    
    Attributes:
        rect: Rectángulo que define la posición y tamaño del botón
        color: Color de fondo del botón
        icon_func: Función que dibuja el icono del botón
        action: Identificador de la acción asociada al botón
        is_selected: Indica si el botón está seleccionado
        text: Texto a mostrar en el botón (alternativa a iconos)
    """
    def __init__(self, x, y, width, height, color, icon_func=None, action=None, text=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.icon_func = icon_func
        self.action = action
        self.is_selected = False
        self.text = text
        if self.text:
             pygame.font.init()
             font_size = 18 if action == 'clear' else 24
             self.font = pygame.font.SysFont(None, font_size)
             self.text_surf = self.font.render(text, True, BLACK)
             self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, surface):
        """
        Dibuja el botón en la superficie especificada.
        
        Args:
            surface: Superficie pygame donde se dibujará el botón
        """
        pygame.draw.rect(surface, self.color, self.rect)
        
        border_color = BLACK if self.is_selected and self.action not in ['clear'] else GRAY
        pygame.draw.rect(surface, border_color, self.rect, 2)

        if self.icon_func:
            self.icon_func(surface, self.rect)
        elif self.text:
            surface.blit(self.text_surf, self.text_rect)

    def handle_event(self, event):
        """
        Procesa eventos de usuario relacionados con el botón.
        
        Args:
            event: Evento pygame a procesar
            
        Returns:
            El identificador de acción si el botón fue clickeado, None en caso contrario
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action not in ['clear']:
                    self.is_selected = True
                return self.action
        return None

# Funciones para dibujar iconos
def draw_line_icon(surface, rect):
    """Dibuja un icono de línea."""
    pygame.draw.line(surface, BLACK, rect.topleft + pygame.Vector2(5, 5),
                     rect.bottomright - pygame.Vector2(5, 5), 2)

def draw_curve_icon(surface, rect):
    """Dibuja un icono de curva Bézier."""
    p0 = rect.topleft + pygame.Vector2(5, rect.height * 0.7)
    p1 = rect.topleft + pygame.Vector2(rect.width * 0.3, 5)
    p2 = rect.topright + pygame.Vector2(-rect.width * 0.3, rect.height - 5)
    p3 = rect.bottomright + pygame.Vector2(-5, -rect.height * 0.7)
    
    points = []
    steps = 12
    for i in range(steps + 1):
        t = i / steps
        inv_t = 1 - t
        x = (inv_t**3 * p0[0] + 
             3 * inv_t**2 * t * p1[0] + 
             3 * inv_t * t**2 * p2[0] + 
             t**3 * p3[0])
        y = (inv_t**3 * p0[1] + 
             3 * inv_t**2 * t * p1[1] + 
             3 * inv_t * t**2 * p2[1] + 
             t**3 * p3[1])
        points.append((int(x), int(y)))
    
    if len(points) > 1:
        pygame.draw.lines(surface, BLACK, False, points, 2)

def draw_rect_icon(surface, rect):
    """Dibuja un icono de rectángulo."""
    icon_rect = rect.inflate(-10, -10)
    pygame.draw.rect(surface, BLACK, icon_rect, 2)

def draw_circle_icon(surface, rect):
    """Dibuja un icono de círculo."""
    pygame.draw.circle(surface, BLACK, rect.center, rect.width // 2 - 5, 2)

def draw_ellipse_icon(surface, rect):
    """Dibuja un icono de elipse."""
    icon_rect = rect.inflate(-10, -16)
    pygame.draw.ellipse(surface, BLACK, icon_rect, 2)

def draw_triangle_icon(surface, rect):
    """Dibuja un icono de triángulo."""
    points = [rect.midtop + pygame.Vector2(0, 5),
              rect.bottomleft + pygame.Vector2(5, -5),
              rect.bottomright + pygame.Vector2(-5, -5)]
    pygame.draw.polygon(surface, BLACK, points, 2)

def draw_polygon_icon(surface, rect):
    """Dibuja un icono de polígono (pentágono)."""
    points = [rect.midtop + pygame.Vector2(0, 5),
              rect.topright + pygame.Vector2(-5, 15),
              rect.bottomright + pygame.Vector2(-15, -5),
              rect.bottomleft + pygame.Vector2(15, -5),
              rect.topleft + pygame.Vector2(5, 15)]
    pygame.draw.polygon(surface, BLACK, points, 2)

class Panel:
    """
    Clase base para todos los paneles de la interfaz.
    
    Attributes:
        rect: Rectángulo que define la posición y tamaño del panel
        color: Color de fondo del panel
        buttons: Lista de botones contenidos en el panel
    """
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.buttons = []

    def draw(self, surface):
        """
        Dibuja el panel y sus botones en la superficie especificada.
        
        Args:
            surface: Superficie pygame donde se dibujará el panel
        """
        pygame.draw.rect(surface, self.color, self.rect)
        for button in self.buttons:
            button.draw(surface)

    def handle_event(self, event):
        """
        Procesa eventos de usuario relacionados con los botones del panel.
        
        Args:
            event: Evento pygame a procesar
            
        Returns:
            El identificador de acción del botón clickeado, None si ninguno fue clickeado
        """
        for button in self.buttons:
            action = button.handle_event(event)
            if action:
                if hasattr(button, 'is_selected') and button.action not in ['clear']:
                    for b in self.buttons:
                        if hasattr(b, 'is_selected'): b.is_selected = False
                    button.is_selected = True
                return action
        return None

class ToolPanel(Panel):
    """
    Panel de herramientas de dibujo (línea, círculo, rectángulo, etc.)
    """
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self._setup_buttons()

    def _setup_buttons(self):
        """Configura los botones de herramientas en el panel."""
        button_size = 40
        padding = (self.rect.width - button_size) // 2
        y_offset = 10
        current_y = self.rect.y + y_offset

        tools = [
            ('line', draw_line_icon),
            ('curve', draw_curve_icon),
            ('rectangle', draw_rect_icon),
            ('circle', draw_circle_icon),
            ('triangle', draw_triangle_icon),
            ('polygon', draw_polygon_icon),
            ('ellipse', draw_ellipse_icon),
        ]

        for tool_name, icon_func in tools:
            button = Button(self.rect.x + padding,
                            current_y,
                            button_size, button_size,
                            WHITE,
                            icon_func=icon_func,
                            action=tool_name)
            self.buttons.append(button)
            current_y += button_size + 5

        # Botón de limpiar
        clear_button = Button(self.rect.x + padding,
                              current_y + 10,
                              button_size, button_size,
                              LIGHT_GRAY,
                              action='clear',
                              text='Limpiar')
        self.buttons.append(clear_button)

class ColorPanel(Panel):
    """
    Panel de selección de colores.
    
    Attributes:
        color_map: Diccionario que mapea identificadores de colores a valores RGB
    """
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self._setup_buttons()

    def _setup_buttons(self):
        """Configura los botones de colores en el panel."""
        button_size = 40
        padding = (self.rect.width - button_size) // 2
        y_offset = 10

        colors = [
            (YELLOW, 'color_yellow'),
            (BLUE, 'color_blue'),
            (RED, 'color_red'),
            (GREEN, 'color_green'),
            (ORANGE, 'color_orange'),
            (WHITE, 'color_white'),
            (GRAY, 'color_gray'),
            (BLACK, 'color_black')
        ]

        self.color_map = {name: rgb for rgb, name in colors}

        for i, (color_val, action_name) in enumerate(colors):
            button = Button(self.rect.x + padding,
                            self.rect.y + y_offset + i * (button_size + 5),
                            button_size, button_size,
                            color=color_val,
                            action=action_name)
            self.buttons.append(button)

    def handle_event(self, event):
        """
        Procesa eventos y devuelve el valor RGB del color seleccionado.
        
        Args:
            event: Evento pygame a procesar
            
        Returns:
            Valor RGB del color seleccionado o None
        """
        action = super().handle_event(event)
        if action and action in self.color_map:
             for btn in self.buttons:
                 btn.is_selected = (btn.action == action)
             return self.color_map[action]
        return None

class AlgorithmPanel(Panel):
    """
    Panel para seleccionar algoritmos de dibujo de líneas.
    
    Attributes:
        selected_algorithm: Algoritmo actualmente seleccionado
        title_surf, title_rect: Superficie y posición del título del panel
    """
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self._setup_buttons()
        self.selected_algorithm = 'pygame'

    def _setup_buttons(self):
        """Configura los botones de algoritmos en el panel."""
        button_width = self.rect.width - 10
        button_height = 30
        y_offset = 10

        # Título del panel
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 24)
        self.title_surf = self.font.render("Algoritmos de Línea", True, BLACK)
        self.title_rect = self.title_surf.get_rect(
            center=(self.rect.x + self.rect.width // 2, self.rect.y + y_offset)
        )
        
        y_offset += 30

        algorithms = [
            ('pygame', 'Pygame'),
            ('dda', 'DDA'),
            ('bresenham', 'Bresenham')
        ]

        for i, (algo_id, algo_name) in enumerate(algorithms):
            button = Button(self.rect.x + 5,
                            self.rect.y + y_offset + i * (button_height + 5),
                            button_width, button_height,
                            color=LIGHT_GRAY,
                            action=algo_id,
                            text=algo_name)
            if algo_id == 'pygame':
                button.is_selected = True
            self.buttons.append(button)
            
    def draw(self, surface):
        """
        Dibuja el panel, sus botones y el título.
        
        Args:
            surface: Superficie pygame donde se dibujará el panel
        """
        super().draw(surface)
        surface.blit(self.title_surf, self.title_rect)

    def handle_event(self, event):
        """
        Procesa eventos y actualiza el algoritmo seleccionado.
        
        Args:
            event: Evento pygame a procesar
            
        Returns:
            Identificador del algoritmo seleccionado o None
        """
        action = super().handle_event(event)
        if action in ['pygame', 'dda', 'bresenham']:
            self.selected_algorithm = action
            for btn in self.buttons:
                btn.is_selected = (btn.action == action)
            return action
        return None

class AlgorithmCirclePanel(Panel):
    """
    Panel para seleccionar algoritmos de dibujo de círculos.
    
    Attributes:
        selected_algorithm: Algoritmo actualmente seleccionado
        title_surf, title_rect: Superficie y posición del título del panel
    """
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self._setup_buttons()
        self.selected_algorithm = 'pygame'

    def _setup_buttons(self):
        """Configura los botones de algoritmos en el panel."""
        button_width = self.rect.width - 10
        button_height = 30
        y_offset = 10

        # Título del panel
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 24)
        self.title_surf = self.font.render("Algoritmos de Círculo", True, BLACK)
        self.title_rect = self.title_surf.get_rect(
            center=(self.rect.x + self.rect.width // 2, self.rect.y + y_offset)
        )
        
        y_offset += 30

        algorithms = [
            ('pygame', 'Pygame'),
            ('bresenham', 'Bresenham')
        ]

        for i, (algo_id, algo_name) in enumerate(algorithms):
            button = Button(self.rect.x + 5,
                            self.rect.y + y_offset + i * (button_height + 5),
                            button_width, button_height,
                            color=LIGHT_GRAY,
                            action=algo_id,
                            text=algo_name)
            if algo_id == 'pygame':
                button.is_selected = True
            self.buttons.append(button)

    def draw(self, surface):
        """
        Dibuja el panel, sus botones y el título.
        
        Args:
            surface: Superficie pygame donde se dibujará el panel
        """
        super().draw(surface)
        surface.blit(self.title_surf, self.title_rect)

    def handle_event(self, event):
        """
        Procesa eventos y actualiza el algoritmo seleccionado.
        
        Args:
            event: Evento pygame a procesar
            
        Returns:
            Identificador del algoritmo seleccionado o None
        """
        action = super().handle_event(event)
        if action in ['pygame', 'bresenham']:
            self.selected_algorithm = action
            for btn in self.buttons:
                btn.is_selected = (btn.action == action)
            return action
        return None

class PolygonSidesPanel(Panel):
    """
    Panel para seleccionar el número de lados del polígono.
    
    Attributes:
        selected_sides: Número de lados seleccionado
        title_surf, title_rect: Superficie y posición del título del panel
    """
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self._setup_buttons()
        self.selected_sides = 5
        
    def _setup_buttons(self):
        """Configura los botones de selección de lados en el panel."""
        button_width = self.rect.width - 10
        button_height = 30
        y_offset = 10
        
        # Título del panel
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 24)
        self.title_surf = self.font.render("Lados del Polígono", True, BLACK)
        self.title_rect = self.title_surf.get_rect(
            center=(self.rect.x + self.rect.width // 2, self.rect.y + y_offset)
        )
        
        y_offset += 30
        
        # Opciones de lados
        sides_options = [
            (3, "3 lados"),
            (4, "4 lados"),
            (5, "5 lados"),
            (6, "6 lados"),
            (8, "8 lados")
        ]
        
        for i, (sides, text) in enumerate(sides_options):
            button = Button(self.rect.x + 5,
                            self.rect.y + y_offset + i * (button_height + 5),
                            button_width, button_height,
                            color=LIGHT_GRAY,
                            action=str(sides),
                            text=text)
            if sides == 5:
                button.is_selected = True
            self.buttons.append(button)
    
    def draw(self, surface):
        """
        Dibuja el panel, sus botones y el título.
        
        Args:
            surface: Superficie pygame donde se dibujará el panel
        """
        super().draw(surface)
        surface.blit(self.title_surf, self.title_rect)
        
    def handle_event(self, event):
        """
        Procesa eventos y actualiza el número de lados seleccionado.
        
        Args:
            event: Evento pygame a procesar
            
        Returns:
            Número de lados seleccionado o None
        """
        action = super().handle_event(event)
        if action and action.isdigit():
            sides = int(action)
            self.selected_sides = sides
            for btn in self.buttons:
                btn.is_selected = (btn.action == action)
            return sides
        return None
