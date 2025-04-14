// Importing necessary libraries
import javax.swing.*; // For GUI components like JFrame, JButton, JTable
import javax.swing.table.DefaultTableModel; // For managing table data
import java.awt.*; // For layout and components
import java.awt.event.*; // For event handling
import java.util.ArrayList; // To store product list
import java.util.HashMap;
import java.util.Map;

// Class to represent each product
class Product {
    int id;
    String name, category;
    int quantity;
    double price;

    public Product(int id, String name, String category, int quantity, double price) {
        this.id = id;
        this.name = name;
        this.category = category;
        this.quantity = quantity;
        this.price = price;
    }
}

// Node class for Binary Search Tree (BST)
class Node {
    Product product;
    Node left, right;

    public Node(Product product) {
        this.product = product;
        left = right = null;
    }
}

// BST class for managing inventory
class InventoryBST {
    private Node root;

    // Insert product into BST
    public void insert(Product product) {
        root = insertRec(root, product);
    }

    private Node insertRec(Node root, Product product) {
        if (root == null) return new Node(product);
        if (product.id < root.product.id)
            root.left = insertRec(root.left, product);
        else if (product.id > root.product.id)
            root.right = insertRec(root.right, product);
        return root;
    }

    // Inorder traversal to return sorted product list
    public java.util.List<Product> inorder() {
        java.util.List<Product> products = new ArrayList<>();
        inorderRec(root, products);
        return products;
    }

    private void inorderRec(Node root, java.util.List<Product> products) {
        if (root != null) {
            inorderRec(root.left, products);
            products.add(root.product);
            inorderRec(root.right, products);
        }
    }

    // Search product by ID
    public Product searchById(int id) {
        Node node = search(root, id);
        return node != null ? node.product : null;
    }

    private Node search(Node root, int id) {
        if (root == null || root.product.id == id) return root;
        if (root.product.id > id) return search(root.left, id);
        return search(root.right, id);
    }

    // Search product by category
    public java.util.List<Product> searchByCategory(String category) {
        java.util.List<Product> results = new ArrayList<>();
        searchByCategoryRec(root, category.toLowerCase(), results);
        return results;
    }

    private void searchByCategoryRec(Node root, String category, java.util.List<Product> results) {
        if (root != null) {
            searchByCategoryRec(root.left, category, results);
            if (root.product.category.equalsIgnoreCase(category))
                results.add(root.product);
            searchByCategoryRec(root.right, category, results);
        }
    }

    // Delete a product by ID
    public void delete(int id) {
        root = deleteRec(root, id);
    }

    private Node deleteRec(Node root, int id) {
        if (root == null) return root;
        if (id < root.product.id) {
            root.left = deleteRec(root.left, id);
        } else if (id > root.product.id) {
            root.right = deleteRec(root.right, id);
        } else {
            if (root.left == null) return root.right;
            else if (root.right == null) return root.left;

            root.product = minValue(root.right);
            root.right = deleteRec(root.right, root.product.id);
        }
        return root;
    }

    private Product minValue(Node root) {
        Product min = root.product;
        while (root.left != null) {
            min = root.left.product;
            root = root.left;
        }
        return min;
    }
}

// GUI Class
public class InventoryGUI extends JFrame {
    private InventoryBST inventory = new InventoryBST(); // BST object
    private Map<Integer, Integer> cart = new HashMap<>(); // Cart for buying
    private JTable productTable;
    private DefaultTableModel tableModel;

    public InventoryGUI() {
        setTitle("Inventory Management System"); // Window title
        setSize(800, 500); // Window size
        setDefaultCloseOperation(EXIT_ON_CLOSE); // Close app on exit
        setLocationRelativeTo(null); // Center the window
        setLayout(new BorderLayout()); // Layout for placing components

        initializeInventory(); // Add some default products
        createGUI(); // Create GUI layout
    }

    // Add sample products
    private void initializeInventory() {
        inventory.insert(new Product(1, "Laptop", "Electronics", 10, 999.99));
        inventory.insert(new Product(2, "Smartphone", "Electronics", 20, 699.99));
        inventory.insert(new Product(3, "Headphones", "Electronics", 30, 149.99));
        inventory.insert(new Product(4, "T-shirt", "Clothing", 50, 19.99));
    }

    // GUI Layout
    private void createGUI() {
        // Table setup
        tableModel = new DefaultTableModel(new String[]{"ID", "Name", "Category", "Quantity", "Price"}, 0);
        productTable = new JTable(tableModel);
        refreshTable();

        JScrollPane scrollPane = new JScrollPane(productTable);
        add(scrollPane, BorderLayout.CENTER); // Add table to center

        // Control Panel (bottom panel)
        JPanel controlPanel = new JPanel(); // panel = container for buttons
        JButton addBtn = new JButton("Add Product");
        JButton deleteBtn = new JButton("Delete Product");
        JButton searchBtn = new JButton("Search");
        JButton buyBtn = new JButton("Buy");
        JButton checkoutBtn = new JButton("Checkout");

        // Adding actions to buttons
        addBtn.addActionListener(e -> addProductDialog());
        deleteBtn.addActionListener(e -> deleteSelectedProduct());
        searchBtn.addActionListener(e -> searchDialog());
        buyBtn.addActionListener(e -> buyProductDialog());
        checkoutBtn.addActionListener(e -> checkout());

        // Add buttons to panel
        controlPanel.add(addBtn);
        controlPanel.add(deleteBtn);
        controlPanel.add(searchBtn);
        controlPanel.add(buyBtn);
        controlPanel.add(checkoutBtn);

        add(controlPanel, BorderLayout.SOUTH); // Add panel to bottom
    }

