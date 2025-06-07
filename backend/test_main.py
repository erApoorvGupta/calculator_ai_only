import sys
import os
# Add the backend directory to sys.path to allow imports from main
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import math # Ensure math is imported
import pytest
import pytest_asyncio # Import pytest_asyncio
from httpx import AsyncClient, ASGITransport # Import ASGITransport
from main import app # Import your FastAPI app

# Mark all tests in this module as async
pytestmark = pytest.mark.asyncio

@pytest_asyncio.fixture(scope="module")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000") as ac:
        yield ac

async def test_read_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Calculator API is running!"}

@pytest.mark.parametrize("x, y, expected_result", [
    (5, 3, 8.0),
    (-1, 1, 0.0),
    (0, 0, 0.0),
    (1.5, 2.5, 4.0),
])
async def test_api_add(client: AsyncClient, x: float, y: float, expected_result: float):
    response = await client.get(f"/add?x={x}&y={y}")
    assert response.status_code == 200
    data = response.json()
    assert data["x"] == x
    assert data["y"] == y
    assert data["operation"] == "addition"
    assert data["result"] == expected_result

@pytest.mark.parametrize("x, y, expected_result", [
    (10, 3, 7.0),
    (-1, -1, 0.0),
    (0, 5, -5.0),
    (5.5, 2.5, 3.0),
])
async def test_api_subtract(client: AsyncClient, x: float, y: float, expected_result: float):
    response = await client.get(f"/subtract?x={x}&y={y}")
    assert response.status_code == 200
    data = response.json()
    assert data["x"] == x
    assert data["y"] == y
    assert data["operation"] == "subtraction"
    assert data["result"] == expected_result

@pytest.mark.parametrize("x, y, expected_result", [
    (5, 3, 15.0),
    (-2, 4, -8.0),
    (0, 100, 0.0),
    (1.5, 2.0, 3.0),
])
async def test_api_multiply(client: AsyncClient, x: float, y: float, expected_result: float):
    response = await client.get(f"/multiply?x={x}&y={y}")
    assert response.status_code == 200
    data = response.json()
    assert data["x"] == x
    assert data["y"] == y
    assert data["operation"] == "multiplication"
    assert data["result"] == expected_result

@pytest.mark.parametrize("x, y, expected_result", [
    (10, 2, 5.0),
    (-6, 3, -2.0),
    (0, 5, 0.0),
    (7.5, 2.5, 3.0),
])
async def test_api_divide_valid(client: AsyncClient, x: float, y: float, expected_result: float):
    response = await client.get(f"/divide?x={x}&y={y}")
    assert response.status_code == 200
    data = response.json()
    assert data["x"] == x
    assert data["y"] == y
    assert data["operation"] == "division"
    assert data["result"] == expected_result

async def test_api_divide_by_zero(client: AsyncClient):
    response = await client.get("/divide?x=10&y=0")
    assert response.status_code == 400
    assert response.json() == {"detail": "Cannot divide by zero"}

@pytest.mark.parametrize("endpoint", ["add", "subtract", "multiply", "divide"])
@pytest.mark.parametrize("x_val, y_val", [
    ("abc", "5"), # Non-numeric x
    ("5", "xyz"), # Non-numeric y
    ("foo", "bar"),# Both non-numeric
])
async def test_api_invalid_input_types(client: AsyncClient, endpoint: str, x_val: str, y_val: str):
    response = await client.get(f"/{endpoint}?x={x_val}&y={y_val}")
    assert response.status_code == 422 # FastAPI's default for validation errors
    # We can also check the detail if needed, but status code is often enough
    # Example: assert "value is not a valid float" in response.json()["detail"][0]["msg"]

# Tests for Scientific API Endpoints

