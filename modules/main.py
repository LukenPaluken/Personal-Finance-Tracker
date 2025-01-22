import tools as tool
import user as us


def main_menu() -> None:
    tool.clean_screen()
    tool.print_logo()
    OPTIONS = ["Dashboard", "Transactions", "Goals", "Accounts", "Close"]
    tool.show_options(OPTIONS)

    while True:
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
                    us.menu("data/users.json")
                case "5":
                    print("Closing...")
                case _:
                    print("Please enter a correct option.")
                    continue
                    
        except KeyboardInterrupt:
            print("Program interrupted. Exiting...")
            break

main_menu()
