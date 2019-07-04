CANVAS_W = 600  # canvas size, in pixels
CANVAS_H = 600
T_STEP = 50  # ms per timestep
MAX_STEPS = 1000/T_STEP*30  # at most 30 seconds
GRAVITY = 1/4  # acceleration due to gravity, per timestep
RATIONALIZER = 4  # multiplying everything by this value gives integers
MAX_SPEED_X = 4  # speed cap, inclusive
MAX_SPEED_Y = 3
CHAR_H = 38  # size of the character rectangle
CHAR_W = 30

INITIAL_LOCATION = -200, 200  # center of bottom edge
INITIAL_PLATFORM = (-400, 200, 0, 205), 0  # just for convenience, Derrick will always start on this platform

# Whether the two rectangles overlap. Both parameters assumed to be in the form x0, y0, x1, y1.
def boxes_intersect(box1, box2):
    return (box1[0] <= box2[2] and box2[0] <= box1[2] and
            box1[1] <= box2[3] and box2[1] <= box1[3])

def point_distance(s, t):
    return t[0] - s[0], t[1] - s[1]

def point_sum(s, t):
    return s[0] + t[0], s[1] + t[1]

def get_character_box(point):
    x, y = point
    return x - CHAR_W/2, y - CHAR_H, x + CHAR_W/2, y

def get_bottom_of_box(box):
    return box[0], box[3], box[2], box[3]

def clamp_speed(speed):
    return min(MAX_SPEED_X, max(-MAX_SPEED_X, speed[0])), min(MAX_SPEED_Y, max(-MAX_SPEED_Y, speed[1]))