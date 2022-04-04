# task implementation for omnipresent
# API with an endpoint that returns all the employees with additional country specific details fetched after consuming an external API.

The following is the folder structure of the application

```
Omnipresent
├───Amrita_Jayakumar
|   ├───app
│   |   ├───static
|   |   |   └───init_data.json
│   |   └───templates
|   |   ├───__init__.py
|   |   ├───service.py
|   |   ├───views.py
|   ├───external_api
|   |   └───countries.py
|   |───config.py
|   |───docker-compose.yml
|   |───Dockerfile
|   |───init_db.py
|   |───main.py
|   |───requirements.text
|   |───schema.sql
|   |───tests
│   |   ├───functional
|   |   |   └───functional_test.py
│   |   ├───unit
|   |   |   └───unit_test.py
|   |───uwsgi.ini
|   |───README.md
```

FOLDER STRUCTURE EXPLAINED

   app/static/init_data.json

        Contains the data for initializing database.

   app/__init__.py

        Contains the initializations required for the app

   app/service.py

        Contains the business Logic and DB connections

   app/views.py

        Contains the endpoint defined for the API

   external_api/countries.py

        Contains the API call to fetch the country specific information from https://restcountries.com/ as required in the task. Have consumed two endpoints

        1. https://restcountries.com/v2/all
        2. https://restcountries.com/v2/alpha/{code} (alternatively uses both endpoints as and when required.)


   config.py

        Contains all configurables that are used in the application. Have separate configuration available for each environment like DEV, PRODUCTION tESTING etc which can beustilized accordingly.
        
        DATABASE_URI, REGIONS, COUNTRIES_API_URL, CACHE_TYPE, CACHE_DEFAULT_TIMEOUT have been added to the config files and each configuration have been named to be self explanatory.

        The regions which require additional identifier for a user has been configured here as a list so that there is a provision to add more of such regions that might need this extra identifier in the future can be added here. The key for the additional identifier in the return json will be "uid".

   Dockerfile Explained:

        FROM python:3.8-alpine : Docker allows us to inherit existing images and hence we can reuse a Python image and install it in our Docker image. Alpine is a lightweight Linux distro that will serve as the OS on which we install our image

        WORKDIR /python-docker : We proceed to set the working directory as /python-docker, which will be the root directory of our application in the container

        COPY requirements.txt requirements.txt : Here, we copy the requirements file and its content (the generated packages and dependencies) into the python-docker folder of the image

        RUN pip3 install -r requirements.txt: This command installs all the dependencies defined in the requirements.txt file into our application within the container

        RUN python init_db.py : This command runs the init_db.py file which will inturn create the database in SQLite and create the table mentioned in schema.sql and insert the data given in app/static/init_data.json

        COPY . . : This copies every other file and its respective contents into the python-docker folder that is the root directory of our application within the container

        CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"] : Finally, this appends the list of parameters to perform the command that runs the application. This is similar to how you would run the Python app on your terminal using the python view.py command

        It is under the assumption that docker and all related dependencies are already installed, we are now ready to build the application.

        cd /Omnipresent/Amrita_jayakumar/
        docker build -t omni_docker .

        We can run the docker image by using the following command.
        docker run -p 5000:5000 -d omni_docker 

        this will now deploy the application at http://localhost:5000/

        incase multiple containers are required, you can utilize the docker-compose.yml

        Please feel free to add other required dependencies into the docker-compose.yml and run it after a build command is fired

        docker-compose build
        docker-compose up -d

   init_db.py

        This script does the following:
            1. creates a database file in the docker container named database.db
            2. will read through the schema.sql, Drop any existing table with the same name and create the Table to oncemore to user data
            3. will read through init_data.json and insert the data into the newly created table.

   main.py

        entry point to the application

   requirements.txt

        contains all the dependencies required for the application to run successfully.
        All the dependencies are pip installed into the docker container during build.

   schema.sql

        container the SQL code for dropping any existing table with the same name and created a new table to hold user/employee data.

   uwsgi.ini

        contains the wsgi configurations required to deploy the application.


API ENDPOINTS EXPLAINED:

      http://localhost:5000/users
      METHODS: GET
      
      GET:
          fetches all users in the Database with all country specific details fetched from the countries API and the additonal Identifier for the users in the regions of Europe and Asia.
          The database used is SQLite as it works well with most low to medium traffic databases. Any API that gets a fewer than 100k requests per day will work well with SQLite

      If pagination is required, then the offset and limit needs to be passed in the URL.
         GET http://localhost:5000/users?limit=3&offset=0 - fetches first 3 user records
         GET http://localhost:5000/users?limit=3&offset=3 - fetches next 3 user records and so on..

      The GET request will fetch all countries from the countries API and cache it for 24 hours. SimpleCache from flask has been chosen to cache this data.  The country data doesnt look like changing always and hence the 24hrs timeout was chosen.

      An option to force fetch the country information have been made and can be achieved by htting the following:
         GET http://localhost:5000/users?refresh=true

AREAS OF IMPROVEMENT:

1. Can use token based authentication to secure the API (JWT implementation. Couldn't do it due to constraints of time)
2. Can use Redis for caching

TESTS

    Test scripts for functional and unit test have been added to the repository but could not work more on it due to constraints of time.




