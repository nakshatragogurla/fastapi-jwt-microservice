
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from sqlalchemy.orm import Session

import models
import schemas
import auth
from database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="JWT Authentication Microservice",
    description="REST API with JWT authentication and protected item management",
    version="1.0.0",
)

# Authentication schemes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", auto_error=False)
bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    oauth_token: str | None = Depends(oauth2_scheme),
    bearer_credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    # Accept a token from either authentication scheme
    token = oauth_token or (
        bearer_credentials.credentials if bearer_credentials else None
    )

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = auth.decode_access_token(token)

    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


@app.get("/")
def home():
    return {"message": "JWT Authentication Microservice is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post(
    "/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = db.query(models.User).filter(
        (models.User.username == user_data.username)
        | (models.User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )

    user = models.User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=auth.hash_password(user_data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(
        models.User.username == form_data.username
    ).first()

    if not user or not auth.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "access_token": auth.create_access_token(user.id),
        "token_type": "bearer",
    }


@app.post(
    "/items",
    response_model=schemas.ItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_item(
    item_data: schemas.ItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    item = models.Item(
        title=item_data.title,
        description=item_data.description,
        owner_id=current_user.id,
    )

    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/items", response_model=list[schemas.ItemResponse])
def list_items(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return db.query(models.Item).filter(
        models.Item.owner_id == current_user.id
    ).all()


@app.get("/items/{item_id}", response_model=schemas.ItemResponse)
def get_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    item = db.query(models.Item).filter(
        models.Item.id == item_id,
        models.Item.owner_id == current_user.id,
    ).first()

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    return item


@app.delete("/items/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    item = db.query(models.Item).filter(
        models.Item.id == item_id,
        models.Item.owner_id == current_user.id,
    ).first()

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}
