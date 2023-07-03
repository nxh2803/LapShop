import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import db

origins= [
    "http://localhost:3000"
]

def init_app():
    db.init()

    app = FastAPI(
        title= "App",
        description= "Login Page",
        version= "1"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    @app.on_event("startup")
    async def starup():
        await db.create_all()
    
    @app.on_event("shutdown")
    async def shutdown():
        await db.close()

    from app.controller import authentication, users, product, brand, cart_product, cart, order, invoice

    app.include_router(authentication.router)
    app.include_router(users.router)
    app.include_router(product.router)
    app.include_router(brand.router)
    app.include_router(cart.router)
    app.include_router(cart_product.router)
    app.include_router(order.router)
    app.include_router(invoice.router)

    return app

app = init_app()

def start():
    """Launched with 'poetry run start' at root level """
    uvicorn.run("app.main:app", host="localhost", port=8888, reload=True)