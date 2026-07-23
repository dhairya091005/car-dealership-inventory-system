# DriveDesk - Car Dealership Inventory System

DriveDesk is a full-stack web application designed for car dealerships to manage their vehicle inventory. It provides secure user authentication, role-based access control (Admin vs. Regular User), and complete inventory management features like purchasing and restocking vehicles.

Built with a modern stack leveraging **FastAPI**, **React**, and **Tailwind CSS**, and developed using strict **Test-Driven Development (TDD)** practices.

---

## 🚀 Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL (via SQLAlchemy ORM)
- **Authentication**: JWT (JSON Web Tokens) using `python-jose`
- **Data Validation**: Pydantic V2
- **Testing**: Pytest & HTTPX (26 passing tests covering all endpoints)

### Frontend
- **Framework**: React 18 (Vite)
- **Routing**: React Router DOM v6
- **Styling**: Tailwind CSS v4 & Lucide React Icons
- **HTTP Client**: Axios

---

## 🛠️ Setup Instructions

### 1. Database Setup
Ensure you have PostgreSQL running locally. You can use Docker:
```bash
docker run --name drivedesk-pg -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=car_dealership -p 5433:5432 -d postgres
```

### 2. Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the `backend/` directory:
```env
DATABASE_URL=postgresql://postgres:admin@localhost:5433/car_dealership
SECRET_KEY=your-super-secret-key
FIRST_ADMIN_EMAIL=admin@drivedesk.com
```

Run the backend development server:
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000` (Swagger UI at `/docs`).

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
The frontend will be available at `http://localhost:5173`.

---

## 🔒 Role-Based Access Control

The system implements two distinct roles:
1. **USER** (Default): Can view inventory, search/filter vehicles, and simulate "purchasing" a vehicle (decreases stock).
2. **ADMIN**: Has full CRUD access. Can add new vehicles, update details, delete vehicles, restock inventory, and promote other users to Admin status via the Admin Panel.

*Note: The first admin is automatically provisioned on startup if their email matches `FIRST_ADMIN_EMAIL` in your `.env` file.*

---

## 🧪 Testing

The backend is fully tested using TDD principles (Red-Green-Refactor). The test suite uses an isolated SQLite in-memory database to ensure tests are fast, reliable, and don't pollute the production database.

To run the test suite:
```bash
cd backend
pytest app/tests/ -v
```

---

## 📝 API Endpoints Summary

### Auth (`/api/auth`)
- `POST /register` - Register a new user
- `POST /login` - Authenticate and receive JWT

### Vehicles (`/api/vehicles`)
- `GET /` - List/search vehicles (Auth required)
- `POST /` - Add a vehicle (Admin only)
- `PUT /{id}` - Update a vehicle (Admin only)
- `DELETE /{id}` - Delete a vehicle (Admin only)

### Inventory (`/api/vehicles/{id}`)
- `POST /purchase` - Decrease stock by 1 (Auth required)
- `POST /restock` - Increase stock (Admin only)

### Admin (`/api/admin`)
- `GET /users` - List all registered users (Admin only)
- `POST /promote-user` - Promote a user to ADMIN role (Admin only)
