import os
import oracledb
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    try:
        connection = oracledb.connect(
            user="EMPLOYEE_USER",
            password=os.getenv("ORACLE_PASSWORD"),
            dsn="localhost:1522/FREEPDB1"
        )

        print("Database connected successfully.")
        return connection

    except oracledb.DatabaseError as e:
        print("Database connection failed.")
        print("Error:", e)
        return None


# ==========================================
# ADD EMPLOYEE
# ==========================================

def add_employee(connection):

    print("\n========== Add Employee ==========")

    name = input("Enter name: ")
    email = input("Enter email: ")
    phone = input("Enter phone: ")
    department = input("Enter department: ")
    job_role = input("Enter job role: ")

    try:
        salary = float(input("Enter salary: "))

        if salary <= 0:
            print("Salary must be greater than 0.")
            return

    except ValueError:
        print("Please enter a valid salary.")
        return

    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO employees
            (
                id,
                name,
                email,
                phone,
                department,
                job_role,
                salary,
                joining_date
            )
            VALUES
            (
                employee_seq.NEXTVAL,
                :1,
                :2,
                :3,
                :4,
                :5,
                :6,
                SYSDATE
            )
        """, (
            name,
            email,
            phone,
            department,
            job_role,
            salary
        ))

        connection.commit()

        print("Employee added successfully.")

    except oracledb.DatabaseError as e:
        connection.rollback()
        print("Database error:", e)

    finally:
        cursor.close()


# ==========================================
# VIEW ALL EMPLOYEES
# ==========================================

def view_employees(connection):

    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                id,
                name,
                email,
                phone,
                department,
                job_role,
                salary,
                joining_date
            FROM employees
            ORDER BY id
        """)

        employees = cursor.fetchall()

        if not employees:
            print("\nNo employee records found.")
            return

        print("\n================ Employee List ================")

        for employee in employees:

            print("\n-----------------------------------------------")
            print(f"ID           : {employee[0]}")
            print(f"Name         : {employee[1]}")
            print(f"Email        : {employee[2]}")
            print(f"Phone        : {employee[3]}")
            print(f"Department   : {employee[4]}")
            print(f"Job Role     : {employee[5]}")
            print(f"Salary       : {employee[6]}")
            print(f"Joining Date : {employee[7]}")

        print("-----------------------------------------------")

    except oracledb.DatabaseError as e:
        print("Database error:", e)

    finally:
        cursor.close()


# ==========================================
# SEARCH EMPLOYEE
# ==========================================

