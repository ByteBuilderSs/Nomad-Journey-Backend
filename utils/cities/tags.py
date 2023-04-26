import psycopg2
import csv
import uuid

conn = psycopg2.connect(
    host="localhost",
    database="nomadjourney",
    user="postgres",
    password="aysa1380"
)

with open('hobbies.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  
    rows = [(str(uuid.uuid4()), *row) for row in reader] 

table_name = 'blog_tag'
columns = ','.join(['uid','tag_name']) 
placeholders = ','.join(['%s', '%s'])  

query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"


with conn.cursor() as cursor:
    for row in rows:
        cursor.execute(query, row)
    conn.commit()


conn.close()
