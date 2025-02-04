import pygame, random, sys

def point_to_line_distance(point, line_start, line_end):
    """Calculate shortest distance from a point to a line segment (THX BOOTS)"""
    line_vec = line_end - line_start    # Vector from line start to end
    point_vec = point - line_start      # Vector from line start to point
    line_length = line_vec.length()     # Length of line
    
    if line_length == 0:
        return point_vec.length()
        
    # Project point_vec onto line_vec to find closest point
    t = max(0, min(1, point_vec.dot(line_vec) / (line_length * line_length)))
    # Closest point on line segment
    projection = line_start + line_vec * t
    # Distance from point to closest point
    return (point - projection).length()

def point_in_triangle(point, triangle_points):
    """Returns True if point is inside the triangle"""
    a, b, c = triangle_points
    # Check if point is on same side of all three lines
    def sign(p1, p2, p3):
        return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)
    
    d1 = sign(point, a, b)
    d2 = sign(point, b, c)
    d3 = sign(point, c, a)
    
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    
    return not (has_neg and has_pos)

def exit_msg():
    print("Asteroids ended!")                           # Th-Th-That's it folks!
    sys.exit()

def rect_surface(bar_w, bar_h, colour):
    bar_surface = pygame.Surface((bar_w, bar_h), pygame.SRCALPHA)  
    bar_surface.fill(colour)  
    return bar_surface

def render_line(font, text, bar_surface, colour, vertical_offset=0):
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect(center=(bar_surface.get_width() / 2, vertical_offset))
    bar_surface.blit(text_surface, text_rect)

def biased_random():
    r = random.random()     # Raw random from 0 to 1
    return r * r            # Square or cube it to bias towards 0

def scale_to_circle(image, circle_radius):
    # Calculate the new size (maintain aspect ratio)
    original_size = image.get_size()
    scale = (circle_radius * 2) / max(original_size)
    new_width = int(original_size[0] * scale)
    new_height = int(original_size[1] * scale)
    
    # Scale the image
    scaled_image = pygame.transform.smoothscale(image, (new_width, new_height))
    return scaled_image

def apply_tint(image, tint_color):
    tinted = image.copy()
    tinted.fill(tint_color, special_flags=pygame.BLEND_RGBA_MULT)
    return tinted

def create_circle_mask(radius): # Create a circle
    surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(surf, (255, 255, 255), (radius, radius), radius)
    return pygame.mask.from_surface(surf)
