# Full Stack Trivia API Backend

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

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## Endpoints

#### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
```
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```

#### GET '/questions'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Fetches a list of questions. Questions are paginated, if no argument for page is given, the first page is returned. Default: 10 questions per page.
- Request Arguments: None
- Returns: A JSON object with four keys:
  - categories, that contains an object of id: category_string key:value pairs
  - questions, that contain a list of dictionaries of question: text of a question, answer: text of an answer, category: category_id, difficulty: difficulty level, id: id of a question
  - success, that is a boolean of whether a request is successful or not (True/False)
  - total_questions, that is an integer giving a total number of questions in the trivia game
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
        ...
        }
    ],
    "success": true,
    "total_questions": 21
}  
```
#### GET '/categories/<int:category_id>/questions'
- Fetches a dictionary with all questions that fall into the provided category_id
- Request Arguments: category_id (integer)
- Returns: A JSON object with three keys:
  - questions, that contain a list of dictionaries of question: text of a question, answer: text of an answer, category: category_id, difficulty: difficulty level, id: id of a question
  - success, that is a boolean of whether a request is successful or not (True/False)
  - total_questions, that is an integer giving a total number of questions in the trivia game
```
{
    "questions": [
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
        ...
          }
    ],
    "success": true,
    "total_questions": 4
```

#### POST '/questions'
- Adds a new question to the Trivia game
- Request Body: A JSON object of the following type (example):
```
{
    "question": "When do you like to go to gym?",
    "answer": "19815",
    "category": 1,
    "difficulty": 4
}
```
- Returns: if the request is correct one gets the following JSON object with `id` of the question added and `success = True` 
```
{
    "id": 71,
    "success": true
}
```
#### POST '/questions'
- Notice that the same endpoint/request also allows to use the search field to search for any text field among all questions in the database.
- Request Body: Should include a dictionary "searchTerm: {{text}}". Example:
```
{
    "searchTerm":"what"
}
```
- Returns: A JSON object with all questions containing the `searchTerm`, request status and total number of questions.
```

    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
        ...
        }
    ],
    "success": true,
    "total_questions": 8
}
```

#### POST '/quizzes'
- Fetches a new question in the Trivia game for a given category
- Request Body: One needs to choose category ("Science") and provide an `id` of a question. It is possible also to add IDs into `previous_questions` list. That way a new question will be chosen among those that fall into the "Science" category and are not present in the `previous_questions` list.
```
{
    "previous_questions": [],
    "quiz_category": 
    {
        "type": "Science",
        "id": 1
    }
}
```

#### DELETE '/questions/<int:question_id>'
- Deletes a question with a given id from the database.
- Request Arguemnt: question_id
- Returns: A JSON object with the status of the request (`success` is true or not) and the `id` of the deleted question.
```
{
    "question_id": 68,
    "success": true
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
