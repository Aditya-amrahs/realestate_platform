from database import SessionLocal, engine, Base
import models
from auth import hash_password
from datetime import date, time

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# ── Clean slate no data available.
db.query(models.PropertyView).delete()
db.query(models.Favorite).delete()
db.query(models.Booking).delete()
db.query(models.Property).delete()
db.query(models.Agent).delete()
db.query(models.User).delete()
db.commit()

# ── Users & Agents (agents are also users with role="agent")
user1 = models.User(
    name="Aditya Sharma",
    email="aditya@test.com",
    password=hash_password("test123"),
    role="user",
)
user2 = models.User(
    name="Priya Mehta",
    email="priya@test.com",
    password=hash_password("test123"),
    role="user",
)
agent1 = models.User(
    name="Rahul Agent",
    email="rahul@test.com",
    password=hash_password("test123"),
    role="agent",
)
agent2 = models.User(
    name="Sneha Agent",
    email="sneha@test.com",
    password=hash_password("test123"),
    role="agent",
)

for u in [user1, user2, agent1, agent2]:
    db.add(u)
db.commit()

# --─ Agents (linked to user accounts)
a1 = models.Agent(user_id=agent1.id)
a2 = models.Agent(user_id=agent2.id)
db.add(a1)
db.add(a2)
db.commit()

# ── Properties
# the properties list with this — adds image_url to each
properties = [
    models.Property(
        title="Sunny 2BHK in Indiranagar",
        city="Bangalore",
        price=8500000,
        type="apartment",
        size=1100,
        agent_id=a1.id,
        image_url="https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800&auto=format&fit=crop",
    ),
    models.Property(
        title="Spacious Villa with Garden",
        city="Bangalore",
        price=25000000,
        type="villa",
        size=3200,
        agent_id=a1.id,
        image_url="https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&auto=format&fit=crop",
    ),
    models.Property(
        title="Modern Studio near Metro",
        city="Mumbai",
        price=6200000,
        type="apartment",
        size=520,
        agent_id=a1.id,
        image_url="https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&auto=format&fit=crop",
    ),
    models.Property(
        title="3BHK Independent House",
        city="Delhi",
        price=15000000,
        type="house",
        size=2100,
        agent_id=a2.id,
        image_url="https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800&auto=format&fit=crop",
    ),
    models.Property(
        title="Luxury Penthouse Sea View",
        city="Mumbai",
        price=45000000,
        type="apartment",
        size=4100,
        agent_id=a2.id,
        image_url="https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&auto=format&fit=crop",
    ),
    models.Property(
        title="Plot in Whitefield",
        city="Bangalore",
        price=9000000,
        type="plot",
        size=2400,
        agent_id=a2.id,
        image_url="https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800&auto=format&fit=crop",
    ),
    models.Property(
        title="Cozy 1BHK Koramangala",
        city="Bangalore",
        price=5500000,
        type="apartment",
        size=650,
        agent_id=a1.id,
        image_url="https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=800&auto=format&fit=crop",
    ),
    models.Property(
        title="Farmhouse with Pool",
        city="Pune",
        price=32000000,
        type="villa",
        size=5000,
        agent_id=a2.id,
        image_url="https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&auto=format&fit=crop",
    ),
]

for p in properties:
    db.add(p)
db.commit()

# ── Property views (for analytics + trending) ─────
for prop in properties[:5]:
    for _ in range(prop.size // 200):  # more views for bigger properties
        db.add(models.PropertyView(property_id=prop.id))
db.commit()

# ── Favorites
db.add(models.Favorite(user_id=user1.id, property_id=properties[0].id))
db.add(models.Favorite(user_id=user1.id, property_id=properties[2].id))
db.add(models.Favorite(user_id=user2.id, property_id=properties[4].id))
db.commit()

# ── Bookings
db.add(
    models.Booking(
        user_id=user1.id,
        property_id=properties[0].id,
        visit_date=date(2025, 6, 15),
        visit_time=time(10, 0),
    )
)
db.add(
    models.Booking(
        user_id=user2.id,
        property_id=properties[3].id,
        visit_date=date(2025, 6, 18),
        visit_time=time(14, 30),
    )
)
db.commit()

db.close()
print("Seeded successfully.")
print("\nTest credentials:")
print("  User  → aditya@test.com  / test123")
print("  User  → priya@test.com   / test123")
print("  Agent → rahul@test.com   / test123")
print("  Agent → sneha@test.com   / test123")
