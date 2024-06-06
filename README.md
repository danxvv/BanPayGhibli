# Users Ghibli API

## Table of Contents

- [Project Description](#project-description)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Usage](#usage)
  - [Endpoints](#endpoints)
- [Testing](#testing)
- [Cloud Deployment](#cloud-deployment)
- [Postman Collection](#postman-collection)

## Project Description

This project is a take-home coding challenge for BanPay. Its an API that allows all CRUD on an Users Table adding the feature to call the Ghibli API based on user's role.

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Docker
- Docker Compose

## Features

- Complete CRUD operations on the Users table
- Role-based access control
- Authentication with JWT
- Call Ghibli API based on user's role
- OpenAPI documentation
- Dockerized

## Prerequisites

- Docker
- Python
- Postman (optional)

## Getting Started

1. Clone the repository:

   ```bash
   git clone <repository_url> users_ghibli_api
   ```

2. Change directory to the project root:

   ```bash
   cd users_ghibli_api
   ```

3. Copy the `.env.example` file to `.env`:

   ```bash
   cp .env.example .env
   ```

4. Run the Docker containers:

   ```bash
   docker-compose up
   ```

## Usage

- OpenAPI documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Endpoints

### Authentication

#### Login Access Token

**POST** `/api/v1/auth/login/access-token`

- **Summary**: Obtain an access token.
- **Request Body**:
  - `username`: string (required)
  - `password`: string (required)
- **Responses**:
  - `200`: Successful Response (returns a `Token`) with an `access_token` to be used in the `Authorization` header
  - `422`: Validation Error (returns an `HTTPValidationError`)

### Users

#### Read Users

**GET** `/api/v1/users/`

- **Summary**: Retrieve a list of users.
- **Headers**:
  - `Authorization`: `Bearer {access_token}`
- **Responses**:
  - `200`: Successful Response (returns an array of `User` objects)
- **Security**: Only with `admin`

#### Create User

**POST** `/api/v1/users/`

- **Summary**: Create a new user.
- **Request Body**:
  - `name`: string (required)
  - `email`: string (required)
  - `password`: string (required)
  - `role_id`: integer (required)
- **Responses**:
  - `200`: Successful Response (returns a `User`)
  - `422`: Validation Error (returns an `HTTPValidationError`)

#### Read User

**GET** `/api/v1/users/{user_id}`

- **Summary**: Retrieve a user by ID.
- **Headers**:
  - `Authorization`: `Bearer {access_token}`
- **Parameters**:
  - `user_id`: string (format: uuid4) (required)
- **Responses**:
  - `200`: Successful Response (returns a `User`)
  - `422`: Validation Error (returns an `HTTPValidationError`)
- **Security**: `admin` or `user` with the same `user_id`

#### Update User

**PUT** `/api/v1/users/{user_id}`

- **Summary**: Update an existing user by ID.
- **Headers**:
  - `Authorization`: `Bearer {access_token}`
- **Parameters**:
  - `user_id`: string (format: uuid4) (required)
- **Request Body**:
  - `name`: string
  - `password`: string
- **Responses**:
  - `200`: Successful Response (returns a `User`)
  - `422`: Validation Error (returns an `HTTPValidationError`)
- **Security**: `admin` or `user` with the same `user_id`

#### Delete User

**DELETE** `/api/v1/users/{user_id}`

- **Summary**: Delete a user by ID.
- **Headers**:
  - `Authorization`: `Bearer {access_token}`
- **Parameters**:
  - `user_id`: string (format: uuid4) (required)
- **Responses**:
  - `204`: Successful Response
  - `422`: Validation Error (returns an `HTTPValidationError`)
- **Security**: Only with `admin`

### Roles

#### Read Roles

**GET** `/api/v1/users/roles/`

- **Headers**:
  - `Authorization`: `Bearer {access_token}`
- **Summary**: Retrieve a list of roles.
- **Responses**:
  - `200`: Successful Response (returns an array of `Role` objects)
- **Security**: Only with `admin`

#### Create Role

**POST** `/api/v1/users/roles/`

- **Summary**: Create a new role.
- **Headers**:
  - `Authorization`: `Bearer {access_token}`
- **Request Body**:
  - `name`: string (required)
- **Responses**:
  - `200`: Successful Response (returns a `Role`)
  - `422`: Validation Error (returns an `HTTPValidationError`)
- **Security**: Only with `admin`

#### Assign Role

**POST** `/api/v1/users/{user_id}/roles/{role_id}`

- **Summary**: Assign a role to a user.
- **Headers**:
  - `Authorization`: `Bearer {access_token}`
- **Parameters**:
  - `user_id`: string (format: uuid4) (required)
  - `role_id`: integer (required)
- **Responses**:
  - `204`: Successful Response
  - `422`: Validation Error (returns an `HTTPValidationError`)
- **Security**: Only with `admin`

### Ghibli

#### Read Ghibli

**GET** `/api/v1/ghibli/`

- **Summary**: Retrieve a list of Ghibli items based on the user's role.
- **Headers**:
  - `Authorization`: `Bearer {access_token}`
- **Parameters**:
  - `limit`: integer (default: 10)
  - `fields`: array of fields to return
- **Responses**:
  - `200`: Successful Response (returns a list of Ghibli items)
  - `422`: Validation Error (returns an `HTTPValidationError`)

#### Read Ghibli By Id

**GET** `/api/v1/ghibli/{ghibli_id}`

- **Summary**: Retrieve a Ghibli item by ID based on the user's role.
- **Headers**:
  - `Authorization`: `Bearer {access_token}`
- **Parameters**:
  - `ghibli_id`: string (format: uuid4) (required)
  - `fields`: array of fields to return
- **Responses**:
  - `200`: Successful Response (returns a Ghibli item)
  - `422`: Validation Error (returns an `HTTPValidationError`)

## Testing

To run the tests, execute the following command with the Docker container running:

```bash
docker compose exec api pytest
```

## Cloud Deployment

You can test the API on the cloud using the following link:
[https://ghibli.danielmojica.me/docs](https://ghibli.danielmojica.me/docs) to see the OpenAPI documentation.

## Postman Collection

Provide a Postman collection to test the API:
`BanPay_Home_Assignment.postman_collection.json` Just import it to your Postman with project already running or **change the URL to the cloud deployment provided above**.
Collection is already set up with the environment variables to make it easier to test.
