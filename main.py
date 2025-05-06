"""
Graficador Interactivo con Pygame
---------------------------------
Aplicación que permite dibujar figuras geométricas usando diferentes algoritmos de gráficos.
Implementa una interfaz gráfica con herramientas de dibujo y opciones de configuración.
"""
import pygame
import sys
import ui
import fig

# Inicialización de Pygame
pygame.init()

# Dimensiones y configuración del layout
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
LEFT_PANEL_WIDTH = 60
RIGHT_PANEL_WIDTH = 60
ALGORITHM_PANEL_HEIGHT = 120
CANVAS_WIDTH = SCREEN_WIDTH - LEFT_PANEL_WIDTH - RIGHT_PANEL_WIDTH

# Definición de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Configuración de la ventana principal
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Graficador Interactivo")

def create_canvas_surfaces(show_algorithm_panel):
    """
    Crea o recrea las superficies del canvas y previsualización.
    
    Args:
        show_algorithm_panel: Boolean que indica si se muestra el panel de algoritmos
        
    Returns:
        Tupla con (canvas_surface, preview_surface, canvas_height)
    """
    canvas_height = SCREEN_HEIGHT - (ALGORITHM_PANEL_HEIGHT if show_algorithm_panel else 0)
    
    canvas_surf = pygame.Surface((CANVAS_WIDTH, canvas_height))
    canvas_surf.fill(WHITE)
    
    preview_surf = pygame.Surface((CANVAS_WIDTH, canvas_height), pygame.SRCALPHA)
    
    return canvas_surf, preview_surf, canvas_height

# Inicialización de paneles de UI
tool_panel = ui.ToolPanel(0, 0, LEFT_PANEL_WIDTH, SCREEN_HEIGHT, LIGHT_GRAY)
color_panel = ui.ColorPanel(SCREEN_WIDTH - RIGHT_PANEL_WIDTH, 0, RIGHT_PANEL_WIDTH, SCREEN_HEIGHT, LIGHT_GRAY)
algorithm_line_panel = ui.AlgorithmPanel(LEFT_PANEL_WIDTH, 0, CANVAS_WIDTH, ALGORITHM_PANEL_HEIGHT, LIGHT_GRAY)
algorithm_circle_panel = ui.AlgorithmCirclePanel(LEFT_PANEL_WIDTH, 0, CANVAS_WIDTH, ALGORITHM_PANEL_HEIGHT, LIGHT_GRAY)
polygon_sides_panel = ui.PolygonSidesPanel(LEFT_PANEL_WIDTH, 0, CANVAS_WIDTH, ALGORITHM_PANEL_HEIGHT, LIGHT_GRAY)

# Estado inicial de la aplicación
selected_tool = None
selected_color = BLACK
selected_line_algorithm = 'pygame'
selected_circle_algorithm = 'pygame'
selected_polygon_sides = 5
drawing = False
start_pos = None
current_mouse_pos = None
show_algorithm_panel = False
current_algorithm_panel = None
points = [] 
point_radius = 5

# Lista para almacenar figuras permanentes
drawn_shapes = []

# Creación de superficies iniciales
canvas_surface, preview_surface, CANVAS_HEIGHT = create_canvas_surfaces(show_algorithm_panel)

