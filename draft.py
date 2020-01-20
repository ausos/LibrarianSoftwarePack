import data_base as db
import pandas as pd


connection, cursor = db.connect_db()

cursor.execute("SELECT * FROM books")
result = cursor.fetchall()

#pd.DataFrame(result)
print(pd.DataFrame(result))
#print(result)


#db.delete_all(cursor, connection)


db.close_connection(connection, cursor)
