import os

import pymysql
from fastapi import FastAPI, HTTPException
from pymysql.err import OperationalError

# Database configuration using environment variables
DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "visitdb")

app = FastAPI()

# Function to establish a database connection
def get_db_connection():
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except OperationalError as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to database: {str(e)}")

# Function to initialize the database and create the visits table
def init_db():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Create table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS visits (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    count INT DEFAULT 0
                )
            """)
            # Insert initial row if table is empty
            cursor.execute("INSERT INTO visits (count) SELECT 0 WHERE NOT EXISTS (SELECT 1 FROM visits)")
        connection.commit()
    except OperationalError as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize database table: {str(e)}")
    finally:
        connection.close()

# Startup event to initialize the database
@app.on_event("startup")
async def startup_event():
    init_db()

# Root endpoint to increment and display the visit count
@app.get("/")
async def read_root():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Increment the visit count
            cursor.execute("UPDATE visits SET count = count + 1 WHERE id = 1")
            # Fetch the updated count
            cursor.execute("SELECT count FROM visits WHERE id = 1")
            result = cursor.fetchone()
            count = result["count"] if result else 0
        connection.commit()
        return {"message": f"Visit count: {count}"}
    except OperationalError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        connection.close()
