from pymongo import MongoClient

# Replace with your MongoDB connection string
client = MongoClient('mongodb://localhost:27017/')

# Replace with your database and collection names
db = client['zomato_db']
restaurant_collection = db['zomato_test']

new_field = {"temp": 0}

# Update all documents to include the new field
# result = collection.update_many(
#     {},
#     {'$set': new_field}
# )

restaurant_id = 6317637
restaurant = restaurant_collection.find_one({'Restaurant ID': restaurant_id})
print(restaurant["Aggregate rating"])

new_rating = 4.8
restaurant_collection.update_one(
    {'Restaurant ID': restaurant_id},
    {
        "$set": {"Aggregate rating": new_rating},
        "$inc": {"Votes": -1}
    }
    
)


# print(f"Modified {result.modified_count} documents")
# restaurant_collection.close()