    // Refresh table contents
    private void refreshTable() {
        tableModel.setRowCount(0);
        for (Product p : inventory.inorder()) {
            tableModel.addRow(new Object[]{p.id, p.name, p.category, p.quantity, p.price});
        }
    }

    // Add product input dialog
    private void addProductDialog() {
        JTextField idField = new JTextField(), nameField = new JTextField();
        JTextField categoryField = new JTextField(), quantityField = new JTextField(), priceField = new JTextField();

        Object[] message = {
                "ID:", idField,
                "Name:", nameField,
                "Category:", categoryField,
                "Quantity:", quantityField,
                "Price:", priceField,
        };

        int option = JOptionPane.showConfirmDialog(this, message, "Add Product", JOptionPane.OK_CANCEL_OPTION);
        if (option == JOptionPane.OK_OPTION) {
            try {
                Product product = new Product(
                        Integer.parseInt(idField.getText()),
                        nameField.getText(),
                        categoryField.getText(),
                        Integer.parseInt(quantityField.getText()),
                        Double.parseDouble(priceField.getText())
                );
                inventory.insert(product);
                refreshTable();
            } catch (Exception ex) {
                JOptionPane.showMessageDialog(this, "Invalid input!");
            }
        }
    }

    // Delete selected product from table
    private void deleteSelectedProduct() {
        int row = productTable.getSelectedRow();
        if (row >= 0) {
            int id = (int) tableModel.getValueAt(row, 0);
            inventory.delete(id);
            refreshTable();
        } else {
            JOptionPane.showMessageDialog(this, "Please select a product to delete.");
        }
    }

    // Search Dialog: By ID or Category
    private void searchDialog() {
        String[] options = {"By ID", "By Category"};
        int choice = JOptionPane.showOptionDialog(this, "Search Product", "Search",
                JOptionPane.DEFAULT_OPTION, JOptionPane.QUESTION_MESSAGE, null, options, options[0]);

        if (choice == 0) { // By ID
            String idStr = JOptionPane.showInputDialog("Enter Product ID:");
            try {
                Product p = inventory.searchById(Integer.parseInt(idStr));
                JOptionPane.showMessageDialog(this, p != null ? "Found: " + p.name : "Product not found!");
            } catch (Exception e) {
                JOptionPane.showMessageDialog(this, "Invalid ID!");
            }
        } else if (choice == 1) { // By Category
            String category = JOptionPane.showInputDialog("Enter Category:");
            java.util.List<Product> results = inventory.searchByCategory(category);
            if (!results.isEmpty()) {
                StringBuilder sb = new StringBuilder("Results:\n");
                for (Product p : results) {
                    sb.append(p.name).append("\n");
                }
                JOptionPane.showMessageDialog(this, sb.toString());
            } else {
                JOptionPane.showMessageDialog(this, "No products found in this category!");
            }
        }
    }

    // Buy product dialog (enter ID and quantity)
    private void buyProductDialog() {
        String idStr = JOptionPane.showInputDialog("Enter Product ID to Buy:");
        String qtyStr = JOptionPane.showInputDialog("Enter Quantity:");
        try {
            int id = Integer.parseInt(idStr);
            int qty = Integer.parseInt(qtyStr);
            Product p = inventory.searchById(id);
            if (p != null && qty <= p.quantity) {
                cart.put(id, cart.getOrDefault(id, 0) + qty);
                p.quantity -= qty;
                refreshTable();
                JOptionPane.showMessageDialog(this, "Added to cart!");
            } else {
                JOptionPane.showMessageDialog(this, "Invalid quantity or product!");
            }
        } catch (Exception e) {
            JOptionPane.showMessageDialog(this, "Invalid input!");
        }
    }

    // Checkout the cart
    private void checkout() {
        if (cart.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Cart is empty!");
            return;
        }

        double total = 0;
        StringBuilder bill = new StringBuilder("Checkout Bill:\n");
        for (Map.Entry<Integer, Integer> entry : cart.entrySet()) {
            Product p = inventory.searchById(entry.getKey());
            int qty = entry.getValue();
            double cost = qty * p.price;
            bill.append(p.name).append(" x ").append(qty).append(" = ₹").append(cost).append("\n");
            total += cost;
        }

        bill.append("Total: ₹").append(total);
        JOptionPane.showMessageDialog(this, bill.toString());
        cart.clear(); // Clear cart after checkout
    }

    // Main method
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new InventoryGUI().setVisible(true));
    }
}
