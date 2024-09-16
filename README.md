# HVV Air Pollution API

This FastAPI application provides authentication and pollution data retrieval services through a set of secure endpoints. Users can authenticate, manage their account, and fetch pollution data for different countries and years.

## Table of Contents
- [Endpoints](#endpoints)
   - [Authentication](#authentication)
   - [Pollution Data](#pollution-data)
- [Useage Instructions](#useage-instructions)
- [Security](#security)
- [Testing](#testing)
   - [Testing Response Status](#testing-response-status)
   - [Testing Response Content](#testing-response-content)
   - [Testing Response Errors](#testing-response-errors)
- [Installation via Github Container Registry](#installation-via-github-container-registry)
- [Deployment and Workflow Setup](#deployment-and-workflow-setup)
   - [Create the GitHub Repository from zipped files](#create-the-github-repository-from-zipped-files)
   - [Build and run the docker container](#build-and-run-the-docker-container)
- [Branching Strategy](#branching-strategy)
  - [Main Branch: main](#main-branch-main)
  - [Dev Branch: dev](#dev-branch-dev)
  - [Development Branches: feature/ Prefix](#development-branches-feature-prefix)
  - [Hotfix Branches: hotfix/ Prefix](#hotfix-branches-hotfix-prefix)
  - [Pull Requests and Code Reviews](#pull-requests-and-code-reviews)
    - [Branch Protection Rule:](#branch-protection-rule)
    - [Access Protection Rules:](#access-protection-rules)
    - [Tag Protection Rules:](#tag-protection-rules)
    - [File Path Protection:](#file-path-protection)
---

## Endpoints

### Authentication

1. **POST `/auth/token`**
   - **Description**: This endpoint allows users to log in by providing a username and password. On successful login, it returns a JWT token that must be used to authenticate subsequent requests.
   - **Request Body**:
     - `grant_type`: **password**
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
     - `year`: integer (Year)
   - **Response**: JSON data containing pollution metrics for the specified country and year.
   - **Authentication Required**: Yes (JWT Token)

---

## Useage Instructions

1. **User Registration**

If not already done, use the endpoint `/auth/register` to create a new user.

2. **Authenticate with FastAPI**

As most calls within the API require a JWT Token, authenticate with FastAPI by interacting with the Oauth-Flow (Green Button on the top-right of the page) to generate an Access Token. Client ID and Client Secret are not required for this application.

3. **Fetch Air Pollution Data**

Once authenticated, the endpoint `/pollution_data/get` can be used to fetch air pollution data. Keep in mind, that data is only availble between 2010 and 2021 and not all countries have data for every year. If that is the case an error message will be displayed instead of the regular response indicating that there is no data for the selected year or country.

Example calls:
- country: Australia, year: 2014
- country: United States, year: 2011
- country: Uruguay, year: 2018

---

## Security

This application implements several layers of security to protect user data and ensure secure access to the endpoints:

1. **JWT Authentication**: 
   - All endpoints (except `/auth/register` and `/auth/token`) require the user to be authenticated using a valid JWT token. This token is generated upon successful submission of the /auth/token-request and must be included in the `Authorization` header of subsequent requests in the format `Bearer <token>`.
   
   Within FastAPI this token can also be generated by interacting with the OAuth-UI.

2. **Password Protection**:
   - User passwords are securely hashed and stored to prevent unauthorized access. Plaintext passwords are never stored or transmitted. The secret-key used for hashing is stored in a .env-file for this demo application and is part of the built docker image. For production use and in general, there are better options such as providing the secret-key as github secret or docker build argument.

3. **Two-Factor Authentication (2FA)**:
   - For additional security, users can enable two-factor authentication (2FA). Once enabled, users will be required to provide a 2FA code (from an authenticator app) in addition to their username and password during login. For the current version, this feature is disabled.

4. **HTTPS**:
   - The application should be deployed behind an HTTPS-enabled server to encrypt all communication between the client and the server, ensuring sensitive data like passwords and tokens are protected in transit. For the purpose of this demo, this feature is not enabled.

5. **Client Id & Client Secret** (Optional):
    - The application can optionally use a client_id and client_secret to authorize and authenticate API clients. This ensures only authorized applications can access the API and helps with tracking usage and applying rate limiting to mitigate brute-force attacks or prevent abuse of authentication endpoints.

---

## Testing

This application includes automated tests using FastAPI's `TestClient`. Below are the tests that are performed:

### Testing Response Status

Tests verify that fastAPI runs as expected and a 200 response is returned.

### Testing Response Content

Tests check if the response content includes the expected data, verifying the data for selected countries.

### Testing Response Errors

Tests ensure proper error handling by verifying that the correct error messages and status codes are returned when invalid data are supplied.

---

## Installation via Github Container Registry

The HVV Air Pollution API can be pulled from the GitHub Container Registry and run using Docker. Follow the steps below:

1. **Authenticate Docker with the GitHub Container Registry**

   ```bash
   docker login ghcr.io
   ```
   Use your Github-Username and a personal access token (PAT). The access token needs the following scopes:
   - repos
   - workflows
   - write_packages

   An access token can be created by navigating to the User Settings:
   
   `Settings` &rarr; `Developer settings` &rarr; `Personal Access Tokens` &rarr; `Tokens (classic)`

2. **Pull the image from GitHub Container Registry**
    ```bash
    docker pull ghcr.io/<your-repo/<your-containername>:latest
    ```

3. **Run the container**
    ```bash
    sudo docker run -d --name hvv-api -p 80:7555 ghcr.io/<your-repo/<your-containername>:latest
    ```

4. **Access the API**

    The api can be accessed under http://localhost/docs. If accessing the page is not possible, make sure that port 80 and 7555 are open. It might also be necessary to change the port mapping in the docker run statement.

## Deployment and Workflow Setup

This section outlines the steps to unzip a GitHub repository, create a new GitHub repository, clone it, run the Docker container, and push changes to trigger a GitHub Actions workflow.

### Create the GitHub Repository from zipped files

1. On Linux/Unix, use the following command to unzip the files:
    ```bash
    unzip <repository-name>.zip
    cd <repository-name>
    ```

    On Windows, just unzip the files in the explorer.

2. Create a new GitHub Repository

    Create a new repository on github.com. In preparation for adding the workflow to build the docker container, add a Personal Access Token (PAT) as Secret under `Settings` &rarr; `Secrets and Variables` &rarr; `Actions` named **GHCR_TOKEN**.
    The **GHCR_TOKEN** needs to have the following scopes:
    - repos
    - workflows
    - write_packages

3. Create the local repository

    Create the local repository and push your code to the dev-branch using the following code: 
    ```bash
    git init
    git add .
    git commit -m "Initial commit"

    git remote add origin https://github.com/<username>/<repository-name>.git
    git push -u origin dev
    ```
    ### Build and run the docker container

    To build and run the docker container using the dockerfile and compose.yaml within the repository, follow these steps:

    1. Build the docker image

    ```bash
    docker compose build [--no-cache]
    ```

    2. Start the docker image
    ```bash
    docker compose up [-d]
    ```

## Branching Strategy

   ### Main Branch: main
   Purpose: Serves as the primary line for the project, from which releases are generated.

   Process:

   The main branch should always be deployable and contains the most stable code.
   All changes to the main branch must be submitted via Pull Requests (PRs), which must be reviewed by at least two other team member.

   ### Dev Branch: dev
   Purpose: Serves as the primary developement line for the project, from which the main branch is updated.

   Process:

   All changes to the dev branch must be submitted via Pull Requests (PRs), which must be reviewed by at least two other team member.


   ### Development Branches: feature/ Prefix
   Purpose: A separate branch for each new feature or client requirement.

   Process:

   Each new feature or client project receives its own branch, e.g., feature/new-reporting-module.
   The branch name should clearly describe the feature or project for easy identification.
   Once completed, the feature branch is merged into the main branch via a PR. The PR must pass code reviews and all automated tests.

   ### Hotfix Branches: hotfix/ Prefix
   Purpose: Quick fixes for critical bugs in the main branch.

   Process:

   Hotfixes are developed on a separate branch, e.g., hotfix/critical-database-fix.
   Once completed, the hotfix is merged into the main branch and simultaneously into the current development branch to avoid regressions.

   ### Pull Requests and Code Reviews
   Goal: Ensure that the new code is error-free and consistent with the existing project code.

   #### Branch Protection Rule:
   All commits must be made to a non-protected branch and submitted through a pull request before being merged into a protected branch. Pull requests targeting a protected branch require two approvals and no pending change requests to proceed with the merge. This rule applies to the dev branch.

   #### Access Protection Rules:
   Only users with bypass permissions are authorized to create or delete branches. This rule applies to both the main and dev branches.

   #### Tag Protection Rules:
   Only users with bypass permissions are authorized to create or delete tags. Applied to main and dev branch.

   #### File Path Protection:
   Prevent commits that make changes to specified files in the main and dev branches from being pushed to the commit history. Applied to main and dev branch.

