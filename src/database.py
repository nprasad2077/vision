from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    color = Column(String)
    size = Column(String)
    additional_attributes = Column(JSON)
    

# Create local engine
engine = create_engine('sqlite:////home/ravi/code/vision/data/sample_db.db')

# Create tables in engine
Base.metadata.create_all(engine)

# Create session maker
Session = sessionmaker(bind=engine)



def store_item(item_data):
    session = Session()
    
    new_item = Item(
        name=item_data.name,
        type=item_data.type,
        color=item_data.color,
        size=item_data.size,
        additional_attributes=item_data.additional_attributes
    )
    
    session.add(new_item)
    session.commit()
    session.close()
    
def get_all_items():
    session = Session()
    items = session.query(Item).all()
    session.close()
    return items
