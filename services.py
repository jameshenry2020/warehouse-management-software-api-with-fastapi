import fastapi as _fastapi
import fastapi.security as _security
import database
import models
import jwt as _jwt
import passlib.hash as _hash
import sqlalchemy.orm as _orm
import email_validator as email_check

import schema as _schema

_JWT_SECRET="fjerdjgkthisisnotsafe"

def _create_database():
    return database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db=database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_user_by_email(email:str, db:_orm.Session):
    return db.query(models.User).filter(models.User.email==email).first()

async def create_user(user:_schema.UserCreate, db:_orm.Session):
    try:
        valid= email_check.validate_email(email=user.email)
        email=valid.email
    except email_check.EmailNotValidError:
        raise _fastapi.HTTPException(
            status_code=_fastapi.status.HTTP_404_NOT_FOUND,
            detail="please enter valid email"
        )
    hashed_password=_hash.bcrypt.hash(user.password)
    user_obj=models.User(first_name=user.first_name, last_name=user.last_name, email=email,hash_password=hashed_password )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj



async def create_token(user:models.User):
    user_schema_obj=_schema.User.from_orm(user)
    user_dict=user_schema_obj.dict()
    del user_dict['date_joined']
    token = _jwt.encode(user_dict, _JWT_SECRET)
    return dict(access_token=token, token_type="bearer")

async def authenticate_user(email:str, password:str, db:_orm.Session):
    user= await get_user_by_email(email=email, db=db)
    if not user:
        return False
    if not user.verify_password(password=password):
        return False
    return user

oauth2schema=_security.OAuth2PasswordBearer("/api/token")
async def get_current_user(db:_orm.Session=_fastapi.Depends(get_db), token:str =_fastapi.Depends(oauth2schema)):
    try:
        payload=_jwt.decode(token, _JWT_SECRET, algorithms=["HS256"])
        user=db.query(models.User).get(payload["id"])
    except:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid email or password")
    return _schema.User.from_orm(user)

async def create_dimension(dimension:_schema.DimensionCreate, db:_orm.Session):
    dimension=models.Dimension(**dimension.dict())
    db.add(dimension)
    db.commit()
    db.refresh(dimension)
    return _schema.Dimension.from_orm(dimension)


async def get_single_dimension(dimension_id:int, db:_orm.Session):
    dimension=db.query(models.Dimension).filter(models.Dimension.id == dimension_id).first()

    if dimension is None:
        raise _fastapi.HTTPException(status_code=404, detail="this dimension these not exist")
    return _schema.Dimension.from_orm(dimension)

async def get_dimensions(db:_orm.Session):
    dimensions=db.query(models.Dimension).all()
    return dimensions

async def create_location(location:_schema.LocationCreate, db:_orm.Session):
    dimension=db.query(models.Dimension).filter(models.Dimension.id ==location.dimension_id).first()
    if dimension is None:
        raise _fastapi.HTTPException(status_code=404, detail="invalid dimension")
    location=models.Bin(bin_name=location.bin_name, row_number=location.row_number, capacity=location.capacity, dimension_id=dimension.id)  
    db.add(location)
    db.commit()
    db.refresh(location)
    return _schema.Location.from_orm(location)



async def get_bin_locations(db:_orm.Session):
    locations=db.query(models.Dimension).all()
    return locations

async def get_bin_location(location_id:int, db:_orm.Session):
    location=db.query(models.Bin).filter(models.Bin.id == location_id).first()
    if location is None:
        raise _fastapi.HTTPException(status_code=404, detail="this location these not exist")
    return _schema.Location.from_orm(location)


