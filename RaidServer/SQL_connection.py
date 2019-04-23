import sqlite3
import re


class SQL_connection():
    def __init__(self):
        sqlite_file = "my_db.splite"
        self.conn = sqlite3.connect(sqlite_file)
        self.conn.create_function("REGEXP", 2, self.regexp)
        self.c = self.conn.cursor()
        self.c.execute('CREATE TABLE IF NOT EXISTS usernamePassword (username VARCHAR(100) , password VARCHAR(100))')
        self.c.execute('CREATE TABLE IF NOT EXISTS adminPassword (admin VARCHAR(100), password VARCHAR(100))')
        self.c.execute(
            'CREATE TABLE IF NOT EXISTS userFiles (USERNAME VARCHAR(100), FILENAME VARCHARA(200), PARTS_NUM INT, FILE_LEN INT) ')
        self.c.execute('CREATE TABLE IF NOT EXISTS dataServer (MAC VARCHAR(100))')
        self.c.execute('CREATE TABLE IF NOT EXISTS dataServerFiles (MAC VARCHAR(100), FILE_PART_NAME VARCHAR(220))')
        self.conn.commit()

    def create_new_username(self, username, password):
        self.c.execute('INSERT INTO usernamePassword VALUES (?,?)', (username, password))
        self.conn.commit()

    def create_new_admin(self, andim, password):
        self.c.execute('INSERT INTO adminPassword VALUES (?,?)', (andim, password))
        self.conn.commit()

    def check_username_taken(self, username):
        self.c.execute('SELECT username FROM usernamePassword WHERE username = (?)', (username,))
        return len(self.c.fetchone()) > 0

    def check_admin_taken(self, admin):
        self.c.execute('SELECT admin FROM adminPassword WHERE admin = (?)', (admin,))
        return len(self.c.fetchone()) > 0

    def check_user_legal(self, username, password):
        self.c.execute('SELECT username FROM usernamePassword WHERE username = (?) AND password = (?)',
                       (username, password))
        return len(self.c.fetchone()) > 0

    def check_admin_legal(self, admin, password):
        self.c.execute('SELECT admin FROM adminPassword WHERE admin = (?) AND password = (?)', (admin, password))
        return len(self.c.fetchone()) > 0

    def save_user_file(self, username, filename, parts_num, file_len):
        self.c.execute('INSERT INTO userFiles VALUES (?,?,?,?)', (username, filename, parts_num, file_len))
        self.conn.commit()

    def get_user_file_info(self, username, filename):
        """
        :param username:
        :param filename:
        :return: (parts num, file len) if exists, otherwise: None
        """
        self.c.execute('SELECT PARTS_NUM,FILE_LEN FROM userFiles WHERE USERNAME = (?) AND FILENAME = (?)',
                       (username, filename,))
        return self.c.fetchone()

    def get_user_file_list(self, username):
        """
        :param username:
        :return: [(filename1,),(filename2,),....]
        """
        self.c.execute('SELECT FILENAME FROM userFiles WHERE USERNAME = (?)',
                       (username,))
        return self.c.fetchall()

    def add_data_server(self, mac_address):
        self.c.execute('INSERT INTO dataServer VALUES (?)', (mac_address,))
        self.conn.commit()

    def add_data_server_file_part(self, mac_address, file_part_name):
        self.c.execute('INSERT INTO dataServerFiles VALUES (?,?)', (mac_address, file_part_name))
        self.conn.commit()

    def regexp(self, expr, item):
        print "regexp"
        print item
        print expr
        reg = re.compile(expr)
        print reg.search(item) is not None
        return reg.search(item) is not None

    def delete_user_file(self, username, filename):
        self.c.execute('DELETE FROM userFiles WHERE USERNAME = (?) AND FILENAME = (?)', (username, filename))
        reg_part = username + r"[$]" + filename[:filename.rfind(".")]+ r"_(\d+)_(\d+)" + filename[filename.rfind("."):]
        reg_xor = username + r"[$]" + filename[:filename.rfind(".")]+ r"_(\d+)_[-]1" + filename[filename.rfind("."):]
        reg = reg_part + r"|" + reg_xor
        self.c.execute('DELETE FROM dataServerFiles WHERE FILE_PART_NAME REGEXP ?', [reg])
        self.conn.commit()


if __name__ == '__main__':
    a = SQL_connection()
    a.save_user_file("noam", "somename2", 5, 10)
    print a.get_user_file_info("noam", 'somename2')
    print a.get_user_file_info("noam", "otherfilename")
    print a.get_user_file_list("noam")
    print a.get_user_file_list("noam1")
    a.add_data_server_file_part("some address", "noam$task_4_-1.txt")
    #a.delete_user_file("noam", "task.txt")
    print a.get_user_file_list("noam")
