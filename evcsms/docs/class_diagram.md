# Class Diagram - EVCSMS (OOP & Architecture)

Demonstrating Object-Oriented Software Modeling and Design (OOSMD) patterns:
- **GRASP Patterns**:
  - `BookingController`: GRASP Controller coordinating booking workflows.
  - `Booking`: GRASP Creator for `ChargingSession`.
  - `ChargingSession`: GRASP Information Expert calculating energy and total cost.
  - `Notification`: GRASP High Cohesion handling messaging only.
  - `Payment`: GRASP Low Coupling dependent only on Session and User.
- **SOLID Principles**:
  - **Single Responsibility Principle (SRP)**: `PaymentService` manages billing only.
  - **Open-Closed Principle (OCP)** & **Liskov Substitution Principle (LSP)**: `PaymentMethod` strategy hierarchy (`UPIPayment`, `CardPayment`, `WalletPayment`) swappable without client code modifications.
  - **Interface Segregation Principle (ISP)**: `IBookingService`, `IPaymentService`, `IStationService`, `ISessionService`.
  - **Dependency Inversion Principle (DIP)**: High-level controllers depend on service interfaces injected via FastAPI.

```mermaid
classDiagram
    direction TB

    %% Presentation / Controller Layer
    class BookingController {
        -IBookingService booking_service
        +create_booking(user_id, charger_id, start_time, end_time, vehicle_id)
        +get_user_bookings(user_id)
        +cancel_booking(booking_id, user_id)
    }

    class SessionController {
        -ISessionService session_service
        +start_session(booking_id, user_id)
        +stop_session(session_id, user_id, custom_units)
        +get_session(session_id)
    }

    class PaymentController {
        -IPaymentService payment_service
        +process_payment(session_id, user_id, payment_mode, details)
        +get_user_payments(user_id)
        +get_invoice(payment_id, user_id, is_admin)
    }

    %% Service Interfaces (ISP / DIP)
    class IBookingService {
        <<interface>>
        +create_booking(user_id, charger_id, start_time, end_time, vehicle_id)
        +get_user_bookings(user_id)
        +cancel_booking(booking_id, user_id)
        +check_slot_conflict(charger_id, start_time, end_time)
    }

    class IPaymentService {
        <<interface>>
        +process_payment(session_id, user_id, payment_mode, details)
        +get_user_payments(user_id)
        +get_invoice(payment_id, user_id, is_admin)
    }

    class ISessionService {
        <<interface>>
        +start_session(booking_id, user_id)
        +stop_session(session_id, user_id, custom_units)
        +get_session(session_id)
    }

    %% Service Implementations
    class BookingService {
        -BookingRepository booking_repo
        -ChargerRepository charger_repo
        -VehicleRepository vehicle_repo
        -NotificationService notif_service
        +create_booking(...)
        +check_slot_conflict(...)
    }

    class PaymentService {
        -PaymentRepository payment_repo
        -SessionRepository session_repo
        +process_payment(...)
        +get_invoice(...)
    }

    class SessionService {
        -SessionRepository session_repo
        -BookingRepository booking_repo
        -ChargerRepository charger_repo
        +start_session(...)
        +stop_session(...)
    }

    %% Strategy Pattern (OCP / LSP)
    class PaymentMethod {
        <<abstract>>
        +mode_name: str
        +process_transaction(amount, details)* Tuple
    }

    class UPIPayment {
        +mode_name: "UPI"
        +process_transaction(amount, details) Tuple
    }

    class CardPayment {
        +mode_name: "Card"
        +process_transaction(amount, details) Tuple
    }

    class WalletPayment {
        +mode_name: "Wallet"
        +process_transaction(amount, details) Tuple
    }

    class PaymentStrategyFactory {
        -_strategies: Dict
        +get_strategy(mode) PaymentMethod
        +register_strategy(mode, strategy)
    }

    %% Domain Entities Layer (GRASP)
    class ChargingStation {
        +int station_id
        +string name
        +string city
        +float latitude
        +float longitude
        +add_charger(charger)
    }

    class Charger {
        +int charger_id
        +string type
        +string connector_type
        +float power_kw
        +string status
        +float price_per_unit
        +reserve()
        +start_charging()
        +release()
    }

    class Vehicle {
        +int vehicle_id
        +string reg_no
        +float battery_capacity
        +string connector_type
        +is_compatible_with(charger_connector) bool
    }

    class Booking {
        +int booking_id
        +datetime start_time
        +datetime end_time
        +string status
        +create_session() ChargingSession
        +cancel()
        +expire()
    }

    class ChargingSession {
        +int session_id
        +datetime start_time
        +datetime end_time
        +float units_consumed
        +float total_cost
        +string status
        +compute_energy_and_cost(power_kw, price_per_unit, end_time) float
    }

    class Payment {
        +int payment_id
        +float amount
        +string payment_mode
        +string status
        +string transaction_id
    }

    class Notification {
        +int notification_id
        +int user_id
        +string message
        +datetime timestamp
        +mark_as_read()
    }

    %% Inheritance and Interface Realizations
    IBookingService <|.. BookingService
    IPaymentService <|.. PaymentService
    ISessionService <|.. SessionService

    PaymentMethod <|-- UPIPayment
    PaymentMethod <|-- CardPayment
    PaymentMethod <|-- WalletPayment

    BookingController --> IBookingService
    PaymentController --> IPaymentService
    SessionController --> ISessionService

    PaymentService --> PaymentStrategyFactory
    PaymentStrategyFactory --> PaymentMethod

    %% Domain Entity Interactions (GRASP Creator & Information Expert)
    ChargingStation "1" o-- "*" Charger : aggregates
    Booking ..> ChargingSession : creates (Creator)
    ChargingSession ..> Charger : references power_kw (Expert)
    Booking --> Vehicle : validates connector
    Payment --> ChargingSession : references
```
