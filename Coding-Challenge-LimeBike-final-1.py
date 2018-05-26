import bisect
import unittest


class ItemCounter:
    """Counter to process rides and print the items in transit at each unique time interval."""
    def __init__(self):
        self.ride_cnt = 0;
        self.start_time = []
        self.end_time = []
        self.orig_item = {}
        self.intervals = []
        self.item_counter = {}

    def process_ride(self, ride):
        """Processes a ride object and updates the item time intervals."""
        if not ride.items:
            return
        self._add_time(ride.start_time)
        self._add_time(ride.end_time)
        self.start_time.append(ride.start_time)
        self.end_time.append(ride.end_time)
        self.orig_item[self.ride_cnt] = ride.items
        self.ride_cnt = self.ride_cnt+1
    
    def _add_time(self, new_time):
        # Helper function to add time interval into sorted list
        time_index = bisect.bisect(self.intervals, new_time)
        if (time_index > 0):
            if (self.intervals[time_index - 1] != new_time):
                self.intervals.insert(time_index, new_time)
        else:
            self.intervals.insert(time_index, new_time)

    def _add_items(self, old_items, items):
        # Helper function to add two item dictionaries
        new_items = {}
        for key in old_items:
            if key in items:
                new_items[key] = old_items[key] + items[key]
            else:
                new_items[key] = old_items[key]
        for key in items:
            if key not in old_items:
                new_items[key] = items[key]
        return new_items

    def print_items_per_interval(self):
        # Generates items per interval based on the sorted intervals 
        # by adding the new items to the time interval before it
        # Then prints the report items per time interval
        for i in range(0, len(self.intervals) - 1):
            self.item_counter[i] = {}
            for j in range(0, self.ride_cnt):
                if (self.intervals[i] >= self.start_time[j] and self.intervals[i] < self.end_time[j]):
                    self.item_counter[i] = self._add_items(self.orig_item[j], self.item_counter[i])
        
        print 'Items per Interval Report:\n' 
        for i in range(0, len(self.intervals)-1):
            if self.item_counter[i]:
                print self.intervals[i] + ' - ' + self.intervals[i+1] + ' -> '
            for key in self.item_counter[i]:
                print('             %s = %s' % (key, self.item_counter[i][key]))


