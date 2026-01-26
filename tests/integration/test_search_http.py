def test_search_nota_ri_via_http(client, session_factory):
    from tests.integration.seed_nota_ri import seed_nota_ri

    seed_nota_ri(session_factory)

    response = client.get(
        "/api/nota_ri/search",
        params={"q": "bomba", "limit": 10},
    )

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1

    item = data[0]

    assert "item" in item
    assert "score" in item
    assert "highlight" in item

    entity = item["item"]

    assert entity["num_ri"] == "20041742"
    assert "bomba" in item["highlight"].lower()
    assert item["score"] > 0
