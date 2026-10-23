# Entity-Relationship Diagram (3NF) - EVCSMS

The database design strictly satisfies Third Normal Form (3NF):
- Every non-key attribute depends directly on the primary key, the whole key, and nothing but the key.
- Transitive dependencies are removed (e.g. Station attributes isolated from Chargers, Session attributes isolated from Bookings).

```mermaid
erDiagram
    USER ||--o{ VEHICLE : "owns"
    USER ||--o{ BOOKING : "places"
    USER ||--o{ NOTIFICATION : "receives"
    USER ||--o| ADMIN : "has profile"
    
    STATION ||--|{ CHARGER : "contains"
    
    CHARGER ||--o{ BOOKING : "scheduled for"
    VEHICLE ||--o{ BOOKING : "assigned to"
    
    BOOKING ||--o| CHARGING_SESSION : "generates"
    CHARGING_SESSION ||--o| PAYMENT : "settled by"

    USER {
        int id PK
        string name
        string email UK
        string phone_no
        string password_hash
        string role "EV_OWNER | ADMIN"
        datetime created_at
    }

    VEHICLE {
        int id PK
        string reg_no UK
        float battery_capacity "kWh"
        string connector_type "CCS2 | Type 2 | CHAdeMO"
        int user_id FK
    }

    STATION {
        int id PK
        string name
        string city
        string state
        string country
        float latitude
        float longitude
        string address
        datetime created_at
    }

    CHARGER {
        int id PK
        int station_id FK
        string type "AC | DC Fast"
        string connector_type "CCS2 | Type 2 | CHAdeMO"
        float power_kw
        string status "Available | Busy | Reserved | Offline"
        float price_per_unit "INR / kWh"
    }

    BOOKING {
        int id PK
        int user_id FK
        int charger_id FK
        int vehicle_id FK
        datetime start_time
        datetime end_time
        string status "Pending | Confirmed | Cancelled | Completed | Expired"
        boolean reminder_sent
        datetime created_at
    }

    CHARGING_SESSION {
        int id PK
        int booking_id FK
        datetime start_time
        datetime end_time
        float units_consumed "kWh"
        float total_cost "INR"
        string status "Active | Completed"
    }

    PAYMENT {
        int id PK
        int session_id FK
        float amount
        string payment_mode "UPI | Card | Wallet"
        string status "Pending | Success | Failed"
        string transaction_id UK
        datetime created_at
    }

    ADMIN {
        int id PK
        int user_id FK
        string name
        string email
    }

    NOTIFICATION {
        int id PK
        int user_id FK
        text message
        datetime timestamp
        string type
        boolean is_read
    }
```
