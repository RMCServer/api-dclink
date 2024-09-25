import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def link_user_to_discord(link_token: str, discord_user_id: int) -> bool:
    connection = get_db_connection()

    if connection is None:
        print("Failed to connect to the database.")
        return False

    cursor = connection.cursor(dictionary=True)

    # Check if the link_token exists
    query_check = "SELECT * FROM users WHERE link_token = %s"
    query_update = "UPDATE users SET synced_discord = %s WHERE link_token = %s"

    try:
        cursor.execute(query_check, (link_token,))
        result = cursor.fetchone()

        if result:
            cursor.execute(query_update, (discord_user_id, link_token))
            connection.commit()
            return True
        else:
            print(f"No user found with link_token '{link_token}'.")
            return False
    except Exception as e:
        print(f"Error during database operation: {e}")
        return False
    finally:
        cursor.close()
        connection.close()
