# Education Online App API Backend

## Motivation

This is a project that I worked on for the Udacity Full Stack Web Developer Nanodegree Program.
The code contains mostly backend and can be run locally (for testing, for example), but also deployed on the Heroku server. 

Here is the link to the application that is running on Heroku:
`https://education-online-app.herokuapp.com`.

The idea of the application is simple: provide a list of courses along with information on price, domain, duration and others that are available online. One can have a list of all courses or choose by domains. It is suggested that the application was used by three groups of users:

1. Students can consult courses, domains and see courses for a given domain.
2. Platforms that are interested in providing the courses can add new courses or add/modify platforms. Imagine a new platform appears and it wants to be added to the list, so it has the necessary rights to add and modify the data.
3. Admins of the application have all the rights to add, modify and delete data.

Below I provide the token to test the API on the heroku server. Since it is a backend-only application, I create my tokens using the `https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}` link.

1 - Student Token (actually, you do not need it, because what students can access is available without authentication):
`eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhBOFoxNG9kLUFUbVNPWFRMY1VmXyJ9.eyJpc3MiOiJodHRwczovL29ubGluZWVkdWNhdGlvbi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY4MzY2OGE4ZDI1YTIwMDc1YzhhOTNhIiwiYXVkIjoiQ291cnNlQW5kRG9tYWluIiwiaWF0IjoxNjAzMDg2NTUzLCJleHAiOjE2MDMxNzI5NTMsImF6cCI6InRFZXBtbjVKNkxtMmpJak5EUTJNbTE1R05oOXNHNXgwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6W119.K6uWDjqFVOowFjaR318UCpGmYMA9yv06IYqJc3FPkPRkCsurq0O7T5V8GN2SDc3xXWEM8_rBpBMrMuRlIdg0TmdEie45lzTwRkNlBiZWIHqletFtk6PkbTqJV3_ellQc7BNcfKg3RyEuqttiNwA8vLtKo4SpI96-XbNcSC1OpaWpS-SH0mklIKcBlEvqxwTXXZpbp9B9bfc_r3xwcwJEYgIq3Cjt-VMfvR8N1jYY5IwAz8JDCvWYi28VAtM8zoV-uKkn2F8V8DdGS_qnqjMc8YRQMHD67IermMnqKPlIzg7FKn6oa7rFVk9v5-DocxFL0fQErhzZ3RQZTqeKgvQhQw`

2 - Platform Token:
`eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhBOFoxNG9kLUFUbVNPWFRMY1VmXyJ9.eyJpc3MiOiJodHRwczovL29ubGluZWVkdWNhdGlvbi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY4MzcxZDg4ZDI1YTIwMDc1YzhjNzJmIiwiYXVkIjoiQ291cnNlQW5kRG9tYWluIiwiaWF0IjoxNjAzMDg2NTk2LCJleHAiOjE2MDMxNzI5OTYsImF6cCI6InRFZXBtbjVKNkxtMmpJak5EUTJNbTE1R05oOXNHNXgwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJwYXRjaDpkb21haW4iLCJwb3N0Om5ld19jb3Vyc2UiLCJwb3N0Om5ld19kb21haW4iXX0.GNgxiriwTV0ewXmNSBlvUyup2nBxKLyn2NkfHFUX-0DnDJQJMXHhFj96cHJ0ZvH1fBU9gFS5qVcwnPyIw_Sdvfu1xBWDL4YHwdzaZF521MR606xsokXcq7q1IoAuKwWoAFQncRO46twlc1vzEyk0jRYkfatARHxWJ259wsPkYcl8I-MZoEuDa6GxRuCfMhwMWPNJk95pM3_lRqqNkIImgPgVwNy7m-aD0zHUS2uHeYASBPZ039sG7Nsd6pM-Pnb-VsrYATBsJMWwJAPyntJ8hVKYiIIqUYG8p8m-PNtooujvRPiHhxsd8CpuT6ZGiC1NG0fxZqMtmgVkvcpUt6AU5w`

3 - Admin Token:
`eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhBOFoxNG9kLUFUbVNPWFRMY1VmXyJ9.eyJpc3MiOiJodHRwczovL29ubGluZWVkdWNhdGlvbi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY4NGFmNDg4MTAyZjcwMDc2NTgzNmM2IiwiYXVkIjoiQ291cnNlQW5kRG9tYWluIiwiaWF0IjoxNjAzMDg2NjM1LCJleHAiOjE2MDMxNzMwMzUsImF6cCI6InRFZXBtbjVKNkxtMmpJak5EUTJNbTE1R05oOXNHNXgwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Y291cnNlIiwiZGVsZXRlOmRvbWFpbiIsInBhdGNoOmRvbWFpbiIsInBvc3Q6bmV3X2NvdXJzZSIsInBvc3Q6bmV3X2RvbWFpbiJdfQ.Yz_dxZzRak9zGeRQUaRh7Ge3D_IUh3FL_zQNE8gXnWHt4i7CaeE8TDQVl1bOVBCZsYPvyCWk_6DyHy-K9Hnvh0QFrKgqib_5_i_BDX4DPK3dd6gi3BOC7mYmfEyH14b6eWh3yGMTtdOrHQsYYP06RmoHwvfx3GgzWgkPAPImYSASpVLdqTab0YC-7r_u31lphIkB1VdrWSR_CNPvhQPLPJ8ZYC3Ts6LiWBnEqhS0lkMEz7I3g7VrlEct8XrgmmeRxJx6ghjuoHXDLN2Jz18ioCieltJtUzBMZapLIab1urylCKjcpr6WTgLLurwgefaako0iMqwgJ0m8zdgu-OhRdw`

