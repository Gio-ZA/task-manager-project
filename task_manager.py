"""
Task Management System

This program manages user authentication and task tracking. Users can:
- Log in with username and password
- Add new tasks and view all or personal tasks
- Mark tasks as complete or edit assigned tasks (if not completed)
- Admin users can register new users, delete tasks, generate reports, and view statistics
- Reports summarize overall and per-user task statuses, including completion and overdue tasks
"""
from datetime import date, datetime


def cancel_operation(user_input: str) -> bool:
    """
    Checks if the user wants to cancel the current input operation.

    If the user enters 'x' (in any case), a cancellation message is
    printed and the function returns True to indicate the process
    should stop.

    Args:
        user_input (str): The input entered by the user.

    Returns:
        bool: True if the user entered 'x' to cancel, otherwise False.
    """
    if user_input.lower() == "x":
        print("Operation cancelled.")
        return True
    return False


def get_existing_usernames() -> list[str]:
    """
    Reads all existing usernames from 'user.txt'.

    This function opens the 'user.txt' file, extracts the usernames from
    each line, converts them to lowercase for consistency, and returns a
    list of all usernames.

    Returns:
        list[str]: A list containing all existing usernames in
        lowercase.
    """
    with open("user.txt", "r") as file:
        existing_users = []
        for line in file:
            parts = line.strip().split(", ")

            # Ensure line isn't empty
            if parts:
                username = parts[0]
                existing_users.append(username.lower())
    return existing_users


def reg_user() -> None:
    """
    Registers a new user by collecting a valid username and password.

    This function prompts the user to enter a new username and password,
    with an option to cancel the process at any input step by typing
    'x'. It validates that the username contains only letters and checks
    if the password and confirmation match. If all inputs are valid, the
    new user credentials are saved to 'user.txt'.

    Returns:
        None
    """
    print("Please type 'x' at any time to cancel registration.\n")

    existing_users = get_existing_usernames()

    # Get new username
    while True:
        new_username = input("Enter new username: ").lower()
        if cancel_operation(new_username):
            return

        if not new_username.isalpha():
            print("Username must only contain letters.")

        elif new_username in existing_users:
            print(
                f"{new_username} already exists. Please create a new username"
            )

        else:
            break

    # Get password
    new_password = input("Enter a password: ")
    if cancel_operation(new_password):
        return

    confirm_password = input("Confirm password: ")
    if cancel_operation(confirm_password):
        return

    # Check password match
    if new_password != confirm_password:
        print("Password confirmation does not match. Registration failed.")
        return

    # Save user to file
    try:
        with open("user.txt", "a+") as file:
            file.seek(0)
            content = file.read()
            if not content.endswith("\n"):
                file.write("\n")
            file.write(f"{new_username}, {new_password}\n")
        print(f"User '{new_username}' registered successfully.")
    except IOError as e:
        print(f"Error saving user: {e}")


def add_task() -> None:
    """
    Adds a new task to 'tasks.txt' after validating that the assigned
    user exists.

    Prompts the user for the username to assign the task to, title, 
    description, and due date. The task is only added if the assigned
    username exists in 'user.txt'. The task is marked as incomplete by
    default.

    Returns:
        None
    """
    print("Please type 'x' at any time to cancel.\n")

    existing_users = get_existing_usernames()

    # Check if assigned user exists.
    while True:
        assigned_user = input(
            "Enter the username of the person the task "
            "is assigned to: "
        ).lower().strip()
        if cancel_operation(assigned_user):
            return

        if assigned_user in existing_users:
            break

        print(
            f"User '{assigned_user}' does not exist."
            "Please enter a valid username."
        )

    # Get task information
    while True:
        task_title = input("Enter the title of the task: ")
        if cancel_operation(task_title):
            return

        if task_title.strip() == "":
            print("Input cannot be blank")
        else:
            break

    while True:
        task_description = input("Enter a description of the task: ")
        if cancel_operation(task_description):
            return

        if task_description.strip() == "":
            print("Input cannot be blank")
        else:
            break

    while True:
        due_date = input(
            "Enter the due date of the task (e.g., 06 Oct 2025): "
        )
        if cancel_operation(due_date):
            return

        # Try parsing the date
        try:
            due_date_obj = datetime.strptime(due_date, "%d %b %Y").date()
            due_date_str = due_date_obj.strftime("%d %b %Y")
            break
        except ValueError:
            print(
                "Invalid date format." 
                "Please enter the date in DD MMM YYYY format."
            )

    assigned_date = date.today().strftime("%d %b %Y")
    task_complete = "No"

    task_entry = (
            f"{assigned_user}, {task_title}, {task_description}, "
            f"{assigned_date}, {due_date_str}, {task_complete}\n"
    )

    try:
        with open("tasks.txt", "a+") as task_file:
            task_file.seek(0)
            content = task_file.read()
            # Check if a new line should be added
            if not content.endswith("\n"):
                task_file.write("\n")

            task_file.write(task_entry)
        print("Task added successfully.")
    except FileNotFoundError:
        print("The 'tasks.txt' file does not exist")
    except IOError as e:
        print(f"Error writing to 'tasks.txt': {e}")


