import sqlite3
from sqlite3 import Error

class database():
    databseConnection = None
    cursor = None

    def __init__(self, dbFile):
        self.databseConnection = sqlite3.connect("users.db")
        self.cursor = self.databseConnection.cursor()

    def creating_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS client 
            (user_id INTEGER, name TEXT, temperature INTEGER, humidity INTEGER, light_intensity INTEGER, PRIMARY KEY(user_id))
            """)
        self.databseConnection.commit()
        
    def insert_table(self, id, name, tmp, hum, light):
        sqlite_insert_query = """INSERT INTO client
                            (user_id, name, temperature, humidity, light_intensity) 
                            VALUES 
                            (?, ?, ?, ?, ?)"""

        self.cursor.execute(sqlite_insert_query, (id, name, tmp, hum, light) )
        self.databseConnection.commit()
        print("Record inserted successfully into client table ", self.cursor.rowcount)

    def viewAll_table(self):
        self.cursor.execute("""SELECT * FROM client""")
        print(self.cursor.fetchall())

    def getUserdata_table(self, id):
        self.refreshSQL()
        self.cursor.execute("SELECT * FROM client WHERE user_id = ?", (id,))
        self.databseConnection.commit()
    
        arrayData = []
        emptyData = []
        dataArduino = self.cursor.fetchall()
        print(len(dataArduino))
        if len(dataArduino) == 0:
            return emptyData
        else:
            print(dataArduino)
            for x in dataArduino:
                # print(x)
                arrayData.append(x) 
            return arrayData

    def refreshSQL(self):
        self.databseConnection = sqlite3.connect("projectDb.db")
        self.cursor = self.databseConnection.cursor()

    def update_table(id, name, tmp, hum, light):
        sqliteConnection = sqlite3.connect('projectDb.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        cursor.execute("UPDATE client SET (name = ?, temperature = ?, humidity = ?,light_intensity = ?) WHERE user_id = ?", (name, tmp, hum, light, id))
        sqliteConnection.commit()
 
    def delete_table(self, id):
     
        self.cursor.execute("DELETE FROM client WHERE user_id = ?", (id,))
        self.databseConnection.commit()
       
if __name__ == '__main__':
    db = database('users.db')
    value = db.getUserdata_table('2261075326')
    print(len(value))
    print(value)
    print(value[0])

    
