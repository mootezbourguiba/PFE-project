"""
User Management Page

This module provides the user management interface for administrators.
"""

import streamlit as st
import pandas as pd
from utils.auth import require_administrator, init_session_state
from components.sidebar import render_sidebar
from components.header import render_header
from utils.api import get_users, create_user, update_user, disable_user, enable_user


def show() -> None:
    """
    Display the user management page.
    """
    # Initialize session state and require authentication
    init_session_state()
    require_administrator()
    
    # Page configuration
    st.set_page_config(
        page_title="User Management",
        page_icon="👥",
        layout="wide"
    )
    
    # Custom CSS for dark avionics theme
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0D1B2A 0%, #1E3A5F 100%);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Render sidebar
    render_sidebar()
    
    # Render header
    render_header("User Management")
    
    # Tabs for different operations
    tab1, tab2, tab3 = st.tabs(["📋 View Users", "➕ Create User", "✏️ Edit User"])
    
    # Tab 1: View Users
    with tab1:
        st.markdown("### All Users")
        
        # Search and filter
        col1, col2 = st.columns(2)
        with col1:
            search = st.text_input("🔍 Search users", placeholder="Search by username or email")
        with col2:
            role_filter = st.selectbox("🎭 Filter by role", ["All", "administrator", "maintenance_engineer", "drone_operator"])
        
        # Fetch users
        users = get_users()
        
        if users:
            users_df = pd.DataFrame(users)
            
            # Apply filters
            if search:
                users_df = users_df[
                    users_df['username'].str.contains(search, case=False) |
                    users_df['email'].str.contains(search, case=False)
                ]
            
            if role_filter != "All":
                users_df = users_df[users_df['role'] == role_filter]
            
            # Display users table
            if not users_df.empty:
                display_df = users_df[['id', 'username', 'email', 'role', 'disabled', 'created_at']].copy()
                display_df.columns = ['ID', 'Username', 'Email', 'Role', 'Disabled', 'Created At']
                display_df['Disabled'] = display_df['Disabled'].apply(lambda x: '❌ Yes' if x else '✅ No')
                display_df['Role'] = display_df['Role'].replace({
                    'administrator': '👤 Administrator',
                    'maintenance_engineer': '🔧 Maintenance Engineer',
                    'drone_operator': '🚁 Drone Operator'
                })
                
                st.dataframe(display_df, use_container_width=True)
            else:
                st.info("No users match your search criteria.")
        else:
            st.info("No users found in the system.")
    
    # Tab 2: Create User
    with tab2:
        st.markdown("### Create New User")
        
        with st.form("create_user_form"):
            username = st.text_input("Username", placeholder="Enter username")
            email = st.text_input("Email", placeholder="Enter email address")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm password")
            role = st.selectbox("Role", ["maintenance_engineer", "drone_operator", "administrator"])
            
            submitted = st.form_submit_button("Create User", type="primary")
            
            if submitted:
                if not username or not email or not password:
                    st.error("Please fill in all required fields.")
                elif password != confirm_password:
                    st.error("Passwords do not match.")
                elif len(password) < 8:
                    st.error("Password must be at least 8 characters long.")
                else:
                    with st.spinner("Creating user..."):
                        result = create_user(username, email, password, role)
                        if result:
                            st.success(f"User '{username}' created successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to create user. Username or email may already exist.")
    
    # Tab 3: Edit User
    with tab3:
        st.markdown("### Edit User")
        
        users = get_users()
        
        if users:
            user_options = {f"{u['username']} ({u['email']})": u['id'] for u in users}
            selected_user = st.selectbox("Select user to edit", list(user_options.keys()))
            
            if selected_user:
                user_id = user_options[selected_user]
                user = next((u for u in users if u['id'] == user_id), None)
                
                if user:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### User Information")
                        st.info(f"**Username:** {user['username']}")
                        st.info(f"**Email:** {user['email']}")
                        st.info(f"**Role:** {user['role']}")
                        st.info(f"**Status:** {'Disabled' if user['disabled'] else 'Active'}")
                    
                    with col2:
                        st.markdown("#### Actions")
                        
                        # Update user form
                        with st.form("update_user_form"):
                            new_email = st.text_input("New Email", value=user['email'])
                            new_role = st.selectbox("New Role", ["administrator", "maintenance_engineer", "drone_operator"], 
                                                   index=["administrator", "maintenance_engineer", "drone_operator"].index(user['role']))
                            
                            update_submitted = st.form_submit_button("Update User")
                            
                            if update_submitted:
                                with st.spinner("Updating user..."):
                                    result = update_user(user_id, email=new_email, role=new_role)
                                    if result:
                                        st.success("User updated successfully!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to update user.")
                        
                        # Disable/Enable user
                        st.markdown("---")
                        
                        if not user['disabled']:
                            if st.button("🔒 Disable User", type="secondary"):
                                reason = st.text_input("Reason for disabling", placeholder="Enter reason")
                                if st.button("Confirm Disable", type="primary"):
                                    with st.spinner("Disabling user..."):
                                        result = disable_user(user_id, disabled=True, reason=reason)
                                        if result:
                                            st.success("User disabled successfully!")
                                            st.rerun()
                                        else:
                                            st.error("Failed to disable user.")
                        else:
                            if st.button("🔓 Enable User", type="primary"):
                                with st.spinner("Enabling user..."):
                                    result = enable_user(user_id)
                                    if result:
                                        st.success("User enabled successfully!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to enable user.")
        else:
            st.info("No users found in the system.")
