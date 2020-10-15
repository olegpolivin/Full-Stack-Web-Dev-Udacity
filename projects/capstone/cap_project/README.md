# Education Online App API Backend
## Getting started
### Installing dependencies

I recommend using `Anaconda` to create a virtual environment, and next run the necessary dependencies:
```
pip install -r requirements.txt
```

## Database Setup
With Postgres running, restore a database using the `EducationOnlineDB.psql` file provided. From the `cap_project` folder in terminal run:
```
psql EducationOnlineDB < EducationOnlineDB.psql
```

## Running the server
From within the `cap_project` directory first ensure you are working using your created virtual environment.
To run the server, execute:

```
python app.py
```

## Endpoints


## Testing
To run the tests, do the following:
```
dropdb EducationOnlineDBTest
createdb EducationOnlineDBTest
psql EducationOnlineDBTest < EducationOnlineDB.psql
python test_app.py
```
