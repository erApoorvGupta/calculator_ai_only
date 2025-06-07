from fastapi import FastAPI, HTTPException
import math # New import

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

# Scientific Calculator Functions

def power(base: float, exponent: float) -> float:
    try:
        return math.pow(base, exponent)
    except ZeroDivisionError: # Handles base=0 and exponent<0
        raise HTTPException(status_code=400, detail="Cannot raise zero to a negative power")
    except ValueError as e: # Handles other specific math domain errors if any from pow
        raise HTTPException(status_code=400, detail=str(e))

def square_root(number: float) -> float:
    if number < 0:
        raise HTTPException(status_code=400, detail="Cannot calculate square root of a negative number")
    return math.sqrt(number)

def ln(number: float) -> float: # Natural logarithm
    if number <= 0:
        raise HTTPException(status_code=400, detail="Natural logarithm is undefined for non-positive numbers")
    return math.log(number)

def log10(number: float) -> float: # Base-10 logarithm
    if number <= 0:
        raise HTTPException(status_code=400, detail="Base-10 logarithm is undefined for non-positive numbers")
    return math.log10(number)

def get_pi() -> float:
    return math.pi

def sine(angle_radians: float) -> float:
    return math.sin(angle_radians)

def cosine(angle_radians: float) -> float:
    return math.cos(angle_radians)

def tangent(angle_radians: float) -> float:
    # tan(pi/2 + k*pi) is undefined.
    # We need to check if angle_radians is close to pi/2, 3pi/2, etc.
    # A simple check for exact multiples of pi/2 where cos is zero.
    # Must use abs_tol when comparing to zero.
    if math.isclose(math.cos(angle_radians), 0, abs_tol=1e-9):
        raise HTTPException(status_code=400, detail="Tangent is undefined for angles where cos is zero (e.g., pi/2, 3pi/2)")
    return math.tan(angle_radians)

def reciprocal(number: float) -> float:
    if number == 0:
        raise HTTPException(status_code=400, detail="Cannot calculate reciprocal of zero")
    return 1 / number

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

# Scientific Calculator API Endpoints

@app.get("/power")
async def api_power(base: float, exponent: float):
    result = power(base, exponent) # This function now raises HTTPException directly
    return {"base": base, "exponent": exponent, "operation": "power", "result": result}

@app.get("/sqrt")
async def api_square_root(number: float):
    result = square_root(number) # Raises HTTPException
    return {"number": number, "operation": "square_root", "result": result}

@app.get("/ln")
async def api_ln(number: float):
    result = ln(number) # Raises HTTPException
    return {"number": number, "operation": "natural_logarithm", "result": result}

@app.get("/log10")
async def api_log10(number: float):
    result = log10(number) # Raises HTTPException
    return {"number": number, "operation": "base10_logarithm", "result": result}

@app.get("/pi")
async def api_get_pi():
    result = get_pi()
    return {"operation": "pi_constant", "result": result}

@app.get("/sine")
async def api_sine(angle: float): # Assuming angle is in radians as per function def
    result = sine(angle)
    return {"angle_radians": angle, "operation": "sine", "result": result}

@app.get("/cosine")
async def api_cosine(angle: float): # Assuming angle is in radians
    result = cosine(angle)
    return {"angle_radians": angle, "operation": "cosine", "result": result}

@app.get("/tangent")
async def api_tangent(angle: float): # Assuming angle is in radians
    result = tangent(angle) # Raises HTTPException
    return {"angle_radians": angle, "operation": "tangent", "result": result}

@app.get("/reciprocal")
async def api_reciprocal(number: float):
    result = reciprocal(number) # Raises HTTPException
    return {"number": number, "operation": "reciprocal", "result": result}
