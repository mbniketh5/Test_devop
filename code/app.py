import streamlit as st
import sqlite3
import bcrypt

# Database Connection
conn = sqlite3.connect('database.db', check_same_thread=False)
c = conn.cursor()

# Create Table
c.execute('''
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    email TEXT UNIQUE,
    password TEXT,
    department TEXT
)
''')
conn.commit()

# Password Hashing
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

# App Configuration
st.set_page_config(
    page_title="DevOps_Test Organization",
    page_icon="🚀",
    layout="wide"
)

# Header
st.title("🚀 DevOps_Test Organization")
st.markdown("### Employee Registration Portal")

menu = ["Register", "Login"]
choice = st.sidebar.selectbox("Menu", menu)

# Registration Page
if choice == "Register":
    st.subheader("Employee Registration Form")

    with st.form("registration_form"):
        full_name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        department = st.selectbox(
            "Department",
            ["DevOps", "Cloud", "Development", "QA", "Security"]
        )
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        submit = st.form_submit_button("Register")

        if submit:
            if password != confirm_password:
                st.error("Passwords do not match!")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters.")
            else:
                try:
                    hashed_pw = hash_password(password)

                    c.execute(
                        '''
                        INSERT INTO users
                        (full_name,email,password,department)
                        VALUES(?,?,?,?)
                        ''',
                        (
                            full_name,
                            email,
                            hashed_pw,
                            department
                        )
                    )

                    conn.commit()
                    st.success("Registration Successful!")
                except sqlite3.IntegrityError:
                    st.error("Email already exists.")

# Login Page
elif choice == "Login":
    st.subheader("Employee Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        c.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        user = c.fetchone()

        if user:
            stored_password = user[3]

            if verify_password(password, stored_password):
                st.success(f"Welcome {user[1]}")

                st.markdown("---")
                st.subheader("Employee Dashboard")

                col1, col2 = st.columns(2)

                with col1:
                    st.info(f"Name: {user[1]}")
                    st.info(f"Email: {user[2]}")

                with col2:
                    st.info(f"Department: {user[4]}")
                    st.info(f"Employee ID: {user[0]}")

            else:
                st.error("Invalid Password")
        else:
            st.error("User Not Found")