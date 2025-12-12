from typing import Optional, Dict, Any
from ..database import get_master_db, get_client
from bson import ObjectId

class OrgRepository:
    def __init__(self):
        self._master = get_master_db()
        self._client = get_client()

    async def find_org_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        return await self._master["organizations"].find_one({"organization_name": name})

    async def insert_org(self, payload: Dict[str, Any]) -> ObjectId:
        result = await self._master["organizations"].insert_one(payload)
        return result.inserted_id

    async def update_org(self, filter_q, update_q):
        await self._master["organizations"].update_one(filter_q, update_q)

    async def delete_org_metadata(self, name: str):
        await self._master["organizations"].delete_one({"organization_name": name})

    async def find_admin_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        return await self._master["admins"].find_one({"email": email})

    async def insert_admin(self, payload: Dict[str, Any]) -> ObjectId:
        result = await self._master["admins"].insert_one(payload)
        return result.inserted_id

    async def update_admin_org(self, admin_id: ObjectId, new_org_name: str):
        await self._master["admins"].update_one({"_id": admin_id}, {"$set": {"organization_name": new_org_name}})

    async def delete_admins_for_org(self, org_name: str):
        await self._master["admins"].delete_many({"organization_name": org_name})

    def get_org_db(self, org_name: str):
        db_name = f"org_{org_name}"
        return self._client[db_name]

    async def ensure_org_db_created(self, org_name: str):
        db = self.get_org_db(org_name)
        await db["__init__"].insert_one({"created_at": True})
        await db["__init__"].delete_many({})

    async def list_org_collections(self, org_name: str):
        db = self.get_org_db(org_name)
        return await db.list_collection_names()

    async def copy_db(self, src_org: str, dest_org: str):
        src_db = self.get_org_db(src_org)
        dest_db = self.get_org_db(dest_org)

        colls = await src_db.list_collection_names()
        for coll_name in colls:
            src_coll = src_db[coll_name]
            dest_coll = dest_db[coll_name]
            async for doc in src_coll.find({}):
                await dest_coll.insert_one(doc)

    async def drop_org_db(self, org_name: str):
        db_name = f"org_{org_name}"
        self._client.drop_database(db_name)
