from fastapi import FastAPI, HTTPException

app = FastAPI()

# Calculator logic
def add(x: float, y: float) -> float:
    return x + y

def subtract(x: float, y: float) -> float:
    return x - y

def multiply(x: float, y: float) -> float:
    return x * y

def divide(x: float, y: float) -> float:
    if y == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    return x / y

@app.get("/")
async def read_root():
    return {"message": "Calculator API is running!"}

@app.get("/add")
async def api_add(x: float, y: float):
    result = add(x, y)
    return {"x": x, "y": y, "operation": "addition", "result": result}

@app.get("/subtract")
async def api_subtract(x: float, y: float):
    result = subtract(x, y)
    return {"x": x, "y": y, "operation": "subtraction", "result": result}

@app.get("/multiply")
async def api_multiply(x: float, y: float):
    result = multiply(x, y)
    return {"x": x, "y": y, "operation": "multiplication", "result": result}

@app.get("/divide")
async def api_divide(x: float, y: float):
    # The divide function itself now raises HTTPException
    result = divide(x, y)
    return {"x": x, "y": y, "operation": "division", "result": result}
