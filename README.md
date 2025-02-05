# DSA_Java_S2
eCommerce Website Inventory Management System using Java
(Proposed solution - subjected to changes as per faculties' opinions and advice) 
Problem statement:
Helping businesses to have the right amount of inventory to meet customer demand. 

Features:
1. Adding an item
2. Updating an item
3. Deleting an item
4. Viewing stock
5. Searching and sorting products based on category, name, price, product ID 
6. User authentication using password (login and signup)

Tech Stack:
1. Frontend - Basically the User interface in which all tasks are carried out (HTML preferably)
2. Backend - Can be considered as the “engine” of this system. It carries out every single operation behind the scenes and communicates with the frontend (Java + Spring Boot)
3. Database Management System - MySQL to handle inventory 
4. RESTful API - Developed using Postman and is used to connect the frontend to the database. It’s like a messenger between frontend and backend and is used to fetch data. (yet to finalize upon implementation due to various constraints)



Workflow overview:
1. Users/Admins login using their credentials (hashing to be implemented) 
2. Users can browse products based on product names, category, prices and place orders using the website interface
3. Admins can carry out CRUD (Create, Read, Update, Delete) operations 
4. The frontend sends HTTP requests to the backend to carry out the operations via RESTful APIs
5. The backend receives the request, processes the requests, applies business logic and interacts with the database. 
6. The backend then performs CRUD operations to retrieve data or update inventory data
7. The backend then sends the processed data to the frontend to be displayed through the API
8. The frontend then updates the User Interface accordingly
9. When orders are placed, the backend automatically updates the inventory and manages the stock levels. 

