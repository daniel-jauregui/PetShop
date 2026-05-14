from app.db.session import SessionLocal
from app.models.pet import Pet

# 50 pets with different types, ages, and names
pets_data = [
    {"name": "Buddy", "type": "dog", "age": 3},
    {"name": "Luna", "type": "cat", "age": 2},
    {"name": "Max", "type": "dog", "age": 5},
    {"name": "Bella", "type": "cat", "age": 1},
    {"name": "Charlie", "type": "dog", "age": 4},
    {"name": "Lucy", "type": "dog", "age": 2},
    {"name": "Cooper", "type": "dog", "age": 6},
    {"name": "Daisy", "type": "dog", "age": 3},
    {"name": "Rocky", "type": "dog", "age": 7},
    {"name": "Molly", "type": "dog", "age": 2},
    {"name": "Bear", "type": "dog", "age": 4},
    {"name": "Duke", "type": "dog", "age": 5},
    {"name": "Stella", "type": "dog", "age": 1},
    {"name": "Tucker", "type": "dog", "age": 3},
    {"name": "Penny", "type": "dog", "age": 2},
    {"name": "Zeus", "type": "dog", "age": 6},
    {"name": "Chloe", "type": "dog", "age": 4},
    {"name": "Bentley", "type": "dog", "age": 3},
    {"name": "Lily", "type": "dog", "age": 1},
    {"name": "Oliver", "type": "cat", "age": 2},
    {"name": "Simba", "type": "cat", "age": 3},
    {"name": "Nala", "type": "cat", "age": 1},
    {"name": "Milo", "type": "cat", "age": 4},
    {"name": "Leo", "type": "cat", "age": 2},
    {"name": "Cleo", "type": "cat", "age": 5},
    {"name": "Oscar", "type": "cat", "age": 3},
    {"name": "Jasper", "type": "cat", "age": 1},
    {"name": "Finn", "type": "cat", "age": 2},
    {"name": "Lola", "type": "cat", "age": 4},
    {"name": "Salem", "type": "cat", "age": 6},
    {"name": "Shadow", "type": "cat", "age": 3},
    {"name": "Coco", "type": "cat", "age": 2},
    {"name": "Ginger", "type": "cat", "age": 5},
    {"name": "Smokey", "type": "cat", "age": 4},
    {"name": "Pepper", "type": "cat", "age": 1},
    {"name": "Mittens", "type": "cat", "age": 2},
    {"name": "Thumper", "type": "rabbit", "age": 1},
    {"name": "Snowball", "type": "rabbit", "age": 2},
    {"name": "Cinnamon", "type": "rabbit", "age": 3},
    {"name": "Oreo", "type": "rabbit", "age": 1},
    {"name": "Clover", "type": "rabbit", "age": 2},
    {"name": "Flopsy", "type": "rabbit", "age": 1},
    {"name": "Cotton", "type": "rabbit", "age": 2},
    {"name": "Rusty", "type": "hamster", "age": 1},
    {"name": "Peanut", "type": "hamster", "age": 2},
    {"name": "Cookie", "type": "hamster", "age": 1},
    {"name": "Nibbles", "type": "hamster", "age": 1},
    {"name": "Whiskers", "type": "hamster", "age": 2},
    {"name": "Goldie", "type": "fish", "age": 1},
    {"name": "Bubbles", "type": "fish", "age": 2},
    {"name": "Sunny", "type": "fish", "age": 1},
    {"name": "Coral", "type": "fish", "age": 3},
    {"name": "Tweety", "type": "bird", "age": 2},
]

db = SessionLocal()

try:
    for pet_data in pets_data:
        pet = Pet(**pet_data)
        db.add(pet)
    db.commit()
    print(f"Successfully added {len(pets_data)} pets to the database!")
except Exception as e:
    db.rollback()
    print(f"Error: {e}")
finally:
    db.close()