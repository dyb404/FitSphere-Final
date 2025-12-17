# Database Setup Guide

## Fixing PostgreSQL Connection Error

The error `password authentication failed for user "postgres"` means your PostgreSQL password doesn't match the default.

### Option 1: Update .env File (Recommended)

1. **Create/Edit `.env` file** in the `backend` folder:
   ```bash
   cd backend
   # Create .env file (or edit if exists)
   ```

2. **Add your PostgreSQL credentials:**
   ```env
   DATABASE_URL=postgresql://postgres:YOUR_ACTUAL_PASSWORD@localhost:5432/fitsphere
   SECRET_KEY=your-secret-key-change-in-production-min-32-characters-long
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

   **Replace `YOUR_ACTUAL_PASSWORD`** with your PostgreSQL password.

### Option 2: Update config.py Directly

Edit `backend/app/core/config.py`:

```python
DATABASE_URL: str = "postgresql://postgres:YOUR_PASSWORD@localhost:5432/fitsphere"
```

Replace `YOUR_PASSWORD` with your actual PostgreSQL password.

### Option 3: Reset PostgreSQL Password

If you forgot your password:

**Windows (using pgAdmin):**
1. Open pgAdmin
2. Right-click on PostgreSQL server → Properties
3. Go to Connection tab
4. Update password

**Command Line:**
```bash
# Connect as postgres user
psql -U postgres

# Change password
ALTER USER postgres WITH PASSWORD 'newpassword';

# Exit
\q
```

### Option 4: Use Different PostgreSQL User

If you have another PostgreSQL user:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/fitsphere
```

## Verify Database Connection

1. **Test connection:**
   ```bash
   psql -U postgres -d fitsphere
   ```

2. **If database doesn't exist, create it:**
   ```bash
   psql -U postgres
   CREATE DATABASE fitsphere;
   \q
   ```

## Common Database URLs

- **Default (if password is 'postgres'):**
  ```
  postgresql://postgres:postgres@localhost:5432/fitsphere
  ```

- **No password (not recommended):**
  ```
  postgresql://postgres@localhost:5432/fitsphere
  ```

- **Custom user:**
  ```
  postgresql://myuser:mypassword@localhost:5432/fitsphere
  ```

- **Different port:**
  ```
  postgresql://postgres:password@localhost:5433/fitsphere
  ```

## After Fixing Connection

1. **Restart the backend server:**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Seed the database:**
   ```bash
   python seed_data.py
   ```

3. **Verify it works:**
   - Check http://localhost:8000
   - Should see: `{"message":"FitSphere API is running"}`

