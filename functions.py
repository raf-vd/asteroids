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

