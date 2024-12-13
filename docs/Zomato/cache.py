import heapq 

# Cache operations allowed:

# query(key)               : queries a given key and returns (1, val) or [0]
# insert(key, value)       : inserts given key value pair into cache


class Cache:

    # Timestamp notes the moment when a particular key is queried
    # Timestamp is also used when adding a key to the cache
    # Hence Timestamp is incremented in both query function and add_to_cache functions
    # This prevents two keys from having same timestamps, even if they are added subsequently

    timestamp = 0


    def __init__(self, SIZE):
        self.SIZE = SIZE
        self.minheap = []       # stores : (timestamp, key) 
        self.cache = {}         # stores key: (value)
        self.length = 0 

    def update_timestamp(self):
        pass 
    
    def query(self, key):
        return_value = None

        if key in self.cache:
            value = self.cache[key]
            self.update_timestamp()
            # self.cache[key][1] = Cache.timestamp
            return_value = (1, value) 
        
        else:
            return_value = [0]

        Cache.timestamp += 1
        return return_value
    
    def remove_from_cache(self, key):
        del self.cache[key]
        self.length -= 1
        
    def drop_from_cache(self):

        lru_key = None 
        minimum_timestamp = float('inf')  # initializes to a maximum value

        for key in self.cache:
            timestamp = self.cache[key][1]

            if timestamp < minimum_timestamp:
                minimum_timestamp = timestamp
                lru_key = key 

        
        self.remove_from_cache(lru_key)

    def add_to_cache(self, key, value):
        self.cache[key] = [value, Cache.timestamp]
        self.length += 1
        Cache.timestamp += 1
        
        
    
    def insert(self, key, value):

        if self.length == self.SIZE:
            self.drop_from_cache()

        self.add_to_cache(key, value)
        
        



