import psycopg2
import csv

conn = psycopg2.connect(
    host="localhost",
    database="nomadjourney",
    user="postgres",
    password="aysa1380"
)

with open('languages.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  
    rows = [row for row in reader]

table_name = 'utils_language'
columns = ','.join(['id','language_name']) 
placeholders = ','.join(['%s', '%s'])  

query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"


with conn.cursor() as cursor:
    for row in rows:
        cursor.execute(query, row)
    conn.commit()


conn.close()
