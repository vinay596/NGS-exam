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
def submit_response(student_id, question_id, selected_option):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch the correct answer for the question
    cursor.execute("SELECT correct_answer FROM questions WHERE id = %s", (question_id,))
    correct_answer = cursor.fetchone()[0]

    # Determine if the submitted answer is correct
    is_correct = (selected_option == correct_answer)
    
    # Insert the response into the Responses table
    cursor.execute(
        "INSERT INTO responses (student_id, question_id, selected_option, is_correct) VALUES (%s, %s, %s, %s)",
        (student_id, question_id, selected_option, is_correct)
    )
    
    connection.commit()
    cursor.close()
    connection.close()
    
    return is_correct

def calculate_marks(student_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Calculate the total number of correct answers
    cursor.execute("SELECT COUNT(*) FROM responses WHERE student_id = %s AND is_correct = TRUE", (student_id,))
    total_marks = cursor.fetchone()[0]

    # Update or insert the total marks into the Marks table
    cursor.execute(
        "INSERT INTO marks (student_id, total_marks) VALUES (%s, %s) ON DUPLICATE KEY UPDATE total_marks = VALUES(total_marks)",
        (student_id, total_marks)
    )
    
    connection.commit()
    cursor.close()
    connection.close()
    
    return total_marks
# Example function to fetch questions from the database
def fetch_questions(category):
    db_connection = get_db_connection()
    if db_connection is not None:
        cursor = db_connection.cursor(dictionary=True)
        query = "SELECT * FROM questions WHERE category = %s"
        cursor.execute(query, (category,))
        questions = cursor.fetchall()
        cursor.close()
        db_connection.close()
        return questions
    else:
        return []


# Example usage
if __name__ == "__main__":
    category = 'aptitude'  # Or 'verbal', depending on what categories you have
    questions = fetch_questions(category)
    for question in questions:
        print(question)
