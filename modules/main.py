import tools as tool
import user as us
import constants as con
import time


FILE_PATH = con.FILE_PATH


def main_menu() -> None:
    """
    Handles the execution of the main program.
    """
    while True:
        if us.stop_main_loop:
            break
        
        tool.clean_screen()
        tool.print_logo()
        # Check the active user
        if not us.get_logged_in_user():
            print("No active user. Redirecting to login...")
            time.sleep(1)
            us.login_to_account(FILE_PATH)
            continue
        else:
            tool.clean_screen()
            tool.print_logo()
            print(f"Welcome, {us._logged_in_user}!\n")
            tool.show_options(con.USER_OPTIONS)

            try:
                op = input("Enter an option: ")

                match op:
                    case "1":
                        pass
                    case "2":
                        pass
                    case "3":
                        pass
                    case "4":
                        us.menu(FILE_PATH)
                    case "5":
                        print("Logging out...")
                        # Log out user
                        us.set_logged_in_user(None)
                        time.sleep(1)
                    case _:
                        print("Please enter a valid option.")
                        continue
                    
            except KeyboardInterrupt as e:
                print(f"Error. {e}")
                

main_menu()
