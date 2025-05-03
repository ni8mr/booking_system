# Entity-Relationship Diagram (ERD)

This document provides a text-based representation of the ERD for the Booking System, covering the core tables: `cart`, `cart_item`, `booking`, `category`, `subcategory`, `service`, and `partner_slot`. Relationships are indicated with foreign keys.

## ERD Representation


## Notes
- **Schemas**:
  - `cart`, `cart_item`, `booking`: In `cart` schema (used by `cart_service`).
  - `category`, `subcategory`, `service`: In `catalog` schema (used by `catalog_service`).
  - `partner_slot`: In `slot` schema (used by `slot_service`).
- **Relationships**:
  - `cart` 1:N `cart_item`, `booking`.
  - `cart_item` N:1 `service`, `partner_slot`.
  - `service` N:1 `subcategory`.
  - `subcategory` N:1 `category`.
- **Indexes** (recommended):
  - `cart(user_id)`: For user-specific queries.
  - `cart_item(cart_id, service_id, slot_id)`: For efficient joins.
  - `partner_slot(partner_id, service_id, slot_time)`: For availability checks.
  - `booking(order_id)`: For order lookups.