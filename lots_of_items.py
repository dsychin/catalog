from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


categories = ['CPU', 'CPU Cooler', 'Motherboard', 'Memory', 'Storage',
              'Video Card', 'Case', 'Power Supply', 'Optical Drive',
              'Operating System', 'Monitor']
for category in categories:
    data = Category(name=category)
    session.add(data)
    session.commit()

data = User(username='dsychin', email='chin.sy.des@gmail.com')
session.add(data)
session.commit()


class Items:
    def __init__(self, name, description, category_id, created_by_id):
        self.name = name
        self.description = description
        self.category_id = category_id
        self.created_by_id = created_by_id

items = [Items('GTX 1060', 'Mid-range GPU', 6, 1)]

for item in items:
    data = Item(name=item.name, description=item.description,
                category_id=item.category_id, created_by_id=item.created_by_id)
    session.add(data)
    session.commit()