def display_task(task_parts: list[str]) -> None:
    """
    Displays a single task in a user-friendly format.

    Args:
        task_parts (list): A list containing the following 6 elements in
        order:
            [0] assigned_to (str)
            [1] task_title (str)
            [2] task_description (str)
            [3] date_assigned (str)
            [4] due_date (str)
            [5] task_complete (str)

    Returns:
        None
    """
    assigned_to = task_parts[0]
    task_title = task_parts[1]
    task_description = task_parts[2]
    date_assigned = task_parts[3]
    due_date = task_parts[4]
    task_complete = task_parts[5]

    print("─" * 60)
    print(f"Task:\t\t  {task_title}")
    print(f"Assigned to:\t  {assigned_to}")
    print(f"Date assigned:\t  {date_assigned}")
    print(f"Due date:\t  {due_date}")
    print(f"Task Complete?\t  {task_complete}")
    print("Task description:")
    print(f"  {task_description}")
    print("─" * 60)


def view_all() -> None:
    """
    Reads all tasks from the 'tasks.txt' file and displays them in a
    user-friendly, structured format.

    Each line in the file is expected to contain task information
    separated by a comma and a space, in the following order:
    assigned_to, task_title, task_description, date_assigned,
    due_date, task_complete.

    The function prints each task using the display_task() function.

    Returns:
        None
    """
    try:
        with open("tasks.txt", "r") as task_file:
            for line in task_file:
                task_parts = line.strip().split(", ")
                display_task(task_parts)
    except FileNotFoundError:
        print("The 'tasks.txt' file does not exist.")


def get_valid_task_number(user_tasks: dict[int, int]) -> int | None:
    """
    Prompts the user for a valid displayed task number.

    Args:
        user_tasks (dict): A mapping of display numbers to actual task indexes.

    Returns:
        int or None: Actual task index in tasks.txt or None if cancelled.
    """
    task_input = input("Enter the task number (or 'x' to cancel): ").lower()

    if task_input == 'x':
        return None

    if not task_input.isdigit():
        print("Invalid input. Please enter a number.")
        return get_valid_task_number(user_tasks)

    display_number = int(task_input)
    if display_number not in user_tasks:
        print("Invalid task number. Please try again.")
        return get_valid_task_number(user_tasks)

    return user_tasks[display_number]


def mark_task_complete(
    tasks: list[str], user_tasks: dict[int, int]
) -> list[str]:
    """
    Prompts the user to select and mark one of their tasks as complete.

    The function verifies that the task number entered is valid and
    belongs to the current user. If the task is not already completed,
    it updates the completion status in memory and writes the change to
    'tasks.txt'.

    Args:
        tasks (list[str]): All task lines from 'tasks.txt'.
        user_tasks (dict[int, int]): Mapping from displayed task numbers
        to actual task indices in 'tasks.txt'.

    Returns:
        list[str]: The updated list of task lines.
    """
    while True:
        task_num = get_valid_task_number(user_tasks)
        if task_num is None:
            print("Input cancelled.")
            return tasks

        task_parts = tasks[task_num].strip().split(", ")
        if task_parts[-1].lower() == "yes":
            print("This task is already marked as complete.")
        else:
            task_parts[-1] = "Yes"
            tasks[task_num] = ", ".join(task_parts) + "\n"
            with open("tasks.txt", "w") as task_file:
                task_file.writelines(tasks)
            print("Task marked as complete.")
        return tasks


