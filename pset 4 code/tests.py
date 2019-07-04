import unittest
from labyrinth import Labyrinth, explore_single, explore_multiple

class TestExplore(unittest.TestCase):
##    def test_explore_single_basic(self):
####        
##        rooms = ['A', 'B', 'C', 'D']
##        corridors = [('A', 'B', 0), ('A', 'C', 1), ('B', 'D', 3)]
##        filters = [('A', 0), ('B', 1), ('C', 3)]
##                     
##        start = 'A'
##        goal = 'D'
##        labyrinth = Labyrinth(rooms, corridors, filters, start, goal)
##        self.assertEqual(explore_single(labyrinth), 6)
####        
##        rooms = ['A', 'B', 'C', 'D']
##        corridors = [('A', 'B', 0), ('B', 'D', 2), ('B', 'C', 0), ('C', 'D', 3)]
##        filters = [('A', 0), ('C', 2), ('D', 3), ('D', 1)]
##        start = 'A'
##        goal = 'D'
##        labyrinth = Labyrinth(rooms, corridors, filters, start, goal)
##        self.assertEqual(explore_single(labyrinth), 4)  
##    def test_2(self):
##        # Same as the previous test, except we require filter type 3 to go from B to D.
##        rooms = ['A', 'B', 'C', 'D']
##        corridors = [('A', 'B', 1), ('A', 'B', 0), ('A', 'B', 2), ('B', 'C', 2),('A', 'C', 3), ('B', 'D', 3), ('B', 'D', 0), ('D', 'C', 0) ] 
##        filters = [('A', 0), ('B', 3), ('D', 2)]
##        start = 'A'
##        goal = 'C'
##        labyrinth = Labyrinth(rooms, corridors, filters, start, goal)
##        self.assertEqual(explore_single(labyrinth), 3)
##
##    def test_please(self):
##        rooms = ['A', 'B', 'C']
##        corridors = [('B', 'C', 1), ('A', 'B', 2)]
##        filters = [('B', 1), ('C', 2)]
##        start = 'B'
##        goal = 'A'
##        labyrinth = Labyrinth(rooms, corridors, filters, start, goal)
##        self.assertEqual(explore_single(labyrinth), 3)

    def test_help(self):
        rooms = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        corridors = [
            ('A', 'B', 1),
            ('B', 'C', 1),
            ('C', 'D', 1),
            ('D', 'E', 1),
            ('E', 'F', 1),
            ('F', 'G', 2)
        ]
        filters = [('D', 1), ('C', 2)]
        start = 'D'
        goal = 'G'
        labyrinth = Labyrinth(rooms, corridors, filters, start, goal)
        self.assertEqual(explore_single(labyrinth), 5)

        # There are two edges leading to the goal room, D. However the filter of type 3 cannot be obtained
        # without reaching the goal room itself. So the explorer must first go to C to pick up the filter
        # of type 2. Thus the fastest sequence of actions is: 
        # pick up filter 0, go from A to B, go from B to C, pick up filter 2, go from C to B, go from B to D.
    def test_explore_single_basic_1(self):
        rooms = ['A', 'B', 'C', 'D', 'E', 'F']
        corridors = [('A', 'B', 0), ('B', 'D', 2), ('B', 'C', 0), ('C', 'D', 3), ('C', 'E', 3), ('C', 'E', 1), ('C', 'F', 1)]
        filters = [('A', 0), ('C', 2), ('D', 3), ('E', 1)]
        start = 'A'
        goal = 'F'
        labyrinth = Labyrinth(rooms, corridors, filters, start, goal)
        self.assertEqual(explore_single(labyrinth), 8)

##    def test_explore_single_basic_2(self):
##        rooms = ['A', 'B', 'C']
##        corridors = [
##            ('A', 'B', 0),
##            ('B', 'C', 0),
##        ]
##        filters = [('A', 0)]
##        start = 'A'
##        goal = 'C'
##        labyrinth = Labyrinth(rooms, corridors, filters, start, goal)
##        self.assertEqual(explore_single(labyrinth), 2)
##
##    def test_explore_single_basic_3(self):
##        rooms = ['A', 'B', 'C', 'D', 'E', 'F']
##        corridors = [
##            ('A', 'B', 1),
##            ('B', 'C', 0),
##            ('C', 'D', 0),
##            ('D', 'E', 0),
##            ('E', 'F', 0),
##            ('F', 'A', 0)
##        ]
##        filters = [('A', 0)]
##        start = 'A'
##        goal = 'C'
##        labyrinth = Labyrinth(rooms, corridors, filters, start, goal)
##        self.assertEqual(explore_single(labyrinth), 4)
##    def test_explore_single_unreachable(self):
##        # Same as the previous test, except we require filter type 3 to go from B to D.
##        rooms = ['A', 'B', 'C', 'D']
##        corridors = [('A', 'B', 0), ('B', 'D', 3), ('B', 'C', 0), ('C', 'D', 3)]
##        filters = [('A', 0), ('C', 2), ('D', 3), ('D', 1)]
##        start = 'A'
##        goal = 'D'
##        labyrinth = Labyrinth(rooms, corridors, filters, start, goal)
##        self.assertEqual(explore_single(labyrinth), None)  
######
##    def test_explore_multiple_basic(self):
##        #   L  --  S  --  R
##        #          |
##        #          D
##        #          |
##        #          G
##        rooms = ['S', 'L', 'R', 'D', 'G']
##        corridors = [('D', 'G', 3), ('S', 'L', 0), ('S', 'R', 1), ('S', 'D', 2)]
##        filters = [('S', 0), ('S', 1), ('R', 2), ('L', 3)]
##        start = 'S'
##        goal = 'G'
##        labyrinth = Labyrinth(rooms, corridors, filters, start, goal)
##        # A single explorer needs 6 timesteps to get to the goal.
## #       self.assertEqual(explore_multiple(labyrinth, 20), 1)
##        self.assertEqual(explore_multiple(labyrinth, 6), 1)
##        # Two explorers can make it in 5 timesteps. One explorer goes right, picks up filter 2, goes back and drops it at S.
##        # Meanwhile, the other explorer goes left, picks up filter 3, goes back to S, picks up filter 2,
##        # and finally proceeds to D and G.
## #       self.assertEqual(explore_multiple(labyrinth, 5), 2)
##        # No matter how many explorers you have, it's not possible to reach the goal in 4 or fewer timesteps.
###        self.assertEqual(explore_multiple(labyrinth, 4), None)
####
##    def test_explore_multiple_unreachable(self):
##        # Same as the previous test, except filter type 2 is unreachable.
##        rooms = ['S', 'L', 'R', 'D', 'G']
##        corridors = [('S', 'L', 0), ('S', 'R', 1), ('S', 'D', 2), ('D', 'G', 3)]
##        filters = [('S', 0), ('S', 1), ('D', 2), ('L', 3)]
##        start = 'S'
##        goal = 'G'
##        labyrinth = Labyrinth(rooms, corridors, filters, start, goal)
##        self.assertEqual(explore_multiple(labyrinth, 18), None)

if __name__ == '__main__':
    print("Running some cursory tests...")
    unittest.main()
