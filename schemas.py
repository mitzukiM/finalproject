from pydantic import BaseModel, Field, HttpUrl, AnyUrl


class PatchProduct(BaseModel):
    price: float = Field(ge=0.01, lt=10000, examples=[125, 325])
    title: str = Field(
        min_length=3,
        examples=[
            "Ця квітка не лише красива, але й корисна"
        ],
    )


class NewProduct(PatchProduct):

    description: str = Field(
        min_length=20,
        max_length=1024,
        examples=[
            "Ромашка – це ніжна квітка з білими пелюстками, що оточують яскраво-жовту серцевину. Її тонкий аромат"
            " наповнює повітря свіжістю та спокоєм. Ромашка росте на луках, полях та узбіччях доріг, створюючи "
            "мальовничі килими."
        ],
    )
    cover: str = Field(
        examples=[
            "https://sens.in.ua/content/images/25/76x110l80nn0/toi-khto-poliubyt-tebe-u-vsii-tvoii-zhaliuhidnii-slavi-72965851471885.webp"
        ]
    )


class ProductId(BaseModel):
    id: str


class SavedProduct(ProductId, NewProduct):
    pass
