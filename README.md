# Employee Management System

A console-based Employee Management System built using Python and Oracle Database. The application allows users to manage employee records and generate basic employee and salary reports.

## Features

- Add new employees
- View all employees
- Search employee by ID
- Update employee details
- Delete employee records
- Department-wise employee summary
- Salary summary
- Input validation
- Exception handling
- Oracle database connectivity
- Transaction handling using commit and rollback

## Technologies Used

- Python 3.10
- Oracle Database
- Oracle SQL
- Python `oracledb` library
- Git & GitHub
- Visual Studio Code

## Database

The project uses an Oracle database with an `employees` table containing:

- Employee ID
- Name
- Email
- Phone
- Department
- Job Role
- Salary
- Joining Date

An Oracle sequence is used to generate employee IDs.

## Project Structure

```text
Employee-Management-System-Python-Oracle/
│
├── employeemanagement.py
├── README.md
├── .gitignore
└── .env