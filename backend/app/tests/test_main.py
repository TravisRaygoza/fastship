from httpx import AsyncClient
import pytest

### We have to create them into async context because the endpoints are async


@pytest.mark.asyncio
async def test_app(client: AsyncClient):
    response = await client.get("/")
    print("[Response]", response.json())
    assert response.status_code == 200