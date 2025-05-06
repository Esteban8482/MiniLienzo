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
ALGORITHM_PANEL_HEIGHT = 120 # Altura del panel de algoritmos
CANVAS_WIDTH = SCREEN_WIDTH - LEFT_PANEL_WIDTH - RIGHT_PANEL_WIDTH

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

# --- Función para crear/recrear superficies ---
def create_canvas_surfaces(show_algorithm_panel):
    # Calcular altura del canvas según si se muestra el panel de algoritmos
    canvas_height = SCREEN_HEIGHT - (ALGORITHM_PANEL_HEIGHT if show_algorithm_panel else 0)
    
    # Crear superficies con la altura adecuada
    canvas_surf = pygame.Surface((CANVAS_WIDTH, canvas_height))
    canvas_surf.fill(WHITE) # Lienzo blanco inicial
    
    preview_surf = pygame.Surface((CANVAS_WIDTH, canvas_height), pygame.SRCALPHA) # SRCALPHA para transparencia
    
    return canvas_surf, preview_surf, canvas_height

# --- Crear instancias de los paneles de UI ---
# Asumiendo que ui.py define ToolPanel y ColorPanel
tool_panel = ui.ToolPanel(0, 0, LEFT_PANEL_WIDTH, SCREEN_HEIGHT, LIGHT_GRAY)
color_panel = ui.ColorPanel(SCREEN_WIDTH - RIGHT_PANEL_WIDTH, 0, RIGHT_PANEL_WIDTH, SCREEN_HEIGHT, LIGHT_GRAY)
# Paneles para algoritmos
algorithm_line_panel = ui.AlgorithmPanel(LEFT_PANEL_WIDTH, 0, CANVAS_WIDTH, ALGORITHM_PANEL_HEIGHT, LIGHT_GRAY)
algorithm_circle_panel = ui.AlgorithmCirclePanel(LEFT_PANEL_WIDTH, 0, CANVAS_WIDTH, ALGORITHM_PANEL_HEIGHT, LIGHT_GRAY)
# Panel para seleccionar lados del polígono
polygon_sides_panel = ui.PolygonSidesPanel(LEFT_PANEL_WIDTH, 0, CANVAS_WIDTH, ALGORITHM_PANEL_HEIGHT, LIGHT_GRAY)

# --- Estado de la aplicación ---
selected_tool = None
selected_color = BLACK # Color inicial por defecto
selected_line_algorithm = 'pygame' # Algoritmo inicial por defecto para líneas
selected_circle_algorithm = 'pygame' # Algoritmo inicial por defecto para círculos
selected_polygon_sides = 5 # Número de lados por defecto para polígonos
drawing = False
start_pos = None
current_mouse_pos = None # Posición actual relativa al canvas
show_algorithm_panel = False # Inicialmente oculto
current_algorithm_panel = None # Panel de algoritmos actualmente visible
# Para marcar puntos en figuras multi-punto
points = [] 
point_radius = 5 # Radio de los puntos de referencia

# Lista para almacenar las figuras dibujadas permanentemente
drawn_shapes = []

