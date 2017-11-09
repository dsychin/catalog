#!/usr/bin/python3
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


categories = ['CPU', 'Motherboard', 'Memory', 'Storage',
              'Video Card', 'Case', 'Power Supply']
for category in categories:
    data = Category(name=category)
    session.add(data)
    session.commit()

data = User(name='Desmond Chin', email='chin.sy.des@gmail.com')
session.add(data)
session.commit()


class Items:
    def __init__(self, name, description, category_id, created_by_id):
        self.name = name
        self.description = description
        self.category_id = category_id
        self.created_by_id = created_by_id


items = [Items(
    'Intel i7 6700K',
    'The Intel® Core™ i7 6000-series processors are based on the new '
    'architecture codenamed Skylake. The 6th Gen Intel processors support '
    'Intel® Turbo Boost Technology which gives you an extra boost and '
    'increases processor frequency when you need it most. Choose a \'K\' '
    'SKU, which can be easily overclocked for even greater performance.',
    1, 1),
    Items(
    'Intel Core i9 Socket 2066 Skylake-X',
        'These new high-end Core X CPUs are based on the Skylake X '
        'architecture and are designed to fit into the new Socket 2066 and so '
        'require an Intel X299 motherboard. These 10-core CPUs support '
        'HyperThreading and so are ideal for heavy multitasking and content '
        'creation applications.', 1, 1),
    Items(
    'GTX 1060',
        'The GeForce GTX 1060 graphics card is loaded with innovative new '
        'gaming technologies, making it the perfect choice for the latest '
        'high-definition games. Powered by NVIDIA Pascal™—the most advanced '
        'GPU architecture ever created—the GeForce GTX 1060 delivers '
        'brilliant performance that opens the door to virtual reality and '
        'beyond.', 5, 1),
    Items(
    'RX 580',
        'The RX 580 is a new and improved version of the RX 480, which is '
        'based on the power efficient Polaris architecture with 14nm FinFET '
        'transistors. The RX 580 has 2,304 stream processors and 8GB of GDDR5 '
        'memory and so provides silky smooth frame rates on a 1920 x 1080 or '
        '2560 x 1440 monitor with all the detail settings dialled up. The '
        'Radeon RX 580 is a solid choice for a high end gaming PC especially '
        'as it supports advanced technologies such as DirectX 12, CrossFire '
        'and FreeSync.', 5, 1)
]

for item in items:
    data = Item(name=item.name, description=item.description,
                category_id=item.category_id, created_by_id=item.created_by_id)
    session.add(data)
    session.commit()
