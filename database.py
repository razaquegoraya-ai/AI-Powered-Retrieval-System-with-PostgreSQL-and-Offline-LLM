from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from faker import Faker
from datetime import datetime, timedelta
import random
from config import DB_CONFIG
from tqdm import tqdm

# Create the database URL
DB_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

# Create the SQLAlchemy engine
engine = create_engine(DB_URL)
Base = declarative_base()

# Define the models
class Customer(Base):
    __tablename__ = 'customers'
    
    customer_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    address = Column(String(200))
    registration_date = Column(DateTime)
    
    orders = relationship('Order', back_populates='customer')
    
    # Create indexes for frequently queried fields
    __table_args__ = (
        Index('idx_customer_email', 'email'),
        Index('idx_customer_name', 'name'),
    )

class Product(Base):
    __tablename__ = 'products'
    
    product_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(500))
    price = Column(Float)
    category = Column(String(50))
    stock_quantity = Column(Integer)
    
    order_items = relationship('OrderItem', back_populates='product')
    
    __table_args__ = (
        Index('idx_product_category', 'category'),
        Index('idx_product_name', 'name'),
    )

class Order(Base):
    __tablename__ = 'orders'
    
    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    order_date = Column(DateTime)
    total_amount = Column(Float)
    status = Column(String(20))
    
    customer = relationship('Customer', back_populates='orders')
    items = relationship('OrderItem', back_populates='order')
    
    __table_args__ = (
        Index('idx_order_customer', 'customer_id'),
        Index('idx_order_date', 'order_date'),
    )

class OrderItem(Base):
    __tablename__ = 'order_items'
    
    item_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    quantity = Column(Integer)
    unit_price = Column(Float)
    
    order = relationship('Order', back_populates='items')
    product = relationship('Product', back_populates='order_items')

class Review(Base):
    __tablename__ = 'reviews'
    
    review_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'))
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    rating = Column(Integer)
    comment = Column(String(500))
    review_date = Column(DateTime)
    
    __table_args__ = (
        Index('idx_review_product', 'product_id'),
        Index('idx_review_customer', 'customer_id'),
    )

def create_sample_data(session):
    fake = Faker()
    
    # Create customers
    print("Creating customers...")
    customers = []
    for _ in tqdm(range(1000)):
        customer = Customer(
            name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            address=fake.address(),
            registration_date=fake.date_time_between(start_date='-2y')
        )
        customers.append(customer)
    session.add_all(customers)
    session.commit()
    
    # Create products
    print("Creating products...")
    products = []
    categories = ['Electronics', 'Books', 'Clothing', 'Home & Garden', 'Sports']
    for _ in tqdm(range(500)):
        product = Product(
            name=fake.product_name(),
            description=fake.text(max_nb_chars=200),
            price=round(random.uniform(10, 1000), 2),
            category=random.choice(categories),
            stock_quantity=random.randint(0, 1000)
        )
        products.append(product)
    session.add_all(products)
    session.commit()
    
    # Create orders and order items
    print("Creating orders and order items...")
    for _ in tqdm(range(2000)):
        customer = random.choice(customers)
        order = Order(
            customer_id=customer.customer_id,
            order_date=fake.date_time_between(start_date='-1y'),
            status=random.choice(['Pending', 'Completed', 'Shipped', 'Cancelled']),
            total_amount=0
        )
        session.add(order)
        session.flush()
        
        # Add 1-5 items to each order
        total = 0
        for _ in range(random.randint(1, 5)):
            product = random.choice(products)
            quantity = random.randint(1, 5)
            item = OrderItem(
                order_id=order.order_id,
                product_id=product.product_id,
                quantity=quantity,
                unit_price=product.price
            )
            total += quantity * product.price
            session.add(item)
        
        order.total_amount = total
    
    # Create reviews
    print("Creating reviews...")
    for _ in tqdm(range(3000)):
        review = Review(
            product_id=random.choice(products).product_id,
            customer_id=random.choice(customers).customer_id,
            rating=random.randint(1, 5),
            comment=fake.text(max_nb_chars=200),
            review_date=fake.date_time_between(start_date='-1y')
        )
        session.add(review)
    
    session.commit()

def init_db():
    # Create all tables
    Base.metadata.create_all(engine)
    
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        create_sample_data(session)
        print("Sample data created successfully!")
    except Exception as e:
        print(f"Error creating sample data: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == '__main__':
    init_db() 