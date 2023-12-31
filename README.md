﻿# Task-Management--Zaawansowane-Programowanie-gc01-SII-23-24

## Installation

Firstly, if you don't have Python 3.11 installed on your device you should visit [this page](https://www.python.org/downloads/release/python-3117/)

### Setup Virtualenv on Windows

```shell
deactivate
rmdir venv
py -3.11 -m pip install --upgrade pip
py -3.11 -m pip install virtualenv
py -3.11 -m virtualenv venv
.\venv\Scripts\activate
.\venv\Scripts\python.exe -m pip install -r .\requirements.txt
```

If any problem with activating venv try: 

```
For Windows 11, Windows 10, Windows 7, Windows 8, Windows Server 2008 R2 or Windows Server 2012, run the following commands as Administrator:

x86 (32 bit):
Open C:\Windows\SysWOW64\cmd.exe
Run the command: powershell Set-ExecutionPolicy RemoteSigned

x64 (64 bit):
Open C:\Windows\system32\cmd.exe
Run the command: powershell Set-ExecutionPolicy RemoteSigned
```
## Running the application 

After setup virtualenv you'll need to copy file `ENV/local.env.example` to `ENV/local.env` and edit it accordingly to your needs

### On Windows

```shell
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload 
```
The application will be accessible at http://127.0.0.1:8000. Hot reload will be available

You'll need to have PostgreSQL installed on your computer and have it properly configured. 
Therefore, it's recommended to run the app using `docker-compose`

### Using `docker-compose`

If you have not installed Docker on your computer yet you should do it :) Follow instructions on this page: 
https://docs.docker.com/get-docker/

Build and run the application using Docker Compose:

```bash
docker-compose up task-manager postgres --build
```
The application will be accessible at http://127.0.0.1:8000. Hot reload will be available

## Documentation
The API documentation is available after running server app at: http://localhost:8000/docs

## Development

### Tests

To run tests you have to start app and test database containers with: 

```bash
docker-compose up task-manager test-db --build
```

Then you can run them by simply typing

```bash
pytest
```

### Linter
In the root folder just type in terminal:
```bash
mypy app
```

### Format
In the root folder just type in terminal:
```bash
black app
```

## Additional Information
- FastAPI Documentation: https://fastapi.tiangolo.com/
- Docker Documentation: https://docs.docker.com/
- Docker Compose Documentation: https://docs.docker.com/compose/
- Mypy Documentation: https://mypy.readthedocs.io/en/stable/index.html
- Black Documentation: https://black.readthedocs.io/en/stable/
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/en/20/