def edit_task(tasks: list[str], user_tasks: dict[int, int]) -> list[str]:
    """
    Allows the user to edit one of their incomplete tasks.

    Tasks are shown to the user with custom numbering starting at 1.
    This function uses a mapping between those displayed numbers and
    actual task indices in 'tasks.txt' to perform edits correctly.

    The user can choose to update the username assigned to the task
    or change its due date. Completed tasks cannot be edited.
    All changes are validated and saved to 'tasks.txt'.

    Args:
        tasks (list[str]): All task lines from 'tasks.txt'.
        user_tasks (dict[int, int]): Mapping from displayed task numbers
        to actual line indices in 'tasks.txt'.

    Returns:
        list[str]: The updated list of task lines.
    """
    while True:
        task_index = get_valid_task_number(user_tasks)
        if task_index is None:
            print("Input cancelled.")
            return tasks

        task_parts = tasks[task_index].strip().split(", ")

        if task_parts[-1].lower() == "yes":
            print("Completed tasks cannot be edited.")
            return tasks

        while True:
            edit_choice = input(
                "\nWhat would you like to edit?\n"
                "1 - Username assigned to task\n"
                "2 - Due date\n"
                "x - Cancel\n: "
            ).lower()

            if cancel_operation(edit_choice):
                break

            if edit_choice == "1":
                new_user = input("Enter the new username: ").lower()
                if cancel_operation(new_user):
                    print("Cancelled username update.")
                    break

                valid_users = get_existing_usernames()

                if new_user not in valid_users:
                    print("User does not exist.")
                    break

                if new_user == task_parts[0].lower():
                    print(
                        f"The task is already assigned to '{new_user}'. "
                        "No changes made."
                    )
                    break

                task_parts[0] = new_user
                tasks[task_index] = ", ".join(task_parts) + "\n"
                with open("tasks.txt", "w") as task_file:
                    task_file.writelines(tasks)
                print("Username updated.")
                break

            if edit_choice == "2":
                new_due_date = input("Enter the new due date (DD MMM YYYY): ")
                if cancel_operation(new_due_date):
                    print("Cancelled due date update.")
                    break
                try:
                    parsed_date = datetime.strptime(new_due_date, "%d %b %Y")
                    formatted_date = parsed_date.strftime("%d %b %Y")
                    task_parts[4] = formatted_date
                    tasks[task_index] = ", ".join(task_parts) + "\n"
                    with open("tasks.txt", "w") as task_file:
                        task_file.writelines(tasks)
                    print("Due date updated.")
                except ValueError:
                    print("Invalid date format. Use DD MMM YYYY.")
                break

            print("Invalid option. Please enter 1, 2, or x.")
        return tasks


def view_mine(current_user: str) -> None:
    """
    Displays tasks assigned to the current user and allows task
    management.

    The user can view their tasks, mark them as complete, or edit them
    (change assigned user or due date). Completed tasks cannot be
    edited.

    Args:
        current_user (str): The username of the currently logged-in
        user.

    Returns:
        None
    """
    try:
        with open("tasks.txt", "r") as task_file:
            tasks = task_file.readlines()

        user_tasks = {}
        display_number = 1

        for i, task_line in enumerate(tasks):
            task_parts = task_line.strip().split(", ")
            if task_parts[0].lower() == current_user.lower():
                print(f"\nTask Number: {display_number}")
                display_task(task_parts)
                user_tasks[display_number] = i
                display_number += 1

        if not user_tasks:
            print("You have no tasks assigned.")
            return

        while True:
            choice = input(
                "\nSelect what you would like to do:\n"
                "1 - Mark a task as complete\n"
                "2 - Edit a task\n"
                "x - Exit\n: "
            ).lower()

            if cancel_operation(choice):
                return

            if choice == "1":
                tasks = mark_task_complete(tasks, user_tasks)
            elif choice == "2":
                tasks = edit_task(tasks, user_tasks)
            else:
                print("Invalid option. Please choose 1, 2, or x.")

    except FileNotFoundError:
        print("The 'tasks.txt' file does not exist.")


def view_completed() -> None:
    """
    Displays all completed tasks from tasks.txt in a formatted layout.

    This function reads tasks from the file, checks for those marked as
    completed ("Yes"), and prints them using the standard task format.

    Returns:
        None
    """
    try:
        with open("tasks.txt", "r") as file:
            found = False
            for line in file:
                task_parts = line.strip().split(", ")
                if task_parts[-1].strip().lower() == "yes":
                    print("\n" + "=" * 40)
                    display_task(task_parts)
                    found = True

            if not found:
                print("No completed tasks found.")
    except FileNotFoundError:
        print("The file 'tasks.txt' does not exist.")


