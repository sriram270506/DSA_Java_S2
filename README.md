# DSA_Java_S2
eCommerce Website Inventory Management System 

Problem statement:
Helping businesses to have the right amount of inventory to meet customer demand. 

Features:
1. Adding an item
2. Updating an item
3. Deleting an item
4. Viewing stock
5. Searching and sorting products based on category, and product ID 
6. User authentication using password (login - Customer and Admin)

Tech Stack:
For DSA - 
  1. Python - Backend (with BST implementation and OOP design patterns)
  2. Streamlit, Pandas and Plotly - Frontend

For Java -
  1. Java - Backend (with BST implementation and OOP design patterns)
  2. Window Builder: Swing - Frontend


Workflow overview:
1. Users/Admins login using their credentials (hashing to be implemented) 
2. Users can browse products based on product ID or category and place orders using the website interface
3. Admins can carry out CRUD (Create, Read, Update, Delete) operations 
4. The frontend sends HTTP requests to the backend to carry out the operations 
5. The backend receives the request, processes the requests, applies business logic and interacts with the database. 
6. The backend then performs CRUD operations to retrieve data or update inventory data
7. The backend then sends the processed data to the frontend to be displayed
8. The frontend then updates the User Interface accordingly
9. When orders are placed, the backend automatically updates the inventory and manages the stock levels. 

