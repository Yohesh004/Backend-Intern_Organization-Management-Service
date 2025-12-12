from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict
from ..models.schemas import OrgCreateRequest, OrgUpdateRequest, OrgDeleteRequest
from ..repositories.org_repository import OrgRepository
from ..auth import hash_password, get_current_admin
from ..database import get_master_db

router = APIRouter(prefix="/org", tags=["org"])
repo = OrgRepository()

@router.post("/create", status_code=201)
async def create_organization(payload: OrgCreateRequest):
    name = payload.organization_name.strip().lower()
    if await repo.find_org_by_name(name):
        raise HTTPException(status_code=400, detail="Organization name already exists")

    await repo.ensure_org_db_created(name)
    db_name = f"org_{name}"

    hashed = hash_password(payload.password)
    admin_record = {"email": payload.email, "hashed_password": hashed, "organization_name": name}
    admin_id = await repo.insert_admin(admin_record)

    meta = {
        "organization_name": name,
        "database_name": db_name,
        "admin_id": admin_id
    }
    org_id = await repo.insert_org(meta)
    return {
        "message": "Organization created",
        "organization": {
            "id": str(org_id),
            "organization_name": name,
            "database_name": db_name,
            "admin_id": str(admin_id)
        }
    }

@router.get("/get")
async def get_organization(organization_name: str):
    org = await repo.find_org_by_name(organization_name)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return {
        "id": str(org["_id"]),
        "organization_name": org["organization_name"],
        "database_name": org["database_name"],
        "admin_id": str(org["admin_id"])
    }

@router.put("/update", status_code=200)
async def update_organization(payload: OrgUpdateRequest, admin_ctx=Depends(get_current_admin)):
    if admin_ctx["organization"] != payload.organization_name:
        raise HTTPException(status_code=403, detail="Not authorized to update this organization")

    old_name = payload.organization_name.strip().lower()
    new_name = payload.new_organization_name.strip().lower()

    if old_name == new_name:
        raise HTTPException(status_code=400, detail="New name must be different")

    existing = await repo.find_org_by_name(new_name)
    if existing:
        raise HTTPException(status_code=400, detail="Target organization name already exists")

    org_meta = await repo.find_org_by_name(old_name)
    if not org_meta:
        raise HTTPException(status_code=404, detail="Organization not found")

    await repo.ensure_org_db_created(new_name)
    await repo.copy_db(src_org=old_name, dest_org=new_name)

    new_db_name = f"org_{new_name}"
    await repo.update_org({"organization_name": old_name}, {"$set": {"organization_name": new_name, "database_name": new_db_name}})

    master_db = get_master_db()
    await master_db["admins"].update_many({"organization_name": old_name}, {"$set": {"organization_name": new_name}})

    return {"message": "Organization renamed and data migrated", "organization_name": new_name, "database_name": new_db_name}

@router.delete("/delete", status_code=200)
async def delete_organization(payload: OrgDeleteRequest, admin_ctx=Depends(get_current_admin)):
    if admin_ctx["organization"] != payload.organization_name:
        raise HTTPException(status_code=403, detail="Not authorized to delete this organization")

    org_meta = await repo.find_org_by_name(payload.organization_name)
    if not org_meta:
        raise HTTPException(status_code=404, detail="Organization not found")

    await repo.drop_org_db(payload.organization_name)
    await repo.delete_admins_for_org(payload.organization_name)
    await repo.delete_org_metadata(payload.organization_name)

    return {"message": f"Organization '{payload.organization_name}' deleted successfully"}
