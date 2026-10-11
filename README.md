\# FastAPI JWT Authentication Microservice



\## Project Description

A REST API built using Python and FastAPI for user registration, login, JWT authentication, and protected item management.



\## Features

\- User registration and login

\- Password hashing using bcrypt

\- JWT token generation and validation

\- Protected API endpoints

\- Create, view, and delete items

\- SQLite database integration

\- Swagger API documentation



\## Technologies Used

\- Python

\- FastAPI

\- SQLAlchemy

\- SQLite

\- PyJWT

\- bcrypt

\- Uvicorn



\## Installation



1\. Clone the repository.

2\. Create a virtual environment:

&#x20;  `python -m venv venv`

3\. Activate it in PowerShell:

&#x20;  `.\\venv\\Scripts\\Activate.ps1`

4\. Install dependencies:

&#x20;  `pip install -r requirements.txt`

5\. Run the application:

&#x20;  `uvicorn main:app --reload`



\## API Documentation

Open these URLs after starting the server:



\- Swagger UI: http://127.0.0.1:8000/docs

\- Health check: http://127.0.0.1:8000/health



\## API Endpoints



| Method | Endpoint | Purpose |

|---|---|---|

| GET | `/` | Root endpoint |

| GET | `/health` | Health check |

| POST | `/register` | Register a user |

| POST | `/login` | Log in and get a token |

| POST | `/items` | Create an item |

| GET | `/items` | View items |

| GET | `/items/{item\_id}` | View a specific item |

| DELETE | `/items/{item\_id}` | Delete an item |



Item endpoints require authentication.



\## Security

\- Passwords are hashed before storage.

\- JWT tokens expire after a configured period.

\- Configure a strong `JWT\_SECRET\_KEY` before deployment.

\- Never upload passwords, tokens, or secret environment files.



\## Purpose

This project demonstrates REST API development, authentication, and database integration using FastAPI.

