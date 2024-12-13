# Cache operations allowed:

# query(key)               : queries a given key and returns (1, val) or [0]
# insert(key, value)       : inserts given key value pair into cache

class Q2_cache:
    
    # Timestamp notes the moment when a particular key is queried
    # Timestamp is also used when adding a key to the cache
    # Hence Timestamp is incremented in both query function and add_to_cache functions
    # This prevents two keys from having same timestamps, even if they are added subsequently
    
    timestamp = 0

    def __init__(self, SIZE):
        self.SIZE1 = SIZE
        self.SIZE2 = SIZE 
        self.cache_once = {}        # stores keys that occured once
        self.cache_many = {}        # stores keys that occured more than once
        self.length_cache_once = 0
        self.length_cache_many = 0

    def add_to_cache_once(self, key, value):        # add given value to cache
        self.cache_once[key] = [value, Q2_cache.timestamp]
        self.length_cache_once += 1
        Q2_cache.timestamp += 1

    def add_to_cache_many(self, key, value):
        self.cache_many[key] = [value, Q2_cache.timestamp]
        self.length_cache_many += 1
        Q2_cache.timestamp += 1

    def remove_from_cache_once(self, key):          # removes given value from cache
        del self.cache_once[key]
        self.length_cache_once -= 1

    def remove_from_cache_many(self, key):
        del self.cache_many[key]
        self.length_cache_many -= 1

    def drop_from_cache(self, cache, choice):                 # finds out the least recently used key and calls the remove function
        lru_key = None 
        minimum_timestamp = float('inf')    #initialize to maximum

        for key in cache:
            occurance = cache[key][1]

            if occurance < minimum_timestamp:
                minimum_timestamp = occurance 
                lru_key = key 
        
        if choice == 1: self.remove_from_cache_once(lru_key)
        elif choice == 2: self.remove_from_cache_many(lru_key)

    def query(self, key):

        if key in self.cache_many:

            value = self.cache_many[key][0]
            return_value = [1, value]
            self.cache_many[key][1] = Q2_cache.timestamp
        
        elif key in self.cache_once:
            
            value = self.cache_once[key][0]
            return_value = [1, value]
            
            if self.length_cache_many == self.SIZE2:
                self.drop_from_cache(self.cache_many, 2)
            
            self.add_to_cache_many(key, value)
            self.remove_from_cache_once(key)

        else:

            return_value = [0]

        return return_value
    

    def insert(self, key, value):

        if self.length_cache_once == self.SIZE1:
            self.drop_from_cache(self.cache_once, 1)

        self.add_to_cache_once(key, value)


    
