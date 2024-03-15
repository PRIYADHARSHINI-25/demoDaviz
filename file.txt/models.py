import mysql.connector
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2023",
    database="db"
)
cursor = db.cursor()


cursor.execute("""
               CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);
               """)



def add_user(username, email, password):
    sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
    val = (username, email, password)
    cursor.execute(sql, val)
    db.commit()
    
    
def delete_user(id):
    sql='DELETE FROM users WHERE id=(%s)'
    val=(id,)
    cursor.execute(sql,val)
    db.commit()
