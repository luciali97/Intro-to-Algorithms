import unittest
import random
from study import inefficient_allocate_time, allocate_time

class TestAllocation(unittest.TestCase):
    def _test_random_classes(self, n, upper_bound):
        T = n*upper_bound/4
        classes1 = []
        for _ in range(n):
            classes1.append((random.randint(1, upper_bound), random.randint(1, upper_bound)))
        classes2 = list(classes1)  # Copy in case one method modifies.
        benefit1 = inefficient_allocate_time(classes1, T)
        benefit2 = allocate_time(classes2, T)
        self.assertEqual(benefit1, benefit2)

    def test_random_classes_large(self):
        print("Large test...")
        # Will take a very long time with the provided implementation.
        # As you improve your algorithm, you'll want to modify these tests.
        self._test_random_classes(10**3, 500)

    def test_random_classes_small(self):
        print("Small test...")
        self._test_random_classes(10**2, 100)        

if __name__ == '__main__':
    print("Running some cursory tests...")
    unittest.main()
