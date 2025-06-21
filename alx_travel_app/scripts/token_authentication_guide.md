# Token Authentication Guide

This guide shows how to authenticate with the JWT token endpoint in your application.

## Obtaining a Token

To get a JWT token, you need to make a POST request (not GET) to the token endpoint with your credentials.

### Using Postman

1. **Set up a POST request to the token endpoint**:
   - URL: `http://localhost:8000/api/v1/token/`
   - Method: POST

2. **Add your credentials in the request body**:
   - Go to the "Body" tab
   - Select "raw" and "JSON" format
   - Enter your credentials:
   ```json
   {
       "email": "your_email@example.com",
       "password": "your_password"
   }
   ```

3. **Send the request**:
   - If your credentials are correct, you'll receive a JSON response with access and refresh tokens:
   ```json
   {
       "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
       "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
   }
   ```

## Using the Token

Once you have the token, use it to authenticate your requests:

1. **Set up an authenticated request**:
   - URL: `http://localhost:8000/api/v1/users/` (or any other protected endpoint)
   - Method: GET (or POST, PUT, etc.)

2. **Add the Authorization header**:
   - Go to the "Headers" tab
   - Add a header:
     - Key: `Authorization`
     - Value: `Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...` (use your access token)

3. **Send the request**:
   - You should now be able to access protected resources

## Common Issues

- **Method Not Allowed (405)**: This means you're using the wrong HTTP method. The token endpoint only accepts POST requests, not GET.
- **Unauthorized (401)**: Your token is invalid or expired.
- **Bad Request (400)**: Your request body is malformed or missing required fields.

## Refreshing Tokens

When your access token expires, use the refresh token to get a new one:

1. **Make a POST request to the refresh endpoint**:
   - URL: `http://localhost:8000/api/v1/token/refresh/`
   - Method: POST
   - Body:
   ```json
   {
       "refresh": "your_refresh_token"
   }
   ```

2. **You'll receive a new access token**:
   ```json
   {
       "access": "new_access_token"
   }
   ```
