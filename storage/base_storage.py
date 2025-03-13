import os
import uuid
from abc import ABC, abstractmethod
import json
from fastapi import HTTPException, status
from pymongo import MongoClient
from schemas import NewProduct, SavedProduct, ProductId, PatchProduct
from settings import settings


class BaseStorage(ABC):
    @abstractmethod
    def create_product(self, new_product: NewProduct) -> SavedProduct:
        pass

    @abstractmethod
    def get_product(self, product_id: str, with_raise) -> SavedProduct:
        pass

    @abstractmethod
    def get_products(
        self, q: str = "", limit: int = 10, skip: int = 0
    ) -> list[SavedProduct]:
        pass

    @abstractmethod
    def delete_product(self, product_id: str) -> None:
        pass

    @abstractmethod
    def patch_product(self, product_id: str, data: PatchProduct) -> SavedProduct:
        pass


class MongoStorage(BaseStorage):
    def __init__(self, uri: str):
        client = MongoClient(uri)
        db = client.products
        collection_product = db.products
        self.collection_product = collection_product

    def patch_product(self, product_id: str, data: PatchProduct) -> SavedProduct:
        query = {"id": product_id}
        payload = {"$set": {"price": data.price, "title": data.title}}
        result = self.collection_product.update_one(query, payload)
        if result.modified_count != 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )
        return self.get_product(product_id)

    def create_product(self, new_product: NewProduct) -> SavedProduct:
        payload = {
            "title": new_product.title,
            "price": new_product.price,
            "description": new_product.description,
            "cover": new_product.cover,
            "id": uuid.uuid4().hex,
        }
        self.collection_product.insert_one(payload)
        saved_product = SavedProduct(**payload)
        return saved_product

    def get_product(self, product_id: str, with_raise: bool = True) -> SavedProduct:
        query = {"id": product_id}
        book = self.collection_product.find_one(query)
        if not book and not with_raise:
            return None

        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )
        return book

    def get_products(
        self, q: str = "", limit: int = 10, skip: int = 0
    ) -> list[SavedProduct]:
        query = {}
        if q:
            query = {
                "$or": [
                    {
                        "title": {
                            "$regex": q,
                            "$options": "i",
                        }
                    },
                    {
                        "description": {
                            "$regex": q,
                            "$options": "i",
                        }
                    },
                ]
            }
        flowers = self.collection_product.find(query).limit(limit).skip(skip)
        return flowers or []

    def delete_product(self, product_id: str) -> None:
        query = {"id": product_id}
        self.collection_product.delete_many(query)


storage: BaseStorage = MongoStorage(settings.MONGO_URI)
