import os
import pytest
from test_app import client, test_data

# enable auth0
# os.environ["DISABLE_AUTH0"] = "0"
if os.environ.get("DISABLE_AUTH0"):
    del os.environ["DISABLE_AUTH0"]


MANAGER_TOKEN = os.environ["MANAGER_TOKEN"]
CHEF_TOKEN = os.environ["CHEF_TOKEN"]


@pytest.fixture
def manager_header():
    return {'Authorization': 'Bearer {}'.format(MANAGER_TOKEN)}


@pytest.fixture
def chef_header():
    return {'Authorization': 'Bearer {}'.format(CHEF_TOKEN)}


test_dish = {
        'name': 'sushi', 'price': 15,
        'ingredient': [{'name': 'salmon', 'allergen': 'seafood'},
                       {'name': 'rice', 'allergen': ''}]
    }


# test public, with get permission
def test_public_get_dish(client):
    res = client.get('/dish/1')
    assert res.status_code == 200
    dish = res.json['result']
    assert dish['name'] == 'pizza'
    assert [i['name'] for i in dish['ingredient']] == ['tomato', 'cheese', 'flour']


def test_public_post_dish_unauthorized(client, test_dish):
    res = client.post('/dish', json=test_dish)
    assert res.status_code == 401


def test_public_delete_dish(client):
    res = client.delete('/dish/1')
    assert res.status_code == 401


# test manager, with get, delete permission
def test_manager_get_dish(client):
    res = client.get('/dish/1')
    assert res.status_code == 200
    dish = res.json['result']
    assert dish['name'] == 'pizza'
    assert [i['name'] for i in dish['ingredient']] == ['tomato', 'cheese', 'flour']


def test_manager_delete_dish(client, manager_header):
    res = client.delete('/dish/3', headers=manager_header)
    assert res.status_code == 200


def test_manager_post_dish_unauthorized(client, manager_header, test_dish):
    res = client.post('/dish', json=test_dish, headers=manager_header)
    assert res.status_code == 401


# test chef, with all permissions
def test_chef_get_dish(client):
    res = client.get('/dish/1')
    assert res.status_code == 200
    dish = res.json['result']
    assert dish['name'] == 'pizza'
    assert [i['name'] for i in dish['ingredient']] == ['tomato', 'cheese', 'flour']


def test_chef_delete_dish(client, chef_header):
    res = client.delete('/dish/2', headers=chef_header)
    assert res.status_code == 200


def test_chef_post_dish(client, chef_header, test_dish):
    res = client.post('/dish', json=test_dish, headers=chef_header)
    assert res.status_code == 200
