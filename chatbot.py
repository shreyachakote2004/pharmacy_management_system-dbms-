# import streamlit as st
# import mysql.connector
# import pandas as pd  # Import Pandas for proper table formatting
# import google.generativeai as genai

# # Database Connection Function
# def get_db_connection():
#     return mysql.connector.connect(
#         host='localhost', user='root', password='Shreya@123', database='PharmacyManagement'
#     )

# # Initialize session state
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
#     st.session_state.user_type = None  # 'Customer' or 'Manager'
#     st.session_state.user_id = None    # Stores the user ID


# # Configure Gemini API
# API_KEY = "AIzaSyDCy142-54gqPVp_svs9M_0y4zayUZpSoY"
# genai.configure(api_key=API_KEY)
# model = genai.GenerativeModel("gemini-pro")

# # Initialize chat history for the chatbot
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# # Pharmacy Management Functions
# def signup_user(email, password, name, age, sex, phone, address):
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     # Check if email already exists
#     cursor.execute("SELECT C_ID FROM Customer WHERE EmailID = %s", (email,))
#     existing_user = cursor.fetchone()

#     if existing_user:
#         st.error("Email already registered. Please log in instead.")
#     else:
#         # Insert into Customer table
#         cursor.execute(
#             "INSERT INTO Customer (C_name, Age, Sex, Address, Pwd, EmailID) VALUES (%s, %s, %s, %s, %s, %s)",
#             (name, age, sex, address, password, email)
#         )
#         conn.commit()

#         # Get the newly created Customer ID
#         cursor.execute("SELECT C_ID FROM Customer WHERE EmailID = %s", (email,))
#         customer_id = cursor.fetchone()[0]

#         # Insert into CustomerPhone table ONLY IF phone number is provided
#         if phone.strip():  # Ensures non-empty phone
#             cursor.execute(
#                 "INSERT INTO CustomerPhone (C_ID, Ph_no) VALUES (%s, %s)",
#                 (customer_id, phone)
#             )
#             conn.commit()

#         st.success("Signup successful! You can now log in.")

#     cursor.close()
#     conn.close()

# # Login Function
# def login_user(username, password, user_type):
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     if user_type == "Customer":
#         query = "SELECT C_ID FROM Customer WHERE EmailID = %s AND Pwd = %s"
#     else:
#         query = "SELECT M_ID FROM Manager WHERE M_name = %s AND M_pwd = %s"

#     cursor.execute(query, (username, password))
#     result = cursor.fetchone()

#     if result:
#         st.session_state.logged_in = True
#         st.session_state.user_type = user_type
#         st.session_state.user_id = result[0]
#         st.success(f"Logged in as {user_type}!")
#     else:
#         st.error("Invalid credentials. Please try again.")

#     cursor.close()
#     conn.close()

# # Function to Place Order (Customer)
# def place_order():
#     if not st.session_state.logged_in or st.session_state.user_type != "Customer":
#         st.error("You must be logged in as a customer!")
#         return

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     cursor.execute("SELECT D_ID, D_name FROM Drugs")
#     drugs = cursor.fetchall()

#     drug_dict = {d[1]: d[0] for d in drugs}
#     drug_name = st.selectbox("Select Drug", list(drug_dict.keys()))
#     quantity = st.number_input("Enter Quantity", min_value=1, step=1)

#     if st.button("Place Order"):
#         drug_id = drug_dict[drug_name]
#         cursor.execute(
#             "INSERT INTO Orders (C_ID, Qty, Name, Item) VALUES (%s, %s, %s, %s)",
#             (st.session_state.user_id, quantity, f"Order for {drug_name}", drug_name)
#         )
#         conn.commit()
#         st.success("Successfully placed order!")

#     cursor.close()
#     conn.close()

# # Function to View Orders (Customer)
# def view_orders():
#     if not st.session_state.logged_in or st.session_state.user_type != "Customer":
#         st.error("You must be logged in as a customer!")
#         return

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     cursor.execute("SELECT Order_ID, Qty, Name, Item FROM Orders WHERE C_ID = %s", (st.session_state.user_id,))
#     orders = cursor.fetchall()

