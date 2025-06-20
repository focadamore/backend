from typing import Optional

from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()
hotels = [
    {"id": 1, "title": "Дубай", "name": "Dubai"},
    {"id": 2, "title": "Сочи", "name": "Sochi"},
]


@app.get("/")
def func():
    """return hello"""
    return {"title": "Hello page"}


@app.delete("/hotels/{hotel_id}")
def delete_hotel(id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != id]
    return {"status": "OK"}


@app.put("/hotels/{hotel_id}")
def change_hotel(id: int,
                 title: str = Body(embed=True),
                 name: str = Body(embed=True)
                 ):
    for hotel in hotels:
        if hotel["id"] == id:
            hotel["title"] = title
            hotel["name"] = name
            return {"status": "OK"}
        return {"status": "404 - Not Found"}


@app.patch("/hotels/{hotel_id}")
def change_hotel_lightly(id: int,
                         title: Optional[str] = Body(None, embed=True),
                         name: Optional[str] = Body(None, embed=True)
                         ):
    for hotel in hotels:
        if hotel["id"] == id:
            hotel["title"] = title or hotel["title"]
            hotel["name"] = name or hotel["name"]
            return {"status": "OK"}
        return {"status": "404 - Not Found"}


@app.get("/hotels")
def get_hotels(title: str = Query("Сочи", description="Название города")):
    return [hotel for hotel in hotels]
    # return [hotel for hotel in hotels if hotel["title"] == title]


@app.post("/hotels")
def add_hotel(title: str = Body(embed=True)):
    hotels.append(
        {
            "id": hotels[-1]["id"] + 1,
            "title": title
        }
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
