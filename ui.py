import pygame

# --- Colores (podrían importarse o definirse centralmente) ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128) # Un gris más oscuro para iconos/bordes
LIGHT_GRAY = (220, 220, 220)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# --- Clase Botón (simple) ---
class Button:
    def __init__(self, x, y, width, height, color, icon_func=None, action=None, text=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color # Color de fondo o representativo (para colores)
        self.icon_func = icon_func # Función que dibuja el icono
        self.action = action # Identificador de la acción (e.g., 'line', 'color_red')
        self.is_selected = False # Para resaltar el botón seleccionado
        self.text = text
        if self.text:
             pygame.font.init() # Asegurar que font esté inicializado
             self.font = pygame.font.SysFont(None, 24) # Fuente simple
             self.text_surf = self.font.render(text, True, BLACK)
             self.text_rect = self.text_surf.get_rect(center=self.rect.center)


    def draw(self, surface):
        # Dibuja el fondo del botón
        pygame.draw.rect(surface, self.color, self.rect)
        # Dibuja el borde (resaltado si está seleccionado)
        # No resaltar botones de acción como 'clear'
        border_color = BLACK if self.is_selected and self.action not in ['clear'] else GRAY
        pygame.draw.rect(surface, border_color, self.rect, 2) # Borde de 2 píxeles

        # Dibuja el icono si existe una función para ello
        if self.icon_func:
            self.icon_func(surface, self.rect)
        elif self.text:
            surface.blit(self.text_surf, self.text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # No cambiar seleccion para botones de acción directa
                if self.action not in ['clear']:
                    self.is_selected = True
                return self.action
        return None

# --- Funciones para dibujar iconos simples (marcadores de posición) ---
def draw_line_icon(surface, rect):
    pygame.draw.line(surface, BLACK, rect.topleft + pygame.Vector2(5, 5),
                     rect.bottomright - pygame.Vector2(5, 5), 2)

def draw_curve_icon(surface, rect):
    # Simple curva cuadrática como placeholder
    points = [rect.topleft + pygame.Vector2(5, rect.height - 5),
              rect.midtop + pygame.Vector2(0, 5),
              rect.bottomright - pygame.Vector2(5, 5)]
    pygame.draw.lines(surface, BLACK, False, points, 2)

def draw_rect_icon(surface, rect):
    icon_rect = rect.inflate(-10, -10)
    pygame.draw.rect(surface, BLACK, icon_rect, 2)

def draw_circle_icon(surface, rect):
    pygame.draw.circle(surface, BLACK, rect.center, rect.width // 2 - 5, 2)

def draw_triangle_icon(surface, rect):
    points = [rect.midtop + pygame.Vector2(0, 5),
              rect.bottomleft + pygame.Vector2(5, -5),
              rect.bottomright + pygame.Vector2(-5, -5)]
    pygame.draw.polygon(surface, BLACK, points, 2)

def draw_polygon_icon(surface, rect): # Placeholder simple (pentagono)
    points = [rect.midtop + pygame.Vector2(0, 5),
              rect.topright + pygame.Vector2(-5, 15),
              rect.bottomright + pygame.Vector2(-15, -5),
              rect.bottomleft + pygame.Vector2(15, -5),
              rect.topleft + pygame.Vector2(5, 15)]
    pygame.draw.polygon(surface, BLACK, points, 2)

# --- Clase Panel Base (opcional, por si hay lógica común) ---
class Panel:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.buttons = []

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        for button in self.buttons:
            button.draw(surface)

    def handle_event(self, event):
        for button in self.buttons:
            action = button.handle_event(event)
            if action:
                 # Deseleccionar otros botones y seleccionar el actual (si aplica)
                 # Solo deseleccionar si el boton clickeado es seleccionable
                 if hasattr(button, 'is_selected') and button.action not in ['clear']:
                    for b in self.buttons:
                        if hasattr(b, 'is_selected'): b.is_selected = False
                    button.is_selected = True
                 # Para botones de acción directa como 'clear', no cambiamos la selección
                 # pero sí devolvemos la acción.
                 return action
        return None

# --- Panel de Herramientas --- Add Clear Button
class ToolPanel(Panel):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self._setup_buttons()

    def _setup_buttons(self):
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
            ('ellipse', None), # Añadir elipse, sin icono por ahora
        ]

        for tool_name, icon_func in tools:
            # Placeholder simple para elipse si no hay icono
            text = tool_name.capitalize() if not icon_func and tool_name == 'ellipse' else None
            button = Button(self.rect.x + padding,
                            current_y,
                            button_size, button_size,
                            WHITE, # Fondo blanco para botones de icono
                            icon_func=icon_func,
                            action=tool_name,
                            text=text)
            self.buttons.append(button)
            current_y += button_size + 5

        # Botón de Limpiar al final
        clear_button = Button(self.rect.x + padding,
                              current_y + 10, # Un poco más de espacio
                              button_size, button_size,
                              LIGHT_GRAY, # Color diferente
                              action='clear',
                              text='Limpiar')
        self.buttons.append(clear_button)


# --- Panel de Colores ---
class ColorPanel(Panel):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self._setup_buttons()

    def _setup_buttons(self):
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

        # Mapeo de action string a valor RGB real
        self.color_map = {name: rgb for rgb, name in colors}

        for i, (color_val, action_name) in enumerate(colors):
            button = Button(self.rect.x + padding,
                            self.rect.y + y_offset + i * (button_size + 5),
                            button_size, button_size,
                            color=color_val, # El color del botón es el color a seleccionar
                            action=action_name)
            self.buttons.append(button)

    # Sobreescribir handle_event para devolver el valor RGB
    def handle_event(self, event):
        action = super().handle_event(event)
        if action and action in self.color_map:
             # Seleccionar el botón de color clickeado
             for btn in self.buttons:
                 btn.is_selected = (btn.action == action)
             return self.color_map[action] # Devolver el color RGB
        return None
