# COMP2001 Trail Microservice

_The final coursework of COMP2001_

## CommentsService Microservice
This repository contains the CommentsService microservice developed for COMP2001.
The Trail microservice uses Flask-based RESTful API, SQLAlchemy and Docker. It manages comments made by the users of the app; this includes the CRUD functions.
Features include:
- Users can create and update comments
- Only admins can delete(archive) comments
- Can retrieve comments, can also be retrieved with ID

## Technologies
- Flask
- Azure Data Studio
- Swagger
- Docker

## Deployment
http://cent-5-534.uopnet.plymouth.ac.uk/COMP2001/PRai/api/ui

### How to Run the Project

1. Clone the repository
```
git clone <your-repo-url>
cd <project-folder>
```

2. Activate the virtual environment

```
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies

```
pip install -r requirements.txt
```

4. Run the application

```
python app.py
```

You will be given a url, example:
```
http://127.0.0.1:8000
```

5. Access the app

* Home page: `http://127.0.0.1:8000/`
* Swagger API: `http://127.0.0.1:8000/api/ui`

---

Notes
* Use `Ctrl+C` to stop the server.
