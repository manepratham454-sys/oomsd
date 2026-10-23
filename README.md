# EV Charging Station Management System (EVCSMS)

This project contains the complete source code, tests, documentation, and diagrams for the full-stack **EV Charging Station Management System (EVCSMS)**.

- **Backend Folder**: [`evcsms/backend/`](./evcsms/backend/)
- **Frontend Folder**: [`evcsms/frontend/`](./evcsms/frontend/)
- **Diagrams & Specs**: [`evcsms/docs/`](./evcsms/docs/)
  - [3NF Entity Relationship Diagram](./evcsms/docs/er_diagram.md)
  - [OOP Class Diagram (GRASP & SOLID)](./evcsms/docs/class_diagram.md)
  - [Booking Flow Sequence Diagram](./evcsms/docs/sequence_diagram.md)
  - [Use Cases Specification](./evcsms/docs/use_cases.md)

Detailed setup guide and Mermaid diagrams are located in [`evcsms/README.md`](./evcsms/README.md).

### Quick Start (PowerShell on Windows)

#### 1. Backend Server
```powershell
cd evcsms\backend
python -m pip install -r requirements.txt
python seed.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- Swagger API Docs: `http://localhost:8000/docs`

#### 2. Frontend App
```powershell
cd evcsms\frontend
npm install
npm run dev
```
- Web Application: `http://localhost:5173`

#### 3. Run Backend Pytest Tests
```powershell
cd evcsms\backend
python -m pytest -v
```

#### Demo Credentials:
- **Station Admin**: `admin@evcsms.com` / `adminpassword123`
- **EV Owner**: `owner@evcsms.com` / `ownerpassword123`
