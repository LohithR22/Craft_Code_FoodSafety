import streamlit as st
import sqlite3
from PIL import Image
from io import BytesIO
from gemini_solution import get_solution_from_gemini


def manager_page():
    st.header("Manager Dashboard")

    # Fetch complaints from database
    issues = get_issues()

    # Check if there are any issues to display
    if issues:
        for issue_id, issue_type, image, description in issues:
            with st.container():
                st.subheader(f"Issue Type: {issue_type}")
                st.image(Image.open(BytesIO(image)), caption="Uploaded Image", use_column_width=True)
                st.write(f"Description: {description}")

                # Clear Issue Button placed before the AI suggestion
                clear_button = st.button(f"Clear Issue {issue_id}", key=f"clear_{issue_id}")
                
                if clear_button:
                    clear_issue(issue_id)
                    st.success(f"Issue {issue_id} cleared!")
                    st.rerun()

                # Show AI suggestion only if the issue hasn't been cleared
                solution = get_solution_from_gemini(image)
                if solution:
                    st.write(f"AI Suggested Solution: {solution}")
                else:
                    st.write("Failed to get AI suggested solution.")
    else:
        st.write("No issues have been raised yet.")

# Function to fetch issues from the database
def get_issues():
    conn = sqlite3.connect('auditing.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, issue_type, image, description FROM issues")
    return cursor.fetchall()

# Function to clear issues from the database
def clear_issue(issue_id):
    conn = sqlite3.connect('auditing.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM issues WHERE id = ?", (issue_id,))
    conn.commit()
    conn.close()