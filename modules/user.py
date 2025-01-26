import tools as tool
import re
import time


#"_" shows that it's a variable meant for internal use. Must not be modified directly.
_logged_in_user = None

FILE_PATH = "data/users.json"


#Getter function. Allows for global variable usage across different modules.
def get_logged_in_user() -> str:
    """
    Gets currently logged-in user.
    
    Returns:
        logged_in_user (str): Username of currently logged-in user.
    """
    return _logged_in_user


#Setter function. Allows for updates to global variable.
def set_logged_in_user(username: str) -> None:
    """
    Sets currently logged-in user.
    
    Parameters:
        username (str): Username of currently logged-in user.
    """
    global _logged_in_user
    _logged_in_user = username
    
    
def verified_username(username: str, file: str) -> bool:
    """
    Verifies the validity and availability of a username.
    
    Args:
        username (str): The username entered by the user.
        file (str): The file path of the JSON file containing existing usernames.
        
    Returns:
        bool: True if the username is valid and available, False otherwise.
    """
    users = tool.read_json(file)
        
    username_pattern = r"^[a-zA-Z0-9_]+$"

    if not re.match(username_pattern, username):
        print("Error: Username can only contain letters, numbers, and underscores.")
        return False
    if len(username) < 4 or len(username) > 15:
        print("Error: Username must be between 4 and 15 characters.")
        return False
    if username in users:
        print("Error: This username is already taken.")
        return False
    
    

def login_to_account(file: str) -> bool:
    """
    Handles account login, acocount lock, and confirmation.
    
    If there are no active usernames in DB, user is prompted to create one.
    
    If user wrongly inputs password wrong 3 times, account is locked for 10 minutes.
    
    Parameters:
        file (str): The file path of the JSON file containing existing user info.
        
    Returns:
        bool
    """

    users = tool.read_json(file)

    tool.clean_screen()
    tool.print_logo()
    print("Welcome to account login!")
    
    while True:
        if not users:
            user_choice = input("There are currently no active accounts. Do you wish to create one? (y/n): ").lower().strip()
            
            if user_choice == "y":
                print("Redirecting...")
                time.sleep(1)
                create_account(file)
                return
            if user_choice == "n":
                print("Returning...")
                time.sleep(1)
                return
            else:
                print("Please enter a valid option (y/n).")
                continue
        else:
            username = input("Enter your username: ").lower().strip()
            
            if username not in users.keys():
                print("Username doesn't exist.")
                continue
            
            user_data = users[username]
            
            if user_data.get("locked", False):
                lock_time = user_data.get("lock_time")
                if lock_time:
                    current_time = time.time()
                    cooldown_period = 6000
                    if current_time - lock_time < cooldown_period:
                        remaining_time = cooldown_period - (current_time - lock_time)
                        print(
                            f"Your account is locked. Please try again in {remaining_time // 60} minutes."
                        )
                        time.sleep(1)
                        return
                    else:
                        print(
                            "Your account has been unlocked. You can try logging in again."
                        )
                        user_data["locked"] = False
                        user_data["failed_attempts"] = 0
                        del user_data["lock_time"]
                        tool.write_json(file, users)
                        time.sleep(1)
                        return

            for attempt in range(3):
                password = input("Enter password: ")

                if password == user_data["password"]:
                    print("Login successful!")
                    user_data["failed_attempts"] = 0
                    tool.write_json(file, users)
                    time.sleep(1)
                    set_logged_in_user(username)
                    return
                    
                else:
                    print(f"Incorrect password. Attempts left: {2 - attempt}")

                    user_data["failed_attempts"] = user_data.get("failed_attempts", 0) + 1

                    if user_data["failed_attempts"] >= 3:
                        user_data["locked"] = True
                        user_data["lock_time"] = time.time()
                        print(
                            "Your account has been locked due to too many failed attempts."
                        )
                        tool.write_json(file, users)
                        time.sleep(1)
                        return

            return True


def create_account(file: str) -> None:
    pass


#note: json is created when write_json() is called.