from app.db.session import SessionLocal
from app.models.product import Product

products_data = [
    # Food
    {"name": "Premium Dog Kibble", "description": "High-protein dry food for adult dogs", "price": 49.99, "stock": 50, "category": "food", "pet_type": "dog"},
    {"name": "Salmon Cat Pate", "description": "Wet food can with delicious wild salmon for cats", "price": 2.49, "stock": 120, "category": "food", "pet_type": "cat"},
    {"name": "Premium Bird Seed Mix", "description": "Mix of seeds and dried fruits for canaries and parakeets", "price": 8.99, "stock": 40, "category": "food", "pet_type": "bird"},
    {"name": "Rabbit Pellets Alfalfa", "description": "Nutritious pellets enriched with vitamins for rabbits", "price": 12.50, "stock": 35, "category": "food", "pet_type": "rabbit"},
    
    # Toys
    {"name": "Indestructible Rubber Bone", "description": "Extremely durable rubber bone for aggressive chewers", "price": 14.99, "stock": 30, "category": "toys", "pet_type": "dog"},
    {"name": "Laser Pointer Chase Toy", "description": "Keep your cat active with this automated red laser toy", "price": 9.99, "stock": 60, "category": "toys", "pet_type": "cat"},
    {"name": "Chew Wooden Ladder", "description": "Hanging natural wood ladder for birds to climb and chew", "price": 6.49, "stock": 25, "category": "toys", "pet_type": "bird"},
    {"name": "Running Hamster Wheel", "description": "Silent spinner wheel for hamsters and small rodents", "price": 11.99, "stock": 20, "category": "toys", "pet_type": "hamster"},

    # Accessories
    {"name": "Reflective Dog Harness", "description": "Comfortable harness with reflective strips for safe night walks", "price": 24.99, "stock": 15, "category": "accessories", "pet_type": "dog"},
    {"name": "Self-Cleaning Litter Box", "description": "Automatic cleaning litter box for busy owners", "price": 199.99, "stock": 5, "category": "accessories", "pet_type": "cat"},
    {"name": "Aquarium Filter Internal", "description": "Quiet water filter for small to medium fish tanks", "price": 18.50, "stock": 18, "category": "accessories", "pet_type": "fish"},

    # Medicine
    {"name": "Flea and Tick Collar", "description": "Long-lasting protection collar against fleas and ticks", "price": 35.99, "stock": 45, "category": "medicine", "pet_type": "dog"},
    {"name": "Cat Hairball Remedy Gel", "description": "Tasty gel that helps prevent and eliminate hairballs", "price": 7.99, "stock": 50, "category": "medicine", "pet_type": "cat"},
    {"name": "Avian Vitamin Drops", "description": "Water-soluble multivitamin drops for pet birds", "price": 5.99, "stock": 30, "category": "medicine", "pet_type": "bird"}
]

db = SessionLocal()

try:
    # Clear existing products to prevent duplicates on re-run
    db.query(Product).delete()
    
    for prod_data in products_data:
        product = Product(**prod_data)
        db.add(product)
    db.commit()
    print(f"Successfully added {len(products_data)} products to the database!")
except Exception as e:
    db.rollback()
    print(f"Error: {e}")
finally:
    db.close()
