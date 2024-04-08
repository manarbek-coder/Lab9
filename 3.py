import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    radius = 15
    x = 0
    y = 0
    mode = 'blue'
    points = []
    drawing_shape = None
    color = (255, 255, 255)  # Default color is white (eraser)

    while True:

        pressed = pygame.key.get_pressed()

        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'
                elif event.key == pygame.K_e:
                    mode = 'eraser'
                elif event.key == pygame.K_1:
                    drawing_shape = 'rectangle'
                elif event.key == pygame.K_2:
                    drawing_shape = 'circle'
                elif event.key == pygame.K_3:
                    drawing_shape = 'square'  # New: Draw square
                elif event.key == pygame.K_4:
                    drawing_shape = 'right_triangle'  # New: Draw right triangle
                elif event.key == pygame.K_5:
                    drawing_shape = 'equilateral_triangle'  # New: Draw equilateral triangle
                elif event.key == pygame.K_6:
                    drawing_shape = 'rhombus'  # New: Draw rhombus

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click grows radius or starts drawing shape
                    if drawing_shape is None:
                        radius = min(200, radius + 1)
                    else:
                        start_pos = event.pos
                        if drawing_shape in ['rectangle', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus']:
                            points.append(start_pos)
                        elif drawing_shape == 'circle':
                            points.append((start_pos, 0))
                elif event.button == 3:  # Right click shrinks radius
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEMOTION:
                if drawing_shape is not None:
                    if drawing_shape in ['rectangle', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus']:
                        points[-1] = event.pos
                    elif drawing_shape == 'circle':
                        points[-1] = (points[-1][0], max(radius, distance(points[-1][0], event.pos)))
                else:
                    # if mouse moved, add point to list
                    position = event.pos
                    points = points + [position]
                    points = points[-256:]

        screen.fill((0, 0, 0))

        # draw all points
        i = 0
        while i < len(points) - 1:
            if drawing_shape == 'rectangle':
                drawRectangle(screen, points[i], points[i + 1], color)
            elif drawing_shape == 'circle':
                drawCircle(screen, points[i][0], points[i][1], points[i + 1], color)
            elif drawing_shape == 'square':  # New: Draw square
                drawSquare(screen, points[i], points[i + 1], color)
            elif drawing_shape == 'right_triangle':  # New: Draw right triangle
                drawRightTriangle(screen, points[i], points[i + 1], color)
            elif drawing_shape == 'equilateral_triangle':  # New: Draw equilateral triangle
                drawEquilateralTriangle(screen, points[i], points[i + 1], color)
            elif drawing_shape == 'rhombus':  # New: Draw rhombus
                drawRhombus(screen, points[i], points[i + 1], color)
            else:
                drawLineBetween(screen, i, points[i], points[i + 1], radius, mode)
            i += 1

        pygame.display.flip()

        clock.tick(60)


def drawLineBetween(screen, index, start, end, width, color_mode):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))

    if color_mode == 'blue':
        color = (c1, c1, c2)
    elif color_mode == 'red':
        color = (c2, c1, c1)
    elif color_mode == 'green':
        color = (c1, c2, c1)
    elif color_mode == 'eraser':
        color = (0, 0, 0)  # Eraser color is black

    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)


def drawRectangle(screen, start, end, color):
    rect = pygame.Rect(start, (end[0] - start[0], end[1] - start[1]))
    pygame.draw.rect(screen, color, rect, 2)  # 2 is the line thickness


def drawCircle(screen, center, radius, color):
    pygame.draw.circle(screen, color, center, radius, 2)  # 2 is the line thickness


def drawSquare(screen, start, end, color):
    rect_width = abs(end[0] - start[0])
    rect_height = abs(end[1] - start[1])
    min_side = min(rect_width, rect_height)
    if end[0] >= start[0]:
        if end[1] >= start[1]:
            end = (start[0] + min_side, start[1] + min_side)
        else:
            end = (start[0] + min_side, start[1] - min_side)
    else:
        if end[1] >= start[1]:
            end = (start[0] - min_side, start[1] + min_side)
        else:
            end = (start[0] - min_side, start[1] - min_side)
    drawRectangle(screen, start, end, color)


def drawRightTriangle(screen, start, end, color):
