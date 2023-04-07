# Handled Edge cases and Validations Performed
- Captured API level exceptions
- Validations applied on date fields (date_from, date_to). Allowed format is YYYY-MM-DD.
- Validations applied on origin and destination field. 
    - Handled min-max length of string. So that these string fields are not exploited.
    - Disallowed punctuation characters (eg !@,*...) Only letters and underscores are accepted.
    - Provided origin and destination parameters are checked whether they are present in the database or not. So that relevant message can be returned in response.


# Tests
The development approach was TDD. Tests are implemented for shared utility methods and API endpoint. Tests can be found at *src/tests*. 

![tests](./assets/tests.png)


# API code structure
```bash
├── Dockerfile
├── app
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── models
│   │   │   └── rates.py        # (Model for API endpoint)
│   │   ├── routes
│   │   │   └── rates.py        # (API endpoint)
│   │   └── utils               # (Shared utility methods)
│   │       ├── __init__.py
│   │       ├── crud.py
│   │       ├── queries.py      # (SQL queries)
│   │       └── shared.py       # Methods for validations and preloaded data
│   ├── db.py
│   ├── logging.conf
│   └── main.py                 # (API startup code)
├── logs
│   └── logfile.log
├── requirements.txt
└── tests                       # (Unit tests)
    ├── __init__.py
    ├── conftest.py
    ├── test_rates.py           # (Tests for the rates endpoints)
    └── test_shared.py          # (Tests for the shared utility methods)
```

# Setup and Execution

The docker compose file contains three services
- web: For the API
- db: For the postgres database
- pgadmin: Pgadmin client for database

Follow the instructions to run and test the project.  
<br>
Start docker compose
``` bash
docker compose up -d --build
```

<br>

Open the following link in the browser to test API: http://localhost:8002/docs. 

<br>


To view or query database through pgadmin, do the following:

``` bash
docker ps
```
Copy the the id of the postgres container. Use this id to check the IP address.


```bash
docker inspect <put-id-here> | grep IPAddress
```

The result will look something like this

```
"SecondaryIPAddresses": null,
"IPAddress": "",
        "IPAddress": "172.24.0.4",
```
Copy this IPAddress. Then Login to pgadmin web interface through http://localhost:5050. You can get the login and pass from docker-compose file. Register a server and use that IPAddress as host.