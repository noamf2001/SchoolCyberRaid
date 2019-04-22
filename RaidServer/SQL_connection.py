import sqlite3


class SQL_connection():
    def __init__(self):
        sqlite_file = "my_db.splite"
        self.conn = sqlite3.connect(sqlite_file)
        self.c = self.conn.cursor()
        self.c.execute('CREATE TABLE IF NOT EXISTS usernamePassword (username VARCHAR(100) , password VARCHAR(100))')
        self.c.execute('DELETE FROM usernamePassword WHERE username=(?);',("noam",))
        self.conn.commit()

    def create_new_username(self, username, password):
        self.c.execute('INSERT INTO usernamePassword VALUES (?,?)', (username, password))
        self.conn.commit()

    def check_username_taken(self, username):
        self.c.execute('SELECT username FROM usernamePassword WHERE username = (?)', (username,))
        return len(self.c.fetchone()) > 0

    def check_user_legal(self, username, password):
        self.c.execute('SELECT username FROM usernamePassword WHERE username = (?) AND password = (?)', (username,password))
        return len(self.c.fetchone()) > 0


if __name__ == '__main__':
    a = SQL_connection()
    print a.create_new_username("noam", "ppp")
    print a.check_username_taken("noam")
    print a.check_user_legal("noam","ppp")
