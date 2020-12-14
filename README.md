## Full Stack Capstone project

### Goals
The api is a restuarant menu hosted on Heroku https://menu-api101.herokuapp.com with:  

2 tables: dish and ingredient    
dish with id, name, price, indredients;  
indredient with id, name, allergen, associated dish id.  

3 roles: public, manager and chef  
public permission= view menu dish to leanr price, ingradients and allergens; search allergen to avoid some dishes;  
  
manager permission= public permission + delete menu dish;  
chef permission= manager permission + create new dishes and update them.  


### Setup
Create a virtual env for the project  
```
conda create -n your_env 
```

Install dependencies  
```
pip install -r requirements.txt
```

Setup env variables, env variables in setup.sh    
```
source setup.sh
```

### Test on local
Start the app
```
 run.sh
```
go to  http://127.0.0.1:5000/  
'healty' indicates the app is up and running.  

Test app and RBCA
```
pytest test_app.py

pytest test_rbca.py
```

### Deploy on Heroku
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
will also show 'healty'

A menu.postman_collection.json file is available for Postman tests. 

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