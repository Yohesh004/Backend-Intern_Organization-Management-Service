from fastapi import APIRouter, HTTPException, status
from ..models.schemas import AdminLoginRequest, TokenResponse
from ..repositories.org_repository import OrgRepository
from ..auth import verify_password, create_access_token, hash_password

router = APIRouter(prefix="/admin", tags=["admin"])
repo = OrgRepository()

@router.post("/create", status_code=201)
async def create_admin(email_payload: dict):
    email = email_payload.get("email")
    password = email_payload.get("password")
    org_name = email_payload.get("organization_name")

    if not email or not password or not org_name:
        raise HTTPException(status_code=400, detail="email, password and organization_name required")

    existing = await repo.find_admin_by_email(email)
    if existing:
        raise HTTPException(status_code=400, detail="Admin already exists")

    hashed = hash_password(password)
    admin_record = {"email": email, "hashed_password": hashed, "organization_name": org_name}
    inserted_id = await repo.insert_admin(admin_record)
    return {"admin_id": str(inserted_id)}

@router.post("/login", response_model=TokenResponse)
async def login(payload: AdminLoginRequest):
    admin = await repo.find_admin_by_email(payload.email)
    if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not verify_password(payload.password, admin["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"admin_id": str(admin["_id"]), "organization": admin["organization_name"]})
    return {"access_token": token}
