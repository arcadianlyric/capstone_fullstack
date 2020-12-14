## Full Stack Capstone project

#### Goals
The api is a restuarant menu with:  
2 tables: dish and ingredient  
3 roles: public, manager and chef  
public can only view menu dish to leanr price, ingradients and possible allergens;  
manager can view and delete menu dish;  
chef can view and delete as well as create new dishes and update them.  


#### Setup
Create a virtual env for the project  
```bash
conda create -n your_env 
```

Install dependencies  
```bash
pip install -r requirements.txt
```

Setup env variables  
```bash
source setup.sh
```

#### Test on local
Start the app
```bash
bash run.sh
```
then go to  http://127.0.0.1:5000/  
will show 'healty' 

Test app and RBCA
```bash
pytest test_app.py

pytest test_rbca.py
```

#### Deploy on Heroku
Create app on Heroku
```bash
heroku create menu-api101
git push heroku master
```

Setup config
```bash
heroku config:set AUTH0_DOMAIN="dev-4vns9i2p.us.auth0.com"
heroku config:set ALGORITHMS="RS256"
heroku config:set API_AUDIENCE="udacity-menu-cc"
...
```

Initiate database
```bash
heroku run python3 ./manage.py db init --app menu-api101
```

Test
```bash
heroku open
```
will also show 'healty'

A menu.postman_collection.json file is available for Postman tests. 

#### Endpoints
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
GET '/questions'
- Fetch all questions
- Request Arguments: None
- Return An object with questions, total questions, dish. 
{
    "dish": {
        "1": "science",
        "2": "art",
        "3": "geography",
        "4": "history",
        "5": "entertainment",
        "6": "sports"
    },
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        ...
    ],
    "total_questions": 43
}
```

```
DELET '/questions/<int:question_id>'
- Delect questions by id
- Request question_id
- Return an object with deleted question_id and status if successful 
{
    "deleted_question": 6,
    "success": true
}
```

```
POST '/questions'
- Add a new question
- Request
new_question = {
            "question": "What is the 5th element ?",
            "answer": "B",
            "difficulty": 1,
            "category": 1
        }
- Return created new question id, total_questions, paginated questions, status
{
    "created": 48,
    "questions": [
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
    "total_questions": 42
}
```

```
POST '/questions/search'
- Fetches questions that match search term
- Request search term
- Return an object of questions match the search term, total_questions, status
{
    'questions': [{
    'answer': 'Edward Scissorhands', 
    'category': 5, 
    'difficulty': 3, 
    'id': 6, 
    'question': 'What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?'
    }], 
    'success': True, 
    'total_questions': 1
    }
```

```
GET '/dish/<int:category_id>/questions'
- Fetch questions by category_id
- Request category_id
- Return all questions in the category
{
    "questions": [
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

```
POST '/quizzes'
- Randomly select a question in a category that is not included in previous questions as a quizz
- Request category_id 
- Return selected question, status
{
    "questions": 
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



## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```