from fastapi import FastAPI
from src.utils import fetch_query,execute_query 
app = FastAPI()

@app.get("/")
async def home():
    return {"message":"Server is Live!"}

@app.get("/home/habits")
async def get_habits():
    s = fetch_query({})    
    return s

@app.get("/home/habits/{habit_id}")
async def get_habit_by_id(habit_id):
    s = fetch_query({"filters":{"id":{"op":"=","val":habit_id}}})
    return s

@app.post("/home/habits")
async def insert_habit(payload: dict):
    columns = ", ".join(payload.keys())
    placeholders = ", ".join(["?"] * len(payload))
    query = f"INSERT INTO habits ({columns}) VALUES ({placeholders})"
    execute_query(query, payload)
    return {"status": "success"}

