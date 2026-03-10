from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.models.product import Product

engine = create_engine('sqlite:///rayeva.db')
session = Session(engine)
products = session.query(Product).all()
print(f'Total products: {len(products)}')
for p in products:
    print(f'  - {p.name}: ${p.base_price}')
