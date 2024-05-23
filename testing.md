# Test Failure Scenario

## Scenario: User Login with Incorrect Password

**Test Case**: `test_login`

**Description**: The test case `test_login` might fail if the user tries to log in with an incorrect password. In this scenario, even though the user exists in the database, the provided password does not match the stored password hash, resulting in a 401 Unauthorized error.

**Steps to Reproduce**:
1. Sign up a user with username `testuser` and password `password`.
2. Attempt to log in with username `testuser` and an incorrect password (e.g., `wrongpassword`).
3. The server should return a 401 Unauthorized status, indicating that the credentials are invalid.

**Expected Output**:
```json
{
    "message": "Invalid Username or Password"
}
