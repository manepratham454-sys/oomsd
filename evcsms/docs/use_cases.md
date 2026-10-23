# Use Cases Specification - EVCSMS

The EV Charging Station Management System (EVCSMS) serves four primary actors:
1. **EV Owner**
2. **Station Admin**
3. **Payment Gateway (Mock)**
4. **System Scheduler (APScheduler)**

---

## 1. Actor: EV Owner

| Use Case ID | Use Case Name | Pre-conditions | Primary Flow | Post-conditions |
|---|---|---|---|---|
| **UC-01** | Register & Authenticate | User is a new or existing user | Submits name, email, phone, and password. System hashes password with bcrypt and returns a signed JWT bearer token. | User session authenticated as `EV_OWNER`. |
| **UC-02** | Manage Electric Vehicles | User logged in | Registers EV with registration number, battery capacity (kWh), and connector type (`CCS2`, `Type 2`, `CHAdeMO`). | Vehicle is linked to the user for compatibility validation. |
| **UC-03** | Search Charging Stations | User logged in or guest | User filters by city, connector type, availability, or supplies lat/lng coordinates for Haversine distance search. | Interactive map and station cards rendered with distance and live charger counts. |
| **UC-04** | Check Charger Availability | Station selected | System queries real-time status of all chargers (`Available`, `Busy`, `Reserved`, `Offline`). | Live status badges and tariff displayed to user. |
| **UC-05** | Book Charging Slot | Station and charger selected | User selects preferred vehicle, start time, and end time. System verifies connector compatibility and rejects overlapping slots. | Charger marked `Reserved`, booking confirmed, confirmation notification dispatched. |
| **UC-06** | Start Charging Session | Confirmed booking exists | User arrives at station within grace window (up to 15 min before start time). Clicks "Start Charging". | Charger state set to `Busy`, session initiated, telemetry ticker starts. |
| **UC-07** | Stop Charging Session | Active session in progress | User stops charging or time window concludes. System computes: $\text{Units} = \text{Power (kW)} \times \text{Duration (h)}$, $\text{Cost} = \text{Units} \times \text{PricePerUnit}$. | Session status `Completed`, charger released to `Available`, billing summary generated. |
| **UC-08** | Process Payment | Session completed | User selects payment mode (UPI, Card, Digital Wallet). Strategy executes transaction. | Transaction ID generated, payment marked `Success`, session marked paid. |
| **UC-09** | View & Download Invoice | Payment completed | User requests invoice for a session. System calculates net amount, 18% GST breakdown, and station metadata. | Itemized tax invoice rendered. |
| **UC-10** | Receive & Read Notifications | User logged in | System displays unread badge counter. User views reminder alerts and marks notifications as read. | Notifications marked read in database. |

---

## 2. Actor: Station Admin

| Use Case ID | Use Case Name | Pre-conditions | Primary Flow | Post-conditions |
|---|---|---|---|---|
| **UC-11** | Admin Authentication | Admin credentials | Log in with role `ADMIN`. | Authenticated with administrative privileges. |
| **UC-12** | Station Management | Admin logged in | Create, update, or remove physical charging stations with geo-coordinates and city details. | Station catalog updated in database and live map. |
| **UC-13** | Charger & Tariff Configuration | Station exists | Add chargers with power ratings (e.g. 7.4 kW AC, 60 kW DC Fast), configure connector types, and adjust unit price (₹/kWh). | New pricing and charger slots immediately available for booking. |
| **UC-14** | Override Charger Operational State | Station exists | Admin toggles charger status (`Available`, `Busy`, `Reserved`, `Offline` for maintenance). | Real-time state updated and live bookings prevented if offline. |
| **UC-15** | View Analytics & Usage Reports | Admin logged in | Admin navigates to Reports tab to inspect daily energy delivered (kWh), session counts, daily revenue, and station utilization rates. | Recharts graphs visualizes daily trends and summary cards. |

---

## 3. Actor: Payment Gateway (Mock)

| Use Case ID | Use Case Name | Primary Flow | Post-conditions |
|---|---|---|---|
| **UC-16** | Execute Strategy Transaction | Receives amount, mode (`UPI`, `Card`, `Wallet`), and mock credentials. Evaluates transaction rules and issues gateway response. | Returns boolean status, transaction ID (e.g., `UPI-XXXXXXXX`), and gateway message. |

---

## 4. Actor: System Scheduler (APScheduler)

| Use Case ID | Use Case Name | Trigger | Primary Flow | Post-conditions |
|---|---|---|---|---|
| **UC-17** | Expire Unclaimed Bookings | Cron every 60s | Checks for confirmed bookings where start time is > 10 minutes in the past and no charging session has started. | Booking set to `Expired`, charger reset to `Available`, alert notification dispatched to user. |
| **UC-18** | Send Advance Slot Reminders | Cron every 60s | Queries bookings starting within the next 15 minutes where `reminder_sent == False`. | Reminder notification dispatched, `reminder_sent` flagged `True`. |
