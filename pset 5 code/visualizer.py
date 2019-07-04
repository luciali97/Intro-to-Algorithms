import tkinter as tk
import time
import pickle
import copy
from globals import *

class Visualizer(object):
    def __init__(self, platforms=[], actions=None):
        self.actions = actions  # list of actions to play back
        self.t = 0

        self.character_speed = 0, 0
        self.platforms = [INITIAL_PLATFORM]
        self.platforms.extend(sorted(platforms, key = lambda p: p[0]))

        self.root = tk.Tk()
        self.root.title("Platforms")
        self.root.bind('<Left>', self.handle_left)
        self.root.bind('<Right>', self.handle_right)
        self.root.bind('<Up>', self.handle_up)

        self.reset_button = tk.Button(self.root, text = 'Reset', command = self.reset)
        self.reset_button.pack()

        self.text_output = tk.Text(master=self.root, height=1, width=40)
        self.text_output.pack()

        self.score_display = tk.Text(master=self.root, height=1, width=20)
        self.score_display.pack()
        self.score = 0
        self.scored = set()

        self.canvas = tk.Canvas(self.root, width=CANVAS_W, height=CANVAS_H)
        self.canvas.focus_set()
        self.canvas.configure(xscrollincrement='1')  # 1 pixel
        self.canvas.xview_scroll(INITIAL_LOCATION[0], "units")

        self.character = self.canvas.create_rectangle(*get_character_box(INITIAL_LOCATION), outline='white', fill='blue')
        self.character_photo = tk.PhotoImage(file='frog.gif')
        self.character_image = self.canvas.create_image((INITIAL_LOCATION[0], INITIAL_LOCATION[1]-CHAR_H/2), image=self.character_photo)

        self.platform_rectangles = []
        for platform in self.platforms:
            (x0, y0, x1, y1), score = platform
            # Save the reference to be able to change outline color later.
            self.platform_rectangles.append(self.canvas.create_rectangle(x0, y0, x1, y1, outline='red', fill='black'))

        self.on_ground = True
        self.last_keypress = None
        self.canvas.pack()
        self.canvas.after(0, self.animation)
        self.root.mainloop()

    # Returns the coordinates of the midpoint of the base of the character box.
    def get_character_location(self):
        character_box = self.canvas.coords(self.character)
        return (character_box[0] + character_box[2])/2, character_box[3]

    # Move both the image and the rectangle.
    def move_character(self, displacement):
        self.canvas.move(self.character, *displacement)
        self.canvas.move(self.character_image, *displacement)

    # Basically reset all the parts of the GUI that may have changed.
    def reset(self):
        current_location = self.get_character_location()
        self.character_speed = 0, 0

        displacement = point_distance(current_location, INITIAL_LOCATION)
        self.move_character(displacement)
        self.canvas.itemconfig(self.character, fill='blue')
        self.canvas.xview_scroll(int(INITIAL_LOCATION[0] - self.canvas.canvasx(0)), "units")
        for platform in self.platform_rectangles:
            self.canvas.itemconfig(platform, outline='red')
        self.t = 0
        self.canvas.update()

    # Only handle keypresses once per timestep.
    def handle_left(self, event):
        self.last_keypress = 'left'

    def handle_right(self, event):
        self.last_keypress = 'right'

    def handle_up(self, event):
        self.last_keypress = 'up'

    def animation(self):
        if self.actions and self.t < len(self.actions):
            # Ignore user input and replay the given list of actions, if one is provided and we haven't already played it.
            self.last_keypress = self.actions[self.t]
            display_text = 'Replaying action ' + str(self.t) + '/' + str(len(self.actions)) + ': ' + str(self.last_keypress) + '.'
            self.t+=1
        else:
            # Otherwise, use the user's most recent key press.
            display_text = 'User input: ' + str(self.last_keypress) + '.'
        self.text_output.delete(1.0, tk.END)
        self.text_output.insert(tk.END, display_text)

        # Query the canvas to get the bounding box of Derrick.
        character_box = list(self.canvas.coords(self.character))
        # We (arbitrarily) keep track of the midpoint of Derrick's bottom edge. 
        character_location = self.get_character_location()
        new_speed = list(self.character_speed)
        displacement = list(self.character_speed)
        snap_to_platform = False

        # Derrick is assumed to be in the air
        self.on_ground = False
        for i, platform in enumerate(self.platform_rectangles):
            platform_box = self.canvas.coords(platform)
            if boxes_intersect(platform_box, get_bottom_of_box(character_box)):
                # ... unless we find a platform with which his bottom edge intersects.
                self.on_ground = True
                snap_to_platform = True
                # If this is the case, we snap to the platform: set our y-velocity to zero and our y-position to be exactly on the upper edge.
                new_speed[1] = 0
                displacement[1] = platform_box[1] - character_location[1] 
                self.canvas.itemconfig(platform, outline='green')
                # Increase our score if we haven't yet visited this platform.
                if i not in self.scored:
                    self.score += self.platforms[i][1]
                    self.scored.add(i)
                    self.score_display.delete(1.0, tk.END)
                    self.score_display.insert(tk.END, 'Score:' + str(self.score))
            elif boxes_intersect(platform_box, character_box):
                # Otherwise, check to see if we're colliding with some other part of the character; fatal.
                self.character_speed = 0, 0
                self.canvas.itemconfig(self.character, fill='red')
                self.canvas.after(T_STEP, self.animation)
                return

        if self.on_ground:
            # Pressing left or right causes the character to accelerate.
            if self.last_keypress == 'left':
                displacement[0] -= 1
                new_speed[0] -= 1
            elif self.last_keypress == 'right':
                displacement[0] += 1
                new_speed[0] += 1
            # Pressing up causes the character to jump. Jumps always have a fixed height.
            elif self.last_keypress == 'up':
                displacement[1] = -3
                new_speed[1] = -3
        else:
            # Otherwise, the sole force acting on Derrick is gravity.
            new_speed[1] += GRAVITY

        self.move_character(displacement)  # not clamped!
        self.character_speed = clamp_speed(new_speed)

        # Move the camera as necessary.
        character_location = self.get_character_location()
        out_of_region_left = (self.canvas.canvasx(0) + CANVAS_W/5) - character_location[0]
        if out_of_region_left > 0 and self.character_speed[0] < 0:
            self.canvas.xview_scroll(int(self.character_speed[0]), "units")
        out_of_region_right = character_location[0] - (self.canvas.canvasx(0) + CANVAS_W - CANVAS_W/5)
        if out_of_region_right > 0 and self.character_speed[0] > 0:
            self.canvas.xview_scroll(int(self.character_speed[0]), "units")

        self.last_keypress = None
        self.canvas.after(T_STEP, self.animation)

if __name__ == "__main__":
    print("Running an example...")
    platforms = [((10, 240, 60, 250), 25), ((80, 200, 150, 210), 9), ((170, 180, 210, 190), 5), ((280, 160, 360, 170), 1), ((400, 190, 450, 200), 12)]

    LOAD_ACTIONS = False
    if LOAD_ACTIONS:
        with open('actions', 'rb') as IN:
            actions = pickle.load(IN)
    else:
        actions = None
    v = Visualizer(platforms=platforms, actions=actions)
