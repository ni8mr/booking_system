# Booking System
## Overview
The Booking System is a microservices platform for service booking, built with FastAPI, PostgreSQL, and Redis. See architecture.md for details.
Prerequisites

## Docker (Install Docker)
Docker Compose (included with Docker Desktop or Install Compose)

## Build
Build Docker images:
``docker compose -f infra/docker/docker-compose.yml build``

## Run
Start services in detached mode:
``docker compose -f infra/docker/docker-compose.yml up -d``

## Check status:
``docker compose -f infra/docker/docker-compose.yml ps``

## Stop services:
``docker compose -f infra/docker/docker-compose.yml down``

## Service Ports

| Service          | Port       | Description                     |
|------------------|------------|---------------------------------|
| cart_service     | 8001:8000  | Manages user carts, checkout    |
| catalog_service  | 8002:8000  | Lists categories, services      |
| slot_service     | 8003:8000  | Manages slot availability       |
| order_api        | 8004:8000  | Mocked order management API     |
| postgres         | 5432:5432  | PostgreSQL database             |
| redis            | 6379:6379  | Redis cache for slot_service    |


## Environment variables for Booking System
### Copy to .env and update values

### JWT Public Key (RSA public key for RS256 verification)
JWT_PUBLIC_KEY=-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkcp9DkMyvX06iEJ2MDYa
QQH+oPH4FEH+l7TjDEvEVJVbnRTVFTGIoCr1PWGB4KwEEQDRnZbRDxzWOrTd25jN
EnKRsxXpWgrM9YQuMZBwziAq4yMYgbFPfI25GiFXOsthUvJDE+OpBbGkwWJpBWuz
rzP4TT5oEbl6MqdvliUE5mv/7af47koSFWKldm3/4aZrAmcdYk496pOWmW4HSHS0
w8xrwd69KxJM2vswcNA8PqRp1FRRhDYGJkzrFwmwwqI0P0Xb6vHxce0a7WG2UK4P
FjsrS+HUMErNy0r9POusL9UE1AUCXSEvUACMk5fRN+q/7SJ5tzmxt/R7Bl+Eoghx
uQIDAQAB
-----END PUBLIC KEY-----

### PostgreSQL credentials
POSTGRES_USER=sheba_user
POSTGRES_PASSWORD=sheba_password
POSTGRES_DB=sheba

### Redis (optional, defaults to localhost:6379)
REDIS_HOST=redis
REDIS_PORT=6379

## Notes

- **JWT_PUBLIC_KEY**: Embedded in docker-compose.yml due to issues importing from .env. In production, use .env or a secrets manager.
- **Testing**: Use generate_jwt.py to create JWT tokens for authenticated endpoints (requires Python 3.10+, python-jose).
- **Troubleshooting**: If services aren’t accessible, check logs (docker compose logs <service>) and ports (netstat -tulnp | grep 800[1-3]).