#     if orders:
#         df = pd.DataFrame(orders, columns=["Order ID", "Quantity", "Order Name", "Item"])
#         st.subheader("Your Orders:")
#         st.table(df)
#     else:
#         st.info("No orders found.")

#     cursor.close()
#     conn.close()

# # Function to View Inventory (Manager)
# def view_inventory():
#     if not st.session_state.logged_in or st.session_state.user_type != "Manager":
#         st.error("You must be logged in as a manager!")
#         return

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     cursor.execute("SELECT D_ID, Rem_qty FROM Inventory")
#     inventory = cursor.fetchall()

#     if inventory:
#         df = pd.DataFrame(inventory, columns=["Drug ID", "Remaining Quantity"])
#         st.subheader("Inventory Status:")
#         st.table(df)

#     cursor.close()
#     conn.close()

# # Function to View Sales Report (Manager)
# def view_sales():
#     if not st.session_state.logged_in or st.session_state.user_type != "Manager":
#         st.error("You must be logged in as a manager!")
#         return

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     cursor.execute("SELECT Sale_ID, Total_amt, Date, Time FROM Sales")
#     sales = cursor.fetchall()

#     if sales:
#         df = pd.DataFrame(sales, columns=["Sale ID", "Total Amount", "Date", "Time"])
#         st.subheader("Sales Report")
#         st.table(df)

#     cursor.close()
#     conn.close()
# # Function to Manage Suppliers (Manager)
# def manage_suppliers():
#     if not st.session_state.logged_in or st.session_state.user_type != "Manager":
#         st.error("You must be logged in as a manager!")
#         return

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     # Display Current Suppliers
#     cursor.execute("SELECT S_ID, S_name, S_address, S_phone FROM Supplier")
#     suppliers = cursor.fetchall()

#     if suppliers:
#         df = pd.DataFrame(suppliers, columns=["Supplier ID", "Name", "Address", "Phone"])
#         st.subheader("Manage Suppliers")
#         st.table(df)

#     action = st.selectbox("Choose Action", ["Add", "Update", "Delete"])

#     if action == "Add":
#         s_name = st.text_input("Supplier Name")
#         s_address = st.text_input("Supplier Address")
#         s_phone = st.text_input("Supplier Phone")

#         if st.button("Add Supplier"):
#             cursor.execute("INSERT INTO Supplier (S_name, S_address, S_phone) VALUES (%s, %s, %s)",
#                            (s_name, s_address, s_phone))
#             conn.commit()
#             st.success("Supplier added successfully!")

#     elif action == "Update":
#         supplier_id = st.number_input("Enter Supplier ID to Update", min_value=1, step=1)
#         cursor.execute("SELECT S_name, S_address, S_phone FROM Supplier WHERE S_ID = %s", (supplier_id,))
#         supplier = cursor.fetchone()
#         if supplier:
#             current_name, current_address, current_phone = supplier
#             new_name = st.text_input("New Name (Leave blank to keep current)", value=current_name)
#             new_address = st.text_input("New Address (Leave blank to keep current)", value=current_address)
#             new_phone = st.text_input("New Phone (Leave blank to keep current)", value=current_phone)
            
#             if st.button("Update Supplier"):
#                 update_fields = []
#                 values = []
                
#                 if new_name and new_name != current_name:
#                     update_fields.append("S_name = %s")
#                     values.append(new_name)
                
#                 if new_address and new_address != current_address:
#                     update_fields.append("S_address = %s")
#                     values.append(new_address)
                
#                 if new_phone and new_phone != current_phone:
#                     update_fields.append("S_phone = %s")
#                     values.append(new_phone)
#                 if update_fields:
#                     query = f"UPDATE Supplier SET {', '.join(update_fields)} WHERE S_ID = %s"
#                     values.append(supplier_id)
                    
#                     cursor.execute(query, tuple(values))
#                     conn.commit()
#                     st.success("Supplier updated successfully!")
#             else:
#                 st.info("No changes were made.")

#     else:
#         st.warning("Supplier ID not found.")

#     cursor.close()
#     conn.close()


# # Chatbot Functions
# def chat_with_gemini(user_input):
#     st.session_state.chat_history.append(("User", user_input))
    
