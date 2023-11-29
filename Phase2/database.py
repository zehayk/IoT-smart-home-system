import sqlite3
from sqlite3 import Error

class database():
    databseConnection = None
    cursor = None

    def __init__(self, dbFile):
        self.databseConnection = sqlite3.connect("users.db")
        self.cursor = self.databseConnection.cursor()

    def creating_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users 
            (user_id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, email TEXT NOT NULL, card_id INTEGER, 
            temperature_threshold INTEGER NOT NULL DEFAULT 24, humidity_threshold INTEGER NOT NULL, brightness_threshold INTEGER NOT NULL DEFAULT 400, 
            photo BLOB NOT NULL)
            """)
        self.databseConnection.commit()
    
    def drop_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS users""")
        self.databseConnection.commit()
        
    def insert_table(self, id, first_name, last_name, email, card_id, tmp, hum, light, photo):
        sqlite_insert_query = """INSERT INTO users
                            (user_id, first_name, last_name, email, card_id, temperature_threshold, humidity_threshold, brightness_threshold, photo) 
                            VALUES 
                            (?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        self.cursor.execute(sqlite_insert_query, (id, first_name, last_name, email, card_id, tmp, hum, light, photo))
        self.databseConnection.commit()
        print("Record inserted successfully into users table ", self.cursor.rowcount)

    def viewAll_table(self):
        self.cursor.execute("""SELECT * FROM users""")
        print(self.cursor.fetchall())

    # def getUserdata_table(self, id=None, card_id=None):
    def getUserdata_table(self, card_id):
        self.refreshSQL()
        # if id:
            # self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (id,))
        # elif card_id:
        # if card_id:
        self.cursor.execute("SELECT * FROM users WHERE card_id = ?", (card_id,))
        # else:
        #     raise Exception("Please provide user id or card id")
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
        self.databseConnection = sqlite3.connect("users.db")
        self.cursor = self.databseConnection.cursor()

    def update_table(id, first_name, last_name, email, card_id, tmp, hum, light, photo):
        sqliteConnection = sqlite3.connect('users.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        cursor.execute("UPDATE users SET (first_name = ?, last_name = ?, email = ?, card_id = ?, temperature_threshold = ?, humidity_threshold = ?, brightness_threshold = ?, photo = ?) WHERE user_id = ?", (first_name, last_name, email, card_id, tmp, hum, light, photo, id))
        sqliteConnection.commit()
 
    def delete_table(self, id):
        self.cursor.execute("DELETE FROM users WHERE user_id = ?", (id,))
        self.databseConnection.commit()

       
if __name__ == '__main__':
    db = database('users.db')
    value = db.getUserdata_table('2261075326')
    print(len(value))
    print(value)
    print(value[0])
    # db.viewAll_table()
    # db.drop_table()
    # # db.creating_table()
    # db.insert_table(1, 'jooji', 'bigboi', 'hayk@email.com', 197128143172, 25, 40, 400, 'assets/images/user1.jpg')
    # db.insert_table(2, 'chicken', 'nugget', 'nuggetchicken121121@gmail.com', 2261075326, 24, 50, 300, 'assets/images/pfp1.jpg')
    # db.insert_table(3, 'cookie', 'joy', 'baduar10@gmail.com', 14176549, 23, 60, 500, 'assets/images/pfp2.jpg')
    # db.viewAll_table()
