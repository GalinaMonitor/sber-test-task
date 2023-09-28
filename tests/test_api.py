from datetime import datetime
from time import sleep

import pytest
from httpx import AsyncClient


@pytest.mark.dependency()
async def test_add_urls_and_get_domains(client: AsyncClient):
    # Add urls
    response = await client.post(
        "/visited_links",
        json=["https://example1.com", "https://example2.com", "https://example3.com"],
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["status"] == "ok"

    # Get domain list
    response = await client.get(
        "/visited_domains",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["domains"] == ["example1.com", "example2.com", "example3.com"]


async def test_negative_add_urls(client: AsyncClient):
    response = await client.post(
        "/visited_links",
        json=["example.com/", "ht://w", "https://"],
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert (
        data["status"][0][0]["msg"]
        == "Input should be a valid URL, relative URL without a base"
    )
    assert data["status"][0][1]["msg"] == "URL scheme should be 'http' or 'https'"
    assert data["status"][0][2]["msg"] == "Input should be a valid URL, empty host"


@pytest.mark.dependency(depends=["test_add_urls_and_get_domains"])
async def test_add_urls_and_get_domains_with_filters(client: AsyncClient):
    # Add urls
    response = await client.post(
        "/visited_links",
        json=["https://example1.com", "https://example2.com", "https://example3.com"],
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["status"] == "ok"

    sleep(1)

    # Add urls with timestamp fix
    timestamp_from = int(datetime.now().timestamp())
    response = await client.post(
        "/visited_links",
        json=["https://example3.com", "https://example4.com", "https://example5.com"],
    )
    timestamp_to = int(datetime.now().timestamp()) + 1
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["status"] == "ok"

    # Get domain list with filter
    response = await client.get(
        f"/visited_domains?from={timestamp_from}&to={timestamp_to}",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["domains"] == ["example3.com", "example4.com", "example5.com"]
