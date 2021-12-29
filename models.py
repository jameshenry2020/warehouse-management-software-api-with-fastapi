import sqlalchemy as _sql
import sqlalchemy.orm as _orm
from datetime import datetime
import passlib.hash as _hash
import database



class User(database.Base):
    __tablename__="users"
    id=_sql.Column(_sql.Integer, primary_key=True, index=True)
    first_name=_sql.Column(_sql.String, nullable=False)
    last_name=_sql.Column(_sql.String, nullable=False)
    email=_sql.Column(_sql.String,unique=True, index=True)
    hash_password=_sql.Column(_sql.String)
    date_joined=_sql.Column(_sql.DateTime, default=datetime.utcnow)
    is_active=_sql.Column(_sql.Boolean, default=True)
    is_staff=_sql.Column(_sql.Boolean, default=True)
   
    customers=_orm.relationship("Customer", back_populates="agent")
    
    def verify_password(self, password:str):
        return _hash.bcrypt.verify(password, self.hash_password)

class Customer(database.Base):
    __tablename__="customers"
    id=_sql.Column(_sql.Integer, primary_key=True, index=True)
    names=_sql.Column(_sql.String)
    email=_sql.Column(_sql.String, nullable=False)
    phone_number=_sql.Column(_sql.String, nullable=False)
    business_name=_sql.Column(_sql.String, nullable=False)
    goods_type=_sql.Column(_sql.String, nullable=False)
    secret_code=_sql.Column(_sql.String, unique=True, nullable=False)
    agent_id=_sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))

    agent=_orm.relationship("User", back_populates="customers")
    items=_orm.relationship("GoodsItem", back_populates="owner")

class Dimension(database.Base):
    __tablename__="bin_dimensions"
    id=_sql.Column(_sql.Integer, primary_key=True, index=True)
    length=_sql.Column(_sql.Float, nullable=False)
    width=_sql.Column(_sql.Float, nullable=False)
    weight=_sql.Column(_sql.Integer, nullable=False)
    maximum_capacity=_sql.Column(_sql.Integer, nullable=False)
    bin=_orm.relationship("Bin", back_populates="dimension")

class Bin(database.Base):
    __tablename__="bin_location"
    id=_sql.Column(_sql.Integer, primary_key=True, index=True)
    bin_name=_sql.Column(_sql.String)
    row_number=_sql.Column(_sql.Integer)
    capacity=_sql.Column(_sql.Integer)
    dimension_id=_sql.Column(_sql.Integer, _sql.ForeignKey("bin_dimensions.id"))
    availability=_sql.Column(_sql.Boolean, default=True)
    dimension=_orm.relationship("Dimension", back_populates="bin")
    items=_orm.relationship("GoodsItem", back_populates="location")

class GoodsItem(database.Base):
    __tablename__ ="items"
    id=_sql.Column(_sql.Integer, primary_key=True, index=True)
    product_name=_sql.Column(_sql.String, nullable=False)
    description=_sql.Column(_sql.String, nullable=False)
    expiration_date=_sql.Column(_sql.Date)
    quantity=_sql.Column(_sql.Integer)
    batch_no=_sql.Column(_sql.Integer)
    weight=_sql.Column(_sql.Integer)
    dispatch_code=_sql.Column(_sql.String(10), unique=True, nullable=False)
    location_id=_sql.Column(_sql.Integer, _sql.ForeignKey("bin_location.id"))
    owner_id=_sql.Column(_sql.Integer, _sql.ForeignKey("customers.id"))
    product_brand=_sql.Column(_sql.String, nullable=False)
    location=_orm.relationship("Bin", back_populates="items")
    owner=_orm.relationship("Customer", back_populates="items")

