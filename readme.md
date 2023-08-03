# Backend System for User Data API

This is a backend system implemented in Python using Flask, SQLAlchemy, and JWT for handling various APIs related to user registration, data storage, retrieval, update, and deletion.

## Table of Contents
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Installation](#installation)
- [Postman](#postman)


## Getting Started

This backend system provides a set of APIs that allow users to register, generate tokens, store, retrieve, update, and delete data associated with their accounts.

## API Endpoints

1. User Registration
   - Endpoint: `/api/register`
   - Method: POST
   - Description: Register a new user with the provided details.

2. Generate Token
   - Endpoint: `/api/token`
   - Method: POST
   - Description: Generate a JWT token by providing valid login credentials.

3. Store Data
   - Endpoint: `/api/data`
   - Method: POST
   - Description: Store user-specific data by providing a key-value pair along with a valid JWT token for authentication.

4. Retrieve Data
   - Endpoint: `/api/data/{key}`
   - Method: GET
   - Description: Retrieve the value associated with a specific key for the authenticated user.

5. Update Data
   - Endpoint: `/api/data/{key}`
   - Method: PUT
   - Description: Update the value associated with an existing key for the authenticated user.

6. Delete Data
   - Endpoint: `/api/data/{key}`
   - Method: DELETE
   - Description: Delete a key-value pair from the database for the authenticated user.


## Installation

To set up and run the backend system locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd FLASK_API_APP

2. `pip install -r requirements.txt`

3. `python -m flask run`

4. Access the APIs at `http://127.0.0.1:5000/{endpoint}`

## Postman

To test the APIs, follow these steps:

1. For User Registration and Generate Token endpoint, send the required data in body section of postman in json
   ```bash
   {
  "username": "mavi",
  "email": "mavi@gmail.com",
  "full_name": "harman singh",
  "age": 26,
  "gender": "male",
  "password": "Aksh@234"
   }

2. For all other endpoints, need to pass the authorization token in the request headers. For that just add a key `Authorization` in headers  and  value as the *token* generated at `/api/token` endpoint.
