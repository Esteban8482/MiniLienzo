import pygame
import sys
import ui  # Importamos el módulo ui
import fig # Importamos fig

# Inicializar Pygame
pygame.init()

# --- Constantes ---
SCREEN_WIDTH = 800  # Ancho total de la ventana
SCREEN_HEIGHT = 600 # Alto total de la ventana
LEFT_PANEL_WIDTH = 60 # Ancho del panel de herramientas
RIGHT_PANEL_WIDTH = 60 # Ancho del panel de colores
CANVAS_WIDTH = SCREEN_WIDTH - LEFT_PANEL_WIDTH - RIGHT_PANEL_WIDTH
CANVAS_HEIGHT = SCREEN_HEIGHT

# Colores (podrían moverse a un archivo de configuración o a ui.py si se prefieren centralizados)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# --- Configuración de la ventana ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Graficador Interactivo")

# --- Superficies ---
# Superficie para el lienzo (área central)
canvas_surface = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
canvas_surface.fill(WHITE) # Lienzo blanco inicial

# Superficie temporal para previsualización (mismo tamaño que el lienzo)
preview_surface = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT), pygame.SRCALPHA) # SRCALPHA para transparencia

# --- Crear instancias de los paneles de UI ---
# Asumiendo que ui.py define ToolPanel y ColorPanel
tool_panel = ui.ToolPanel(0, 0, LEFT_PANEL_WIDTH, SCREEN_HEIGHT, LIGHT_GRAY)
color_panel = ui.ColorPanel(SCREEN_WIDTH - RIGHT_PANEL_WIDTH, 0, RIGHT_PANEL_WIDTH, SCREEN_HEIGHT, LIGHT_GRAY)

# --- Estado de la aplicación ---
selected_tool = None
selected_color = BLACK # Color inicial por defecto
drawing = False
start_pos = None
current_mouse_pos = None # Posición actual relativa al canvas

# Para figuras de múltiples puntos (a implementar)
points = []

# --- Bucle principal ---
running = True
while running:
    # Limpiar la superficie de previsualización en cada frame
    preview_surface.fill((0, 0, 0, 0)) # Relleno transparente

    # --- Manejo de eventos ---
    current_mouse_pos = None # Resetear en cada iteración
    mouse_pos_screen = pygame.mouse.get_pos() # Posición global en la pantalla

    # Calcular posición relativa al canvas si el ratón está sobre él
    is_mouse_on_canvas = False
    if LEFT_PANEL_WIDTH <= mouse_pos_screen[0] < SCREEN_WIDTH - RIGHT_PANEL_WIDTH and \
       0 <= mouse_pos_screen[1] < SCREEN_HEIGHT:
        is_mouse_on_canvas = True
        current_mouse_pos = (mouse_pos_screen[0] - LEFT_PANEL_WIDTH, mouse_pos_screen[1])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Pasar eventos a los paneles para manejar clics en botones
        tool_action = tool_panel.handle_event(event)
        if tool_action:
            if tool_action == 'clear':
                canvas_surface.fill(WHITE) # Limpiar lienzo
                points = [] # Resetear puntos para polígono/curva
            else:
                selected_tool = tool_action
                points = [] # Resetear puntos al cambiar de herramienta
                print(f"Herramienta seleccionada: {selected_tool}") # Para depuración

        color_action = color_panel.handle_event(event)
        if color_action:
            selected_color = color_action
            print(f"Color seleccionado: {selected_color}") # Para depuración

        # Eventos del Lienzo (Canvas)
        if is_mouse_on_canvas:
            canvas_pos = current_mouse_pos # Usar la posición relativa calculada
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Botón izquierdo
                    if selected_tool in ['line', 'rectangle', 'circle', 'ellipse']:
                        drawing = True
                        start_pos = canvas_pos
                    # --- Lógica inicial para multi-puntos (a expandir) ---
                    elif selected_tool in ['triangle', 'polygon', 'curve']:
                        points.append(canvas_pos)
                        print(f"Punto {len(points)} añadido en {canvas_pos} para {selected_tool}")
                        # Dibujar punto/feedback en canvas permanente? O preview?
                        # Por ahora, solo almacenamos

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # Botón izquierdo
                    if drawing and selected_tool and start_pos:
                        end_pos = canvas_pos
                        # Dibujar figura final en canvas_surface
                        if selected_tool == 'line':
                            fig.draw_line(canvas_surface, selected_color, start_pos, end_pos, width=2)
                        elif selected_tool == 'rectangle':
                            rect = fig.get_rect_from_points(start_pos, end_pos)
                            fig.draw_rectangle(canvas_surface, selected_color, rect, width=2)
                        elif selected_tool == 'circle':
                            center, radius = fig.get_circle_params_from_points(start_pos, end_pos)
                            fig.draw_circle(canvas_surface, selected_color, center, radius, width=2)
                        elif selected_tool == 'ellipse':
                             rect = fig.get_rect_from_points(start_pos, end_pos)
                             fig.draw_ellipse(canvas_surface, selected_color, rect, width=2)

                    # Resetear estado de dibujo
                    drawing = False
                    start_pos = None
                    # NO reseteamos `points` aquí para multi-puntos

            # No necesitamos MOUSEMOTION aquí si usamos la preview

    # --- Lógica de Previsualización (si estamos dibujando) ---
    if drawing and selected_tool and start_pos and current_mouse_pos:
        preview_color = selected_color + (150,) # Añadir alpha para transparencia

        if selected_tool == 'line':
            fig.draw_line(preview_surface, preview_color, start_pos, current_mouse_pos, width=2)
        elif selected_tool == 'rectangle':
            rect = fig.get_rect_from_points(start_pos, current_mouse_pos)
            fig.draw_rectangle(preview_surface, preview_color, rect, width=2)
        elif selected_tool == 'circle':
            center, radius = fig.get_circle_params_from_points(start_pos, current_mouse_pos)
            fig.draw_circle(preview_surface, preview_color, center, radius, width=2)
        elif selected_tool == 'ellipse':
             rect = fig.get_rect_from_points(start_pos, current_mouse_pos)
             fig.draw_ellipse(preview_surface, preview_color, rect, width=2)

    # --- Lógica de dibujo ----
    # 1. Dibujar el lienzo permanente
    screen.blit(canvas_surface, (LEFT_PANEL_WIDTH, 0))
    # 2. Dibujar la previsualización sobre el lienzo
    screen.blit(preview_surface, (LEFT_PANEL_WIDTH, 0))
    # 3. Dibujar los paneles de UI encima de todo
    tool_panel.draw(screen)
    color_panel.draw(screen)

    # --- Actualizar la pantalla ---
    pygame.display.flip()

# --- Salir de Pygame ---
pygame.quit()
sys.exit()
