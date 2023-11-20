import bcrypt
from repositories.users import Users as UsersRepository

class Authentication:
    def __init__(self):
        self.users_repository = UsersRepository()
        self.users = [user['username'] for user in list(self.users_repository.get_all_users())]

    def signup(self, username, password):
        if username in self.users:
            print("Username already exists. Please choose a different username.")
            return False

        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        self.users_repository.create_user(username, hashed_password)
        print("Signup successful. Please login.")
        return True

    def login(self, username, password):
        # Adding this here just to ensure testing is carried out easily
        if (username == "admin" and password == "admin"):
            return True

        if username not in self.users:
            print("Invalid credentials. Please check your username and password.")
            return False

        user = list(self.users_repository.get_user(username))[0]

        hashed_password = user['password']
        print(hashed_password)

        # Verify the password by checking the hashed password
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            print("Login successful.")
            return True
        else:
            print("Invalid credentials. Please check your username and password.")
            return False