#     # Get AI response
#     response = model.generate_content(user_input)
#     bot_reply = response.text if response.text else "Sorry, I couldn't process that."
    
#     st.session_state.chat_history.append(("Gemini", bot_reply))
#     return bot_reply

# # Streamlit Chatbot UI
# def chatbot_ui():
#     st.title("💬 Virtual Pharmacy Assistant")

#     # Display chat history
#     for role, message in st.session_state.chat_history:
#         with st.chat_message(role):
#             st.write(message)

#     # User Input
#     user_input = st.chat_input("Ask me anything...")
#     if user_input:
#         bot_reply = chat_with_gemini(user_input)
#         with st.chat_message("User"):
#             st.write(user_input)
#         with st.chat_message("Gemini"):
#             st.write(bot_reply)

# # Main Application UI
# def main():
#     st.title("Pharmacy Management System")

#     menu = st.sidebar.radio("Select Page", ["Home", "Chatbot"])

#     if menu == "Home":
#         if not st.session_state.logged_in:
#             option = st.radio("Choose an option:", ["Login", "Signup"])

#             if option == "Login":
#                 st.subheader("Login")
#                 user_type = st.radio("Login as:", ["Customer", "Manager"])
#                 username = st.text_input("Enter your Email (Customer) or Name (Manager)")
#                 password = st.text_input("Enter your Password", type="password")

#                 if st.button("Login"):
#                     login_user(username, password, user_type)

#             elif option == "Signup":
#                 st.subheader("Signup - New Customer")
#                 email = st.text_input("Email")
#                 password = st.text_input("Password", type="password")
#                 name = st.text_input("Full Name")
#                 age = st.number_input("Age", min_value=1, step=1)  # Added Age field
#                 sex = st.selectbox("Sex", ["Male", "Female", "Other"])  # Added Sex field
#                 phone = st.text_input("Phone Number")
#                 address = st.text_area("Address")

#                 if st.button("Signup"):
#                     if email and password and name and address:
#                         signup_user(email, password, name, age, sex, phone, address)
#                     else:
#                         st.error("All fields except phone number are required!")
#         else:
#             if st.session_state.user_type == "Customer":
#                 st.subheader("Welcome, Customer!")
#                 choice = st.selectbox("Choose an option:", ["Place Order", "View Orders"])

#                 if choice == "Place Order":
#                     place_order()
#                 elif choice == "View Orders":
#                     view_orders()

#             elif st.session_state.user_type == "Manager":
#                 st.subheader("Welcome, Manager!")
#                 choice = st.selectbox("Choose an option:", ["View Inventory", "Manage Suppliers", "See Sales"])

#                 if choice == "View Inventory":
#                     view_inventory()
#                 elif choice == "Manage Suppliers":
#                     manage_suppliers()
#                 elif choice == "See Sales":
#                     view_sales()

#             if st.button("Logout"):
#                 st.session_state.logged_in = False
#                 st.session_state.user_type = None
#                 st.session_state.user_id = None
#                 st.success("You have been logged out. Please refresh the page.")

#     elif menu == "Chatbot":
#         chatbot_ui()

# if __name__ == "__main__":
#     main()



import streamlit as st
import mysql.connector
import pandas as pd  # Import Pandas for proper table formatting
import google.generativeai as genai

# Database Connection Function
def get_db_connection():
    return mysql.connector.connect(
        host='localhost', user='root', password='Shreya@123', database='PharmacyManagement'
    )

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_type = None  # 'Customer' or 'Manager'
    st.session_state.user_id = None    # Stores the user ID

import streamlit as st
import mysql.connector
import pandas as pd
import google.generativeai as genai

# Database Connection Function
def get_db_connection():
    return mysql.connector.connect(
        host='localhost', user='root', password='Shreya@123', database='PharmacyManagement'
    )

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_type = None  
    st.session_state.user_id = None    
    st.session_state.language = "English"  # Default language

