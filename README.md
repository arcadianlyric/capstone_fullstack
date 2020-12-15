## Full Stack Capstone project: menu API backend

### Motivation
The menu app is used for resturants to post menu (price, food ingredients etc.) allowing public customers to check dish price and allergen in them.
A public user can send a get request to check all dish info, or a get request with the dish id, to get dish price, ingredients and allergens. 
A menager can do the same as public user and also send a delete request to remove some items from menu if the resturant decide to discontinue that product. 
A checf can do the same as manager and also post new dish on menu as well as update existing dishes. 

The endpoints and how to send requests to these endpoints are described in the 'Endpoints' session.

All endpoints need to be tested using postman as there is no frontend yet.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Running the server locally
To run the server
```
run.sh
```
go to  http://127.0.0.1:5000/  
'healty' indicates the app is up and running.  


### Test locally
Setup env variables, env variables in setup.sh. Test app and RBCA
```
source setup.sh

pytest test_app.py

pytest test_rbca.py
```

### Deploy on Heroku and tests
Create app on Heroku
```
heroku create menu-api101
git push heroku master
```

Setup config
```
heroku config:set AUTH0_DOMAIN="dev-4vns9i2p.us.auth0.com"
heroku config:set ALGORITHMS="RS256"
heroku config:set API_AUDIENCE="udacity-menu-cc"
...
```

Initiate database
```
heroku run python3 ./manage.py db init --app menu-api101
```

Test
```
heroku open
```
at https://menu-api101.herokuapp.com will also show 'healty'

A menu.postman_collection.json file is available for Postman tests. 

### API behavior and RBAC controls with Auth0
The menu app is a restuarant menu hosted on Heroku https://menu-api101.herokuapp.com with:  

3 roles: public, manager and chef  
public permission= read dish info
get /dish  
get /dish/dish_id
manager permission= public permission + delete dish
delete /dish/dish_id  
chef permission= manager permission + create new dishes and update them
post /dish
patch /dish/dish_id

Auth0 is used for authentication. The following configurations are in a setup.sh file to be used in auth.py:
- AUTH0_DOMAIN
- API_AUDIENCE
- ALGORITHMS
- TOKEN for public, manger and chef roles

2 tables as defined in models.py: dish and ingredient    
dish with id, name, price, indredients;  
indredient with id, name, allergen, associated dish id.  

### Endpoints
```
GET '/dish/<dish_id>'
- Fetches a dictionary of dish in which the keys are the ids and the value is the corresponding string of the dish
- Request: Arguments dish ID
- Return: 
An object with a single key, dish id, name, price,  ingrediets. 
Status
- Example: 
{
    "result": {
        "id": 1,
        "ingredient": [
            {
                "allergen": "seafood",
                "dish_id": 1,
                "id": 42,
                "name": "tuna"
            },
            {
                "allergen": "",
                "dish_id": 1,
                "id": 43,
                "name": "rice"
            }
        ],
        "name": "sushi",
        "price": 10
    },
    "success": true
}
```

```
GET '/dish'
Similar to GET '/dish/<dish_id>'; returns all dishes in the database.   
```

```
POST '/dish'
- Add new dish to the database  
- Request: Body of dish name, price, ingredients  
- Return: 
Body of dish plus id assigned to dish and ingredients  
Status
- Example:
{
    "result": {
        "id": 17,
        "ingredient": [
            {
                "allergen": "seafood",
                "dish_id": 17,
                "id": 44,
                "name": "salmon"
            },
            {
                "allergen": "",
                "dish_id": 17,
                "id": 45,
                "name": "rice"
            }
        ],
        "name": "sushi",
        "price": 15
    },
    "success": true
}
```

```
PATCH '/dish/<dish_id>'
- Update exsisting dish in the database  
- Request: Dish ID, body of new dish name, price, ingredients  
- Return: 
Body of updated dish    
Status
```

```
DELET '/dish/<int:dish_id>'
- Delect dish by id
- Request: dish_id
- Return: 
An object with deleted dish_id  
Status  
{
    "result": 6,
    "success": true
}
```

```
POST '/ingredient/search'
- Fetches dishes whose ingredients contain search term of allergen  
- Request: search term
- Return: 
An list of dishes match the search term  
Status  
- Example: search term = 'seafood'  
{
        {
            "id": 18,
            "ingredient": [
                {
                    "allergen": "seafood",
                    "dish_id": 18,
                    "id": 48,
                    "name": "eel"
                },
                {
                    "allergen": "",
                    "dish_id": 18,
                    "id": 49,
                    "name": "rice"
                }
            ],
            "name": "eel sushi",
            "price": 25
        },
        {
            "id": 19,
            "ingredient": [
                {
                    "allergen": "seafood",
                    "dish_id": 19,
                    "id": 50,
                    "name": "tuna"
                },
                {
                    "allergen": "",
                    "dish_id": 19,
                    "id": 51,
                    "name": "rice"
                }
            ],
            "name": "tuna sushi",
            "price": 15
        }
    ],
    "success": true
}
```

### TODO
frontend
