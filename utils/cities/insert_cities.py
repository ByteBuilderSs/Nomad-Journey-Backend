
import pandas as pd
import psycopg2


df = pd.read_csv(r"world_cities.csv")
# print(df[:100])
# print(len(df))

for data in range(0, len(df)):
    connection = psycopg2.connect(user="postgres", password="aysa1380", host="localhost", port="5432", dbname="nomadjourney")
    cursor = connection.cursor()
    query_select = """SELECT * FROM utils_city WHERE city_name = %s"""    
    cursor.execute(query_select, (df['city'][data],))
    city_record = cursor.fetchall()

    if len(city_record) != 0:
        print(city_record)
    if len(city_record) == 0:
        query_insert = """ INSERT INTO PUBLIC.utils_city(city_name, country, c_lat, c_long, abbrev_city) VALUES (%s, %s, %s, %s, %s)"""        
        values = (df['city'][data], df['country'][data], df['lat'][data], df['lng'][data], df['iso3'][data])
        cursor.execute(query_insert, values)
    connection.commit()
    cursor.close()