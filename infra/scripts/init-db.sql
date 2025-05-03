-- Create schemas
CREATE SCHEMA IF NOT EXISTS cart;
CREATE SCHEMA IF NOT EXISTS catalog;
CREATE SCHEMA IF NOT EXISTS slot;

-- Cart Service tables
CREATE TABLE cart.cart (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cart.cart_item (
    id UUID PRIMARY KEY,
    cart_id UUID REFERENCES cart.cart(id),
    service_id UUID NOT NULL,
    partner_id UUID NOT NULL,
    slot_id UUID NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL NOT NULL
);

CREATE TABLE cart.booking (
    id UUID PRIMARY KEY,
    cart_id UUID REFERENCES cart.cart(id),
    order_id UUID,
    user_id UUID,
    total_price DECIMAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Catalog Service tables
CREATE TABLE catalog.category (
    id UUID PRIMARY KEY,
    name VARCHAR NOT NULL
);

CREATE TABLE catalog.subcategory (
    id UUID PRIMARY KEY,
    name VARCHAR NOT NULL,
    category_id UUID REFERENCES catalog.category(id)
);

CREATE TABLE catalog.service (
    id UUID PRIMARY KEY,
    name VARCHAR NOT NULL,
    subcategory_id UUID REFERENCES catalog.subcategory(id),
    price DECIMAL NOT NULL,
    duration INTEGER NOT NULL
);

-- Slot Service table
CREATE TABLE slot.partner_slot (
    id UUID PRIMARY KEY,
    partner_id UUID NOT NULL,
    service_id UUID NOT NULL,
    slot_time TIMESTAMP NOT NULL,
    is_available BOOLEAN NOT NULL
);