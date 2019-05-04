import sqlite3
import re
import os


class SQL_connection():
    def __init__(self, file_name):
        sqlite_file = file_name
        self.conn = sqlite3.connect(sqlite_file)
        self.conn.create_function("REGEXP", 2, self.regexp)
        self.c = self.conn.cursor()
        self.username_password_table = "username_password"
        self.admin_password_table = "admin_password"
        self.user_files_table = "user_files"
        self.data_server_table = "data_server"
        self.data_server_files_table = "data_server_files"
        self.init_tables()

    def init_tables(self):
        self.c.execute(
            'CREATE TABLE IF NOT EXISTS ' + self.username_password_table + '(username VARCHAR(100) , password '
                                                                           'VARCHAR(100))')
        self.c.execute(
            'CREATE TABLE IF NOT EXISTS ' + self.admin_password_table + ' (admin VARCHAR(100), password VARCHAR(100))')
        self.c.execute(
            'CREATE TABLE IF NOT EXISTS ' + self.user_files_table + '(USERNAME VARCHAR(100), FILENAME VARCHARA(200), '
                                                                    'PARTS_NUM INT, FILE_LEN INT) ')
        self.c.execute('CREATE TABLE IF NOT EXISTS ' + self.data_server_table + ' (MAC VARCHAR(100))')
        self.c.execute(
            'CREATE TABLE IF NOT EXISTS ' + self.data_server_files_table + '(MAC VARCHAR(100), FILE_PART_NAME '
                                                                           'VARCHAR(220))')
        self.conn.commit()

    def create_new_username(self, username, password):
        self.c.execute('INSERT INTO ' + self.username_password_table + ' VALUES (?,?)', (username, password))
        self.conn.commit()

    def create_new_admin(self, admin, password):
        self.c.execute('INSERT INTO ' + self.admin_password_table + ' VALUES (?,?)', (admin, password))
        self.conn.commit()

    def check_username_taken(self, username):
        self.c.execute('SELECT username FROM ' + self.username_password_table + ' WHERE username = (?)', (username,))
        return self.c.fetchone() is not None

    def check_admin_taken(self, admin):
        self.c.execute('SELECT admin FROM ' + self.admin_password_table + ' WHERE admin = (?)', (admin,))
        return self.c.fetchone() is not None

    def check_user_legal(self, username, password):
        self.c.execute(
            'SELECT username FROM ' + self.username_password_table + ' WHERE username = (?) AND password = (?)',
            (username, password))
        return self.c.fetchone() is not None

    def check_admin_legal(self, admin, password):
        self.c.execute('SELECT admin FROM ' + self.admin_password_table + ' WHERE admin = (?) AND password = (?)',
                       (admin, password))
        return self.c.fetchone() is not None

    def save_user_file(self, username, filename, parts_num, file_len):
        self.c.execute('INSERT INTO ' + self.user_files_table + ' VALUES (?,?,?,?)',
                       (username, filename, parts_num, file_len))
        self.conn.commit()

    def get_user_file_info(self, username, filename):
        """
        :param username:
        :param filename:
        :return: (parts num, file len) if exists, otherwise: None
        """
        print "get user file info: " + username + " file name: " + filename
        self.c.execute(
            'SELECT PARTS_NUM,FILE_LEN FROM ' + self.user_files_table + ' WHERE USERNAME = (?) AND FILENAME = (?)',
            (username, filename,))
        result = self.c.fetchone()
        print "and the result is: " + str(result)
        return result

    def get_user_file_list(self, username):
        """
        :param username:
        :return: [(filename1,),(filename2,),....]
        """
        self.c.execute('SELECT FILENAME FROM ' + self.user_files_table + ' WHERE USERNAME = (?)',
                       (username,))
        return self.c.fetchall()

    def add_data_server(self, mac_address):
        self.c.execute('INSERT INTO ' + self.data_server_table + ' VALUES (?)', (mac_address,))
        self.conn.commit()

    def add_data_server_file_part(self, mac_address, file_part_name):
        self.c.execute('INSERT INTO ' + self.data_server_files_table + ' VALUES (?,?)', (mac_address, file_part_name))
        self.conn.commit()

    def regexp(self, expr, item):
        reg = re.compile(expr)
        return reg.search(item) is not None

    def delete_user_file(self, username, filename):
        self.c.execute('DELETE FROM ' + self.user_files_table + ' WHERE USERNAME = (?) AND FILENAME = (?)',
                       (username, filename))
        reg_part = username + r"[$]" + filename[:filename.rfind(".")] + r"_(\d+)_(\d+)" + filename[filename.rfind("."):]
        reg_xor = username + r"[$]" + filename[:filename.rfind(".")] + r"_(\d+)_[-]1" + filename[filename.rfind("."):]
        reg = reg_part + r"|" + reg_xor
        self.c.execute('DELETE FROM ' + self.data_server_files_table + ' WHERE FILE_PART_NAME REGEXP ?', [reg])
        self.conn.commit()

    def delete_data_server(self, mac_address):
        self.c.execute('DELETE FROM ' + self.data_server_table + ' WHERE MAC = (?)', (mac_address,))
        self.c.execute('DELETE FROM ' + self.data_server_files_table + 'WHERE MAX = (?)', (mac_address,))
        self.conn.commit()

    def get_all_data_server(self):
        self.c.execute('SELECT * FROM ' + self.data_server_table)
        result = self.c.fetchall()
        return result

    def close_sql(self):
        self.conn.close()


"""
if __name__ == '__main__':
    a = SQL_connection()
    a.add_data_server("hi everyone")
    a.add_data_server("hi again!")
    a.save_user_file("noam", "somename2", 5, 10)
    print a.get_user_file_info("noam", 'somename2')
    print a.get_user_file_info("noam", "otherfilename")
    print a.get_user_file_list("noam")
    print a.get_user_file_list("noam1")
    a.add_data_server_file_part("some address", "noam$task_4_-1.txt")
    # a.delete_user_file("noam", "task.txt")
    print a.get_user_file_list("noam")
    print a.get_all_data_server()"""
