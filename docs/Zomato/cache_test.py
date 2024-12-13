from Linked_list_cache import Linked_List_cache

class Tests:

    def test_cache(self):
        cache1 = Linked_List_cache(3)

        test_database = {i: i for i in range(1000)}
        queries = [1, 2, 3, 2, 4, 2, 3, 1]

        expected_page_faults = 5   # for LRU_CACHE
        # expected_page_faults = 4        # for Q2_cache

        def check(queries, expected_page_faults):
            page_faults = 0
            for key in queries:
                status = cache1.query(key)

                if status[0] == 1:
                    continue 

                else:
                    page_faults += 1
                    cache1.insert(key, test_database[key])

                # print(cache1.cache1, key, page_faults)
            return (page_faults == expected_page_faults, page_faults)
        

        status, page_faults = check(queries, expected_page_faults)
        
        if status:
            print('SUCCESS')
        else:
            print(f'Expected page faults: {expected_page_faults}')
            print(f'Actual page faults: {page_faults}')



if __name__ == '__main__':
    test = Tests()
    test.test_cache()