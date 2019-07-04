from collections import defaultdict
import copy
import pickle
from globals import *  # the autograder will use the original version of this file

# Suggested functions:
def create_configuration(config, action,platforms):
    location, speed, visited = config 
    new_speed = list(speed)
    displacement = list(speed)
    visited = list(visited)
    on_ground = False
    char_box = (get_character_box(location))
    char_bottom = (get_bottom_of_box(char_box))
    for platform in platforms:
        platform_box, score = platform
        if boxes_intersect(platform_box, char_bottom):
            on_ground = True
            new_speed[1] = 0
            displacement[1] = platform_box[1] - location[1]
            if platform not in visited:
                visited.append(platform)              
        elif boxes_intersect(platform_box, char_box):
            new_speed[0] = 0
            new_speed[1] = 0
            return None
    if on_ground:
        if action == 'left':
            displacement[0] -= 1
            new_speed[0] -= 1
        elif action == 'right':
            displacement[0] += 1
            new_speed[0] += 1
        elif action == 'up':           
            displacement[1] = -3
            new_speed[1] = -3
    else:
        new_speed[1] += GRAVITY
    new_speed = clamp_speed(new_speed)
    location = list(location)
    location[0] += displacement[0]
    location[1] += displacement[1]
    new_config = (tuple(location), tuple(new_speed), tuple(visited))
    return new_config

def compute_score(config):
    if config == None:
        return 0
    visited = config[2]
    total_score = 0
    for platform in visited:
        total_score+=platform[1]
    return total_score

# This is the function called in tests.py and the autograder.
def calculate_best_score(platforms):
    platforms.append((INITIAL_PLATFORM))
    location = (INITIAL_LOCATION)
    cap_score = 0
    for platform in platforms:
        cap_score+=platform[1]
    if cap_score == 0:
        return 0
    actions = ['left','right','up','none']
    memo = {}
    visited = ()
    speed = (0,0)
    start_config = (location, speed,visited)
    depth = 0
    max_score = 0
    queue = set()
    queue.add(start_config)
    while depth < 600 and queue:
        next_queue = set()
        for config in queue:
            dp = {config:compute_score(config)}
            memo.update(dp)
            if memo[config]>max_score:
                max_score = memo[config]
                if max_score ==cap_score:
                    return cap_score
            for action in actions:
                next_config = create_configuration(config,action,platforms)
                if next_config and  next_config not in memo and  next_config not in next_queue:
                    next_queue.add(next_config)
        depth += 1
        queue = next_queue
    return max_score

