from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from rebrickable_utils import find_buildable_sets

app = FastAPI()

class UserSetsInput(BaseModel):
    owned_sets: List[str]  # e.g., ["10265-1", "75192-1"]

@app.post("/buildable-sets")
def get_buildable_sets(data: UserSetsInput):
    try:
        results = find_buildable_sets(data.owned_sets, page_limit=5)
        return {"buildable_sets": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
