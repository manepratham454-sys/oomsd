# Sequence Diagram: Book Charging Slot - EVCSMS

This sequence diagram directly models the booking workflow:
`User searches stations -> system checks charger availability -> available chargers displayed -> user creates booking -> charger reserved -> booking confirmed -> notification sent.`

```mermaid
sequenceDiagram
    autonumber
    actor User as EV Owner
    participant UI as Frontend Client (React)
    participant StationRouter as Station Router
    participant StationCtrl as Station Controller
    participant StationSvc as Station Service
    participant BookingRouter as Booking Router
    participant BookingCtrl as Booking Controller
    participant BookingSvc as Booking Service
    participant ChargerRepo as Charger Repository
    participant BookingRepo as Booking Repository
    participant NotifSvc as Notification Service
    participant DB as SQLite / PostgreSQL

    %% Step 1: User searches stations
    Note over User, UI: Step 1: User Searches Stations
    User->>UI: Selects city / enables nearby geo-search
    UI->>StationRouter: GET /api/v1/stations?city=Pune&available_only=true
    StationRouter->>StationCtrl: get_stations(city="Pune", available_only=true)
    StationCtrl->>StationSvc: get_stations(...)
    
    %% Step 2: System checks charger availability
    Note over StationSvc, DB: Step 2: System Checks Charger Availability
    StationSvc->>DB: Query Stations with joined Chargers
    DB-->>StationSvc: Return stations & charger telemetry
    StationSvc->>StationSvc: Filter available chargers & calculate geo distance
    StationSvc-->>StationCtrl: Station list with available counts & tariffs
    StationCtrl-->>StationRouter: 200 OK [StationResponse]
    StationRouter-->>UI: JSON list of stations
    
    %% Step 3: Available chargers displayed
    Note over UI, User: Step 3: Available Chargers Displayed
    UI->>User: Displays interactive station pins on map & charger cards

    %% Step 4: User creates booking
    Note over User, UI: Step 4: User Creates Booking
    User->>UI: Selects Charger #1, Vehicle (CCS2), Date & Time slot
    UI->>BookingRouter: POST /api/v1/bookings {charger_id, vehicle_id, start_time, end_time}
    BookingRouter->>BookingCtrl: create_booking(user_id, charger_id, start, end, vehicle_id)
    BookingCtrl->>BookingSvc: create_booking(...)

    %% Conflict and Compatibility Validations
    BookingSvc->>BookingSvc: Validate vehicle connector == charger connector
    BookingSvc->>BookingRepo: check_slot_conflict(charger_id, start, end)
    BookingRepo->>DB: Query existing overlapping bookings
    DB-->>BookingRepo: No conflicts found (empty)
    BookingRepo-->>BookingSvc: Conflict check OK (False)

    %% Step 5: Charger reserved & Booking confirmed
    Note over BookingSvc, DB: Step 5: Charger Reserved & Booking Confirmed
    BookingSvc->>DB: INSERT INTO bookings (user_id, charger_id, status='Confirmed')
    DB-->>BookingSvc: Booking record #42 created
    BookingSvc->>ChargerRepo: update_status(charger_id, "Reserved")
    ChargerRepo->>DB: UPDATE chargers SET status='Reserved' WHERE id=1
    DB-->>ChargerRepo: OK

    %% Step 6: Notification sent
    Note over BookingSvc, User: Step 6: Notification Sent
    BookingSvc->>NotifSvc: send_notification(user_id, "Booking #42 confirmed for Charger #1", "BOOKING_CONFIRMED")
    NotifSvc->>DB: INSERT INTO notifications (...)
    DB-->>NotifSvc: Notification saved
    
    BookingSvc-->>BookingCtrl: Booking instance (status='Confirmed')
    BookingCtrl-->>BookingRouter: Serialized BookingResponse
    BookingRouter-->>UI: 201 Created {id: 42, status: "Confirmed", ...}
    UI->>User: Renders Booking Confirmation modal + Notification bell alert badge
```
