import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_create_comment():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/comments/",
            json={"post_id": 1, "content": "Nice post!"},
            headers={"Authorization": "Bearer 1"}
        )
    assert response.status_code == 200
    assert response.json()["content"] == "Nice post!"