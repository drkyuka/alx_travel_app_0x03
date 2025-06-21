#!/usr/bin/env python
"""
Script to test the token endpoint of the ALX Travel App API.
This script makes a POST request to the token endpoint with credentials.
"""

import json
import sys

import requests

# Configuration
API_URL = "http://localhost:8000/api/v1/token/"
DEFAULT_EMAIL = "admin@example.com"
DEFAULT_PASSWORD = "AdminPass123!"

# Colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def get_token(email, password):
    """Make a POST request to the token endpoint with credentials."""
    print(f"{YELLOW}Attempting to get token for {email}...{RESET}")

    # Prepare request data
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    data = {"email": email, "password": password}

    try:
        # Make POST request to token endpoint
        response = requests.post(API_URL, headers=headers, json=data)

        # Check if the request was successful
        if response.status_code == 200:
            tokens = response.json()
            print(f"{GREEN}Success! Received tokens:{RESET}")
            print(f"Access token: {tokens['access'][:20]}...")
            print(f"Refresh token: {tokens['refresh'][:20]}...")
            return tokens
        else:
            print(f"{RED}Error: {response.status_code} - {response.reason}{RESET}")
            if response.text:
                print(f"Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"{RED}Request failed: {str(e)}{RESET}")
        return None


def main():
    """Main function to get a token using default or provided credentials."""
    # Get credentials from command line arguments or use defaults
    if len(sys.argv) >= 3:
        email = sys.argv[1]
        password = sys.argv[2]
    else:
        print(
            f"{YELLOW}Using default credentials. You can provide your own with:{RESET}"
        )
        print("python test_token.py your_email@example.com your_password")
        email = DEFAULT_EMAIL
        password = DEFAULT_PASSWORD

    # Get token
    tokens = get_token(email, password)

    # If successful, save tokens to a file
    if tokens:
        with open("auth_tokens.json", "w") as f:
            json.dump(tokens, f, indent=2)
        print(f"{GREEN}Tokens saved to auth_tokens.json{RESET}")

        # Show example of how to use the token
        print(f"\n{YELLOW}Example of how to use the token in your requests:{RESET}")
        print("1. Add this header to your requests:")
        print(f"   Authorization: Bearer {tokens['access']}")
        print("\n2. Example curl command:")
        print(
            f'   curl -H "Authorization: Bearer {tokens["access"]}" http://localhost:8000/api/v1/users/'
        )


if __name__ == "__main__":
    main()
