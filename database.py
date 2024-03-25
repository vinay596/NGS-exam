import mysql.connector

# Directly define your database configuration
config = {
    'user': 'root',
    'password': 'vinay321',  # Replace with your actual password
    'host': '127.0.0.1',
    'port': 3306,  # Ensure this is an integer
    'database': 'exam_website',
    'raise_on_warnings': True
}

# Function to connect to the database
def get_db_connection():
    try:
        db_connection = mysql.connector.connect(**config)
        print("Database connection successful")
        return db_connection
    except mysql.connector.Error as err:
        print(f"Failed to connect to database: {err}")
        return None

# Example function to fetch questions from the database
def fetch_questions():
    db_connection = get_db_connection()
    if db_connection is not None:
        cursor = db_connection.cursor()
        query = "SELECT * FROM questions"
        cursor.execute(query)
        questions = cursor.fetchall()
        cursor.close()
        db_connection.close()
        return questions
    else:
        return []

# Example usage
if __name__ == "__main__":
    questions = fetch_questions()
    for question in questions:
        print(question)
