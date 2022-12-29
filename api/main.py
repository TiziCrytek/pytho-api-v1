from fastapi import FastAPI

app = FastAPI()


@app.get("/user/{id}")
async def root(id: int, options: str = None):
    return {"id": id, "options": options}