# Language Selection
language_options = {
    "English": {
        "title":"Pharmacy Management system",
        "login": "Login",
        "signup": "Signup",
        "welcome": "Welcome",
        "place_order": "Place Order",
        "view_orders": "View Orders",
        "home": "Home",
        "chatbot": "Chatbot",
        "select_page": "Select Page",
        "enter_email": "Enter your Email (Customer) or Name (Manager)",
        "enter_password": "Enter your Password",
        "login_as": "Login as",
        "customer": "Customer",
        "manager": "Manager",
        "signup_new": "Signup - New Customer",
        "full_name": "Full Name",
        "age": "Age",
        "sex": "Sex",
        "phone": "Phone Number",
        "address": "Address",
        "submit": "Submit",
        "invalid_credentials": "Invalid credentials. Please try again."
    },
    "Kannada": {
        "title":"ಫಾರ್ಮಸಿ ನಿರ್ವಹಣಾ ವ್ಯವಸ್ಥೆ",
        "login": "ಲಾಗಿನ್",
        "signup": "ನೋಂದಣಿ",
        "welcome": "ಸ್ವಾಗತ",
        "place_order": "ಆರ್ಡರ್ ಮಾಡು",
        "view_orders": "ಆರ್ಡರ್‌ಗಳನ್ನು ವೀಕ್ಷಿಸಿ",
        "home": "ಮುಖಪುಟ",
        "chatbot": "ಚಾಟ್‌ಬಾಟ್",
        "select_page": "ಪುಟವನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "enter_email": "ನಿಮ್ಮ ಇಮೇಲ್ (ಗ್ರಾಹಕರು) ಅಥವಾ ಹೆಸರು (ಮ್ಯಾನೇಜರ್) ನಮೂದಿಸಿ",
        "enter_password": "ನಿಮ್ಮ ಗುಪ್ತಪದವನ್ನು ನಮೂದಿಸಿ",
        "login_as": "ಹೀಗೆ ಲಾಗಿನ್ ಆಗಿ",
        "customer": "ಗ್ರಾಹಕ",
        "manager": "ಮ್ಯಾನೇಜರ್",
        "signup_new": "ಹೊಸ ಗ್ರಾಹಕರ ನೋಂದಣಿ",
        "full_name": "ಪೂರ್ಣ ಹೆಸರು",
        "age": "ವಯಸ್ಸು",
        "sex": "ಲಿಂಗ",
        "phone": "ದೂರವಾಣಿ ಸಂಖ್ಯೆ",
        "address": "ವಿಳಾಸ",
        "submit": "ಸಲ್ಲಿಸು",
        "invalid_credentials": "ಅಮಾನ್ಯವಾದ ದಾಖಲಾತಿಗಳು. ದಯವಿಟ್ಟು ಮತ್ತೊಮ್ಮೆ ಪ್ರಯತ್ನಿಸಿ."
    }
}

# UI - Language Selection
st.sidebar.title("🌍 Language")
st.session_state.language = st.sidebar.selectbox("Choose Language", ["English", "Kannada"])

# Get translations based on selected language
L = language_options[st.session_state.language]

