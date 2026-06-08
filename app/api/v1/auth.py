from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, Token
from utils.security import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Registra un nuevo usuario en el sistema local."""
    # 1. Verificar si el usuario ya existe
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered."
        )

    # 2. Encriptar la contraseña limpia antes de guardarla
    hashed_pwd = get_password_hash(user_data.password)

    # 3. Crear la instancia del modelo y persistirla
    new_user = User(username=user_data.username, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Verifica las credenciales y retorna un token de acceso JWT.

    Usa OAuth2PasswordRequestForm para integrarse nativamente con la UI de Swagger docs.
    """
    # 1. Buscar al usuario por su username
    user = db.query(User).filter(User.username == form_data.username).first()

    # 2. Validar existencia y contraseña
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Generar el JWT usando el username como 'subject'
    access_token = create_access_token(subject=user.username)

    return {"access_token": access_token, "token_type": "bearer"}