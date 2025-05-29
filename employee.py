import streamlit as st
from PIL import Image
import sqlite3

def employee_page():
    st.header("Employee Dashboard")

    # Issue type selection
    issue_type = st.radio("Select the type of issue:", ["Food Related Issues(Eg: Packaging Mistake, Wrong Labeling, Spills or Breakage of Container,etc.)", "Issue related to Equipment, Appliances (Cooking equipment, utensils, etc.)"])

    # Image upload
    uploaded_file = st.file_uploader("Upload an image related to the issue", type=["jpg", "jpeg", "png"])

    # Description input
    issue_description = st.text_area("Describe the issue briefly")

    # Submit button
    if st.button("Submit Issue"):
        if uploaded_file is not None and issue_description:
            save_issue(issue_type, uploaded_file, issue_description)
            st.success(f"{issue_type} submitted successfully!")
        else:
            st.error("Please upload an image and write a description.")

# Function to save issue data in the database
def save_issue(issue_type, image, description):
    conn = sqlite3.connect('auditing.db')
    cursor = conn.cursor()

    # Convert image to binary
    image_bytes = image.read()

    # Insert issue into database
    cursor.execute(
        '''INSERT INTO issues (issue_type, image, description) VALUES (?, ?, ?)''',
        (issue_type, image_bytes, description)
    )
    conn.commit()
    conn.close()
