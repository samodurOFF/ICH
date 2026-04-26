import logging

from sqlalchemy import (
    DECIMAL,
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
    create_engine,
    func,
)
from sqlalchemy.orm import DeclarativeBase, declarative_base, relationship, sessionmaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sqlalchemy.engine")
logger.setLevel(logging.INFO)

Base = declarative_base()
engine = create_engine("sqlite:///hm4.db")


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(100))
    in_stock = Column(Boolean, default=True)
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(precision=10, scale=2))
    in_stock = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

with Session() as session:
    with session.begin():
        electronics = Category(name="Electronics", description="Gadgets and devices.")
        books = Category(name="Books", description="Printed and electronic books.")
        clothing = Category(name="Clothing", description="Clothing for men and women.")
        session.add_all([electronics, books, clothing])
        session.commit()

    products = [
        Product(name="Smartphone", price=299.99, category=electronics),
        Product(name="Laptop", price=499.99, category=electronics),
        Product(name="Sci-Fi Novel", price=15.99, category=books),
        Product(name="Jeans", price=40.50, category=clothing),
        Product(name="T-shirt", price=20.00, category=clothing),
    ]
    session.add_all(products)
    session.commit()

with Session() as session:
    all_categories = session.query(Category).all()

    for category in all_categories:
        print(f"\nCategory: {category.name}")
        print(f"Description: {category.description}")
        if category.products:
            for product in category.products:
                print(f"Product: {product.name:<25} | Price: {product.price:>8.2f}")
        else:
            print("  (No products found in this category)")


with Session() as session:
    target_product = session.query(Product).filter(Product.name == "Smartphone").first()
    if target_product:
        target_product.price = 349.99
        session.commit()
        print(f"Successfully updated price for: {target_product.name}")
    else:
        print("Product 'Smartphone' not found.")


with Session() as session:
    results = (
        session.query(Product.category_id, func.count(Product.id))
        .group_by(Product.category_id)
        .all()
    )
    for cat_id, count in results:
        print(f"Category ID: {cat_id} | Total Products: {count}")


with Session() as session:
    results = (
        session.query(Product.category_id, func.count(Product.id))
        .group_by(Product.category_id)
        .having(func.count(Product.id) > 1)
        .all()
    )

    print("\n--- Task 5: Categories with > 1 product ---")
    for cat_id, count in results:
        print(f"Category ID: {cat_id} | Total Products: {count}")