# Bucle principal
running = True
while running:
    # Limpiar previsualización en cada frame
    preview_surface.fill((0, 0, 0, 0))

    # Obtener posición del ratón y calcular coordenadas relativas al canvas
    current_mouse_pos = None
    mouse_pos_screen = pygame.mouse.get_pos()
    is_mouse_on_canvas = False
    
    panel_height_offset = ALGORITHM_PANEL_HEIGHT if show_algorithm_panel else 0
    
    if LEFT_PANEL_WIDTH <= mouse_pos_screen[0] < SCREEN_WIDTH - RIGHT_PANEL_WIDTH and \
       panel_height_offset <= mouse_pos_screen[1] < SCREEN_HEIGHT:
        is_mouse_on_canvas = True
        current_mouse_pos = (mouse_pos_screen[0] - LEFT_PANEL_WIDTH, mouse_pos_screen[1] - panel_height_offset)

    # Gestión de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Procesar eventos del panel de herramientas
        tool_action = tool_panel.handle_event(event)
        if tool_action:
            if tool_action == 'clear':
                drawn_shapes = []
                points = []
            else:
                selected_tool = tool_action
                points = []
                drawing = False
                start_pos = None
                
                # Actualizar panel de algoritmos según herramienta seleccionada
                new_show_algorithm_panel = False
                new_algorithm_panel = None
                
                if selected_tool == 'line':
                    new_show_algorithm_panel = True
                    new_algorithm_panel = 'line'
                elif selected_tool == 'circle':
                    new_show_algorithm_panel = True
                    new_algorithm_panel = 'circle'
                elif selected_tool == 'polygon':
                    new_show_algorithm_panel = True
                    new_algorithm_panel = 'polygon'
                
                if new_show_algorithm_panel != show_algorithm_panel or current_algorithm_panel != new_algorithm_panel:
                    show_algorithm_panel = new_show_algorithm_panel
                    current_algorithm_panel = new_algorithm_panel
                    canvas_surface, preview_surface, CANVAS_HEIGHT = create_canvas_surfaces(show_algorithm_panel)

        # Procesar eventos del panel de colores
        color_action = color_panel.handle_event(event)
        if color_action:
            selected_color = color_action
            
        # Procesar eventos de los paneles de algoritmos
        if show_algorithm_panel:
            if current_algorithm_panel == 'line':
                algorithm_action = algorithm_line_panel.handle_event(event)
                if algorithm_action:
                    selected_line_algorithm = algorithm_action
            elif current_algorithm_panel == 'circle':
                algorithm_action = algorithm_circle_panel.handle_event(event)
                if algorithm_action:
                    selected_circle_algorithm = algorithm_action
            elif current_algorithm_panel == 'polygon':
                sides_action = polygon_sides_panel.handle_event(event)
                if sides_action:
                    selected_polygon_sides = sides_action

        # Procesar eventos de dibujo en el canvas
        if is_mouse_on_canvas:
            canvas_pos = current_mouse_pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo
                    if selected_tool in ['line', 'rectangle', 'circle', 'ellipse']:
                        drawing = True
                        start_pos = canvas_pos
                    elif selected_tool in ['triangle', 'polygon', 'curve']:
                        points.append(canvas_pos)
                        # Finalizar figuras multipunto cuando se alcanza el número requerido de puntos
                        if selected_tool == 'triangle' and len(points) == 3:
                            new_shape = fig.Triangle(points, selected_color, filled=False)
                            drawn_shapes.append(new_shape)
                            points = []
                        elif selected_tool == 'curve' and len(points) == 4:
                            new_shape = fig.BezierCurve(points, selected_color, filled=False)
                            drawn_shapes.append(new_shape)
                            points = []
                        elif selected_tool == 'polygon' and len(points) == selected_polygon_sides:
                            new_shape = fig.Polygon(points, selected_color, filled=False)
                            drawn_shapes.append(new_shape)
                            points = []

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing and selected_tool and start_pos:
                    end_pos = canvas_pos
                    new_shape = None
                    
                    # Crear figura según la herramienta seleccionada
                    if selected_tool == 'line':
                        new_shape = fig.Line(start_pos, end_pos, selected_color, filled=False, algorithm=selected_line_algorithm)
                    elif selected_tool == 'rectangle':
                        new_shape = fig.Rectangle.from_points(start_pos, end_pos, selected_color, filled=False)
                    elif selected_tool == 'circle':
                        new_shape = fig.Circle.from_points(start_pos, end_pos, selected_color, filled=False, algorithm=selected_circle_algorithm)
                    elif selected_tool == 'ellipse':
                         new_shape = fig.Ellipse.from_points(start_pos, end_pos, selected_color, filled=False)

                    if new_shape:
                        drawn_shapes.append(new_shape)

                    drawing = False
                    start_pos = None

    # Generar previsualización durante el arrastre
    if drawing and selected_tool and start_pos and current_mouse_pos:
        preview_color = selected_color
        temp_shape = None

        if selected_tool == 'line':
            temp_shape = fig.Line(start_pos, current_mouse_pos, preview_color, filled=False, algorithm=selected_line_algorithm)
        elif selected_tool == 'rectangle':
            temp_shape = fig.Rectangle.from_points(start_pos, current_mouse_pos, preview_color, filled=False)
        elif selected_tool == 'circle':
            temp_shape = fig.Circle.from_points(start_pos, current_mouse_pos, preview_color, filled=False, algorithm=selected_circle_algorithm)
        elif selected_tool == 'ellipse':
             temp_shape = fig.Ellipse.from_points(start_pos, current_mouse_pos, preview_color, filled=False)

        if temp_shape:
            temp_shape.draw(preview_surface)
    
    # Visualización para figuras multipunto (triángulo, polígono, curva)
    if selected_tool in ['triangle', 'curve', 'polygon'] and len(points) > 0:
        # Dibujar puntos de referencia
        for point in points:
            temp_surface = pygame.Surface((point_radius*2+1, point_radius*2+1), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface, (*selected_color, 200), (point_radius, point_radius), point_radius)
            preview_surface.blit(temp_surface, (point[0]-point_radius, point[1]-point_radius))
            
            # Indicar orden de los puntos
            font = pygame.font.SysFont(None, 20)
            text = font.render(str(points.index(point)+1), True, WHITE)
            text_rect = text.get_rect(center=point)
            preview_surface.blit(text, text_rect)
            
        # Visualizar guías específicas según figura
        if selected_tool == 'curve' and len(points) >= 2:
            # Líneas guía para curvas Bézier
            guide_color = (min(selected_color[0] + 100, 255), 
                          min(selected_color[1] + 100, 255), 
                          min(selected_color[2] + 100, 255), 150)
            
            for i in range(len(points)-1):
                pygame.draw.line(preview_surface, guide_color, points[i], points[i+1], 1)
            
        # Visualizar perímetro parcial para triángulos
        elif selected_tool == 'triangle' and len(points) >= 2:
            for i in range(len(points)-1):
                pygame.draw.line(preview_surface, selected_color, points[i], points[i+1], 1)
            
            if len(points) == 3:
                pygame.draw.line(preview_surface, selected_color, points[2], points[0], 1)
        
        # Visualizar perímetro parcial para polígonos
        elif selected_tool == 'polygon' and len(points) >= 2:
            for i in range(len(points)-1):
                pygame.draw.line(preview_surface, selected_color, points[i], points[i+1], 1)
            
            if len(points) == selected_polygon_sides or (len(points) >= 3):
                pygame.draw.line(preview_surface, selected_color, points[-1], points[0], 1)
            
            # Mostrar contador de puntos
            count_text = f"Punto {len(points)} de {selected_polygon_sides}"
            count_font = pygame.font.SysFont(None, 18)
            count_surf = count_font.render(count_text, True, BLACK)
            count_rect = count_surf.get_rect(topright=(CANVAS_WIDTH - 10, 10))
            preview_surface.blit(count_surf, count_rect)

    # Renderizado de la interfaz
    # 1. Limpiar y actualizar canvas
    canvas_surface.fill(WHITE)
    for shape in drawn_shapes:
        shape.draw(canvas_surface)

    # 2. Componer capas en la pantalla principal
    panel_height_offset = ALGORITHM_PANEL_HEIGHT if show_algorithm_panel else 0
    screen.blit(canvas_surface, (LEFT_PANEL_WIDTH, panel_height_offset))
    screen.blit(preview_surface, (LEFT_PANEL_WIDTH, panel_height_offset))

    # 3. Dibujar interfaz
    tool_panel.draw(screen)
    color_panel.draw(screen)
    
    if show_algorithm_panel:
        if current_algorithm_panel == 'line':
            algorithm_line_panel.draw(screen)
        elif current_algorithm_panel == 'circle':
            algorithm_circle_panel.draw(screen)
        elif current_algorithm_panel == 'polygon':
            polygon_sides_panel.draw(screen)

    # Actualizar display
    pygame.display.flip()

# Finalizar aplicación
pygame.quit()
sys.exit()
