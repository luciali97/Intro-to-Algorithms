import unittest
import cProfile
import random
import events

def sorted_time_description(list):
    return sorted(list, key=lambda x: (x.time, x.description))

class TestTimeline(unittest.TestCase):
    def test_add_and_then_query(self):
        T = 12345
        n = 1234
        timeline = events.Timeline()
        slow_timeline = []

        ID = 0
        for _ in range(n):
            t = random.random() * T
            timeline.add_event(events.Event(t, ID))
            slow_timeline.append(events.Event(t, ID))
            ID += 1
        for _ in range(n):
            bounds = sorted([random.random() * T, random.random() * T])
            one = timeline.events_in_range(*bounds)
            # print('one =')
            # for e in one: 
            #     print ('e1.time = ', e.time)
            two = [e for e in slow_timeline if bounds[0] <= e.time <= bounds[1]]
            # print ('two = ')
            # for e in two:
            #     print ('e2.time = ', e.time)
            self.assertEqual(sorted_time_description(one), sorted_time_description(two), "Test 1 failed.")

    def test_add_and_query(self):
        T = 12346
        n = 1234
        timeline = events.Timeline()
        slow_timeline = []

        ID = 0
        for _ in range(n):
            t = random.random() * T
            timeline.add_event(events.Event(t, ID))
            slow_timeline.append(events.Event(t, ID))
            ID += 1
        for _ in range(2*n):
            if random.random() <= 0.5:
                bounds = sorted([random.random() * T, random.random() * T])
                one = timeline.events_in_range(*bounds)
                two = [e for e in slow_timeline if bounds[0] <= e.time <= bounds[1]]
                self.assertEqual(sorted_time_description(one), sorted_time_description(two), "Test 2 failed.")
            else:
                t = random.random() * T
                timeline.add_event(events.Event(t, ID))
                slow_timeline.append(events.Event(t, ID))
                ID += 1

if __name__ == '__main__':
    print("Running some cursory tests...")
    unittest.main()
#cProfile.run('unittest.main()', sort = 'tottime')