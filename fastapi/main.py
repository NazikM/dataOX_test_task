from fastapi import FastAPI
import uvicorn

from api import real_estate

app = FastAPI()


def configure():
    configure_routing()


def configure_routing():
    app.include_router(real_estate.router)


if __name__ == "__main__":
    configure()
    uvicorn.run(app, host='localhost', port=8000)
else:
    configure()
