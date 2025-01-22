"""change everything to where all the options pop up if user is already logged in, otherwise they only see the 'log in' option.
also, have their username be a 'global' var, so its easily accessed without having to ask for their username.
"""


import tools as tool
import re
import time

def login_to_account(file_name: str) -> str:
    try:
        users = tool.read_json(file_name)
    except FileNotFoundError:
        print(f"File {file_name} not found.")
        return {}

    tool.clean_screen()
    tool.print_logo()
    print("Welcome to account login!")

    while True:
        
        # No Current Accounts Prompt
        if not users:
            user_choice = input("There are currently no active accounts. Do you wish to create one? (y/n): ").lower().strip()
            
            if user_choice == "y":
                print("Redirecting...")
                time.sleep(1)
                create_account(file_name)
                return
            if user_choice == "n":
                print("Returning...")
                time.sleep(1)
                return
            else:
                print("Please enter a valid option (y/n).")
                continue
            
        username = input("Enter your username (-1 to return): ").lower()

        if username == "-1":
            print("Returning...")
            time.sleep(1)
            return

        if username not in users.keys():
            print("Username doesn't exist.")
            continue

        user_data = users[username]

        if user_data.get("locked", False):
            lock_time = user_data.get("lock_time")
            if lock_time:
                current_time = time.time()
                cooldown_period = 30
                if current_time - lock_time < cooldown_period:
                    remaining_time = cooldown_period - (current_time - lock_time)
                    print(
                        f"Your account is locked. Please try again in {remaining_time // 60} minutes."
                    )
                    time.sleep(1)
                    return
                else:
                    # Unlock the account after cooldown period
                    print(
                        "Your account has been unlocked. You can try logging in again."
                    )
                    user_data["locked"] = False
                    user_data["failed_attempts"] = 0
                    del user_data["lock_time"]
                    tool.write_json(file_name, users)
                    time.sleep(1)
                    return

        # Attempt login
        for attempt in range(3):
            password = input("Enter password: ")

            if password == user_data["password"]:
                print("Login successful!")
                user_data["failed_attempts"] = 0
                tool.write_json(file_name, users)
                time.sleep(1)
                return username
                
            else:
                print(f"Incorrect password. Attempts left: {2 - attempt}")

                # Increment failed attempts
                user_data["failed_attempts"] = user_data.get("failed_attempts", 0) + 1

                # Lock the account after 3 failed attempts
                if user_data["failed_attempts"] >= 3:
                    user_data["locked"] = True
                    user_data["lock_time"] = time.time()
                    print(
                        "Your account has been locked due to too many failed attempts."
                    )
                    tool.write_json(file_name, users)
                    time.sleep(1)
                    return

        return True


def valid_password(user_password: str) -> None:
    while True:
        if len(user_password) < 8 or len(user_password) > 16:
            print("Error: Password must be between 8 and 16 characters.")
            continue
        if not any(char.isdigit() for char in user_password):
            print("Error: Password must include at least one number.")
            continue
        if not any(char.isalpha() for char in user_password):
            print("Error: Password must include at least one letter.")
            continue
        if not any(char in "!@#$%^&*()-_+=<>?/" for char in user_password):
            print(
                "Error: Password must include at least one special character (!@#$%^&*()-_+=<>?/)."
            )
            continue
        break
    
    return True
    

def create_account(file_name: str) -> None:
    """
    Create a new user account with validated username, email, and password.
    """
    try:
        users = tool.read_json(file_name)
    except FileNotFoundError:
        print(f"File {file_name} not found.")
        return {}
    username_pattern = r"^[a-zA-Z0-9_]+$"
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    tool.clean_screen()
    tool.print_logo()
    print("Welcome to account creation!")

    while True:
        # Validate Username
        username = input("\nEnter username (4 - 15 characters): ").lower().strip()
        if not re.match(username_pattern, username):
            print("Error: Username can only contain letters, numbers, and underscores.")
            continue
        if len(username) < 4 or len(username) > 15:
            print("Error: Username must be between 4 and 15 characters.")
            continue
        if username in users:
            print("Error: This username is already taken.")
            continue

        # Validate Email
        user_email = input("\nEnter email: ").lower().strip()
        if not re.match(email_pattern, user_email):
            print("Error: Invalid email format. Please try again.")
            continue
        if user_email in [user["email"] for user in users.values()]:
            print("Error: This email is already registered.")
            continue

        # Validate Password
        user_password = input("\nEnter password (8 - 16 characters): ").strip()
        valid_password(user_password)
        
        # Validate Security Question
        print("\nPick one of the following security questions: ")
        tool.show_options(SECURITY_QUESTIONS)
        user_security_question_choice = input("Option: ").strip()
        if user_security_question_choice not in ["1", "2", "3"]:
            print("Pick a correct option (1-3).")
            continue
        
        user_security_question_answer = input("Enter the answer to the chosen security question: ").strip()
        
        if not user_security_question_answer:
            print("Please enter an answer.")
            continue

        # All checks passed
        print("Account successfully created!")
        users[username] = {"email": user_email, "password": user_password, "security_answer": user_security_question_answer, "security_question": user_security_question_choice}
        tool.write_json(file_name, users)
        time.sleep(1)
        break