All information is contained in a postgres database that is located on the heroku server. All CRUD operations on the database are performed using the `FLASK` framework, and the API is described below. 

## Getting started locally
### Installing dependencies

I recommend using `Anaconda` to create a virtual environment, and next run the necessary dependencies:
```
pip install -r requirements.txt
```

## Local Database Setup
With Postgres running, restore a database using the `EducationOnlineDB.psql` file provided. From the `cap_project` folder in terminal run:
```
psql EducationOnlineDB < EducationOnlineDB.psql
```

## Running the server locally
From within the `cap_project` directory first ensure you are working using your created virtual environment.
To run the server, execute:

```
python app.py
```

## Heroku deployment
Here are the steps needed to deploy the application on the Heroku server.

1. `heroku create education-online-app`
2. `git remote add heroku heroku_git_url`
3. `git remote add heroku heroku_git_url`
4. `heroku addons:create heroku-postgresql:hobby-dev --app name_of_your_application`

`git push heroku master` didn't work for me, because my application is not in the root folder for git. So, I used:

5. `git subtree push --prefix projects/capstone/cap_project heroku master`
6. Setting up the database: `heroku run python manage.py db upgrade --app education-online-app`.

Then I followed the extremely helpful post from Amani A. on the `knowledge.udacity.com`:
```
https://knowledge.udacity.com/questions/173007.
I added this code at the end of app.py
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
2. I added DATABASE_URL from heroku instead of SQLALCHEMY_DATABASE_URI in models.py code
3. I installed gunicorn and added it in the requirements.txt through
    pip freeze > requirements.txt
4. I added this code to Procfile:
    web: gunicorn -b :$PORT app:app
5. I added all the environment variables in setup.sh including:
export AUTH0_DOMAIN=
export ALGORITHMS=
export DATABASE_URL=
6. run these in Git Bash :
    git add .
    git commit -m "initial commit"
    git push heroku master
7. run migrations:
    heroku run python manage.py db upgrade --app name_of_your_application
```

Finally, in order to populate the empty postgres database on the Heroku server, I performed the following steps:

1. Uploaded my locally created database to the server, EducationOnlineDB.psql
2. `heroku pg:psql DATABASE_URL --app education-online-app < EducationOnlineDB.psql`

where `DATABASE_URL` is an environment variable that I indicated my heroku account.

## Endpoints

#### GET '/'
- Fetches an index page of the application. It explains a bit what this application is for, and provides links for the `GET /courses` and `GET /domains` routes.
- Request Arguments: None
- Returns: An index page. 
```
Hello! This is an application where
<ul>
	<li>Students may consult online courses in various domains.</li>
	<li>Platforms may add and patch courses.</li>
	<li>Administrator may create, modify and delete courses and platforms.</li>
</ul>

<a href="/courses">See the list of available courses here.</a>
<br>
<a href="/domains">See the list of available domains here.</a>
```

#### GET '/courses'
- Fetches a dictionary of courses in the database
- Courses are paginated. If no argument for page is given, the first page is returned. Default: 10 courses per page.
- Request Arguments: None
- Returns: A JSON object with three keys:
  - courses, that contains an object of key-values pairs. The keys are as follows:
    - course_name: Name of the course in the application
    - domain_id: Id of the domain (corresponding to the one in the Domain table)
    - duration_month: Duration of the course in months
    - id: Id of the course in the database
    - platform_id: Id of the platform where one can find that course (corresponds to the one in the Platform table)
    - price_per_month: Price of the course per month
    - website: Link to the course
  - success, that is a boolean of whether a request is successful or not (True/False)
  - total_courses, that is an integer giving a total number of courses in the education-online application
```
{
    "courses": [
        {
            "course_name": "Algorithms",
            "domain_id": 1,
            "duration_months": 4,
            "id": 1,
            "platform_id": 1,
            "price_per_month": 0,
            "website": "https://www.coursera.org/specializations/algorithms"
        },
        {
        ...
        }

    ],
    "success": true,
    "total_courses": 10
}
```

