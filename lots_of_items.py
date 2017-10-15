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
