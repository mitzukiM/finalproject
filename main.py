from fastapi import FastAPI, status, Request, Form
from fastapi.templating import Jinja2Templates

from schemas import NewProduct, SavedProduct, PatchProduct
from storage.base_storage import storage


app = FastAPI()
templates = Jinja2Templates(directory="templates")


# WEB
@app.get("/")
@app.post("/")
def index(request: Request, q: str = Form(default="")):
    flowers = storage.get_products(q=q)
    context = {"request": request, "flowers": flowers}
    return templates.TemplateResponse(
        "index.html",
        context=context,
    )


@app.get("/map_route")
def map_route(request: Request):

    context = {"request": request}
    return templates.TemplateResponse(
        "map.html",
        context=context,
    )


@app.get("/video")
def video(request: Request):

    context = {"request": request}
    return templates.TemplateResponse(
        "video.html",
        context=context,
    )


@app.get("/{product_id}")
def get_flower_info(request: Request, product_id: str):
    flower = storage.get_product(product_id=product_id, with_raise=False)
    if not flower:
        return templates.TemplateResponse(
            "404.html",
            context={"request": request},
        )

    context = {"request": request, "flower": flower}
    return templates.TemplateResponse(
        "details.html",
        context=context,
    )


# API
@app.post("/flowers/", tags=["Квіти"], status_code=status.HTTP_201_CREATED)
def create_flower(new_flower: NewProduct) -> SavedProduct:
    product = storage.create_product(new_flower)
    return product


@app.get("/flowers/{flower_id}")
def get_flower(flower_id: str) -> SavedProduct:
    flower = storage.get_product(flower_id)
    return flower


@app.get("/flowers/")
def get_flowers(query: str = "", limit: int = 10, skip: int = 0) -> list[SavedProduct]:
    flowers = storage.get_products(q=query, limit=limit, skip=skip)
    return flowers


@app.patch("/flowers/{flower_id}")
def flower_book(flower_id: str, data: PatchProduct) -> SavedProduct:
    product = storage.patch_product(flower_id, data)
    return product


@app.delete("/flowers/{flower_id}")
def delete_flower(flower_id: str) -> dict:
    storage.delete_product(flower_id)
    return {}
