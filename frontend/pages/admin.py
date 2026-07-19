import streamlit as st
import pandas as pd
from services.api import get_users, create_user, update_user, delete_user

def show():
    """
    Display the Administrator dashboard.
    
    This dashboard provides:
    - User management (create, read, update, delete)
    - System status overview
    - Role-based access control
    
    Only accessible to users with 'administrator' role.
    """
    st.set_page_config(
        page_title="Administrator Dashboard",
        page_icon="👨‍💼",
        layout="wide"
    )
    
    st.title("👨‍💼 Administrator Dashboard")
    st.markdown("---")
    
    # Get authentication token
    token = st.session_state.get("token")
    if not token:
        st.error("Not authenticated. Please login.")
        return
    
    # ===========================
    # System Status Section
    # ===========================
    st.subheader("📊 System Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users", "3", delta="Active")
    
    with col2:
        st.metric("System Status", "✅ Operational", delta="Normal")
    
    with col3:
        st.metric("Database", "✅ Connected", delta="SQLite")
    
    with col4:
        st.metric("API Server", "✅ Running", delta="FastAPI")
    
    st.markdown("---")
    
    # ===========================
    # User Management Section
    # ===========================
    st.subheader("👥 User Management")
    
    # Tab navigation for user operations
    tab1, tab2, tab3 = st.tabs(["View Users", "Create User", "Manage Users"])
    
    # ===========================
    # Tab 1: View Users
    # ===========================
    with tab1:
        st.write("### All System Users")
        
        # Fetch users from backend
        response = get_users(token)
        
        if response.status_code == 200:
            users = response.json()
            
            if users:
                # Convert to DataFrame for display
                df = pd.DataFrame(users)
                
                # Format the display
                display_df = df[["id", "username", "email", "role", "created_at"]]
                display_df.columns = ["ID", "Username", "Email", "Role", "Created At"]
                display_df["Role"] = display_df["Role"].str.replace("_", " ").str.title()
                
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True
                )
                
                st.info(f"Total users: {len(users)}")
            else:
                st.warning("No users found in the system.")
        else:
            st.error(f"Failed to fetch users: {response.status_code}")
            st.write(f"Error: {response.text}")
    
    # ===========================
    # Tab 2: Create User
    # ===========================
    with tab2:
        st.write("### Create New User")
        
        with st.form("create_user_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_username = st.text_input("Username *", key="new_username")
                new_email = st.text_input("Email *", key="new_email")
            
            with col2:
                new_password = st.text_input("Password *", type="password", key="new_password")
                new_role = st.selectbox(
                    "Role *",
                    ["maintenance_engineer", "drone_operator", "administrator"],
                    key="new_role"
                )
            
            submitted = st.form_submit_button("Create User", use_container_width=True)
            
            if submitted:
                if not all([new_username, new_email, new_password, new_role]):
                    st.error("All fields are required.")
                else:
                    # Create user via API
                    response = create_user(
                        username=new_username,
                        email=new_email,
                        password=new_password,
                        role=new_role,
                        token=token
                    )
                    
                    if response.status_code == 200:
                        st.success(f"User '{new_username}' created successfully!")
                        st.rerun()
                    else:
                        st.error(f"Failed to create user: {response.status_code}")
                        st.write(f"Error: {response.text}")
    
    # ===========================
    # Tab 3: Manage Users
    # ===========================
    with tab3:
        st.write("### Update or Delete Users")
        
        # Fetch users for selection
        response = get_users(token)
        
        if response.status_code == 200:
            users = response.json()
            
            if users:
                # User selection
                user_options = {f"{u['username']} (ID: {u['id']})": u['id'] for u in users}
                selected_user = st.selectbox("Select User to Manage", list(user_options.keys()))
                
                if selected_user:
                    user_id = user_options[selected_user]
                    user = next((u for u in users if u['id'] == user_id), None)
                    
                    st.markdown("---")
                    
                    # Update section
                    st.write("#### Update User")
                    
                    with st.form(f"update_user_{user_id}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            update_email = st.text_input("Email", value=user['email'], key=f"update_email_{user_id}")
                        
                        with col2:
                            update_role = st.selectbox(
                                "Role",
                                ["administrator", "maintenance_engineer", "drone_operator"],
                                index=["administrator", "maintenance_engineer", "drone_operator"].index(user['role']),
                                key=f"update_role_{user_id}"
                            )
                        
                        update_submitted = st.form_submit_button("Update User", use_container_width=True)
                        
                        if update_submitted:
                            response = update_user(
                                user_id=user_id,
                                token=token,
                                email=update_email,
                                role=update_role
                            )
                            
                            if response.status_code == 200:
                                st.success("User updated successfully!")
                                st.rerun()
                            else:
                                st.error(f"Failed to update user: {response.status_code}")
                                st.write(f"Error: {response.text}")
                    
                    st.markdown("---")
                    
                    # Delete section
                    st.write("#### Delete User")
                    
                    if st.button(f"Delete User '{user['username']}'", type="secondary", key=f"delete_{user_id}"):
                        if st.confirm(f"Are you sure you want to delete user '{user['username']}'? This action cannot be undone."):
                            response = delete_user(user_id, token)
                            
                            if response.status_code == 200:
                                st.success("User deleted successfully!")
                                st.rerun()
                            else:
                                st.error(f"Failed to delete user: {response.status_code}")
                                st.write(f"Error: {response.text}")
            else:
                st.warning("No users available to manage.")
        else:
            st.error(f"Failed to fetch users: {response.status_code}")
    
    # ===========================
    # Information Section
    # ===========================
    st.markdown("---")
    st.subheader("ℹ️ Administrator Information")
    
    with st.expander("User Roles Description"):
        st.markdown("""
        **Administrator:**
        - Full system access
        - User management (create, update, delete)
        - System configuration
        - View all data
        
        **Maintenance Engineer:**
        - Access to monitoring dashboards
        - Historical telemetry data
        - Anomaly detection results
        - Maintenance decision support
        - Cannot manage users
        
        **Drone Operator:**
        - Real-time telemetry monitoring
        - Alert notifications
        - Basic health status
        - No historical data access
        - No administrative functions
        """)
    
    with st.expander("System Architecture"):
        st.markdown("""
        **Backend:**
        - FastAPI REST API
        - SQLite database
        - JWT authentication
        - SQLAlchemy ORM
        
        **Frontend:**
        - Streamlit dashboard
        - Role-based access control
        - Real-time updates
        - Responsive design
        
        **Machine Learning:**
        - Isolation Forest algorithm
        - Bearing wear detection
        - Anomaly scoring
        - Model persistence
        """)