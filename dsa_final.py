import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="eCommerce Website Inventory Management",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to make the app more attractive
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4b4b4b;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 2px solid #f0f0f0;
        margin-bottom: 2rem;
    }
    .page-subtitle {
        font-size: 1.5rem;
        color: #6c757d;
        margin-bottom: 1rem;
    }
    .card {
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        padding: 1.5rem;
        margin-bottom: 1rem;
        background-color: #f9f9f9;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .login-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 2rem;
        background-color: #f8f9fa;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .login-button {
        text-align: center;
        margin-top: 1rem;
    }
    .user-info {
        padding: 0.5rem 1rem;
        background-color: #e9ecef;
        border-radius: 5px;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .metric-container {
        background-color: #e9ecef;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .sidebar .sidebar-content .block-container {
        padding-top: 2rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: bold;
        color: #0366d6;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 1.2rem;
        font-weight: normal;
        color: #6c757d;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Product Classes
# -------------------------------
class Product:
    def __init__(self, id, name, category, quantity, price, description=""):
        self.id = id
        self.name = name
        self.category = category
        self.quantity = quantity
        self.price = price
        self.description = description

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, Category: {self.category}, Quantity: {self.quantity}, Price: ₹{self.price:.2f}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "quantity": self.quantity,
            "price": self.price,
            "description": self.description
        }

class ElectronicsProduct(Product):
    def __init__(self, id, name, quantity, price, description=""):
        super().__init__(id, name, "Electronics", quantity, price, description)

class ClothingProduct(Product):
    def __init__(self, id, name, quantity, price, description=""):
        super().__init__(id, name, "Clothing", quantity, price, description)

class AccessoriesProduct(Product):
    def __init__(self, id, name, quantity, price, description=""):
        super().__init__(id, name, "Accessories", quantity, price, description)

# -------------------------------
# BST Implementation
# -------------------------------
class Node:
    def __init__(self, product):
        self.product = product
        self.left = None
        self.right = None
        self.height = 1

class InventoryBST:
    def __init__(self):
        self.root = None
    
    def get_height(self, node):
        return 0 if not node else node.height
    
    def get_balance(self, node):
        return 0 if not node else self.get_height(node.left) - self.get_height(node.right)
    
    def update_height(self, node):
        if node:
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
    
    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self.update_height(y)
        self.update_height(x)
        return x
    
    def left_rotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self.update_height(x)
        self.update_height(y)
        return y
    
    def insert(self, product):
        self.root = self._insert_rec(self.root, product)
    
    def _insert_rec(self, root, product):
        if not root:
            return Node(product)
        
        if product.id < root.product.id:
            root.left = self._insert_rec(root.left, product)
        elif product.id > root.product.id:
            root.right = self._insert_rec(root.right, product)
        else:
            # If product with same ID exists, we update its details
            root.product = product
            return root
        
        self.update_height(root)
        balance = self.get_balance(root)
        
        # Left Left Case
        if balance > 1 and product.id < root.left.product.id:
            return self.right_rotate(root)
        
        # Right Right Case
        if balance < -1 and product.id > root.right.product.id:
            return self.left_rotate(root)
        
        # Left Right Case
        if balance > 1 and product.id > root.left.product.id:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        
        # Right Left Case
        if balance < -1 and product.id < root.right.product.id:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        
        return root
    
    def inorder(self):
        products = []
        self._inorder_rec(self.root, products)
        return products
    
    def _inorder_rec(self, root, products):
        if root:
            self._inorder_rec(root.left, products)
            products.append(root.product)
            self._inorder_rec(root.right, products)
    
    def search_by_id(self, id):
        return self._search(self.root, id)
    
    def _search(self, root, id):
        if root is None or root.product.id == id:
            return root
        if id < root.product.id:
            return self._search(root.left, id)
        return self._search(root.right, id)
    
    def search_by_category(self, category):
        results = []
        self._search_by_category_rec(self.root, category.lower(), results)
        return results
    
    def _search_by_category_rec(self, root, category, results):
        if root:
            self._search_by_category_rec(root.left, category, results)
            if root.product.category.lower() == category.lower():
                results.append(root.product)
            self._search_by_category_rec(root.right, category, results)
    
    def delete(self, id):
        self.root = self._delete_rec(self.root, id)
    
    def _delete_rec(self, root, id):
        if not root:
            return root
        
        if id < root.product.id:
            root.left = self._delete_rec(root.left, id)
        elif id > root.product.id:
            root.right = self._delete_rec(root.right, id)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            
            successor = self._min_value_node(root.right)
            root.product = successor.product
            root.right = self._delete_rec(root.right, successor.product.id)
        
        if not root:
            return root
        
        self.update_height(root)
        balance = self.get_balance(root)
        
        # Balance if needed
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
        
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
        
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        
        return root
    
    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

# -------------------------------
# Inventory System
# -------------------------------
class InventorySystem:
    def __init__(self):
        self.inventory = InventoryBST()
        self.initialize_inventory()
    
    def initialize_inventory(self):
        products = [
            ElectronicsProduct(1, "Laptop", 10, 999.99, "High-performance laptop with latest specs"),
            ElectronicsProduct(2, "Smartphone", 20, 699.99, "Latest model with advanced camera"),
            ElectronicsProduct(3, "Headphones", 30, 149.99, "Noise-cancelling wireless headphones"),
            ClothingProduct(4, "T-shirt", 50, 19.99, "100% cotton, comfortable fit"),
            ClothingProduct(5, "Jeans", 25, 39.99, "Durable denim with stylish wash"),
            ClothingProduct(7, "Winter Jacket", 15, 89.99, "Warm jacket for cold weather"),
            AccessoriesProduct(6, "Wrist Watch", 10, 99.99, "Elegant timepiece with leather strap"),
            AccessoriesProduct(8, "Sunglasses", 40, 29.99, "UV protection with trendy design"),
            AccessoriesProduct(9, "Backpack", 35, 49.99, "Spacious backpack with multiple compartments")
        ]
        for product in products:
            self.inventory.insert(product)
    
    def get_all_products(self):
        # Fixed implementation to correctly traverse the BST
        products = []
        self._inorder_rec(self.inventory.root, products)
        return products
    
    def _inorder_rec(self, root, products):
        if root:
            self._inorder_rec(root.left, products)
            products.append(root.product)
            self._inorder_rec(root.right, products)
    
    def search_product_by_id(self, id):
        result = self.inventory.search_by_id(id)
        return result.product if result else None
    
    def search_products_by_category(self, category):
        return self.inventory.search_by_category(category)
    
    def add_product(self, id, name, category, quantity, price, description=""):
        if category.lower() == "electronics":
            product = ElectronicsProduct(id, name, quantity, price, description)
        elif category.lower() == "clothing":
            product = ClothingProduct(id, name, quantity, price, description)
        elif category.lower() == "accessories":
            product = AccessoriesProduct(id, name, quantity, price, description)
        else:
            product = Product(id, name, category, quantity, price, description)
        
        self.inventory.insert(product)
        return product
    
    def delete_product(self, id):
        self.inventory.delete(id)
    
    def reduce_product_quantity(self, id, quantity_to_reduce):
        """Reduce product quantity by specified amount and return success"""
        result = self.inventory.search_by_id(id)
        if result and result.product.quantity >= quantity_to_reduce:
            result.product.quantity -= quantity_to_reduce
            return True
        return False
    
    def get_categories(self):
        products = self.get_all_products()
        return sorted(list(set(p.category for p in products)))

# -------------------------------
# Cart and Checkout Functions
# -------------------------------
def add_to_cart(product_id, quantity):
    """Add product to cart with specified quantity"""
    if product_id in st.session_state.cart:
        st.session_state.cart[product_id] += quantity
    else:
        st.session_state.cart[product_id] = quantity
    
    # Check if we're not exceeding available inventory
    product = st.session_state.inventory_system.search_product_by_id(product_id)
    if product and st.session_state.cart[product_id] > product.quantity:
        st.session_state.cart[product_id] = product.quantity
        st.warning(f"Quantity adjusted to available stock ({product.quantity})")
    else:
        st.success(f"Added {quantity} of {product.name} to cart")

def update_cart_quantity(product_id, new_quantity):
    """Update product quantity in cart"""
    product = st.session_state.inventory_system.search_product_by_id(product_id)
    
    if new_quantity <= 0:
        # Remove from cart if quantity is 0 or negative
        if product_id in st.session_state.cart:
            del st.session_state.cart[product_id]
    else:
        # Check if we have enough inventory
        if new_quantity > product.quantity:
            st.session_state.cart[product_id] = product.quantity
            st.warning(f"Quantity adjusted to available stock ({product.quantity})")
        else:
            st.session_state.cart[product_id] = new_quantity

def remove_from_cart(product_id):
    """Remove product from cart"""
    if product_id in st.session_state.cart:
        del st.session_state.cart[product_id]

def clear_cart():
    """Clear all items from cart"""
    st.session_state.cart = {}

def get_cart_items():
    """Get cart items with product details"""
    cart_items = []
    for product_id, quantity in st.session_state.cart.items():
        product = st.session_state.inventory_system.search_product_by_id(product_id)
        if product:
            cart_item = {
                "id": product.id,
                "name": product.name,
                "category": product.category,
                "price": product.price,
                "quantity": quantity,
                "total": product.price * quantity
            }
            cart_items.append(cart_item)
    return cart_items

def get_cart_total():
    """Calculate cart total before tax"""
    cart_items = get_cart_items()
    return sum(item["total"] for item in cart_items)

def get_cart_count():
    """Get total number of items in cart"""
    return sum(st.session_state.cart.values())

def process_checkout():
    """Process checkout and update inventory"""
    success = True
    failed_items = []
    
    # Verify all items are in stock
    for product_id, quantity in st.session_state.cart.items():
        product = st.session_state.inventory_system.search_product_by_id(product_id)
        if not product or product.quantity < quantity:
            success = False
            failed_items.append(product.name if product else f"Product ID {product_id}")
    
    if success:
        # Update inventory quantities
        for product_id, quantity in st.session_state.cart.items():
            st.session_state.inventory_system.reduce_product_quantity(product_id, quantity)
        
        # Clear cart after successful checkout
        clear_cart()
        st.session_state.checkout_success = True
        return True, None
    else:
        return False, failed_items

# -------------------------------
# Streamlit UI
# -------------------------------

def init_session_state():
    """Initialize session state variables"""
    if 'inventory_system' not in st.session_state:
        st.session_state.inventory_system = InventorySystem()
    
    if 'cart' not in st.session_state:
        st.session_state.cart = {}  # {product_id: quantity}
    
    if 'page' not in st.session_state:
        st.session_state.page = "login"
    
    if 'checkout_success' not in st.session_state:
        st.session_state.checkout_success = False
        
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None

def display_product_table(products):
    """Display products in a dataframe"""
    if not products:
        st.info("No products to display.")
        return
    
    df = pd.DataFrame([p.to_dict() for p in products])
    if "description" in df.columns:
        df = df.drop("description", axis=1)
    df['price'] = df['price'].apply(lambda x: f"₹{x:.2f}")
    st.dataframe(df, use_container_width=True)

def display_cart_summary():
    """Display a summary of the cart contents"""
    cart_count = get_cart_count()
    if cart_count > 0:
        cart_total = get_cart_total()
        st.markdown(f"""
        <div style="background-color: #e0f7fa; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
            <h3 style="margin-bottom: 5px; color: #00796b;">Cart Summary</h3>
            <p style="margin-bottom: 5px;"><strong>Items:</strong> {cart_count}</p>
            <p style="margin-bottom: 0;"><strong>Total:</strong> ₹{cart_total:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Your cart is empty.")

def login_page():
    st.markdown("<h1 class='main-header'> eCommerce Website - Login</h1>", unsafe_allow_html=True)
    
    st.markdown("<h2  class='login-header' >User Authentication</h2>", unsafe_allow_html=True)
    
    # Select role
    role = st.radio("Select Role:", ["ADMIN", "CUSTOMER"], horizontal=True)
    
    # Username field
    username = st.text_input("Username:")
    
    # Password field (hidden)
    password = st.text_input("Password:", type="password")
    
    if st.button("Login"):
        if role == "ADMIN" and username == "admin123":
            st.session_state.authenticated = True
            st.session_state.user_role = "admin"
            st.session_state.page = "home"
            st.success("Logged in successfully as Administrator!")
            st.rerun()
        elif role == "CUSTOMER" and username == "customer123":
            st.session_state.authenticated = True
            st.session_state.user_role = "customer"
            st.session_state.page = "home"
            st.success("Logged in successfully as Customer!")
            st.rerun()
        else:
            st.error("Invalid credentials. Please try again.")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Login help
    st.markdown("""
    <div style="max-width: 500px; margin: 2rem auto; padding: 1rem; background-color: #f1f8e9; border-radius: 10px;">
        <h3>Login Help</h3>
        <p><strong>Admin Access:</strong> Username: admin123</p>
        <p><strong>Customer Access:</strong> Username: customer123</p>
        <p>You can enter any password.</p>
    </div>
    """, unsafe_allow_html=True)

def home_page():
    st.markdown("<h1 class='main-header'> Inventory Management</h1>", unsafe_allow_html=True)
    
    st.markdown("<p class='page-subtitle'> Discover amazing products and manage your inventory efficiently.</p>", unsafe_allow_html=True)
    
    # Display quick statistics
    st.subheader("Inventory Overview")
    products = st.session_state.inventory_system.get_all_products()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Products", len(products))
    
    with col2:
        total_items = sum(p.quantity for p in products)
        st.metric("Total Items", total_items)
    
    with col3:
        total_value = sum(p.quantity * p.price for p in products)
        st.metric("Inventory Value", f"₹{total_value:.2f}")
    
    # Display all products in inventory
    st.subheader("All Products in Inventory")
    display_product_table(products)
    
    # Display sample charts
    st.subheader("Inventory Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Category Distribution
        categories = {}
        for product in products:
            categories[product.category] = categories.get(product.category, 0) + 1
        
        if categories:
            df = pd.DataFrame(list(categories.items()), columns=['Category', 'Count'])
            fig = px.pie(df, values='Count', names='Category', title='Product Categories')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Inventory Value by Category
        value_by_category = {}
        for product in products:
            value = product.price * product.quantity
            value_by_category[product.category] = value_by_category.get(product.category, 0) + value
        
        if value_by_category:
            df = pd.DataFrame(list(value_by_category.items()), columns=['Category', 'Value'])
            fig = px.bar(df, x='Category', y='Value', title='Inventory Value by Category')
            fig.update_layout(yaxis_title='Value (₹)', height=400)
            st.plotly_chart(fig, use_container_width=True)

def search_page():
    st.markdown("<h1 class='main-header'>🔍 Search Products</h1>", unsafe_allow_html=True)
    
    # Search options
    search_type = st.radio("Search by:", ["ID", "Category"], horizontal=True)
    
    if search_type == "ID":
        # Search by ID
        id_input = st.number_input("Enter Product ID:", min_value=1, step=1)
        if st.button("Search", key="search_id_button"):
            product = st.session_state.inventory_system.search_product_by_id(id_input)
            if product:
                st.success(f"Product found: {product.name}")
                
                # Display product details
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Product Details")
                    st.write(f"**ID:** {product.id}")
                    st.write(f"**Name:** {product.name}")
                    st.write(f"**Category:** {product.category}")
                    st.write(f"**Price:** ₹{product.price:.2f}")
                    st.write(f"**Quantity in Stock:** {product.quantity}")
                    if product.description:
                        st.write(f"**Description:** {product.description}")
                
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.error(f"No product found with ID: {id_input}")
    
    else:  # Category search
        categories = st.session_state.inventory_system.get_categories()
        category_input = st.selectbox("Select Category:", categories)
        
        if st.button("Search", key="search_category_button"):
            products = st.session_state.inventory_system.search_products_by_category(category_input)
            if products:
                st.success(f"Found {len(products)} products in category: {category_input}")
                display_product_table(products)
            else:
                st.error(f"No products found in category: {category_input}")

def shop_page():
    st.markdown("<h1 class='main-header'>🛒 Shop Products</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Shop by")
        shop_by = st.radio("Select option:", ["Category", "Product ID"])
    
    with col2:
        if shop_by == "Category":
            categories = st.session_state.inventory_system.get_categories()
            selected_category = st.selectbox("Select Category:", categories)
            
            products = st.session_state.inventory_system.search_products_by_category(selected_category)
            
            if products:
                st.success(f"Showing {len(products)} products in {selected_category}")
                
                for product in products:
                    st.markdown(f"""
                    <div style="border: 1px solid #ddd; padding: 15px; border-radius: 10px; margin-bottom: 15px; background-color: #f8f9fa;">
                        <h3 style="margin-bottom: 10px;">{product.name}</h3>
                        <p style="margin-bottom: 5px;"><strong>ID:</strong> {product.id}</p>
                        <p style="margin-bottom: 5px;"><strong>Price:</strong> ₹{product.price:.2f}</p>
                        <p style="margin-bottom: 5px;"><strong>In Stock:</strong> {product.quantity}</p>
                        <p style="margin-bottom: 15px;"><strong>Description:</strong> {product.description}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        quantity = st.number_input(f"Quantity for {product.name}", min_value=1, max_value=product.quantity, value=1, key=f"qty_{product.id}")
                    with col3:
                        if st.button("Add to Cart", key=f"add_{product.id}"):
                            add_to_cart(product.id, quantity)
                            st.rerun()
            else:
                st.info(f"No products found in category: {selected_category}")
        
        else:  # Shop by Product ID
            id_input = st.number_input("Enter Product ID:", min_value=1, step=1)
            
            if st.button("Find Product", key="find_product_button"):
                product = st.session_state.inventory_system.search_product_by_id(id_input)
                
                if product:
                    st.success(f"Product found: {product.name}")
                    
                    st.markdown(f"""
                    <div style="border: 1px solid #ddd; padding: 20px; border-radius: 10px; margin-bottom: 20px; background-color: #f8f9fa;">
                        <h3 style="margin-bottom: 10px;">{product.name}</h3>
                        <p style="margin-bottom: 5px;"><strong>Category:</strong> {product.category}</p>
                        <p style="margin-bottom: 5px;"><strong>Price:</strong> ₹{product.price:.2f}</p>
                        <p style="margin-bottom: 5px;"><strong>In Stock:</strong> {product.quantity}</p>
                        <p style="margin-bottom: 15px;"><strong>Description:</strong> {product.description}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if product.quantity > 0:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            quantity = st.number_input(f"Quantity", min_value=1, max_value=product.quantity, value=1, key=f"qty_single_{product.id}")
                        with col2:
                            if st.button("Add to Cart", key=f"add_single_{product.id}"):
                                add_to_cart(product.id, quantity)
                                st.rerun()
                    else:
                        st.error("This product is out of stock.")
                else:
                    st.error(f"No product found with ID: {id_input}")

def checkout_page():
    st.markdown("<h1 class='main-header'>💰 Checkout</h1>", unsafe_allow_html=True)
    
    if st.session_state.checkout_success:
        st.markdown("""
        <div class="success-message">
            <h2>Thank you for your purchase!</h2>
            <p>Your order has been processed successfully. The inventory has been updated.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Continue Shopping"):
            st.session_state.checkout_success = False
            st.session_state.page = "shop"
            st.rerun()
    else:
        cart_items = get_cart_items()
        
        if not cart_items:
            st.info("Your cart is empty. Add some products to proceed with checkout.")
            
            if st.button("Go to Shop"):
                st.session_state.page = "shop"
                st.rerun()
        else:
            # Display cart items
            st.subheader("Your Cart")
            cart_df = pd.DataFrame(cart_items)
            cart_df['price'] = cart_df['price'].apply(lambda x: f"₹{x:.2f}")
            cart_df['total'] = cart_df['total'].apply(lambda x: f"₹{x:.2f}")
            cart_df = cart_df.rename(columns={
                'id': 'ID',
                'name': 'Product',
                'category': 'Category',
                'price': 'Unit Price',
                'quantity': 'Quantity',
                'total': 'Total'
            })
            st.dataframe(cart_df[['ID', 'Product', 'Category', 'Unit Price', 'Quantity', 'Total']], use_container_width=True)
            
            # Update cart quantities
            st.subheader("Update Quantities")
            for item in cart_items:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"{item['name']} (₹{item['price']:.2f} each)")
                with col2:
                    new_qty = st.number_input(f"Qty", min_value=0, max_value=100, value=item['quantity'], key=f"update_{item['id']}")
                with col3:
                    if st.button("Update", key=f"update_btn_{item['id']}"):
                        update_cart_quantity(item['id'], new_qty)
                        st.rerun()
            
            # Cart totals and checkout
            st.subheader("Order Summary")
            
            subtotal = get_cart_total()
            tax_rate = 0.10  # 10% tax
            tax = subtotal * tax_rate
            total = subtotal + tax
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.write(f"**Subtotal:** ₹{subtotal:.2f}")
                st.write(f"**Tax (10%):** ₹{tax:.2f}")
                st.write(f"**Total:** ₹{total:.2f}")
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                if st.button("Clear Cart"):
                    clear_cart()
                    st.rerun()
                
                if st.button("Process Checkout", key="process_checkout"):
                    success, failed_items = process_checkout()
                    if success:
                        st.rerun()  # Rerun to show success message
                    else:
                        st.error(f"Checkout failed. The following items are no longer available in the requested quantity: {', '.join(failed_items)}")
                st.markdown("</div>", unsafe_allow_html=True)

def add_product_page():
    st.markdown("<h1 class='main-header'>➕ Add New Product</h1>", unsafe_allow_html=True)
    
    # Create form for adding new products
    with st.form("add_product_form"):
        st.subheader("Product Details")
        
        id_input = st.number_input("Product ID", min_value=1, step=1)
        name_input = st.text_input("Product Name")
        
        category_options = ["Electronics", "Clothing", "Accessories", "Other"]
        category_input = st.selectbox("Category", category_options)
        
        if category_input == "Other":
            custom_category = st.text_input("Specify Category")
            if custom_category:
                category_input = custom_category
        
        quantity_input = st.number_input("Quantity", min_value=0, step=1)
        price_input = st.number_input("Price (₹)", min_value=0.0, step=0.01, format="%.2f")
        description_input = st.text_area("Product Description")
        
        submit_button = st.form_submit_button("Add Product")
        
        if submit_button:
            # Check if product ID already exists
            existing_product = st.session_state.inventory_system.search_product_by_id(id_input)
            
            if existing_product:
                st.error(f"A product with ID {id_input} already exists. Please use a different ID.")
            elif not name_input:
                st.error("Product name cannot be empty.")
            else:
                # Add the new product
                new_product = st.session_state.inventory_system.add_product(
                    id_input, name_input, category_input, quantity_input, price_input, description_input
                )
                
                st.success(f"Product '{name_input}' added successfully!")
                
                # Display the added product
                st.subheader("Added Product")
                st.write(f"**ID:** {new_product.id}")
                st.write(f"**Name:** {new_product.name}")
                st.write(f"**Category:** {new_product.category}")
                st.write(f"**Quantity:** {new_product.quantity}")
                st.write(f"**Price:** ₹{new_product.price:.2f}")
                if new_product.description:
                    st.write(f"**Description:** {new_product.description}")

def remove_product_page():
    st.markdown("<h1 class='main-header'>❌ Remove Product</h1>", unsafe_allow_html=True)
    
    # Get all products for selection
    products = st.session_state.inventory_system.get_all_products()
    
    if not products:
        st.info("No products available to remove.")
        return
    
    # Create a selection list of products
    product_options = [f"ID: {p.id} - {p.name} ({p.category})" for p in products]
    selected_product = st.selectbox("Select Product to Remove:", product_options)
    
    # Extract the ID from the selected option
    selected_id = int(selected_product.split(" - ")[0].replace("ID: ", ""))
    
    if st.button("Remove Product"):
        # Find the product to display confirmation
        product = st.session_state.inventory_system.search_product_by_id(selected_id)
        
        if product:
            # Remove the product
            st.session_state.inventory_system.delete_product(selected_id)
            st.success(f"Product '{product.name}' has been removed from inventory.")
            
            # Remove from cart if present
            if selected_id in st.session_state.cart:
                del st.session_state.cart[selected_id]
                st.info("This product has also been removed from your cart.")
        else:
            st.error(f"Failed to remove product with ID {selected_id}.")

def features_page():
    st.markdown("<h1 class='main-header'>✨ Key Features</h1>", unsafe_allow_html=True)
    
    # Show application overview
    st.subheader("Key Features")
    
    features = [
        {
            "title": "🔍 Search Products",
            "description": "Find products quickly by their ID or category."
        },
        {
            "title": "🛒 Shop Products",
            "description": "Browse products and add them to your cart with quantity selection."
        },
        {
            "title": "📊 Inventory Statistics",
            "description": "View visual representations of your inventory data."
        },
        {
            "title": "💰 Checkout Process",
            "description": "Complete purchases with a simple checkout flow."
        },
        {
            "title": "➕ Add New Products",
            "description": "Easily add new products to your inventory."
        },
        {
            "title": "❌ Remove Products",
            "description": "Remove products that are no longer needed."
        },
        {
            "title": "🔐 User Authentication",
            "description": "Different access levels for admin and customer roles."
        }
    ]
    
    # Display features in a more visually appealing way
    for i, feature in enumerate(features):
        if i % 2 == 0:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div style="border: 1px solid #ddd; padding: 20px; border-radius: 10px; margin-bottom: 20px; background-color: #f8f9fa;">
                    <h3 style="color: #0366d6; margin-bottom: 10px;">{feature['title']}</h3>
                    <p style="color: #586069;">{feature['description']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            with col2:
                st.markdown(f"""
                <div style="border: 1px solid #ddd; padding: 20px; border-radius: 10px; margin-bottom: 20px; background-color: #f8f9fa;">
                    <h3 style="color: #0366d6; margin-bottom: 10px;">{feature['title']}</h3>
                    <p style="color: #586069;">{feature['description']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    st.subheader("Technologies Used")
    tech_col1, tech_col2 = st.columns(2)
    
    with tech_col1:
        st.markdown("""
        <div style="border: 1px solid #ddd; padding: 20px; border-radius: 10px; background-color: #f8f9fa;">
            <h3 style="color: #0366d6; margin-bottom: 10px;">Frontend</h3>
            <ul>
                <li><strong>Streamlit:</strong> For building the interactive web interface</li>
                <li><strong>Plotly:</strong> For creating interactive data visualizations</li>
                <li><strong>Pandas:</strong> For data manipulation and display</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with tech_col2:
        st.markdown("""
        <div style="border: 1px solid #ddd; padding: 20px; border-radius: 10px; background-color: #f8f9fa;">
            <h3 style="color: #0366d6; margin-bottom: 10px;">Backend</h3>
            <ul>
                <li><strong>Python:</strong> Core programming language</li>
                <li><strong>Binary Search Tree:</strong> For efficient inventory management</li>
                <li><strong>OOP:</strong> Object-oriented design patterns</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def main():
    # Initialize session state
    init_session_state()
    
    # Show login page if not authenticated
    if not st.session_state.authenticated:
        login_page()
        return
    
    # Sidebar navigation after authentication
    with st.sidebar:
        st.title("Navigation")
        
        # Show user role
        st.markdown(f"""
        <div class="user-info">
            Logged in as: {st.session_state.user_role.upper()}
        </div>
        """, unsafe_allow_html=True)
        
        # Display cart summary in sidebar if customer
        if st.session_state.user_role == "customer":
            display_cart_summary()
        
        # Navigation options based on user role
        if st.session_state.user_role == "admin":
            # Admin navigation
            pages = {
                "🏠 Home": "home",
                "🔍 Search Products": "search",
                "➕ Add Product": "add_product",
                "❌ Remove Product": "remove_product",
                "✨ Features": "features"
            }
        else:
            # Customer navigation
            pages = {
                "🏠 Home": "home",
                "🔍 Search Products": "search",
                "🛒 Shop": "shop",
                "💰 Checkout": "checkout",
                "✨ Features": "features"
            }
        
        for page_name, page_id in pages.items():
            if st.button(page_name, key=f"nav_{page_id}"):
                st.session_state.page = page_id
                st.rerun()
        
        # Logout button
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user_role = None
            st.session_state.page = "login"
            st.rerun()
    
    # Content area - display the selected page
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "search":
        search_page()
    elif st.session_state.page == "shop" and st.session_state.user_role == "customer":
        shop_page()
    elif st.session_state.page == "checkout" and st.session_state.user_role == "customer":
        checkout_page()
    elif st.session_state.page == "add_product" and st.session_state.user_role == "admin":
        add_product_page()
    elif st.session_state.page == "remove_product" and st.session_state.user_role == "admin":
        remove_product_page()
    elif st.session_state.page == "features":
        features_page()
    else:
        st.warning("You do not have permission to access this page.")
        st.session_state.page = "home"
        st.rerun()

if __name__ == "__main__":
    main()