def search_employee(connection):

    try:
        employee_id = int(input("Enter employee ID: "))

    except ValueError:
        print("Please enter a valid employee ID.")
        return

    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT
                id,
                name,
                email,
                phone,
                department,
                job_role,
                salary,
                joining_date
            FROM employees
            WHERE id = :1
        """, (employee_id,))

        employee = cursor.fetchone()

        if employee:

            print("\n--------- Employee Found ---------")
            print(f"ID           : {employee[0]}")
            print(f"Name         : {employee[1]}")
            print(f"Email        : {employee[2]}")
            print(f"Phone        : {employee[3]}")
            print(f"Department   : {employee[4]}")
            print(f"Job Role     : {employee[5]}")
            print(f"Salary       : {employee[6]}")
            print(f"Joining Date : {employee[7]}")
            print("----------------------------------")

        else:
            print("Employee not found.")

    except oracledb.DatabaseError as e:
        print("Database error:", e)

    finally:
        cursor.close()


# ==========================================
# UPDATE EMPLOYEE
# ==========================================

def update_employee(connection):

    try:
        employee_id = int(input("Enter employee ID to update: "))

    except ValueError:
        print("Please enter a valid employee ID.")
        return

    cursor = connection.cursor()

    try:

        # Check whether employee exists
        cursor.execute(
            "SELECT name FROM employees WHERE id = :1",
            (employee_id,)
        )

        employee = cursor.fetchone()

        if not employee:
            print("Employee not found.")
            return

        print(f"\nUpdating employee: {employee[0]}")

        name = input("Enter new name: ")
        email = input("Enter new email: ")
        phone = input("Enter new phone: ")
        department = input("Enter new department: ")
        job_role = input("Enter new job role: ")

        try:
            salary = float(input("Enter new salary: "))

            if salary <= 0:
                print("Salary must be greater than 0.")
                return

        except ValueError:
            print("Please enter a valid salary.")
            return

        cursor.execute("""
            UPDATE employees
            SET
                name = :1,
                email = :2,
                phone = :3,
                department = :4,
                job_role = :5,
                salary = :6
            WHERE id = :7
        """, (
            name,
            email,
            phone,
            department,
            job_role,
            salary,
            employee_id
        ))

        connection.commit()

        print("Employee updated successfully.")

    except oracledb.DatabaseError as e:
        connection.rollback()
        print("Database error:", e)

    finally:
        cursor.close()


# ==========================================
# DELETE EMPLOYEE
# ==========================================

def delete_employee(connection):

    try:
        employee_id = int(input("Enter employee ID to delete: "))

    except ValueError:
        print("Please enter a valid employee ID.")
        return

    cursor = connection.cursor()

    try:

        cursor.execute(
            "SELECT name FROM employees WHERE id = :1",
            (employee_id,)
        )

        employee = cursor.fetchone()

        if not employee:
            print("Employee not found.")
            return

        print(f"Employee found: {employee[0]}")

        confirm = input(
            "Are you sure you want to delete this employee? (yes/no): "
        )

        if confirm.lower() == "yes":

            cursor.execute(
                "DELETE FROM employees WHERE id = :1",
                (employee_id,)
            )

            connection.commit()

            print("Employee deleted successfully.")

        else:
            print("Delete operation cancelled.")

    except oracledb.DatabaseError as e:
        connection.rollback()
        print("Database error:", e)

    finally:
        cursor.close()


# ==========================================
# DEPARTMENT SUMMARY
# ==========================================

def department_summary(connection):

    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT
                department,
                COUNT(*) AS employee_count,
                AVG(salary) AS average_salary
            FROM employees
            GROUP BY department
            ORDER BY department
        """)

        results = cursor.fetchall()

        if not results:
            print("No employee records found.")
            return

        print("\n========== Department Summary ==========")

        for row in results:

            department = row[0]
            employee_count = row[1]
            average_salary = row[2]

            print("\n---------------------------------------")
            print(f"Department     : {department}")
            print(f"Employees      : {employee_count}")
            print(f"Average Salary : {average_salary:.2f}")

        print("---------------------------------------")

    except oracledb.DatabaseError as e:
        print("Database error:", e)

    finally:
        cursor.close()


# ==========================================
# SALARY SUMMARY
# ==========================================

def salary_summary(connection):

    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT
                COUNT(*),
                SUM(salary),
                AVG(salary),
                MAX(salary),
                MIN(salary)
            FROM employees
        """)

        result = cursor.fetchone()

        if result[0] == 0:
            print("No employee records found.")
            return

        employee_count = result[0]
        total_salary = result[1]
        average_salary = result[2]
        highest_salary = result[3]
        lowest_salary = result[4]

        print("\n========== Salary Summary ==========")

        print(f"Total Employees : {employee_count}")
        print(f"Total Salary    : {total_salary:.2f}")
        print(f"Average Salary  : {average_salary:.2f}")
        print(f"Highest Salary  : {highest_salary:.2f}")
        print(f"Lowest Salary   : {lowest_salary:.2f}")

        print("------------------------------------")

    except oracledb.DatabaseError as e:
        print("Database error:", e)

    finally:
        cursor.close()


# ==========================================
# MAIN PROGRAM
# ==========================================

def main():

    connection = get_connection()

    if connection is None:
        return

    try:

        while True:

            print("\n")
            print("==========================================")
            print("       EMPLOYEE MANAGEMENT SYSTEM")
            print("==========================================")
            print("1. Add Employee")
            print("2. View Employees")
            print("3. Search Employee")
            print("4. Update Employee")
            print("5. Delete Employee")
            print("6. Department Summary")
            print("7. Salary Summary")
            print("8. Exit")
            print("==========================================")

            try:
                choice = int(input("Enter your choice: "))

            except ValueError:
                print("Please enter a number from 1 to 8.")
                continue

            if choice == 1:

                add_employee(connection)

            elif choice == 2:

                view_employees(connection)

            elif choice == 3:

                search_employee(connection)

            elif choice == 4:

                update_employee(connection)

            elif choice == 5:

                delete_employee(connection)

            elif choice == 6:

                department_summary(connection)

            elif choice == 7:

                salary_summary(connection)

            elif choice == 8:

                print("\nExiting Employee Management System...")
                break

            else:

                print("Invalid choice. Please select 1 to 8.")

    finally:

        connection.close()
        print("Database connection closed.")


# ==========================================
# PROGRAM START
# ==========================================

if __name__ == "__main__":
    main()