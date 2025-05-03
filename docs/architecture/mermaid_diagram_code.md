erDiagram
    %% Cart Service
    cart ||--o{ cart_item : "has"
    cart ||--o{ booking : "has"
    cart }o--|| External_Users : "belongs to"
    cart {
        UUID id PK
        UUID user_id FK
        ENUM status "active, checked_out"
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }
    cart_item {
        UUID id PK
        UUID cart_id FK
        UUID service_id FK
        INTEGER quantity
        DECIMAL price
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }
    booking {
        UUID id PK
        UUID cart_id FK
        UUID order_id
        DECIMAL total_price
        ENUM status "pending, confirmed, cancelled"
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    %% Catalog Service
    category ||--o{ subcategory : "has"
    subcategory ||--o{ service : "has"
    category {
        UUID id PK
        VARCHAR name
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }
    subcategory {
        UUID id PK
        UUID category_id FK
        VARCHAR name
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }
    service {
        UUID id PK
        UUID subcategory_id FK
        VARCHAR name
        DECIMAL price
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    %% Partner Slot Service
    partner_slot {
        UUID id PK
        UUID service_id FK
        UUID partner_id
        DATE date
        VARCHAR time_slot
        BOOLEAN is_available
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    %% External Users (Stub)
    External_Users {
        UUID id PK "External, not implemented"
    }

    %% Cross-Service Relationships
    cart_item }o--|| service : "references"
    partner_slot }o--|| service : "references"