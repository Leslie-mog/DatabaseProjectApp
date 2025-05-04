import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import datetime

# Set page configuration
st.set_page_config(
    page_title="Influencer Marketing Platform",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database connection function

def get_connection():
    return mysql.connector.connect(
        host=st.secrets["hopper.proxy.rlwy.net"],
        user=st.secrets["root"],
        password=st.secrets["vMHbTeQprGSHYsklwTXAefCfMVnCcSWr"],
        database=st.secrets["railway"],
        port=st.secrets["13734"]
    )

def execute_query(query, params=None, fetch=True):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            result = cursor.fetchall()
            return result
        else:
            conn.commit()
            return cursor.rowcount
    except Exception as e:
        st.error(f"Database error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

# Apply custom CSS
def apply_custom_css():
    st.markdown("""
    <style>
        .main {
            background-color: #f5f7fd;
        }
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .dashboard-card {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .header-style {
            background-color: #4a69bd;
            color: white;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .metric-card {
            background-color: #ffffff;
            border-left: 5px solid #4a69bd;
            padding: 15px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .form-container {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .nav-link {
            background-color: #f8f9fa;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 5px;
            text-align: center;
            cursor: pointer;
        }
        .nav-link:hover {
            background-color: #e9ecef;
        }
        .nav-link-active {
            background-color: #4a69bd;
            color: white;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 5px;
            text-align: center;
        }
        div[data-testid="stVerticalBlock"] div[style*="flex-direction: column;"] div[data-testid="stVerticalBlock"] {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            margin-bottom: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

apply_custom_css()

# Sidebar navigation
with st.sidebar:
    
    st.title("Influencer Marketing Platform")
    
    # Navigation options
    nav_options = [
        "Dashboard", 
        "Influencers", 
        "Brands", 
        "Database Queries"
    ]
    
    # Navigation icons (emojis instead of icon library)
    nav_icons = {
        "Dashboard": "🏠", 
        "Influencers": "👤", 
        "Brands": "🏢", 
        "Database Queries": "🗃️"
    }
    
    # Create selection
    selected = st.session_state.get("selected_page", "Dashboard")
    
    for nav_option in nav_options:
        if st.sidebar.button(
            f"{nav_icons.get(nav_option, '')} {nav_option}",
            key=f"nav_{nav_option}",
            help=f"Navigate to {nav_option}",
            use_container_width=True,
            type="primary" if selected == nav_option else "secondary"
        ):
            selected = nav_option
            st.session_state["selected_page"] = selected
            st.rerun()

# Dashboard
if selected == "Dashboard":
    st.markdown("<div class='header-style'><h1>Dashboard</h1></div>", unsafe_allow_html=True)
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    # Count influencers
    influencer_count = execute_query("SELECT COUNT(*) as count FROM INFLUENCER")[0]['count']
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Total Influencers", influencer_count)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Count brands
    brand_count = execute_query("SELECT COUNT(*) as count FROM BRAND")[0]['count']
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Total Brands", brand_count)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Count applications
    app_count = execute_query("SELECT COUNT(*) as count FROM APPLICATION")[0]['count']
    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Total Applications", app_count)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Count campaigns
    campaign_count = execute_query("SELECT COUNT(*) as count FROM CAMPAIGN")[0]['count']
    with col4:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Total Campaigns", campaign_count)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Charts row
    st.markdown("### Key Insights")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("Applications by Status")
        
        # Get application status data
        app_status = execute_query("SELECT ApplicationStatus, COUNT(*) as count FROM APPLICATION GROUP BY ApplicationStatus")
        if app_status:
            df_app_status = pd.DataFrame(app_status)
            fig = px.pie(df_app_status, names='ApplicationStatus', values='count', 
                         color_discrete_sequence=px.colors.qualitative.Set3,
                         hole=0.4)
            fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("Influencers by Industry")
        
        # Get influencer industry data
        inf_industry = execute_query("SELECT Industry, COUNT(*) as count FROM INFLUENCER GROUP BY Industry")
        if inf_industry:
            df_inf_industry = pd.DataFrame(inf_industry)
            fig = px.bar(df_inf_industry, x='Industry', y='count', 
                         color='Industry', 
                         color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.update_layout(xaxis_title="", yaxis_title="Count", margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Recent applications and upcoming campaigns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("Recent Applications")
        recent_apps = execute_query("""
            SELECT a.Date_Applied, a.ApplicationStatus, a.BID_Amount, i.InfluencerName 
            FROM APPLICATION a
            LEFT JOIN INFLUENCER i ON a.ApplicationID = i.ApplicationID
            ORDER BY a.Date_Applied DESC LIMIT 5
        """)
        if recent_apps:
            st.dataframe(pd.DataFrame(recent_apps), hide_index=True, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("Active Campaigns")
        active_campaigns = execute_query("""
            SELECT CampaignStatus, StartDate, EndDate
            FROM CAMPAIGN
            WHERE CampaignStatus = 'Active'
            ORDER BY StartDate
        """)
        if active_campaigns:
            st.dataframe(pd.DataFrame(active_campaigns), hide_index=True, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

elif selected == "Influencers":
    st.markdown("<div class='header-style'><h1>Influencers Management</h1></div>", unsafe_allow_html=True)
    tabs = ["View Influencers", "Add/Update Influencer"]
    influencer_tab = st.radio("", tabs, horizontal=True)
    
    if influencer_tab == "View Influencers":
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        influencers = execute_query("SELECT * FROM INFLUENCER")
        if influencers:
            st.dataframe(pd.DataFrame(influencers), hide_index=True, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    elif influencer_tab == "Add/Update Influencer":
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        st.subheader("Add/Update Influencer")
        
        # Get existing IDs for update dropdown
        existing_ids = [i['InfluencerID'] for i in execute_query("SELECT InfluencerID FROM INFLUENCER")]
        update_mode = st.checkbox("Update Existing Influencer")
        
        if update_mode and existing_ids:
            influencer_id = st.selectbox("Select Influencer to Update", existing_ids)
            current_data = execute_query("SELECT * FROM INFLUENCER WHERE InfluencerID = %s", (influencer_id,))[0]
        else:
            influencer_id = None
            current_data = {"InfluencerName": "", "Age": 25, "Gender": "Female", "Industry": "", "Handle": "", "Field": ""}
        
        # Form fields
        name = st.text_input("Influencer Name", value=current_data.get("InfluencerName", ""))
        age = st.number_input("Age", min_value=18, max_value=100, value=current_data.get("Age", 25))
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(current_data.get("Gender", "Female")) if current_data.get("Gender") in ["Male", "Female", "Other"] else 0)
        
        # Get industries from database for dropdown
        industries = [i['Industryname'] for i in execute_query("SELECT Industryname FROM INDUSTRY")]
        industry = st.selectbox("Industry", industries, index=industries.index(current_data.get("Industry", "")) if current_data.get("Industry") in industries else 0)
        
        handle = st.text_input("Social Media Handle", value=current_data.get("Handle", ""))
        field = st.text_input("Field/Specialty", value=current_data.get("Field", ""))
        
        # Get application IDs from database for dropdown
        applications = execute_query("SELECT ApplicationID FROM APPLICATION")
        app_ids = [a['ApplicationID'] for a in applications]
        app_id = st.selectbox("Application ID", app_ids)
        
        if st.button("Save Influencer"):
            if update_mode and influencer_id:
                # Update existing record
                update_query = """
                UPDATE INFLUENCER
                SET InfluencerName = %s, Age = %s, Gender = %s, Industry = %s, Handle = %s, Field = %s, ApplicationID = %s
                WHERE InfluencerID = %s
                """
                params = (name, age, gender, industry, handle, field, app_id, influencer_id)
                rows_affected = execute_query(update_query, params, fetch=False)
                if rows_affected:
                    st.success(f"Influencer ID {influencer_id} updated successfully!")
                else:
                    st.error("Failed to update influencer.")
            else:
                # Insert new record
                insert_query = """
                INSERT INTO INFLUENCER (InfluencerName, Age, Gender, Industry, Handle, Field, ApplicationID)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                params = (name, age, gender, industry, handle, field, app_id)
                rows_affected = execute_query(insert_query, params, fetch=False)
                if rows_affected:
                    st.success("New influencer added successfully!")
                else:
                    st.error("Failed to add influencer.")
        
        st.markdown("</div>", unsafe_allow_html=True)

elif selected == "Brands":
    st.markdown("<div class='header-style'><h1>Brands Management</h1></div>", unsafe_allow_html=True)
    
    tabs = ["View Brands", "Add/Update Brand"]
    brand_tab = st.radio("", tabs, horizontal=True)
    
    if brand_tab == "View Brands":
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        brands = execute_query("SELECT * FROM BRAND")
        if brands:
            df_brands = pd.DataFrame(brands)
            st.dataframe(df_brands, hide_index=True, use_container_width=True)
            
            # Bar chart showing brand packages
            st.subheader("Brand Pay Packages")
            fig = px.bar(df_brands, x='Brandname', y='PayPackage', 
                         color='PayPackage',
                         color_continuous_scale='Viridis',
                         labels={'PayPackage': 'Pay Package (USD)', 'Brandname': 'Brand Name'})
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    elif brand_tab == "Add/Update Brand":
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        st.subheader("Add/Update Brand")
        
        # Get existing IDs for update dropdown
        existing_ids = [b['BrandID'] for b in execute_query("SELECT BrandID FROM BRAND")]
        update_mode = st.checkbox("Update Existing Brand")
        
        if update_mode and existing_ids:
            brand_id = st.selectbox("Select Brand to Update", existing_ids)
            current_data = execute_query("SELECT * FROM BRAND WHERE BrandID = %s", (brand_id,))[0]
        else:
            brand_id = None
            current_data = {"Brandname": "", "PayPackage": 10000.00}
        
        # Form fields
        name = st.text_input("Brand Name", value=current_data.get("Brandname", ""))
        pay_package = st.number_input("Pay Package (USD)", 
                                      min_value=1000.00, 
                                      max_value=100000.00, 
                                      value=float(current_data.get("PayPackage", 10000.00)),
                                      step=500.00)
        
        if st.button("Save Brand"):
            if update_mode and brand_id:
                # Update existing record
                update_query = """
                UPDATE BRAND
                SET Brandname = %s, PayPackage = %s
                WHERE BrandID = %s
                """
                params = (name, pay_package, brand_id)
                rows_affected = execute_query(update_query, params, fetch=False)
                if rows_affected:
                    st.success(f"Brand ID {brand_id} updated successfully!")
                else:
                    st.error("Failed to update brand.")
            else:
                # Insert new record
                insert_query = """
                INSERT INTO BRAND (Brandname, PayPackage)
                VALUES (%s, %s)
                """
                params = (name, pay_package)
                rows_affected = execute_query(insert_query, params, fetch=False)
                if rows_affected:
                    st.success("New brand added successfully!")
                else:
                    st.error("Failed to add brand.")
        
        st.markdown("</div>", unsafe_allow_html=True)
elif selected == "Database Queries":
    st.markdown("<div class='header-style'><h1>Database Queries</h1></div>", unsafe_allow_html=True)
    
    # Predefined analytical queries
    QUERIES = [
        {
            "title": "Top 10 Influencers by Highest Bid Amount",
            "sql": """
                SELECT i.InfluencerName, a.BID_Amount 
                FROM APPLICATION a
                JOIN INFLUENCER i ON a.ApplicationID = i.ApplicationID
                ORDER BY a.BID_Amount DESC 
                LIMIT 10
            """,
            "visualization": "bar"
        },
        {
            "title": "Brand Spending Distribution",
            "sql": """
                SELECT b.Brandname, SUM(b.PayPackage) AS TotalSpent 
                FROM BRAND b
    
                GROUP BY b.Brandname
            """,
            "visualization": "pie"
        },
        {
             "title": "Campaign Performance Analysis",
                "sql": """
                    SELECT 
                        c.CampaignStatus,
                        COUNT(a.ApplicationID) AS Applications,
                        AVG(a.BID_Amount) AS AvgBid
                    FROM CAMPAIGN c
                    LEFT JOIN INFLUENCER_CAMPAIGN ic ON c.CampaignID = ic.CampaignID
                    LEFT JOIN INFLUENCER i ON ic.InfluencerID = i.InfluencerID
                    LEFT JOIN APPLICATION a ON i.ApplicationID = a.ApplicationID
                    GROUP BY c.CampaignStatus
                """,
                "visualization": "table"
        },
        {
            "title": "Industry Engagement Statistics",
            "sql": """
                SELECT i.Industry, 
                       COUNT(a.ApplicationID) AS TotalApplications,
                       MAX(a.BID_Amount) AS HighestBid,
                       AVG(a.BID_Amount) AS AvgBid
                FROM INFLUENCER i
                JOIN APPLICATION a ON i.ApplicationID = a.ApplicationID
                GROUP BY i.Industry
            """,
            "visualization": "bar"
        },
        {
            "title": "Active Campaign Timeline",
            "sql": """
                SELECT CampaignID, StartDate, EndDate 
                FROM CAMPAIGN
                WHERE CampaignStatus = 'Active'
                ORDER BY StartDate
            """,
            "visualization": "timeline"
        },
        {
            "title": "Application Status Distribution",
            "sql": """
                SELECT ApplicationStatus, 
                       COUNT(*) AS Count,
                       ROUND(COUNT(*)/(SELECT COUNT(*) FROM APPLICATION)*100,2) AS Percentage
                FROM APPLICATION
                GROUP BY ApplicationStatus
            """,
            "visualization": "pie"
        },
        {
            "title": "Brand-Influencer Matches with Diagnostics",
    "sql": """
        SELECT 
            b.Brandname,
            i.InfluencerName,
            a.BID_Amount,
            a.ApplicationStatus,
            CASE 
                WHEN ba.ApplicationID IS NULL THEN 'No Brand Match'
                ELSE 'Matched'
            END AS BrandMatchStatus
        FROM APPLICATION a
        JOIN INFLUENCER i ON a.ApplicationID = i.ApplicationID
        LEFT JOIN BRAND_APPLICATION ba ON a.ApplicationID = ba.ApplicationID
        LEFT JOIN BRAND b ON ba.BrandID = b.BrandID
        WHERE a.ApplicationStatus IN ('Approved', 'Pending', 'Rejected')
        ORDER BY a.ApplicationStatus DESC
    """,
    "visualization": "table"
        }
    ]

    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    
    # Query selection and parameters
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_query = st.selectbox("Select Query", [q["title"] for q in QUERIES])
    
    with col2:
        st.write("")  # Spacer
        st.write("")  # Spacer
        execute_btn = st.button("🚀 Execute Query", use_container_width=True)
    
    # Get selected query details
    query_data = next(q for q in QUERIES if q["title"] == selected_query)
    
    # Dynamic parameter input
    query_params = st.text_area("Query Parameters (if needed)", 
                              help="Enter parameters as comma-separated values if required by the query")
    
    if execute_btn:
        try:
            # Execute query
            start_time = datetime.datetime.now()
            results = execute_query(query_data["sql"])
            execution_time = (datetime.datetime.now() - start_time).total_seconds()
            
            if results:
                df = pd.DataFrame(results)
                
                # Display metrics
                st.success(f"Fetched {len(df)} rows in {execution_time:.2f} seconds")
                
                # Visualization logic
                if query_data["visualization"] == "bar":
                    fig = px.bar(df, x=df.columns[0], y=df.columns[1], 
                               color=df.columns[0], 
                               title=f"{selected_query} Visualization")
                    st.plotly_chart(fig, use_container_width=True)
                
                elif query_data["visualization"] == "pie":
                    fig = px.pie(df, names=df.columns[0], values=df.columns[1],
                               title=f"{selected_query} Distribution")
                    st.plotly_chart(fig, use_container_width=True)
                
                elif query_data["visualization"] == "timeline":
                    fig = px.timeline(df, x_start="StartDate", x_end="EndDate", y="CampaignID",
                                    title="Campaign Timeline")
                    fig.update_yaxes(autorange="reversed")
                    st.plotly_chart(fig, use_container_width=True)
                
                # Show data table for all visualizations
                st.subheader("Raw Data Preview")
                st.dataframe(df, hide_index=True, use_container_width=True)
                
                # Add export options
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Export as CSV",
                    data=csv,
                    file_name=f"query_results_{datetime.datetime.now().strftime('%Y%m%d')}.csv",
                    mime='text/csv'
                )
            else:
                st.warning("No results found for this query")
                
        except Exception as e:
            st.error(f"Query execution failed: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)