def delete_task() -> None:
    """
    Allows the admin to permanently delete any task from the task list.

    Tasks are displayed with task numbers. The admin selects one, and
    the corresponding task is removed from the file.

    Returns:
        None
    """
    try:
        with open("tasks.txt", "r") as file:
            tasks = file.readlines()

        if not tasks:
            print("No tasks available to delete.")
            return

        # Display all tasks
        print("\nAll Tasks:")
        for i, line in enumerate(tasks):
            task_parts = line.strip().split(", ")
            print(f"\nTask Number: {i + 1}")
            display_task(task_parts)

        # Ask which task to delete
        while True:
            task_num_input = input(
                "\nEnter the task number to delete (or 'x' to cancel): "
            )
            if cancel_operation(task_num_input):
                return

            if task_num_input.isdigit():
                task_num = int(task_num_input) - 1
                if 0 <= task_num < len(tasks):
                    break
            print("Invalid task number. Try again.")

        # Show the task to delete
        print("\nYou are about to delete the following task:")
        display_task(tasks[task_num].strip().split(", "))

        # Confirmation
        while True:
            confirm = input(
                "Are you sure you want to delete this task? (yes/no): "
            ).lower().strip()

            if confirm == "yes":
                tasks.pop(task_num)
                with open("tasks.txt", "w") as file:
                    file.writelines(tasks)
                print("Task deleted successfully.")
                break

            if confirm == "no":
                print("Task deletion cancelled.")
                break

            print("Invalid input. Please type 'yes' or 'no'")

    except FileNotFoundError:
        print("The 'tasks.txt' file does not exist.")


def display_statistics() -> None:
    """
    Display the contents of the task and user overview reports in a
    readable format.

    This function tries to read 'task_overview.txt' and
    'user_overview.txt' and print their contents. If either report file
    is missing, it calls 'generate_reports()' to create them first,
    then displays the reports. It also handles errors if files cannot be
    read.

    Args:
        None

    Returns:
        None
    """
    try:
        # Try opening both files to check if they exist
        with open("task_overview.txt", "r"):
            pass
        with open("user_overview.txt", "r"):
            pass
    except FileNotFoundError:
        print("Report files not found. Generating reports...")
        generate_reports()

    try:
        print("\n====== Task Overview ======\n")
        with open("task_overview.txt", "r") as task_file:
            print(task_file.read())

        print("\n====== User Overview ======\n")
        with open("user_overview.txt", "r") as user_file:
            print(user_file.read())

    except IOError:
        print("Error: Problem reading the report files.")


