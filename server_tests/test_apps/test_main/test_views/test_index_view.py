

def test_main_page(client):
    """This test ensures that main page works."""
    response = client.get('/api/')

    assert response.status_code == 200
    assert '/api/event/' in str(response.content)