# Configure Gemini API
API_KEY = "AIzaSyDCy142-54gqPVp_svs9M_0y4zayUZpSoY"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Initialize chat history for the chatbot
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Pharmacy Management Functions
def signup_user(email, password, name, age, sex, phone, address):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if email already exists
    cursor.execute("SELECT C_ID FROM Customer WHERE EmailID = %s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        st.error("Email already registered. Please log in instead.")
    else:
        # Insert into Customer table
        cursor.execute(
            "INSERT INTO Customer (C_name, Age, Sex, Address, Pwd, EmailID) VALUES (%s, %s, %s, %s, %s, %s)",
            (name, age, sex, address, password, email)
        )
        conn.commit()

        # Get the newly created Customer ID
        cursor.execute("SELECT C_ID FROM Customer WHERE EmailID = %s", (email,))
        customer_id = cursor.fetchone()[0]

        # Insert into CustomerPhone table ONLY IF phone number is provided
        if phone.strip():  # Ensures non-empty phone
            cursor.execute(
                "INSERT INTO CustomerPhone (C_ID, Ph_no) VALUES (%s, %s)",
                (customer_id, phone)
            )
            conn.commit()

        st.success("Signup successful! You can now log in.")

    cursor.close()
    conn.close()

# Login Function
def login_user(username, password, user_type):
    conn = get_db_connection()
    cursor = conn.cursor()

    if user_type == "Customer":
        query = "SELECT C_ID FROM Customer WHERE EmailID = %s AND Pwd = %s"
    else:
        query = "SELECT M_ID FROM Manager WHERE M_name = %s AND M_pwd = %s"

    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result:
        st.session_state.logged_in = True
        st.session_state.user_type = user_type
        st.session_state.user_id = result[0]
        st.success(f"Logged in as {user_type}!")
    else:
        st.error("Invalid credentials. Please try again.")

    cursor.close()
    conn.close()

# Function to Place Order (Customer)
def place_order():
    if not st.session_state.logged_in or st.session_state.user_type != "Customer":
        st.error("You must be logged in as a customer!")
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT D_ID, D_name FROM Drugs")
    drugs = cursor.fetchall()

    drug_dict = {d[1]: d[0] for d in drugs}
    drug_name = st.selectbox("Select Drug", list(drug_dict.keys()))
    quantity = st.number_input("Enter Quantity", min_value=1, step=1)

    if st.button("Place Order"):
        drug_id = drug_dict[drug_name]
        cursor.execute(
            "INSERT INTO Orders (C_ID, Qty, Name, Item) VALUES (%s, %s, %s, %s)",
            (st.session_state.user_id, quantity, f"Order for {drug_name}", drug_name)
        )
        conn.commit()
        st.success("Successfully placed order!")

    cursor.close()
    conn.close()

# Function to View Orders (Customer)
def view_orders():
    if not st.session_state.logged_in or st.session_state.user_type != "Customer":
        st.error("You must be logged in as a customer!")
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT Order_ID, Qty, Name, Item FROM Orders WHERE C_ID = %s", (st.session_state.user_id,))
    orders = cursor.fetchall()

    if orders:
        df = pd.DataFrame(orders, columns=["Order ID", "Quantity", "Order Name", "Item"])
        st.subheader("Your Orders:")
        st.table(df)
    else:
        st.info("No orders found.")

    cursor.close()
    conn.close()

# Function to View Inventory (Manager)
def view_inventory():
    if not st.session_state.logged_in or st.session_state.user_type != "Manager":
        st.error("You must be logged in as a manager!")
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT D_ID, Rem_qty FROM Inventory")
    inventory = cursor.fetchall()

    if inventory:
        df = pd.DataFrame(inventory, columns=["Drug ID", "Remaining Quantity"])
        st.subheader("Inventory Status:")
        st.table(df)

    cursor.close()
    conn.close()

# Function to View Sales Report (Manager)
def view_sales():
    if not st.session_state.logged_in or st.session_state.user_type != "Manager":
        st.error("You must be logged in as a manager!")
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT Sale_ID, Total_amt, Date, Time FROM Sales")
    sales = cursor.fetchall()

    if sales:
        df = pd.DataFrame(sales, columns=["Sale ID", "Total Amount", "Date", "Time"])
        st.subheader("Sales Report")
        st.table(df)

    cursor.close()
    conn.close()
# Function to Manage Suppliers (Manager)
def manage_suppliers():
    if not st.session_state.logged_in or st.session_state.user_type != "Manager":
        st.error("You must be logged in as a manager!")
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    # Display Current Suppliers
    cursor.execute("SELECT S_ID, S_name, S_address, S_phone FROM Supplier")
    suppliers = cursor.fetchall()

    if suppliers:
        df = pd.DataFrame(suppliers, columns=["Supplier ID", "Name", "Address", "Phone"])
        st.subheader("Manage Suppliers")
        st.table(df)

    action = st.selectbox("Choose Action", ["Add", "Update", "Delete"])

    if action == "Add":
        s_name = st.text_input("Supplier Name")
        s_address = st.text_input("Supplier Address")
        s_phone = st.text_input("Supplier Phone")

        if st.button("Add Supplier"):
            cursor.execute("INSERT INTO Supplier (S_name, S_address, S_phone) VALUES (%s, %s, %s)",
                           (s_name, s_address, s_phone))
            conn.commit()
            st.success("Supplier added successfully!")

    elif action == "Update":
        supplier_id = st.number_input("Enter Supplier ID to Update", min_value=1, step=1)
        cursor.execute("SELECT S_name, S_address, S_phone FROM Supplier WHERE S_ID = %s", (supplier_id,))
        supplier = cursor.fetchone()
        if supplier:
            current_name, current_address, current_phone = supplier
            new_name = st.text_input("New Name (Leave blank to keep current)", value=current_name)
            new_address = st.text_input("New Address (Leave blank to keep current)", value=current_address)
            new_phone = st.text_input("New Phone (Leave blank to keep current)", value=current_phone)
            
            if st.button("Update Supplier"):
                update_fields = []
                values = []
                
                if new_name and new_name != current_name:
                    update_fields.append("S_name = %s")
                    values.append(new_name)
                
                if new_address and new_address != current_address:
                    update_fields.append("S_address = %s")
                    values.append(new_address)
                
                if new_phone and new_phone != current_phone:
                    update_fields.append("S_phone = %s")
                    values.append(new_phone)
                if update_fields:
                    query = f"UPDATE Supplier SET {', '.join(update_fields)} WHERE S_ID = %s"
                    values.append(supplier_id)
                    
                    cursor.execute(query, tuple(values))
                    conn.commit()
                    st.success("Supplier updated successfully!")
            else:
                st.info("No changes were made.")

    else:
        st.warning("Supplier ID not found.")

    cursor.close()
    conn.close()


# Chatbot Functions
def chat_with_gemini(user_input):
    st.session_state.chat_history.append(("User", user_input))
    
    # Get AI response
    response = model.generate_content(user_input)
    bot_reply = response.text if response.text else "Sorry, I couldn't process that."
    
    st.session_state.chat_history.append(("Gemini", bot_reply))
    return bot_reply

# Streamlit Chatbot UI
def chatbot_ui():
    st.title("💬 Virtual Pharmacy Assistant")

    # Display chat history
    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(message)

    # User Input
    user_input = st.chat_input("Ask me anything...")
    if user_input:
        bot_reply = chat_with_gemini(user_input)
        with st.chat_message("User"):
            st.write(user_input)
        with st.chat_message("Gemini"):
            st.write(bot_reply)


# Main Application UI
def main():
    title_text = {
        "English": "Pharmacy Management System",
        "Kannada": "ಫಾರ್ಮಸಿ ನಿರ್ವಹಣಾ ವ್ಯವಸ್ಥೆ"
    }
    st.title(title_text[st.session_state.language])

    menu = st.sidebar.radio(L["select_page"], [L["home"], L["chatbot"]])

    if menu == L["home"]:
        if not st.session_state.logged_in:
            option = st.radio("Choose an option:", [L["login"], L["signup"]])

            if option == L["login"]:
                st.subheader(L["login"])
                user_type = st.radio(L["login_as"], [L["customer"], L["manager"]])
                username = st.text_input(L["enter_email"])
                password = st.text_input(L["enter_password"], type="password")

                if st.button(L["login"]):
                    login_user(username, password, "Customer" if user_type == L["customer"] else "Manager")

            elif option == L["signup"]:
                st.subheader(L["signup_new"])
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                name = st.text_input(L["full_name"])
                age = st.number_input(L["age"], min_value=1, step=1)
                sex = st.selectbox(L["sex"], ["Male", "Female", "Other"])
                phone = st.text_input(L["phone"])
                address = st.text_area(L["address"])

                if st.button(L["submit"]):
                    if email and password and name and address:
                        signup_user(email, password, name, age, sex, phone, address)
                    else:
                        st.error("All fields except phone number are required!")

        else:
            if st.session_state.user_type == "Customer":
                st.subheader(f"{L['welcome']}, {L['customer']}!")
                choice = st.selectbox("Choose an option:", [L["place_order"], L["view_orders"]])

                if choice == L["place_order"]:
                    place_order()
                elif choice == L["view_orders"]:
                    view_orders()

            elif st.session_state.user_type == "Manager":
                st.subheader(f"{L['welcome']}, {L['manager']}!")

if __name__ == "__main__":
    main()