## Full Stack Capstone project

### Goals
The api is a restuarant menu with:  

2 tables: dish and ingredient    
dish with id, name, price, indredients;  
indredient with id, name, allergen, associated dish id.  

3 roles: public, manager and chef  
public permission= view menu dish to leanr price, ingradients and allergens; get dish by searching allergen;  
  
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
GET '/dish'
- Fetches a dictionary of dish in which the keys are the ids and the value is the corresponding string of the dish
- Request Arguments: None
- Returns: An object with a single key, dish, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

```
POST '/dish'
- Randomly select a question in a category that is not included in previous ingredient as a quizz
- Request category_id 
- Return selected question, status
{
    "ingredient": 
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
    "success": True
}
```

```
GET '/ingredient'
- Fetch all ingredient
- Request Arguments: None
- Return An object with ingredient, total ingredient, dish. 
{
    "dish": {
        "1": "science",
        "2": "art",
        "3": "geography",
        "4": "history",
        "5": "entertainment",
        "6": "sports"
    },
    "ingredient": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        ...
    ],
    "total_ingredient": 43
}
```

```
DELET '/ingredient/<int:question_id>'
- Delect ingredient by id
- Request question_id
- Return an object with deleted question_id and status if successful 
{
    "deleted_question": 6,
    "success": true
}
```

```
POST '/ingredient'
- Add a new question
- Request
new_question = {
            "question": "What is the 5th element ?",
            "answer": "B",
            "difficulty": 1,
            "category": 1
        }
- Return created new question id, total_ingredient, paginated ingredient, status
{
    "created": 48,
    "ingredient": [
        42,
        [
            {
                "answer": "Apollo 13",
                "category": 5,
                "difficulty": 4,
                "id": 2,
                "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
            },
            ...
        ]
    ],
    "success": true,
    "total_ingredient": 42
}
```

```
POST '/ingredient/search'
- Fetches ingredient that match search term
- Request search term
- Return an object of ingredient match the search term, total_ingredient, status
{
    'ingredient': [{
    'answer': 'Edward Scissorhands', 
    'category': 5, 
    'difficulty': 3, 
    'id': 6, 
    'question': 'What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?'
    }], 
    'success': True, 
    'total_ingredient': 1
    }
```

```
GET '/dish/<int:category_id>/ingredient'
- Fetch ingredient by category_id
- Request category_id
- Return all ingredient in the category
{
    "ingredient": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        ...
}
```


### TODO
frontend  