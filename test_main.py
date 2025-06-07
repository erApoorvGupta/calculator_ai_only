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
