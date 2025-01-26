import tools as tool
import user as us
import time


_logged_in_user = us.get_logged_in_user()

FILE_PATH = "data/users.json"


def main_menu() -> None:
    tool.clean_screen()
    tool.print_logo()

    while True:
        # Check the active user
        if not us.get_logged_in_user():
            print("No active user. Redirecting to login...")
            time.sleep(1)
            us.login_to_account(FILE_PATH)
            continue
        else:
            USER_OPTIONS = ["Dashboard", "Transactions", "Goals", "Accounts", "Log out"]
            tool.show_options(USER_OPTIONS)

            op = input("Enter an option: ")

            match op:
                case "1":
                    pass
                case "2":
                    pass
                case "3":
                    pass
                case "4":
                    pass
                case "5":
                    print("Logging out...")
                    us.set_logged_in_user(None)  # Log out user
                    time.sleep(1)
                case _:
                    print("Please enter a valid option.")
                    continue


main_menu()
