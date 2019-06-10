import sqlite3
import re
import os


class SQL_connection:
    def __init__(self, file_name):
        """
        constructor
        :param file_name: the sqlite file path
        """
        sqlite_file = file_name
        self.conn = sqlite3.connect(sqlite_file)
        self.conn.create_function("REGEXP", 2, self.regexp)
        self.c = self.conn.cursor()
        self.username_password_table = "username_password"
        self.user_files_table = "user_files"
        self.data_server_table = "data_server"
        self.data_server_files_table = "data_server_files"
        self.init_tables()

    def init_tables(self):
        """
        create the tables we are going to use if they does not exists
        """
        self.c.execute(
            'CREATE TABLE IF NOT EXISTS ' + self.username_password_table + '(username VARCHAR(100) , password '
                                                                           'VARCHAR(100))')
        self.c.execute(
            'CREATE TABLE IF NOT EXISTS ' + self.user_files_table + '(USERNAME VARCHAR(100), FILENAME VARCHARA(200), '
                                                                    'PARTS_NUM INT, FILE_LEN INT) ')
        self.c.execute('CREATE TABLE IF NOT EXISTS ' + self.data_server_table + ' (MAC VARCHAR(100))')
        self.c.execute(
            'CREATE TABLE IF NOT EXISTS ' + self.data_server_files_table + '(MAC VARCHAR(100), FILE_PART_NAME '
                                                                           'VARCHAR(220))')
        self.conn.commit()

    def create_new_username(self, username, password):
        """
        save username and password
        :param username:
        :param password:
        """
        self.c.execute('INSERT INTO ' + self.username_password_table + ' VALUES (?,?)', (username, password))
        self.conn.commit()

    def check_username_taken(self, username):
        """
        check if the username is already used by someone else
        :param username:
        :return: boolean
        """
        self.c.execute('SELECT username FROM ' + self.username_password_table + ' WHERE username = (?)', (username,))
        return self.c.fetchone() is not None

    def check_user_legal(self, username, password):
        """
        check if this username and password is in the db
        :param username:
        :param password:
        :return: boolean
        """
        self.c.execute(
            'SELECT username FROM ' + self.username_password_table + ' WHERE username = (?) AND password = (?)',
            (username, password))
        return self.c.fetchone() is not None

    def save_user_file(self, username, filename, parts_num, file_len):
        """
        save a specific file name to belong to username
        :param username:
        :param filename: file name without the username as start of it
        :param parts_num: number of parts to create from this file
        :param file_len: original len of file
        """
        self.c.execute('INSERT INTO ' + self.user_files_table + ' VALUES (?,?,?,?)',
                       (username, filename, parts_num, file_len))
        self.conn.commit()

    def get_user_file_info(self, username, filename):
        """
        get the file info in order to be able to build it
        :param username:
        :param filename:
        :return: (parts num, file len) if exists, otherwise: None
        """
        self.c.execute(
            'SELECT PARTS_NUM,FILE_LEN FROM ' + self.user_files_table + ' WHERE USERNAME = (?) AND FILENAME = (?)',
            (username, filename,))
        result = self.c.fetchone()
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
        """
        add data server to table of data servers that is connected
        :param mac_address:
        """
        self.c.execute('INSERT OR REPLACE INTO ' + self.data_server_table + ' VALUES (?)', (mac_address,))
        self.conn.commit()

    def add_data_server_file_part(self, mac_address, file_part_name):
        """
        save that a data server is now saving a specific file par
        :param mac_address: data server identifier
        :param file_part_name:
        """
        self.c.execute('INSERT INTO ' + self.data_server_files_table + ' VALUES (?,?)', (mac_address, file_part_name))
        self.conn.commit()

    def regexp(self, expr, item):
        """
        check if the item has the regex expression in it
        :param expr:
        :param item:
        :return: boolean if the expr in item (regex wise)
        """
        reg = re.compile(expr)
        return reg.search(item) is not None

    def delete_user_file(self, username, filename):
        """
        delete a file that belong to some user
        delete in the username: file table
        delete in the data server: file part table
        :param username:
        :param filename:
        """
        filename = filename[filename.rfind("$") + 1:]
        self.c.execute('DELETE FROM ' + self.user_files_table + ' WHERE USERNAME = (?) AND FILENAME = (?)',
                       (username, filename))
        reg_part = username + r"[$]" + filename[:filename.rfind(".")] + r"_(\d+)_(\d+)" + filename[filename.rfind("."):]
        reg_xor = username + r"[$]" + filename[:filename.rfind(".")] + r"_(\d+)_[-]1" + filename[filename.rfind("."):]
        reg = reg_part + r"|" + reg_xor
        self.c.execute('DELETE FROM ' + self.data_server_files_table + ' WHERE FILE_PART_NAME REGEXP ?', [reg])

        self.conn.commit()

    def delete_data_server(self, mac_address):
        """
        delete data server in data server table and the data server:files part table
        :param mac_address:
        """
        self.c.execute('DELETE FROM ' + self.data_server_table + ' WHERE MAC = (?)', (mac_address,))
        self.c.execute('DELETE FROM ' + self.data_server_files_table + ' WHERE MAC = (?)', (mac_address,))
        self.conn.commit()

    def get_all_data_server(self):
        """
        :return: [data server 1 mac address, data server 2 mac address....]
        """
        self.c.execute('SELECT * FROM ' + self.data_server_table)
        result = self.c.fetchall()
        return result

    def close_sql(self):
        self.conn.close()

    def get_data_server_files(self, data_server_mac):
        """
        get the file parts saved in specific data server
        :param data_server_mac:
        :return: [file part 1,.....]
        """
        self.c.execute('SELECT * FROM ' + self.data_server_files_table + ' WHERE MAC = (?)', (data_server_mac,))
        result = self.c.fetchall()
        return result


if __name__ == '__main__':
    sql_file_name = "sirst_db.sqlite"
    os.remove(sql_file_name)
    a = SQL_connection(sql_file_name)
    a.add_data_server("02-00-4C-4F-4F-50")
    print a.get_all_data_server()
    print type(a.get_all_data_server())

    a.create_new_username("noam", "pass")
    a.save_user_file("noam", "noam$somename2_34_4.txt", 5, 10)
    a.save_user_file("noam", "noam$someother_2_-1.txt", 5, 10)

    a.add_data_server_file_part("02-00-4C-4F-4F-50", "noam$somename2_34_4.txt")
    a.add_data_server_file_part("02-00-4C-4F-4F-50", "noam$somename2_2_-1.txt")

    print a.get_data_server_files("02-00-4C-4F-4F-50")
    print type(a.get_data_server_files("02-00-4C-4F-4F-50"))

    print a.get_user_file_list("noam")
    print type(a.get_user_file_list("noam"))
    print a.delete_user_file("noam", "noam$somename2.txt")
    print a.get_user_file_list("noam")