def generate_reports() -> None:
    """
    Generate summary reports about tasks and users and save them to
    text files.

    Reads task data from 'tasks.txt' and user data from 'user.txt'. It
    calculates:
    - Total number of tasks, how many are complete, incomplete,
    and overdue.
    - Per-user task statistics including number of tasks assigned,
    completed, incomplete, and overdue.

    The results are written to two files:
    1. 'task_overview.txt' summarizing all tasks.
    2. 'user_overview.txt' summarizing tasks assigned to each user.

    If 'tasks.txt' is missing, the function prints an error and exits
    without creating reports.

    Args:
        None

    Returns:
        None
    """
    try:
        with open("tasks.txt", "r") as file:
            task_lines = file.readlines()
    except FileNotFoundError:
        print("Error: 'tasks.txt' not found.")
        return

    with open("user.txt", "r") as file:
        user_lines = file.readlines()

    # Prepare task statistics
    total_tasks = len(task_lines)
    completed = 0
    uncompleted = 0
    overdue = 0

    today = datetime.today()

    for line in task_lines:
        task_parts = line.strip().split(", ")
        due_date = datetime.strptime(task_parts[4], "%d %b %Y")
        is_completed = task_parts[-1].lower() == "yes"

        if is_completed:
            completed += 1
        else:
            uncompleted += 1
            if due_date < today:
                overdue += 1

    # Write task overview report
    with open("task_overview.txt", "w") as file:
        file.write("Task Overview Report\n")
        file.write("====================\n")
        file.write(f"Total tasks: {total_tasks}\n")
        file.write(f"Completed tasks: {completed}\n")
        file.write(f"Uncompleted tasks: {uncompleted}\n")
        file.write(f"Overdue tasks: {overdue}\n")
        if total_tasks > 0:
            file.write(
                f"Percentage incomplete: "
                f"{uncompleted / total_tasks * 100:.2f}%\n"
            )
            file.write(
                f"Percentage overdue: "
                f"{overdue / total_tasks * 100:.2f}%\n"
            )

    # Prepare user list
    users = []
    for line in user_lines:
        username = line.strip().split(", ")[0].lower()
        users.append(username)

    # Write user overview report
    with open("user_overview.txt", "w") as file:
        file.write("User Overview Report\n")
        file.write("====================\n")
        file.write(f"Total users: {len(users)}\n")
        file.write(f"Total tasks: {total_tasks}\n\n")

        for user in users:
            user_task_count = 0
            user_completed = 0
            user_uncompleted = 0
            user_overdue = 0

            for line in task_lines:
                task_parts = line.strip().split(", ")
                task_user = task_parts[0].lower()

                if task_user == user:
                    user_task_count += 1
                    is_completed = task_parts[-1].lower() == "yes"
                    due_date = datetime.strptime(task_parts[4], "%d %b %Y")

                    if is_completed:
                        user_completed += 1
                    else:
                        user_uncompleted += 1
                        if due_date < today:
                            user_overdue += 1

            file.write(f"User: {user}\n")
            file.write(f"- Tasks assigned: {user_task_count}\n")

            if total_tasks > 0 and user_task_count > 0:
                file.write(
                    f"- % of total tasks: "
                    f"{user_task_count / total_tasks * 100:.2f}%\n"
                    )
                file.write(
                    f"- % completed: "
                    f"{user_completed / user_task_count * 100:.2f}%\n"
                )
                file.write(
                    f"- % uncompleted: "
                    f"{user_uncompleted / user_task_count * 100:.2f}%\n"
                )
                file.write(
                    f"- % overdue: "
                    f"{user_overdue / user_task_count * 100:.2f}%\n"
                )
            else:
                file.write("- No tasks assigned.\n")

            file.write("\n")


# ==== Login Section ====
# Check if user's name and password is correct/exists.
while True:
    login_username = input("Enter user name: ").lower()
    login_password = input("Enter your password: ")

    try:
        with open("user.txt", "r") as file:
            users = file.readlines()

        logged_in = False

        for line in users:
            username, password = line.strip().split(", ")
            if (
                username.lower() == login_username
                and password == login_password
            ):
                print(f"Welcome {username.title()}!")
                logged_in = True
                break

        if logged_in:
            break

        print("Incorrect username or password. Please try again.")

    except FileNotFoundError:
        print("The 'user.txt' file does not exist.")
        break


# Admin menu
if login_username == "admin":
    while True:
        menu = input(
            '''Select one of the following options:
    r - register a user
    a - add task
    va - view all tasks
    vm - view my tasks
    vc - view completed tasks
    del - delete tasks
    ds - display statistics
    gr - generate reports
    e - exit
    : '''
        ).lower().strip()

        if menu == "":
            print("No option selected")
            continue

        if menu == 'r':
            reg_user()

        elif menu == 'a':
            add_task()

        elif menu == 'va':
            view_all()

        elif menu == 'vm':
            view_mine(login_username)

        elif menu == 'vc':
            view_completed()

        elif menu == 'del':
            delete_task()

        elif menu == 'ds':
            display_statistics()

        elif menu == 'gr':
            generate_reports()
            print("Report generated successfully.")

        elif menu == 'e':
            print('Goodbye!!!')
            exit()

        else:
            print("You have entered an invalid input. Please try again")
else:
    # Non-admin menu
    while True:
        menu = input(
            '''Select one of the following options:
    a - add task
    va - view all tasks
    vm - view my tasks
    e - exit
    : '''
        ).lower().strip()

        if menu == "":
            print("No option selected")
            continue

        if menu == 'a':
            add_task()

        elif menu == 'va':
            view_all()

        elif menu == 'vm':
            view_mine(login_username)

        elif menu == 'e':
            print('Goodbye!!!')
            exit()

        else:
            print("You have entered an invalid input. Please try again")
