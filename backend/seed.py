from database import products_collection

products = [
    {"id": 1, "name": "boAt Airdopes 141 Earbuds", "category": "Electronics", "brand": "boAt", "price": 1299, "rating": 4.1,
     "description": "True wireless earbuds with 42 hours total playback, low latency gaming mode and IPX4 water resistance."},
    {"id": 2, "name": "Noise Cancelling Headphones X200", "category": "Electronics", "brand": "SoundPro", "price": 4999, "rating": 4.5,
     "description": "Over-ear Bluetooth headphones with active noise cancellation, 30 hour battery and deep bass for travel and work."},
    {"id": 3, "name": "Redmi Note 13 Smartphone", "category": "Electronics", "brand": "Redmi", "price": 15999, "rating": 4.3,
     "description": "6.67 inch AMOLED display, 108MP camera, 5000mAh battery with fast charging. Great mid-range phone."},
    {"id": 4, "name": "Pro Runner Running Shoes", "category": "Footwear", "brand": "Stride", "price": 2999, "rating": 4.4,
     "description": "Lightweight mesh running shoes with cushioned sole and breathable fabric. Ideal for daily jogging and gym."},
    {"id": 5, "name": "Classic White Sneakers", "category": "Footwear", "brand": "Urbanfit", "price": 1899, "rating": 4.0,
     "description": "Casual unisex sneakers with a clean white finish, comfortable for college and everyday wear."},
    {"id": 6, "name": "Trek 40L Travel Backpack", "category": "Accessories", "brand": "Wildcraft", "price": 2199, "rating": 4.6,
     "description": "Water resistant 40 litre backpack with laptop compartment, padded straps and rain cover. Great for trekking and travel."},
    {"id": 7, "name": "Laptop Backpack 25L", "category": "Accessories", "brand": "Skybags", "price": 1199, "rating": 4.2,
     "description": "Slim 25 litre backpack fitting 15.6 inch laptops, with multiple pockets, suitable for college and office."},
    {"id": 8, "name": "Smart Fitness Band 5", "category": "Electronics", "brand": "FitLife", "price": 1799, "rating": 4.0,
     "description": "Fitness tracker with heart rate monitor, sleep tracking, step counter and 10 day battery life."},
    {"id": 9, "name": "Cotton Casual T-Shirt", "category": "Clothing", "brand": "Roadster", "price": 499, "rating": 4.1,
     "description": "Soft 100 percent cotton round neck t-shirt, regular fit, machine washable."},
    {"id": 10, "name": "Slim Fit Denim Jeans", "category": "Clothing", "brand": "Levi Style", "price": 1999, "rating": 4.3,
     "description": "Stretchable slim fit denim jeans in dark blue, comfortable for all-day wear."},
    {"id": 11, "name": "Stainless Steel Water Bottle 1L", "category": "Home", "brand": "Cello", "price": 599, "rating": 4.5,
     "description": "Double wall insulated bottle keeping drinks cold for 24 hours and hot for 12 hours. Leak proof lid."},
    {"id": 12, "name": "Wireless Gaming Mouse", "category": "Electronics", "brand": "Zephyr", "price": 1499, "rating": 4.4,
     "description": "Ergonomic wireless mouse with 6 programmable buttons, adjustable DPI up to 12000 and RGB lighting."},
]

products_collection.delete_many({})   # clear old data so re-running doesn't create duplicates
products_collection.insert_many(products)
print(f"Inserted {products_collection.count_documents({})} products")