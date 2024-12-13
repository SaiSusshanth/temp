from flask import Flask, request, jsonify
from pymongo import MongoClient
from math import ceil
from flask_cors import CORS
from Linked_list_cache import Linked_List_cache 


app = Flask(__name__)
CORS(app)


# MongoDB configuration
client = MongoClient('localhost', 27017)
db = client['zomato_db']
collection = db['restaurants']
# print(type(collection))
TOTAL_ENTRIES = collection.count_documents({})
PAGE_LIMIT = 10
CACHE_SIZE = 5


cache1 = Linked_List_cache(CACHE_SIZE)

def caching(query_type, args):

    key = (query_type, args)
    status = cache1.query(key)

    if status[0] == 1:
        return_value = status[1]

    else:
        # get restaurant by id
        if query_type == 1:
            id = args 
            return_value = collection.find_one({'Restaurant ID': id})
        
        # get list of restaurants by country or all
        elif query_type == 2:
            country, skips, per_page = args
            if country == None:
                return_value = list(collection.find().skip(skips).limit(per_page))
            
            else:
                return_value = list(collection.find({'Country': country}).skip(skips).limit(per_page))
        
        cache1.insert(key, return_value)
    
    return return_value



@app.route('/restaurant/<int:id>', methods=['GET'])
def get_restaurant(id):
    try:
        # restaurant = collection.find_one({'Restaurant ID': id})
        restaurant = caching(1, id)   #query_type, args

        if restaurant:
            restaurant['_id'] = str(restaurant['_id'])
            return jsonify(restaurant)
        else:
            return jsonify({"error": "Restaurant not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/country', methods=['GET'])
def get_restaurant_by_Country():
    try:
        page = int(request.args.get('page', 1))
        per_page = PAGE_LIMIT
        country = (request.args.get('country', ''))
        skips = per_page * (page - 1)
        rating = float(request.args.get('rating', 5))

        key = (country, skips, per_page)


        # query = {}
        print(country, rating)
        if country == '':
            query = {
                "Aggregate rating": {"$gte" : rating}
            }

        elif rating == "":
            query = {
                "Country" : country
            }

        else:
            query = {
                "$and" : [{"Country" : country}, {"Aggregate rating" : {"$gte" : rating}}]
            }
            
        print(query)
        restaurants = list(collection.find(query).skip(skips).limit(per_page))
        # restaurants = caching(2, (country, skips, per_page))    # query_type, args
        value = restaurants 
        
        total = len(restaurants)
        total_pages = ceil(total / per_page)

        if page > total_pages or page < 1:
            print(page, total_pages, total, page)
            return jsonify({
                "error": "Page out of range",
                "total_pages": total_pages
            }), 400
        
        if restaurants:
            for i in restaurants:
                i["_id"] = str(i['_id'])
            
            return jsonify({
            "restaurants": restaurants,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages
            })
            # return jsonify(restaurants)
        else:
            return jsonify({"error": "No Restaurant found"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    try:
        page = int(request.args.get('page', 1))
        # per_page = int(request.args.get('per_page', 10))
        per_page = PAGE_LIMIT

        # total = collection.count_documents({})
        total = TOTAL_ENTRIES
        total_pages = ceil(total / per_page)

        if page > total_pages or page < 1:
            return jsonify({
                "error": "Page out of range",
                "total_pages": total_pages
            }), 400

        skips = per_page * (page - 1)
        # restaurants = list(collection.find().skip(skips).limit(per_page))
        restaurants = caching(2, (None, skips, per_page))
        for restaurant in restaurants:
            restaurant['_id'] = str(restaurant['_id'])

        return jsonify({
            "restaurants": restaurants,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/update_rating', methods=['GET'])
def update_rating():
    restaurant_id = int(request.args.get('restaurant_id'))
    selected_rating = float(request.args.get('selected_rating'))
    
    return ''



@app.route('/')
def index():
    return 'PlaceHolder for testing'

app.run(host = '0.0.0.0', port = 80)

