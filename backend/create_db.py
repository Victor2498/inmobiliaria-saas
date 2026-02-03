import asyncio
import asyncpg
from app.core.config import settings

async def create_database():
    print(f"Connecting to Postgres at {settings.POSTGRES_SERVER} as {settings.POSTGRES_USER}...")
    try:
        # Connect to default 'postgres' database
        conn = await asyncpg.connect(
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            database='postgres',
            host=settings.POSTGRES_SERVER
        )
        print("Connected successfully to 'postgres' DB.")
        
        # Check if inmonea_db exists
        exists = await conn.fetchval("SELECT 1 FROM pg_database WHERE datname = $1", settings.POSTGRES_DB)
        if not exists:
            print(f"Database {settings.POSTGRES_DB} does not exist. Creating...")
            await conn.execute(f'CREATE DATABASE "{settings.POSTGRES_DB}"')
            print(f"Database {settings.POSTGRES_DB} created successfully!")
        else:
            print(f"Database {settings.POSTGRES_DB} already exists.")
            
        await conn.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    import sys
    import os
    # Fix path
    sys.path.append(os.getcwd())
    asyncio.run(create_database())