# --- Superficies iniciales ---
canvas_surface, preview_surface, CANVAS_HEIGHT = create_canvas_surfaces(show_algorithm_panel)

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
    
    # Ajustar la detección según si el panel de algoritmos está visible
    panel_height_offset = ALGORITHM_PANEL_HEIGHT if show_algorithm_panel else 0
    
    if LEFT_PANEL_WIDTH <= mouse_pos_screen[0] < SCREEN_WIDTH - RIGHT_PANEL_WIDTH and \
       panel_height_offset <= mouse_pos_screen[1] < SCREEN_HEIGHT:
        is_mouse_on_canvas = True
        current_mouse_pos = (mouse_pos_screen[0] - LEFT_PANEL_WIDTH, mouse_pos_screen[1] - panel_height_offset)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Pasar eventos a los paneles para manejar clics en botones
        tool_action = tool_panel.handle_event(event)
        if tool_action:
            if tool_action == 'clear':
                drawn_shapes = [] # Limpiar lista de figuras
                points = []
                # No es necesario limpiar canvas_surface aquí, se redibuja abajo
            else:
                selected_tool = tool_action
                points = [] # Resetear puntos al cambiar de herramienta
                drawing = False # Cancelar cualquier dibujo en progreso
                start_pos = None
                
                # Determinar qué panel de algoritmos mostrar según la herramienta
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
                
                # Recrear superficies si cambió la visibilidad
                if new_show_algorithm_panel != show_algorithm_panel or current_algorithm_panel != new_algorithm_panel:
                    show_algorithm_panel = new_show_algorithm_panel
                    current_algorithm_panel = new_algorithm_panel
                    canvas_surface, preview_surface, CANVAS_HEIGHT = create_canvas_surfaces(show_algorithm_panel)
                
                print(f"Herramienta seleccionada: {selected_tool}") # Para depuración

        color_action = color_panel.handle_event(event)
        if color_action:
            selected_color = color_action
            print(f"Color seleccionado: {selected_color}") # Para depuración
            
        # Manejar eventos de los paneles de algoritmos
        if show_algorithm_panel:
            if current_algorithm_panel == 'line':
                algorithm_action = algorithm_line_panel.handle_event(event)
                if algorithm_action:
                    selected_line_algorithm = algorithm_action
                    print(f"Algoritmo de línea seleccionado: {selected_line_algorithm}")
            elif current_algorithm_panel == 'circle':
                algorithm_action = algorithm_circle_panel.handle_event(event)
                if algorithm_action:
                    selected_circle_algorithm = algorithm_action
                    print(f"Algoritmo de círculo seleccionado: {selected_circle_algorithm}")
            elif current_algorithm_panel == 'polygon':
                sides_action = polygon_sides_panel.handle_event(event)
                if sides_action:
                    selected_polygon_sides = sides_action
                    print(f"Número de lados del polígono seleccionado: {selected_polygon_sides}")

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
                        # --- Lógica para completar figuras multi-puntos ---
                        if selected_tool == 'triangle' and len(points) == 3:
                            new_shape = fig.Triangle(points, selected_color, width=2)
                            drawn_shapes.append(new_shape)
                            points = [] # Resetear para el siguiente triángulo
                        elif selected_tool == 'curve' and len(points) == 4:
                            new_shape = fig.BezierCurve(points, selected_color, width=2)
                            drawn_shapes.append(new_shape)
                            points = [] # Resetear para la siguiente curva
                        elif selected_tool == 'polygon' and len(points) == selected_polygon_sides:
                            new_shape = fig.Polygon(points, selected_color, width=2)
                            drawn_shapes.append(new_shape)
                            points = [] # Resetear para el siguiente polígono

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # Botón izquierdo
                    if drawing and selected_tool and start_pos:
                        end_pos = canvas_pos
                        new_shape = None
                        # Crear la instancia de la figura apropiada
                        if selected_tool == 'line':
                            new_shape = fig.Line(start_pos, end_pos, selected_color, width=2, algorithm=selected_line_algorithm)
                        elif selected_tool == 'rectangle':
                            new_shape = fig.Rectangle.from_points(start_pos, end_pos, selected_color, width=2)
                        elif selected_tool == 'circle':
                            new_shape = fig.Circle.from_points(start_pos, end_pos, selected_color, width=2, algorithm=selected_circle_algorithm)
                        elif selected_tool == 'ellipse':
                             new_shape = fig.Ellipse.from_points(start_pos, end_pos, selected_color, width=2)

                        if new_shape:
                            drawn_shapes.append(new_shape)

                    # Resetear estado de dibujo
                    drawing = False
                    start_pos = None
                    # NO reseteamos `points` aquí para multi-puntos

            # No necesitamos MOUSEMOTION aquí si usamos la preview

    # --- Lógica de Previsualización (si estamos dibujando) ---
    if drawing and selected_tool and start_pos and current_mouse_pos:
        preview_color = selected_color # Usar color normal para preview ahora que es temporal
        temp_shape = None

        if selected_tool == 'line':
            temp_shape = fig.Line(start_pos, current_mouse_pos, preview_color, width=2, algorithm=selected_line_algorithm)
        elif selected_tool == 'rectangle':
            temp_shape = fig.Rectangle.from_points(start_pos, current_mouse_pos, preview_color, width=2)
        elif selected_tool == 'circle':
            temp_shape = fig.Circle.from_points(start_pos, current_mouse_pos, preview_color, width=2, algorithm=selected_circle_algorithm)
        elif selected_tool == 'ellipse':
             temp_shape = fig.Ellipse.from_points(start_pos, current_mouse_pos, preview_color, width=2)

        if temp_shape:
            temp_shape.draw(preview_surface) # Dibujar en la superficie de preview
    
    # --- Dibujar puntos de referencia para figuras multi-punto ---
    # Mostrar los puntos acumulados para triángulo, polígono o curva Bézier
    if selected_tool in ['triangle', 'curve', 'polygon'] and len(points) > 0:
        # Dibujar puntos acumulados
        for point in points:
            # Dibujar un círculo en cada punto con color semitransparente
            temp_surface = pygame.Surface((point_radius*2+1, point_radius*2+1), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface, (*selected_color, 200), (point_radius, point_radius), point_radius)
            preview_surface.blit(temp_surface, (point[0]-point_radius, point[1]-point_radius))
            
            # Añadir un pequeño número para indicar el orden
            font = pygame.font.SysFont(None, 20)
            text = font.render(str(points.index(point)+1), True, WHITE)
            text_rect = text.get_rect(center=point)
            preview_surface.blit(text, text_rect)
            
        # Para curva Bézier, mostrar líneas guía entre puntos si hay al menos 2
        if selected_tool == 'curve' and len(points) >= 2:
            # Dibujar líneas guía con color más claro y semitransparente
            guide_color = (min(selected_color[0] + 100, 255), 
                          min(selected_color[1] + 100, 255), 
                          min(selected_color[2] + 100, 255), 150)
            
            # Conectar los puntos con líneas guía
            if len(points) >= 2:
                for i in range(len(points)-1):
                    pygame.draw.line(preview_surface, guide_color, points[i], points[i+1], 1)
            
        # Para triángulo, mostrar perímetro parcial o completo
        if selected_tool == 'triangle':
            if len(points) >= 2:
                # Dibujar líneas entre los puntos existentes
                for i in range(len(points)-1):
                    pygame.draw.line(preview_surface, selected_color, points[i], points[i+1], 2)
                
                # Conectar el último punto con el primero si hay 3 puntos
                if len(points) == 3:
                    pygame.draw.line(preview_surface, selected_color, points[2], points[0], 2)
        
        # Para polígono, mostrar perímetro parcial o completo
        if selected_tool == 'polygon':
            if len(points) >= 2:
                # Dibujar líneas entre los puntos existentes
                for i in range(len(points)-1):
                    pygame.draw.line(preview_surface, selected_color, points[i], points[i+1], 2)
                
                # Si ya tenemos todos los puntos, o al menos 3, cerramos el polígono
                if len(points) == selected_polygon_sides or (len(points) >= 3 and len(points) < selected_polygon_sides):
                    pygame.draw.line(preview_surface, selected_color, points[-1], points[0], 2)
                
                # Mostrar el contador actual de puntos y el objetivo
                count_text = f"Punto {len(points)} de {selected_polygon_sides}"
                count_font = pygame.font.SysFont(None, 18)
                count_surf = count_font.render(count_text, True, BLACK)
                # Ubicar en la esquina superior derecha de la pantalla
                count_rect = count_surf.get_rect(topright=(CANVAS_WIDTH - 10, 10))
                preview_surface.blit(count_surf, count_rect)

    # --- Lógica de dibujo ----
    # 1. Limpiar canvas permanente (siempre se redibuja todo)
    canvas_surface.fill(WHITE)

    # 2. Dibujar todas las figuras permanentes guardadas
    for shape in drawn_shapes:
        shape.draw(canvas_surface)

    # 3. Dibujar el canvas actualizado en la pantalla
    panel_height_offset = ALGORITHM_PANEL_HEIGHT if show_algorithm_panel else 0
    screen.blit(canvas_surface, (LEFT_PANEL_WIDTH, panel_height_offset))

    # 4. Dibujar la previsualización sobre el canvas
    screen.blit(preview_surface, (LEFT_PANEL_WIDTH, panel_height_offset))

    # 5. Dibujar los paneles de UI encima de todo
    tool_panel.draw(screen)
    color_panel.draw(screen)
    
    # Solo dibujar el panel de algoritmos correspondiente si está visible
    if show_algorithm_panel:
        if current_algorithm_panel == 'line':
            algorithm_line_panel.draw(screen)
        elif current_algorithm_panel == 'circle':
            algorithm_circle_panel.draw(screen)
        elif current_algorithm_panel == 'polygon':
            polygon_sides_panel.draw(screen)

    # --- Actualizar la pantalla ---
    pygame.display.flip()

# --- Salir de Pygame ---
pygame.quit()
sys.exit()
