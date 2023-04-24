from fastapi import FastAPI
from cards import routers as cards_routers
import uvicorn
from database import engine
from cards import models
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cards_routers.router)


if __name__ == "__main__":
    uvicorn.run(app=app, host="web", port=8000)
