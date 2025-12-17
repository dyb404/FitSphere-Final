"""
Helper script to create .env file for database configuration
Run this script and enter your PostgreSQL password when prompted
"""

import os

def create_env_file():
    print("=" * 60)
    print("FitSphere Database Configuration Setup")
    print("=" * 60)
    print()
    
    # Get PostgreSQL password
    print("Enter your PostgreSQL password for user 'postgres':")
    print("(Press Enter if you want to use default 'postgres')")
    password = input("Password: ").strip()
    
    if not password:
        password = "postgres"
        print("Using default password: postgres")
    
    # Get database name
    print()
    print("Enter database name (default: fitsphere):")
    db_name = input("Database name: ").strip()
    if not db_name:
        db_name = "fitsphere"
    
    # Create .env content
    env_content = f"""# Database Configuration
DATABASE_URL=postgresql://postgres:{password}@localhost:5432/{db_name}

# Security
SECRET_KEY=your-secret-key-change-in-production-min-32-characters-long-please-use-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
"""
    
    # Write .env file
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    try:
        with open(env_path, 'w') as f:
            f.write(env_content)
        print()
        print("✅ Success! Created .env file at:", env_path)
        print()
        print("Next steps:")
        print("1. Restart your backend server (Ctrl+C then uvicorn app.main:app --reload)")
        print("2. Run: python seed_data.py")
        print()
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        print()
        print("You can manually create a .env file in the backend folder with:")
        print()
        print(env_content)

if __name__ == "__main__":
    create_env_file()

