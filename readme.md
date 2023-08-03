# Backend System for User Data API

This is a backend system implemented in Python using Flask, SQLAlchemy, and JWT for handling various APIs related to user registration, data storage, retrieval, update, and deletion.

## Table of Contents
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Installation](#installation)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)
- [License](#license)

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


