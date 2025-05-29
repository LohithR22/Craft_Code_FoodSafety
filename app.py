import os
import streamlit as st
from login_system import login_user, signup_user, user_exists
from employee import employee_page  # Your existing employee page code
from manager import manager_page  # Your existing manager page code

# Check if auditing.db exists, and if not, run setup_db.py
def check_and_setup_db():
    if not os.path.exists('auditing.db'):
        st.info("Setting up the database for the first time...")
        # Execute setup_db.py by importing and running it
        import setup_db  # This runs the setup_db.py script automatically

# Call the function to check the database
check_and_setup_db()

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

# Function to handle role selection and reload the page when changed
def select_role():
    if not st.session_state.logged_in:
        st.subheader("Select Your Role")

        # Display "Select a role" option only if a role has not been selected
        role_options = ["Employee", "Manager"]
        if 'role' not in st.session_state or st.session_state.role == "":
            selected_role = st.selectbox("Choose your role", ["Select a role"] + role_options, key="role_selection")
            if selected_role != "Select a role":
                st.session_state.role = selected_role
                st.rerun()  # Reload the page after role selection

# Function to reset the role selection (change role)
def change_role():
    st.session_state.role = ""  # Reset the role selection
    st.rerun()

# Function to handle signing out
def signout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.rerun()

def main():
    st.title("Food Safety Auditing System")

    # Role selection is mandatory before showing login or signup forms
    if 'role' not in st.session_state or st.session_state.role == "":
        select_role()  # Show role selection first
    else:
        # Show the "Change Role" button only if the user is NOT logged in
        if not st.session_state.logged_in:
            if st.button("Change Role"):
                change_role()  # Reset the role selection

        # Show login/signup forms only if the user is not logged in
        if not st.session_state.logged_in:
            st.subheader(f"{st.session_state.role} Login")
            option = st.radio("Login or Sign up", ["Login", "Sign Up"])

            if option == "Login":
                login_form(st.session_state.role)
            else:
                signup_form(st.session_state.role)
        else:
            # Show the dashboard if logged in
            st.success(f"Welcome {st.session_state.username}")
            
            # Sign Out button
            if st.button("Sign Out"):
                signout()  # Reset session state and rerun the page
            
            # Call Manager or Employee page based on the role
            if st.session_state.role == "Manager":
                manager_page()  # Manager's Dashboard with list of issues
            elif st.session_state.role == "Employee":
                employee_page()  # Employee's page to create an issue

# Login form function
def login_form(role):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = user[1]
            st.session_state.role = user[3]
            st.success(f"Logged in as {user[1]} ({user[3]})")
            st.rerun()
        else:
            st.error("Invalid username or password")

# Signup form function
def signup_form(role):
    username = st.text_input("Choose a username")
    password = st.text_input("Choose a password", type="password")
    confirm_password = st.text_input("Confirm your password", type="password")

    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match")
        elif user_exists(username):
            st.error("Username already exists. Please Login")
        else:
            if signup_user(username, password, role):
                st.success(f"{role} account created successfully! You can now login.")
            else:
                st.error("Error creating account. Try again.")

if __name__ == "__main__":
    main()
