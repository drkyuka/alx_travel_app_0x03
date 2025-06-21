#!/bin/bash
# Script to test the token authentication endpoint

# Colors for terminal output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Testing JWT token authentication...${NC}"

# Set variables for easy updating
API_URL="http://localhost:8000/api/v1"
EMAIL="johndoe@example.com"  # Change this to your actual email
PASSWORD="password1"         # Change this to your actual password

# Test with both username and email fields
echo -e "\n${GREEN}Testing with 'username' field:${NC}"
USERNAME_RESPONSE=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$EMAIL\", \"password\": \"$PASSWORD\"}" \
  ${API_URL}/token/)

echo "Response (username field):"
echo $USERNAME_RESPONSE | python -m json.tool 2>/dev/null || echo $USERNAME_RESPONSE

echo -e "\n${GREEN}Testing with 'email' field:${NC}"
TOKEN_RESPONSE=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}" \
  ${API_URL}/token/)

echo "Response (email field):"
echo $TOKEN_RESPONSE | python -m json.tool 2>/dev/null || echo $TOKEN_RESPONSE

# Check if the response contains an access token
if [[ $TOKEN_RESPONSE == *"access"* ]]; then
    echo -e "\n${GREEN}✓ Successfully obtained token!${NC}"
    
    # Extract the access token
    ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | python -c "import sys, json; print(json.load(sys.stdin)['access'])")
    
    # Test using the token to access a protected endpoint
    echo -e "\n${YELLOW}Testing protected endpoint with the token...${NC}"
    USER_RESPONSE=$(curl -s -X GET \
      -H "Authorization: Bearer ${ACCESS_TOKEN}" \
      ${API_URL}/users/)
    
    echo -e "\nResponse from users endpoint:"
    echo $USER_RESPONSE | python -m json.tool 2>/dev/null || echo $USER_RESPONSE
else
    echo -e "\n${RED}✗ Failed to obtain token.${NC}"
    
    # Provide helpful debug information
    echo -e "\n${YELLOW}Checking if the user exists...${NC}"
    USER_CHECK=$(curl -s -X GET ${API_URL}/users/)
    echo $USER_CHECK | python -m json.tool 2>/dev/null || echo $USER_CHECK
    
    # Offer to create a test user
    echo -e "\n${YELLOW}Would you like to create a test user? (y/n)${NC}"
    read -p "Create test user? " CREATE_USER
    
    if [[ $CREATE_USER == "y" || $CREATE_USER == "Y" ]]; then
        echo -e "\n${YELLOW}Creating test user...${NC}"
        TEST_EMAIL="testuser@example.com"
        TEST_PASSWORD="Password123!"
        
        CREATE_RESPONSE=$(curl -s -X POST \
          -H "Content-Type: application/json" \
          -d "{\"email\": \"$TEST_EMAIL\", \"password\": \"$TEST_PASSWORD\", \"first_name\": \"Test\", \"last_name\": \"User\"}" \
          ${API_URL}/users/)
        
        echo "User creation response:"
        echo $CREATE_RESPONSE | python -m json.tool 2>/dev/null || echo $CREATE_RESPONSE
        
        # Try to get token with the new user
        echo -e "\n${YELLOW}Testing token with new test user...${NC}"
        TEST_TOKEN_RESPONSE=$(curl -s -X POST \
          -H "Content-Type: application/json" \
          -d "{\"email\": \"$TEST_EMAIL\", \"password\": \"$TEST_PASSWORD\"}" \
          ${API_URL}/token/)
        
        echo "Response:"
        echo $TEST_TOKEN_RESPONSE | python -m json.tool 2>/dev/null || echo $TEST_TOKEN_RESPONSE
    fi
fi

echo -e "\n${RED}Common issues:${NC}"
echo "1. Make sure you're using the correct field name (email or username)"
echo "2. Make sure you have Content-Type: application/json header"
echo "3. Make sure your JSON is properly formatted"
echo "4. Make sure you're using POST method, not GET"
echo "5. Make sure your credentials are correct"
echo "6. Make sure your server is running"
echo "7. Check if USERNAME_FIELD = 'email' is set in your User model"

echo -e "\nTo create a test user, try this command:"
echo -e "${GREEN}curl -X POST -H \"Content-Type: application/json\" -d '{\"email\": \"testuser@example.com\", \"password\": \"Password123!\", \"first_name\": \"Test\", \"last_name\": \"User\"}' ${API_URL}/users/${NC}"

echo -e "\nTo manually test token authentication, try this command:"
echo -e "${GREEN}curl -X POST -H \"Content-Type: application/json\" -d '{\"email\": \"testuser@example.com\", \"password\": \"Password123!\"}' ${API_URL}/token/${NC}"
