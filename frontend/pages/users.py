"""
User Management Page Module

This module provides user management functionality for administrators including:
- View all users
- Create new users
- Edit existing users
- Disable/enable users
- Search and filter users
"""

import streamlit as st
import pandas as pd
from frontend.utils.auth import require_administrator, init_session_state, get_role_display_name
from frontend.components.header import render_header
from frontend.components.sidebar import render_sidebar
from frontend.components.cards import alert_card
from frontend.utils.api import get_users, create_user, update_user, disable_user, enable_user


def show() -> None:
    """
    Display the User Management page.
    
    This function renders:
    - User table with search and filters
    - Create user form
    - Edit user form
    - Disable/enable user functionality
    - Status badges
    """
    # Initialize session state and require authentication
    init_session_state()
    require_administrator()
    
    # Page configuration is handled in app.py
    
    # Custom CSS for dark avionics theme
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0d1b2a 0%, #1e3a5f 100%);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Render sidebar and header
    render_sidebar()
    render_header("User Management")
    
    # Tabs for different actions
    tab1, tab2, tab3 = st.tabs(["📋 View Users", "➕ Create User", "✏️ Edit User"])
    
    # Tab 1: View Users
    with tab1:
        st.markdown("### All Users")
        
        # Search and filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_query = st.text_input("🔍 Search", placeholder="Search by username or email")
        
        with col2:
            role_filter = st.selectbox("🎭 Filter by Role", ["All", "Administrator", "Maintenance Engineer", "Drone Operator"])
        
        with col3:
            status_filter = st.selectbox("📊 Filter by Status", ["All", "Active", "Disabled"])
        
        # Load users from backend
        users = get_users()
        
        if users:
            # Convert to DataFrame for display
            df = pd.DataFrame(users)
            
            # Apply filters
            if search_query:
                df = df[df['username'].str.contains(search_query, case=False) | 
                       df['email'].str.contains(search_query, case=False)]
            
            if role_filter != "All":
                df = df[df['role'] == role_filter.lower()]
            
            if status_filter != "All":
                if status_filter == "Active":
                    df = df[df['disabled'] == False]
                else:
                    df = df[df['disabled'] == True]
            
            # Display user table
            if not df.empty:
                # Format data for display
                display_df = df.copy()
                display_df['role'] = display_df['role'].apply(get_role_display_name)
                display_df['status'] = display_df['disabled'].apply(lambda x: "🔴 Disabled" if x else "🟢 Active")
                
                st.dataframe(
                    display_df[['id', 'username', 'email', 'role', 'status', 'created_at']],
                    use_container_width=True,
                    hide_index=True
                )
                
                # User actions
                st.markdown("### User Actions")
                selected_user_id = st.selectbox(
                    "Select User",
                    options=df['id'].tolist(),
                    format_func=lambda x: f"ID: {x} - {df[df['id'] == x]['username'].values[0]}"
                )
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("✏️ Edit User", use_container_width=True):
                        st.session_state.edit_user_id = selected_user_id
                        st.session_state.page = "users"
                        st.rerun()
                
                with col2:
                    if st.button("🔒 Disable User", use_container_width=True):
                        if disable_user(selected_user_id, True, "Disabled by administrator"):
                            st.success("User disabled successfully")
                            st.rerun()
                
                with col3:
                    if st.button("🔓 Enable User", use_container_width=True):
                        if enable_user(selected_user_id):
                            st.success("User enabled successfully")
                            st.rerun()
            else:
                st.info("No users found matching the filters.")
        else:
            alert_card(
                "No Users Found",
                "Unable to load users from the backend. Please check your connection and try again.",
                "error"
            )
    
    # Tab 2: Create User
    with tab2:
        st.markdown("### Create New User")
        
        with st.form("create_user_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_username = st.text_input("Username*", placeholder="Enter username")
                new_email = st.text_input("Email*", placeholder="Enter email address")
            
            with col2:
                new_password = st.text_input("Password*", type="password", placeholder="Enter password")
                new_role = st.selectbox("Role*", ["administrator", "maintenance_engineer", "drone_operator"])
            
            submit_create = st.form_submit_button("Create User", use_container_width=True, type="primary")
            
            if submit_create:
                if not new_username or not new_email or not new_password:
                    st.error("Please fill in all required fields.")
                else:
                    if create_user(new_username, new_email, new_password, new_role):
                        st.success("User created successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to create user. Username or email may already exist.")
    
    # Tab 3: Edit User
    with tab3:
        st.markdown("### Edit User")
        
        # Select user to edit
        users = get_users()
        
        if users:
            user_options = {user['id']: f"{user['username']} ({user['email']})" for user in users}
            selected_id = st.selectbox("Select User to Edit", options=list(user_options.keys()), format_func=lambda x: user_options[x])
            
            selected_user = next((user for user in users if user['id'] == selected_id), None)
            
            if selected_user:
                with st.form("edit_user_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        edit_username = st.text_input("Username", value=selected_user['username'], disabled=True)
                        edit_email = st.text_input("Email", value=selected_user['email'])
                    
                    with col2:
                        edit_role = st.selectbox(
                            "Role",
                            ["administrator", "maintenance_engineer", "drone_operator"],
                            index=["administrator", "maintenance_engineer", "drone_operator"].index(selected_user['role'])
                        )
                    
                    submit_edit = st.form_submit_button("Update User", use_container_width=True, type="primary")
                    
                    if submit_edit:
                        if update_user(selected_id, email=edit_email, role=edit_role):
                            st.success("User updated successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to update user. Email may already be in use.")
        else:
            st.info("No users available to edit.")
