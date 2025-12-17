# FitSphere Backend

FastAPI backend for the FitSphere fitness platform.

## Setup Instructions

1. **Install PostgreSQL** (if not already installed)
   - Download from https://www.postgresql.org/download/
   - Create a database named `fitsphere`

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment**
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Environment Variables**
   - Copy `.env.example` to `.env`
   - Update `DATABASE_URL` with your PostgreSQL credentials
   - Update `SECRET_KEY` with a secure random string (min 32 characters)

6. **Run Database Migrations**
   - The tables will be created automatically when you start the server
   - Or run: `python -c "from app.db.database import Base, engine; Base.metadata.create_all(bind=engine)"`

7. **Seed Database (Optional but Recommended)**
   ```bash
   python seed_data.py
   ```
   This will create sample users, workouts, assignments, progress logs, and health tips.

8. **Start the Server**
   ```bash
   uvicorn app.main:app --reload
   ```

9. **Access API**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc

## Sample Accounts

After running `seed_data.py`, you can use these accounts:

- **Trainer**: trainer@fitsphere.com / trainer123
- **Client**: client@fitsphere.com / client123
- **Admin**: admin@fitsphere.com / admin123

## API Endpoints

- `/api/auth` - Authentication (register, login, me)
- `/api/users` - User management
- `/api/workouts` - Workout CRUD
- `/api/assignments` - Workout assignments
- `/api/progress` - Progress logs
- `/api/health-tips` - Health tips

See `/docs` for full API documentation.

