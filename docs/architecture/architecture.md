# Booking System Architecture

## Overview
The Booking System is a microservices-based platform for service booking, comprising three services: `cart_service`, `catalog_service`, and `slot_service`. It uses PostgreSQL for persistent storage, Redis for caching, and REST APIs for communication. JWT authentication secures endpoints, with `customer` and `admin` roles. This document outlines the architecture, design decisions, and a high-level diagram.

## Architecture Components

1. **Microservices**
   - **Cart Service**:
     - Manages user carts (CRUD) and checkout.
     - Endpoints: `POST /carts`, `GET /carts/{cart_id}`, `PUT /carts/{cart_id}`, `DELETE /carts/{cart_id}`, `POST /carts/{cart_id}/checkout`.
     - Database: PostgreSQL (schema: `cart`, tables: `cart`, `cart_item`, `booking`).
     - Dependencies: Calls `slot_service` for slot validation, `order_api` for booking.
   - **Catalog Service**:
     - Provides hierarchical service listings (category → subcategory → service).
     - Endpoints: `GET /categories`, `GET /categories/{category_id}/subcategories`, `GET /subcategories/{subcategory_id}/services`, `GET /services/{service_id}`, admin-only POST endpoints.
     - Database: PostgreSQL (schema: `catalog`, tables: `category`, `subcategory`, `service`).
   - **Slot Service**:
     - Manages partner slot availability (mocked).
     - Endpoints: `GET /slots/{partner_id}/{service_id}`, `POST /slots` (admin-only).
     - Database: PostgreSQL (schema: `slot`, table: `partner_slot`).
     - Caching: Redis for slot availability (1-hour TTL).

2. **Database**:
   - **PostgreSQL**: Single instance with schemas (`cart`, `catalog`, `slot`) for logical separation.
   - **Redis**: Used by `slot_service` for caching slot availability.

3. **Authentication**:
   - **JWT**: Tokens issued by an external auth service, validated in each microservice using `shared/auth/jwt.py`.
   - **Roles**: `customer` (read/write for own data), `admin` (full access).

4. **Mocked Order API**:
   - A simple FastAPI service (`infra/order_api/`) simulating an Order Management System.
   - Endpoint: `POST /orders`, returns `order_id`.


## Design Decisions
1. **Three Microservices**: Limited to `cart_service`, `catalog_service`, `slot_service` per requirements, ensuring focused responsibilities.
2. **Shared PostgreSQL**: Single database with schemas reduces complexity for this assignment. In production, separate databases per service could improve isolation.
3. **Redis Caching**: Used in `slot_service` to optimize slot availability checks, critical for checkout performance.
4. **REST Communication**: Synchronous HTTP calls simplify development. In production, async queues (e.g., RabbitMQ) could enhance resilience.
5. **JWT Authentication**: Centralized token validation via `shared/auth/jwt.py` keeps services lightweight. Role-based access ensures security.
6. **Mocked Order API**: Simplifies integration with an external OMS by returning a UUID (`order_id`).

## Scalability Considerations
- **Horizontal Scaling**: Each service can run multiple instances behind a load balancer.
- **Caching**: Redis reduces database load for slot checks.
- **Stateless Services**: Services store state in PostgreSQL/Redis, enabling easy scaling.
- **Rate Limiting**: Not implemented but could be added via an API gateway (e.g., Kong).