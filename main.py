from fastapi import FastAPI, Depends
import fastapi.security as _security
from sqlalchemy.orm import Session
import schema
from typing import List
import services as _services
import fastapi as _fastapi

app=FastAPI()

@app.post("/api/users")
async def register_user(user:schema.UserCreate, db:Session=Depends(_services.get_db)):
    user_qs=await _services.get_user_by_email(email=user.email, db=db)
    if user_qs:
        raise _fastapi.HTTPException(
            status_code=_fastapi.status.HTTP_400_BAD_REQUEST,
            detail="user with this email already exist"
        )
    user=await _services.create_user(user=user, db=db)
    return await _services.create_token(user=user)

@app.post("/api/token")
async def login_user(form_data:_security.OAuth2PasswordRequestForm=Depends(), db:Session=Depends(_services.get_db)):
    user= await _services.authenticate_user(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail="invalid credentials")
    return await _services.create_token(user=user)

@app.get("/api/users/me", response_model=schema.User)
async def get_user(user:schema.User=_fastapi.Depends(_services.get_current_user)):
    return user

@app.post("/api/dimension", response_model=schema.Dimension)
async def create_dimension(payload:schema.DimensionCreate, user:schema.User=_fastapi.Depends(_services.get_current_user), db:Session=_fastapi.Depends(_services.get_db)):
    return await _services.create_dimension(dimension=payload, db=db)

@app.get("/api/dimension/{dimension_id}", status_code=200, response_model=schema.Dimension)
async def get_dimension(dimension_id:int, auth:schema.User=_fastapi.Depends(_services.get_current_user), db:Session=_fastapi.Depends(_services.get_db)):
    return await _services.get_single_dimension(dimension_id=dimension_id, db=db)


@app.get("/api/dimensions", status_code=200, response_model=List[schema.Dimension])
async def get_dimensions( auth:schema.User=_fastapi.Depends(_services.get_current_user), db:Session=_fastapi.Depends(_services.get_db)):
    return await _services.get_dimensions(db=db)

@app.post("/api/bin", response_model=schema.Location)
async def create_bin_location(bin:schema.LocationCreate, auth:schema.User=_fastapi.Depends(_services.get_current_user), db:Session=_fastapi.Depends(_services.get_db)):
    return await _services.create_location(location=bin, db=db)

@app.get("/api/bin", response_model=List[schema.Location])
async def get_bins( auth:schema.User=_fastapi.Depends(_services.get_current_user), db:Session=_fastapi.Depends(_services.get_db)):
    return await _services.get_bin_locations(db=db)

@app.get("/api/bin/{location_id}", status_code=200, response_model=schema.Location)
async def get_bin_location(location_id:int, auth:schema.User=_fastapi.Depends(_services.get_current_user), db:Session=_fastapi.Depends(_services.get_db)):
    return await _services.get_bin_location(location_id=location_id, db=db)

@app.post(".api/client", response_model=schema.Customer)
async def add_customer(client:schema.CustomerCreate, user:schema.User=_fastapi.Depends(_services.get_current_user), db:Session=_fastapi.Depends(_services.get_db)):
    pass

@app.get("/api/customers", response_model=List[schema.Customer])
async def get_customers(auth:schema.User=_fastapi.Depends(_services.get_current_user), db:Session=_fastapi.Depends(_services.get_db)):
    pass

@app.get("/api/customer/{customer_id}", status_code=200, response_model=schema.Customer)
async def get_single_customer(customer_id:int, auth:schema.User=_fastapi.Depends(_services.get_current_user), db:Session=_fastapi.Depends(_services.get_db)):
    pass