@pytest.mark.parametrize("base, exponent, expected_result", [
    (2, 3, 8.0),
    (4, 0.5, 2.0),
    (5, -2, 0.04),
    (10, 0, 1.0),
    (2.5, 2, 6.25),
])
async def test_api_power_valid(client: AsyncClient, base: float, exponent: float, expected_result: float):
    response = await client.get(f"/power?base={base}&exponent={exponent}")
    assert response.status_code == 200
    data = response.json()
    assert data["base"] == base
    assert data["exponent"] == exponent
    assert data["operation"] == "power"
    assert math.isclose(data["result"], expected_result)

@pytest.mark.parametrize("base, exponent, status_code, detail_substring", [
    (0, -1, 400, "math domain error"), # math.pow(0,-1) raises ValueError: math domain error
    (-2, 0.5, 400, "math domain error"), # math.pow(-2, 0.5) raises ValueError: math domain error
])
async def test_api_power_invalid(client: AsyncClient, base: float, exponent: float, status_code: int, detail_substring: str):
    response = await client.get(f"/power?base={base}&exponent={exponent}")
    assert response.status_code == status_code
    assert detail_substring in response.json()["detail"]

@pytest.mark.parametrize("number, expected_result", [
    (9, 3.0),
    (2, math.sqrt(2)),
    (0, 0.0),
    (1.44, 1.2),
])
async def test_api_sqrt_valid(client: AsyncClient, number: float, expected_result: float):
    response = await client.get(f"/sqrt?number={number}")
    assert response.status_code == 200
    data = response.json()
    assert data["number"] == number
    assert data["operation"] == "square_root"
    assert math.isclose(data["result"], expected_result)

async def test_api_sqrt_invalid(client: AsyncClient):
    response = await client.get("/sqrt?number=-1")
    assert response.status_code == 400
    assert "Cannot calculate square root of a negative number" in response.json()["detail"]

# --- Tests for ln ---
@pytest.mark.parametrize("number, expected_result", [
    (math.e, 1.0),
    (1, 0.0),
    (10, math.log(10)),
])
async def test_api_ln_valid(client: AsyncClient, number: float, expected_result: float):
    response = await client.get(f"/ln?number={number}")
    assert response.status_code == 200
    data = response.json()
    assert data["number"] == number
    assert data["operation"] == "natural_logarithm"
    assert math.isclose(data["result"], expected_result)

@pytest.mark.parametrize("number, status_code, detail_substring", [
    (0, 400, "Natural logarithm is undefined for non-positive numbers"),
    (-1, 400, "Natural logarithm is undefined for non-positive numbers"),
])
async def test_api_ln_invalid(client: AsyncClient, number: float, status_code: int, detail_substring: str):
    response = await client.get(f"/ln?number={number}")
    assert response.status_code == status_code
    assert detail_substring in response.json()["detail"]

# --- Tests for log10 ---
@pytest.mark.parametrize("number, expected_result", [
    (100, 2.0),
    (1, 0.0),
    (0.1, -1.0),
])
async def test_api_log10_valid(client: AsyncClient, number: float, expected_result: float):
    response = await client.get(f"/log10?number={number}")
    assert response.status_code == 200
    data = response.json()
    assert data["number"] == number
    assert data["operation"] == "base10_logarithm"
    assert math.isclose(data["result"], expected_result)

@pytest.mark.parametrize("number, status_code, detail_substring", [
    (0, 400, "Base-10 logarithm is undefined for non-positive numbers"),
    (-10, 400, "Base-10 logarithm is undefined for non-positive numbers"),
])
async def test_api_log10_invalid(client: AsyncClient, number: float, status_code: int, detail_substring: str):
    response = await client.get(f"/log10?number={number}")
    assert response.status_code == status_code
    assert detail_substring in response.json()["detail"]

# --- Test for pi ---
async def test_api_get_pi(client: AsyncClient):
    response = await client.get("/pi")
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "pi_constant"
    assert math.isclose(data["result"], math.pi)

