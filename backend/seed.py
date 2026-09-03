import os
import random
from sqlalchemy.orm import Session
from main import SessionLocal, User, Analysis, get_password_hash

names = [
    "chandana m p", "madan j r", "rakshith y b", "keerthi", "meghana", 
    "loknath swamy", "manoj", "keerthana", "harshini", "chandana m n", 
    "maanya t r", "darshan", "puneeth rajkumar", "yash", "sudeep", 
    "ramesh aravind", "shivanna", "radhika pandit", "ramya", "amulya",
    "kavya", "nithin", "preetham", "shruthi"
]

db = SessionLocal()

try:
    for full_name in names[:20]:
        username = full_name.lower().replace(" ", "")
        email = f"{username}@example.com"
        
        # Check if user exists
        user = db.query(User).filter(User.username == username).first()
        if not user:
            print(f"Adding user: {full_name}")
            hashed_pw = get_password_hash("password123")
            user = User(
                username=username,
                full_name=full_name.title(),
                email=email,
                hashed_password=hashed_pw
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
            # Add some fake analyses for each user
            for j in range(random.randint(1, 3)):
                pred = random.choice(["cancer", "non_cancer"])
                conf = random.uniform(0.65, 0.99)
                analysis = Analysis(
                    prediction=pred,
                    confidence=conf,
                    image_filename=f"sample_{random.randint(1,10)}.jpg",
                    user_id=user.id
                )
                db.add(analysis)
            db.commit()
    print("Database seeding completed.")
finally:
    db.close()
