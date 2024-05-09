# SoftVan User Management
This application manages user authentication and authorization for accessing a specific resource. It is built using FastAPI, a modern web framework for building APIs with Python. The application ensures secure access to resources based on user roles and credentials.

# Features
User Authentication: Users can authenticate using their username and password.
Role-based Access Control: Access to the resource is determined based on user roles.
Logging: All authentication attempts and access requests are logged for security auditing.
Middleware: Each request is assigned a unique request ID for tracking and debugging purposes.
Exception Handling: Custom exception handlers are implemented for different types of errors.

# Installation
To run the application, you need to install the required dependencies listed in the requirements.txt file. You can do this using pip:
pip install -r requirements.txt

# Database Setup
The application uses an SQLite database (users.db) to store user information. You need to run the provided SQL script to create the necessary table and insert sample user data. Execute the following commands in your terminal:
python DB_Users_Insertion.py

# Running the Application
You can start the application using Uvicorn, which is an ASGI server. Run the following command in your terminal:
python -m uvicorn User_Resource_Access_Manager:app --reload

# Testing
The application includes unit tests to verify authentication and access control functionalities. To run the tests, execute the following command:
python -m pytest test_resource.py

# Author
This application is developed and maintained by Tanvi Gupta.
