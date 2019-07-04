import unittest
from platforms import calculate_best_score

class TestExplore(unittest.TestCase):
    def _test_score(self, platforms, expected):
        self.assertEqual(calculate_best_score(platforms), expected)

    def test_empty(self):
        # Note: the default platform will always be present in the world, but its associated score is 0.
        platforms = []
        self._test_score(platforms, 0)
##
    def test_one_platform_fall(self):
        # Derrick can simply travel right until he falls off the starting platform and onto the single platform.
        platforms = [((-50, 220, 300, 230), 17)]
        self._test_score(platforms, 17)
##
    def test_one_platform_jump(self):
        # Derrick needs to jump to get onto the platform.
        platforms = [((0, 185, 200, 195), 91)]
        self._test_score(platforms, 91)

    def test_three_platforms_fall(self):
        platforms = [((10, 240, 60, 250), 19), ((70, 200, 130, 210), 8), ((140, 430, 210, 440), 3)]
        self._test_score(platforms, 27)

    def test_three_platforms_jump(self):
        platforms = [((10, 240, 60, 250), 19), ((70, 200, 130, 210), 8), ((140, 430, 210, 440), 31)]
        self._test_score(platforms, 39)
##
    def test_five_platforms_all(self):
        # Derrick can't jump high enough to go anywhere from the second platform, so he'll need to visit the others first before coming back.
        platforms = [((10, 240, 60, 250), 25), ((80, 200, 150, 210), 9), ((170, 180, 210, 190), 5), ((280, 160, 360, 170), 1), ((400, 190, 450, 200), 12)]
        self._test_score(platforms, 52)
##
if __name__ == '__main__':
    print("Running some cursory tests...")
    unittest.main()
