import tools as tool
import constants as con
import re
import time


# "_" shows that it's a variable meant for internal use. Must not be modified directly.
_logged_in_user = None

stop_main_loop = False

# Getter function. Allows for global variable usage across different modules.
def get_logged_in_user() -> str:
    """
    Gets currently logged-in user.

    Returns:
        logged_in_user (str): Username of currently logged-in user.
    """
    return _logged_in_user


# Setter function. Allows for updates to global variable.
def set_logged_in_user(username: str) -> None:
    """
    Sets currently logged-in user.

    Args:
        username (str): Username of currently logged-in user.
    """
    global _logged_in_user
    _logged_in_user = username


def valid_username(username: str, file: str) -> bool:
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

    return True


def valid_password(password: str) -> bool:
    """
    Args:
        password (str): The password entered by the user.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    if len(password) < 8 or len(password) > 16:
        print("Error: Password must be between 8 and 16 characters.")
        return False
    if not any(char.isdigit() for char in password):
        print("Error: Password must include at least one number.")
        return False
    if not any(char.isalpha() for char in password):
        print("Error: Password must include at least one letter.")
        return False
    if not any(char in "!@#$%^&*()-_+=<>?/" for char in password):
        print(
            "Error: Password must include at least one special character (!@#$%^&*()-_+=<>?/)."
        )
        return False

    return True


def valid_email(email: str, file: str) -> bool:
    users = tool.read_json(file)

    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if not re.match(email_pattern, email):
        print("Error: Invalid email format. Please try again.")
        return False
    if email in [user["email"] for user in users.values()]:
        print("Error: This email is already registered.")
        return False

    return True


def account_unlocked(user: str, file: str) -> None:
    users = tool.read_json(file)
    
    user_data = users[user]
    
    if user_data.get("locked", False):
        lock_time = user_data.get("lock_time")
        if lock_time:
            current_time = time.time()
            cooldown_period = 10
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


def login_to_account(file: str) -> bool:
    """
    Handles account login, acocount lock, and confirmation.

    If there are no active usernames in DB, user is prompted to create an account.

    If user wrongly inputs password wrong 3 times, account is locked for 10 minutes.

    Args:
        file (str): The file path of the JSON file containing existing user info.

    Returns:
        bool: 
    """
    global stop_main_loop
    
    users = tool.read_json(file)

    tool.clean_screen()
    tool.print_logo()
    print("Welcome to account login!")

    while True:
        if not users:
            user_choice = (
                input(
                    "There are currently no active accounts. Do you wish to create one? (y/n): "
                )
                .lower()
                .strip()
            )

            if user_choice == "y":
                print("Redirecting...")
                time.sleep(1)
                create_account(file)
                return
            if user_choice == "n":
                print("Shutting down...")
                time.sleep(1)
                stop_main_loop = True
                break
            else:
                print("Please enter a valid option (y/n).")
                continue
        else:
            username = input("Enter your username (-1 to cancel): ").lower().strip()

            if username == "-1":
                print("Shutting down...")
                time.sleep(1)
                stop_main_loop = True
                break
            
            if username not in users.keys():
                print("Username doesn't exist.")
                continue

            user_data = users[username]

            account_unlocked(username, file)

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

                    user_data["failed_attempts"] = (
                        user_data.get("failed_attempts", 0) + 1
                    )

                    if user_data["failed_attempts"] >= 3:
                        user_data["locked"] = True
                        user_data["lock_time"] = time.time()
                        print(
                            "Your account has been locked due to too many failed attempts."
                        )
                        tool.write_json(file, users)
                        time.sleep(1)
                        return


def create_account(file: str) -> None:
    """Handles account creation.
    
    Once all data is correctly entered, it's added to the JSON.

    Args:
        file (str): The file path of the JSON file containing existing user info.
    """
    users = tool.read_json(file)

    tool.clean_screen()
    tool.print_logo()
    print("Welcome to account creation!")

    while True:
        username = input("Username: ").lower().strip()
        if not valid_username(username, file):
            continue

        password = input("Password: ").strip()
        if not valid_password(password):
            continue

        email = input("Email: ").lower().strip()
        if not valid_email(email, file):
            continue

        print("Choose one of fhe following security questions. You must be able to remember your answer in the future: ")
        tool.show_options(con.SECURITY_QUESTIONS)

        user_security_question_choice = input("Option: ").strip()
        if user_security_question_choice not in ["1", "2", "3"]:
            print("Pick a correct option (1-3).")
            continue

        user_security_question_answer = input(
            f"Answer the chosen security question ({con.SECURITY_QUESTIONS[int(user_security_question_choice) - 1]}): "
        ).strip().lower()

        if not user_security_question_answer:
            print("Please enter an answer.")
            continue

        # All checks passed
        print("Account successfully created!")
        users[username] = {
            "email": email,
            "password": password,
            "security_answer": user_security_question_answer,
            "security_question": user_security_question_choice,
        }
        tool.write_json(file, users)
        time.sleep(1)
        break


def change_password(file: str) -> None:
    """Handles user password changes.

    Args:
        file (str): The file path of the JSON file containing existing user info.
    """
    global _logged_in_user
    
    
    users = tool.read_json(file)
    stop_loop = False
    
    user_data = users[_logged_in_user]
    
    tool.clean_screen()
    tool.print_logo()
    print("Welcome to password change!")
    
    while True:
        for _ in range(2):
            current_password = input("Current password: ").strip()
            
            if current_password == user_data["password"]:
                new_password = input("New password: ").strip()
                
                if valid_password(new_password):
                    user_data["password"] = new_password
                    tool.write_json(file, users)
                    print("Password successfully changed!")
                    time.sleep(1)
                    login_to_account(file)
                    stop_loop = True
                    break
            else:
                print("Incorrect. Try again.")
                continue
        
        if stop_loop == True:
            break
        
        user_choice = input("Continue with security question? (y/n): ").lower().strip()
        
        if user_choice == "y":
            print(f"{con.SECURITY_QUESTIONS[int(user_data["security_question"]) - 1]}")
            
            for attempt in range(3):
                security_question_answer = input("Answer: ")
                
                if security_question_answer == user_data["security_answer"]:
                    new_password = input("New password: ")
                    if valid_password(new_password):
                        user_data["password"] = new_password
                        tool.write_json(file, users)
                        user_data["failed_attempts"] = 0
                        print("Password successfully changed!")
                        time.sleep(1)
                        login_to_account(file)
                        break
                else:
                    print("Incorrect. Try again.")
            
            account_unlocked(_logged_in_user, file)
            
            user_data["failed_attempts"] = (
                        user_data.get("failed_attempts", 0) + 1
                    )

            if user_data["failed_attempts"] >= 3:
                user_data["locked"] = True
                user_data["lock_time"] = time.time()
                print(
                    "Your account has been locked due to too many failed attempts."
                )
                tool.write_json(file, users)
                time.sleep(1)
                return
                    
        if user_choice == "n":
            print("Returning...")
            time.sleep(1)
            return
        else:
            print("Please enter a valid option (y/n).")
            continue
    
    return
            

def menu(file: str) -> None:
    options = ["Create account",
               "Change password",
               "Home"]
    
    while True:
        tool.clean_screen()
        tool.print_logo()
        tool.show_options(options)
        op = input("Enter an option: ")
        
        match op:
            case "1":
                create_account(file)
            case "2":
                change_password(file)
            case "3":
                return
            case _:
                print("Please enter a valid option.")
                continue


