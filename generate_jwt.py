from jose import jwt
import datetime

# Read the private key
with open("private.pem", "r") as f:
    private_key = f.read()

# Define token payload
customer_payload = {
    "sub": "550e8400-e29b-41d4-a716-446655440010",  # Mock user ID
    "role": "customer",
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),  # Expires in 24 hours
    "iat": datetime.datetime.utcnow()
}

admin_payload = {
    "sub": "550e8400-e29b-41d4-a716-446655440011",  # Different mock user ID
    "role": "admin",
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
    "iat": datetime.datetime.utcnow()
}

# Generate tokens
customer_token = jwt.encode(customer_payload, private_key, algorithm="RS256")
admin_token = jwt.encode(admin_payload, private_key, algorithm="RS256")

# Print tokens
print("Customer JWT (jwt_token):")
print(customer_token)
print("\nAdmin JWT (jwt_token_admin):")
print(admin_token)