def delete_account(file_name: str) -> None:
    try:
        users = tool.read_json(file_name)
    except FileNotFoundError:
        print(f"File {file_name} not found.")
        return {}

    tool.clean_screen()
    tool.print_logo()
    print("Welcome to account deletion!")

    while True:
        account_user = input("Enter username of account you wish to delete: ").lower()

        if account_user not in users.keys():
            print("Account doesn't exist.")
            continue

        user_data = users[account_user]

        for attempt in range(3):
            password = input("Enter password: ")
            if password == user_data["password"]:
                break
            else:
                print(f"Incorrect password. Attempts left: {2 - attempt}")
        else:
            print("Too many failed attempts. Returning to main menu.")
            time.sleep(1)
            return

        # Confirmation prompt
        while True:
            print(f"Are you sure you want to delete your account ({account_user})?")
            delete_confirmation = input(
                "Type 'y' to confirm or 'n' to cancel: "
            ).lower()

            if delete_confirmation == "y":
                print("Deleting account...")
                time.sleep(1)
                del users[account_user]
                try:
                    tool.write_json(file_name, users)
                except IOError:
                    print("Error: Unable to save changes to file.")
                    time.sleep(1)
                    return
                print("Account deleted successfully.")
                time.sleep(1)
                return
            elif delete_confirmation == "n":
                print("Account deletion canceled. Returning to main menu.")
                time.sleep(1)
                return
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
                

def change_password(file_name: str, username: str) -> None:
    try:
        users = tool.read_json(file_name)
    except FileNotFoundError:
        print(f"File {file_name} not found.")
        return {}
    
    print("Welcome to password change!")
    
    user_data = users[username]
    incorrect_guesses = 0
    
    while True:
        password = input("\nEnter your old password: ").strip()
        
        if password != user_data["password"]:
            print("Password is incorrect.")
            incorrect_guesses += 1
            
            if incorrect_guesses >= 3:
                op = input("Do you wish to answer a security question? y/n: ").lower().strip()
                if op == "y":
                    print(user_data["security_question"])
                    answer = input("Answer: ")
                    if answer != user_data["security_answer"]:
                        print("Answer is incorrect.")
                        return
                elif op == "n":
                    print("Returning...")
                    time.sleep(1)
                    return
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
                    return
        else:
            new_password = input("Enter new password: ")
            if valid_password(new_password):
                repeat_password = input("Re-enter new password: ")
                if new_password == repeat_password:
                    try:
                        user_data["password"] = new_password
                        tool.write_json(user_data, new_password)
                        print("Password change succesful!")
                        time.sleep(1)
                        return
                    except IOError:
                        print("Error: Unable to save changes to file.")
                        time.sleep(1)
                        return
                else:
                    print("Passwords must be the same.")
                    time.sleep(1)
                    return
            else:
                continue
                

def menu(file_name: str) -> None:
    while True:
        tool.clean_screen()
        tool.print_logo()
        options = ["Login", "Create account", "Delete account", "Change password"]

        tool.show_options(options)

        op = input("Enter an option: ")

        match op:
            case "1":
                username = login_to_account(file_name)
            case "2":
                create_account(file_name)
            case "3":
                delete_account(file_name)
            case "4":
                change_password(file_name, username)
            case _:
                print("Enter a valid option.")


SECURITY_QUESTIONS = ["What is your pet's name?",
                          "What is your favorite movie?",
                          "What is your favorite food?"]