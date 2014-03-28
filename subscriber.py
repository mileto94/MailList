import sqlite3


class Subscriber():
    """docstring for subscriber"""
    def __init__(self, name, email):
        self.__name = name
        self.__email = email
        self.id = -1

    def save(self):
        if self.id == -1:
            self.db_path = sqlite3.connect("maillist.db")
            self.cursor = self.db_path.cursor()
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS Subscribers
                                (id INTEGER PRIMARY KEY autoincrement,
                                 name, email)""")
            subscribers_query = ("""INSERT INTO Subscribers(name, email)
                                    VALUES(?, ?)""")
            subscribers_data = [self.__name, self.__email]
            self.cursor.execute(subscribers_query, subscribers_data)
            id_query = ("""SELECT id FROM Subscribers
                                     WHERE name = ?""")
            id_data = [self.__name]
            id_in_db = self.cursor.execute(id_query, id_data)
            for line in id_in_db:
                self.id = line[0]
            self.db_path.commit()
            self.db_path.close()

        elif self.id != -1:
            self.db_path = sqlite3.connect("maillist.db")
            self.cursor = self.db_path.cursor()
            subscribers_data = [self.__name, self.__email, self.id]
            subscribers_query = ("""UPDATE Subscribers
                                SET name = ?, email = ? WHERE id = ?""")
            self.cursor.execute(subscribers_query, subscribers_data)
            self.db_path.commit()
            self.db_path.close()