#### GET '/domains'
- Fetches a dictionary of domains in the database
- Domains are paginated. If no argument for page is given, the first page is returned. Default: 5 domains per page.
- Request Arguments: None
- Returns: A JSON object with three keys:
  - domains, that contains an object of key-values pairs. The keys are as follows:
    - domain_name: Name of the domain in the application
    - id: Id of the domain in the Domain table
  - success, that is a boolean of whether a request is successful or not (True/False)
  - total_domains, that is an integer giving a total number of domains in the education-online application
```
{
    "domains": [
        {
            "domain_name": "Computer Science",
            "id": 1
        },
        {
            "domain_name": "Machine Learning",
            "id": 2
        },
        {
            "domain_name": "Data Analysis",
            "id": 5
        }
    ],
    "success": true,
    "total_domains": 3
}
```


#### GET '/domains/<int:domain_id>/courses'
- Fetches a dictionary with all courses that fall into the provided domain_id
- Request Arguments: domain_id (integer)
- Returns: A JSON object with two keys:
  - courses_for_domains, that contains objects of key-values pairs. The keys are as follows:
  - success, that is a boolean of whether a request is successful or not (True/False)
```
{
    "courses_for_domain": [
        {
            "course_name": "Convolutional Neural Networks for Visual Recognition",
            "domain_id": 2,
            "duration_months": 3,
            "id": 2,
            "platform_id": 4,
            "price_per_month": 0,
            "website": "http://cs231n.stanford.edu"
        },
        {
            "course_name": "Deep Learning Specialization",
            "domain_id": 2,
            "duration_months": 4,
            "id": 3,
            "platform_id": 1,
            "price_per_month": 41,
            "website": "https://www.coursera.org/specializations/deep-learning"
        },
        {
            "course_name": "Data Scientist Nanodegree",
            "domain_id": 2,
            "duration_months": 4,
            "id": 12,
            "platform_id": 2,
            "price_per_month": 400,
            "website": "https://www.udacity.com/course/data-scientist-nanodegree--nd025"
        },
        {
            "course_name": "AWS Machine Learning Certification Exam|2020 Complete Guide",
            "domain_id": 2,
            "duration_months": 2,
            "id": 16,
            "platform_id": 3,
            "price_per_month": 6,
            "website": "https://www.udemy.com/course/amazon-web-services-machine-learning/"
        }
    ],
    "success": true
}
```

#### POST '/courses'
- Adds a new course to the Application
- Request Body: A JSON object of the following type (example):
```
{
    "course_name": "AWS Machine Learning Certification Exam|2020 Complete Guide", 
    "domain_id": 2,
    "platform_id": 3,
    "website": "https://www.udemy.com/course/amazon-web-services-machine-learning/",
    "price_per_month": 6, 
    "duration_months": 2
}
```
- Authorization: One needs to provide a Bearer token with `Platform` or `Admin` access. 
- Returns: if request is correct one gets the following JSON object with `id` of the course added and `success = True` 
```
{
    "id": 71,
    "success": true
}
```
#### POST '/domains'
- Adds a new domain to the Application
- Request Body: A JSON object of the following type (example):
```
{
    "domain_name": "Data Massage"
}
```
- Authorization: One needs to provide a Bearer token with `Platform` or `Admin` access. 
- Returns: if request is correct one gets the following JSON object with `id` of the domain added and `success = True` 
```
{
    "domain_id": 45,
    "success": true
}
```

#### PATCH '/domains/<int:domain_id>'
- Patches a given domain_id
- Authorization: One needs to provide a Bearer token with `Platform` or `Admin` access. 
- Request Body: A JSON object of the following type (example):
```
{
    "domain_name": "Data Preparation"
}
```
- Returns: if request is correct one gets the following JSON object with `id` of the modified domain, new name and `success = True` 
```
{
    "domain_id": 45,
    "new_name": "Data Preparation",
    "success": true
}
```

#### DELETE '/courses/<int:course_id>'
- Deletes a course with a given id from the database.
- Request Arguemnt: course_id
- Authorization: One needs to provide a Bearer token with `Admin` access. Only Admins can delete courses
- Request Body: None
- Returns: A JSON object with the status of the request (`success` is true or not) and the `id` of the deleted course.
```
{
    "course_id": 61,
    "success": true
}
```

#### DELETE '/domains/<int:domain_id>'
- Deletes a domain with a given id from the database.
- Request Arguemnt: domain_id
- Authorization: One needs to provide a Bearer token with `Admin` access. One Admins can delete domains
- Request Body: None
- Returns: A JSON object with the status of the request (`success` is true or not) and the `id` of the deleted course.
```
{
    "domain_id": 45,
    "success": true
}
```

## Testing
To run the tests locally, do the following:
```
dropdb EducationOnlineDBTest
createdb EducationOnlineDBTest
psql EducationOnlineDBTest < EducationOnlineDB.psql
python test_app.py
```