# --- Tests for sine ---
@pytest.mark.parametrize("angle_radians, expected_result", [
    (0, 0.0),
    (math.pi / 2, 1.0),
    (math.pi, 0.0),
    (math.pi / 6, 0.5),
])
async def test_api_sine_valid(client: AsyncClient, angle_radians: float, expected_result: float):
    response = await client.get(f"/sine?angle={angle_radians}")
    assert response.status_code == 200
    data = response.json()
    assert data["angle_radians"] == angle_radians
    assert data["operation"] == "sine"
    assert math.isclose(data["result"], expected_result, abs_tol=1e-9)

# --- Tests for cosine ---
@pytest.mark.parametrize("angle_radians, expected_result", [
    (0, 1.0),
    (math.pi / 2, 0.0),
    (math.pi, -1.0),
    (math.pi / 3, 0.5),
])
async def test_api_cosine_valid(client: AsyncClient, angle_radians: float, expected_result: float):
    response = await client.get(f"/cosine?angle={angle_radians}")
    assert response.status_code == 200
    data = response.json()
    assert data["angle_radians"] == angle_radians
    assert data["operation"] == "cosine"
    assert math.isclose(data["result"], expected_result, abs_tol=1e-9)

# --- Tests for tangent ---
@pytest.mark.parametrize("angle_radians, expected_result", [
    (0, 0.0),
    (math.pi / 4, 1.0),
])
async def test_api_tangent_valid(client: AsyncClient, angle_radians: float, expected_result: float):
    response = await client.get(f"/tangent?angle={angle_radians}")
    assert response.status_code == 200
    data = response.json()
    assert data["angle_radians"] == angle_radians
    assert data["operation"] == "tangent"
    assert math.isclose(data["result"], expected_result, abs_tol=1e-9)

@pytest.mark.parametrize("angle_radians, status_code, detail_substring", [
    (math.pi / 2, 400, "Tangent is undefined for angles where cos is zero"),
    (3 * math.pi / 2, 400, "Tangent is undefined for angles where cos is zero"),
])
async def test_api_tangent_invalid(client: AsyncClient, angle_radians: float, status_code: int, detail_substring: str):
    response = await client.get(f"/tangent?angle={angle_radians}")
    assert response.status_code == status_code
    assert detail_substring in response.json()["detail"]

# --- Tests for reciprocal ---
@pytest.mark.parametrize("number, expected_result", [
    (2, 0.5),
    (-4, -0.25),
    (0.1, 10.0),
])
async def test_api_reciprocal_valid(client: AsyncClient, number: float, expected_result: float):
    response = await client.get(f"/reciprocal?number={number}")
    assert response.status_code == 200
    data = response.json()
    assert data["number"] == number
    assert data["operation"] == "reciprocal"
    assert math.isclose(data["result"], expected_result)

async def test_api_reciprocal_invalid(client: AsyncClient):
    response = await client.get("/reciprocal?number=0")
    assert response.status_code == 400
    assert "Cannot calculate reciprocal of zero" in response.json()["detail"]

# --- Tests for invalid input types for scientific functions ---
@pytest.mark.parametrize("endpoint", [
    "sqrt", "ln", "log10", "sine", "cosine", "tangent", "reciprocal"
])
@pytest.mark.parametrize("value", ["abc", "xyz"]) # Invalid non-float values
async def test_api_scientific_single_param_invalid_type(client: AsyncClient, endpoint: str, value: str):
    param_name = "angle" if endpoint in ["sine", "cosine", "tangent"] else "number"
    response = await client.get(f"/{endpoint}?{param_name}={value}")
    assert response.status_code == 422

async def test_api_power_invalid_type(client: AsyncClient):
    invalid_params = [
        ("abc", "5"),
        ("5", "xyz"),
        ("foo", "bar")
    ]
    for x_val, y_val in invalid_params:
        response = await client.get(f"/power?base={x_val}&exponent={y_val}")
        assert response.status_code == 422
