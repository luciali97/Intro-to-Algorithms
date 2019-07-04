from __future__ import division
import math
import random
import unittest
import cProfile
from peak_finding import AdversarialGame

# You can run these tests to check if your code is reasonable.
# These are NOT the same tests the autograder is going to use!

"""
    Implementation of the O(\log n) divide-and-conquer peak-finding algorithm.
"""
class PeakFinder(object):
    def __init__(self, n, query_method):
        self.n = n
        self.query_method = query_method

        self.board_state = [None]*n
        self.window_left = 0
        self.window_right = n

        self.query_count = 0

    """
        Repeatedly makes queries until it finds the index of a peak. Returns the number of queries made.
        Uses binary search: at each step, halve the window in which the peak could be found.
    """
    def find_peak(self):
        while self.query_count <= self.n:
            center = (self.window_left + self.window_right)//2

            # If the center of the window is a peak, we are done.
            if self.is_peak(center):
                return self.query_count

            # Otherwise, continue to examine the left or right half of the window.
            if self.window_left < center and self.query(center - 1) > self.query(center):
                self.window_right = center
                continue
            if self.window_right > center + 1 and self.query(center + 1) > self.query(center):
                self.window_left = center + 1
                continue

    def query(self, index):
        # Only make a call to query_method if the value is not already known.
        if self.board_state[index]:
            return self.board_state[index]

        value = self.query_method(index)
        self.query_count += 1

        self.board_state[index] = value
        return value

    def valid_index(self, index):
        return 0 <= index < self.n

    def neighbors(self, index):
        candidate_neighbors = [index - 1, index, index + 1]

        # Note: index is included in the returned list.
        return list(filter(lambda i: self.valid_index(i), candidate_neighbors))

    def is_peak(self, index):
        value = self.query(index)
        return all(self.query(neighbor) <= value for neighbor in self.neighbors(index))

class TestAdversarialGame(unittest.TestCase):
    # Test for part (a)
    def test_consistency(self):
        n = 1234
        adversary = AdversarialGame(n)  # Your adversary (via import).
        indices_to_check = list(range(n))
        values = {}  # Store the results of queries.

        for _ in range(20):
            random.shuffle(indices_to_check)
            for i in indices_to_check:
                value = adversary.query(i)
                self.assertTrue(value > 0, "Consistency test failed: query returned non-positive value.")
                if i in values:
                    self.assertEqual(values[i], value, "Consistency test failed: values not consistent.")
                else:
                    values[i] = value

    # Helper subroutine.
    def run_against_player(self, n):
        adversary = AdversarialGame(n)
        player = PeakFinder(n, adversary.query)
        queries = player.find_peak()
        self.assertTrue(queries >= math.log(n, 2) - 1, "Lower bound test: failed.")

    # Tests for part (b)
    def test_logn_queries(self):
        self.run_against_player(1234567)

    def test_logn_queries_long(self):
        print("This might take a few seconds...")
        for n in range(1, 12345):
            self.run_against_player(n)

cProfile.run('unittest.main()',sort = 'tottime')
##if __name__ == '__main__':
##    unittest.main()

