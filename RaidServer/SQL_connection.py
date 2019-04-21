class SQL_connection():
    def __init__(self):
        self.username_set = set()

    def create_new_username(self, username, password):
        self.username_set.add(username)

    def check_username_taken(self, username):
        return False

    def check_user_legal(self, username, password):
        return username in self.username_set
