# HVV Air Pollution API

This FastAPI application provides authentication and pollution data retrieval services through a set of secure endpoints. Users can authenticate, manage their accounts, and fetch pollution data for different countries and years.

## Table of Contents
- [Endpoints](#endpoints)
  - [Authentication](#authentication)
  - [Pollution Data](#pollution-data)
- [Security](#security)

---

## Endpoints

### Authentication

1. **POST `/auth/token`**
   - **Description**: This endpoint allows users to log in by providing a username and password. On successful login, it returns a JWT token that must be used to authenticate subsequent requests.
   - **Request Body**:
     - `username`: string
     - `password`: string
   - **Response**: JWT token for authenticating further requests.
   - **Authentication Required**: No

2. **GET `/auth/me`**
   - **Description**: Fetch details about the currently authenticated user.
   - **Response**: Information about the authenticated user, including username and authentication details.
   - **Authentication Required**: Yes (JWT Token)

3. **POST `/auth/register`**
   - **Description**: Register a new user by providing a username and password.
   - **Request Body**:
     - `username`: string
     - `password`: string
   - **Response**: Confirmation of successful registration.
   - **Authentication Required**: No

4. **POST `/auth/2fa/enable`**
   - **Description**: Enables two-factor authentication (2FA) for the currently authenticated user. This endpoint generates and displays a QR code for an authentication app (like Google Authenticator).
   - **Response**: QR Code.
   - **Authentication Required**: Yes (JWT Token)

5. **POST `/auth/2fa/verify`**
   - **Description**: Verifies the 2FA code provided by the user during the login process.
   - **Request Body**:
     - `2fa_code`: string (code generated by the 2FA app)
   - **Response**: Confirmation of 2FA verification.
   - **Authentication Required**: Yes (JWT Token)

### Pollution Data

1. **GET `/pollution_data/get`**
   - **Description**: Fetches pollution data for a specific country and year. The user must be authenticated to access this endpoint.
   - **Query Parameters**:
     - `country`: string (Country name)
     - `year`: integer (Year of the pollution data)
   - **Response**: JSON data containing pollution metrics for the specified country and year.
   - **Authentication Required**: Yes (JWT Token)

---

## Security

This application implements several layers of security to protect user data and ensure secure access to the endpoints:

1. **JWT Authentication**: 
   - All endpoints (except `/auth/register` and `/auth/token`) require the user to be authenticated using a valid JWT token. This token is generated upon successful login and must be included in the `Authorization` header of subsequent requests in the format `Bearer <token>`.

2. **Password Protection**:
   - User passwords are securely hashed and stored to prevent unauthorized access. Plaintext passwords are never stored or transmitted.

3. **Two-Factor Authentication (2FA)**:
   - For additional security, users can enable two-factor authentication (2FA). Once enabled, users will be required to provide a 2FA code (from an authenticator app) in addition to their username and password during login.

4. **HTTPS**:
   - The application should be deployed behind an HTTPS-enabled server to encrypt all communication between the client and the server, ensuring sensitive data like passwords and tokens are protected in transit.

5. **Rate Limiting** (Optional):
   - Implementing rate limiting can help mitigate brute-force attacks and prevent abuse of the authentication endpoints.

---

## Running the Application

To run this FastAPI application locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/fastapi-auth-pollution.git