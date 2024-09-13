# HVV Air Pollution API

This Repository contains code to query air pollution data by country and year.


## Authentication & Security

A user is required to use most of the endpoints of the API. The endpoints listed under Auth can be used to create a user and set up 2-Factor Authentication (2FA).

### /auth/token:

Generate an access token using your username and password. Client-ID and Client-Secret can be integrated into this check, but are not required in this version.

### /auth/me:

Get information about the currently logged in user.


## Configuration

Use a `.env` file to configure the application.

Generate a secret key `openssl rand -hex 32` and add it to the `.env` file:

