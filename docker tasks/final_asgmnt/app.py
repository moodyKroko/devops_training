import os

import pymysql
from fastapi import FastAPI, HTTPException
from pymysql.err import OperationalError

# Database configuration using environment variables
DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "leon")
DB_PASSWORD = os.getenv("DB_PASSWORD", "leon123456")
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
            cursorclass=pymysql.cursors.DictCursor,
        )
        return connection
    except OperationalError as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to database: {str(e)}"
        )


# Function to initialize the database and create the visits table
def init_db():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Create table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS visits (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    count INT DEFAULT 0,
                    visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # Insert initial row if table is empty
            cursor.execute(
                "INSERT INTO visits (count) SELECT 0 WHERE NOT EXISTS (SELECT 1 FROM visits)"
            )
        connection.commit()
    except OperationalError as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to initialize database table: {str(e)}"
        )
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
            cursor.execute("INSERT INTO visits () VALUES ()")
            connection.commit()

            # get total visits
            cursor.execute("SELECT COUNT(*) AS total_visits FROM visits")
            total_visits = cursor.fetchone()["total_visits"]

            # Fetch the updated count
            cursor.execute("""
                SELECT DATE(visited_at) AS visit_date, COUNT(*) AS count
                FROM visits
                GROUP BY DATE(visited_at)
                ORDER BY visit_date DESC
            """)
            result = cursor.fetchall()

            daily_breakdown = [
                f"{row['visit_date']}: {row['count']} visits" for row in result
            ]

        return {
            "status": "success",
            "data": {
                "total_visits": total_visits,
                "daily_breakdown": daily_breakdown,
            },
        }
    except OperationalError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        connection.close()
