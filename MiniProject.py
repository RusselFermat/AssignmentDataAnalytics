import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(
    page_title="Undergraduate Employability Dashboard (as of February 2025)", 
    page_icon="🎓", 
    layout="wide"
)

# Animation
st.markdown("""
<style>
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animated-element {
        animation: fadeInUp 0.6s ease-out forwards;
        opacity: 0;
    }
    
    /* Delay animations for staggered effect */
    .stContainer > div:nth-child(1) { animation-delay: 0.1s; }
    .stContainer > div:nth-child(2) { animation-delay: 0.2s; }
    .stContainer > div:nth-child(3) { animation-delay: 0.3s; }
    .stContainer > div:nth-child(4) { animation-delay: 0.4s; }
    .stContainer > div:nth-child(5) { animation-delay: 0.5s; }
    
    /* Sidebar animations */
    .stSidebar > div:nth-child(1) { animation: fadeInUp 0.6s ease-out 0.1s forwards; opacity: 0; }
    .stSidebar > div:nth-child(2) { animation: fadeInUp 0.6s ease-out 0.2s forwards; opacity: 0; }
    
    /* Make sure containers are visible */
    .stApp, .stSidebar { visibility: visible !important; }
</style>
""", unsafe_allow_html=True)

# Load data function with caching
@st.cache_data
def load_data():
    # Load data from CSV file
    df = pd.read_csv('careerdata.csv')
    
    # Data cleaning and preprocessing
    if 'Starting_Salary' in df.columns:
        df['Starting_Salary'] = pd.to_numeric(df['Starting_Salary'], errors='coerce')
    if 'University_GPA' in df.columns:
        df['University_GPA'] = pd.to_numeric(df['University_GPA'], errors='coerce')
    
    return df

df = load_data()

# Sidebar layout
st.sidebar.header("")  # Empty header for spacing

# Add logo at the top (replace with your image path or URL)
st.sidebar.image("Logo.png", 
                 width=200, 
                 use_container_width=True) 
st.sidebar.header("Filter Data")

# Dynamic field selection based on available data
available_fields = df['Field_of_Study'].unique() if 'Field_of_Study' in df.columns else []
selected_fields = st.sidebar.multiselect(
    "Select Fields of Study",
    options=available_fields,
    default=available_fields[:min(3, len(available_fields))] if len(available_fields) > 0 else []
)

# GPA filter (if column exists)
if 'University_GPA' in df.columns:
    gpa_range = st.sidebar.slider(
        "University GPA Range",
        min_value=float(df['University_GPA'].min()),
        max_value=float(df['University_GPA'].max()),
        value=(float(df['University_GPA'].min()), float(df['University_GPA'].max()))
    )
else:
    gpa_range = (0, 4)  # Default range if column doesn't exist

# Salary filter (if column exists)
if 'Starting_Salary' in df.columns:
    salary_range = st.sidebar.slider(
        "Starting Salary Range ($)",
        min_value=int(df['Starting_Salary'].min()),
        max_value=int(df['Starting_Salary'].max()),
        value=(int(df['Starting_Salary'].min()), int(df['Starting_Salary'].max()))
    )
else:
    salary_range = (0, 100000)  # Default range if column doesn't exist

# Gender filter (if column exists)
if 'Gender' in df.columns:
    gender_options = ['All'] + list(df['Gender'].unique())
    gender_filter = st.sidebar.radio(
        "Gender",
        options=gender_options,
        index=0
    )
else:
    gender_filter = 'All'

# Add copyright at the bottom
st.sidebar.markdown("---")  # Horizontal line separator
st.sidebar.markdown("""
<style>
    .copyright {
        font-size: 0.8em;
        color: #666;
        text-align: center;
        margin-top: 20px;
    }
</style>
<div class='copyright'>
    © 2025 RusselJay Corporation<br>
    All Rights Reserved
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<script>
    // Animate sidebar elements
    setTimeout(function(){
        const sidebar = parent.document.querySelectorAll('[data-testid="stSidebar"] > div');
        sidebar.forEach((el, i) => {
            el.style.animation = `fadeInUp 0.6s ease-out ${i * 0.1}s forwards`;
            el.style.opacity = 0;
        });
    }, 100);
</script>
""", unsafe_allow_html=True)


# Apply filters
filtered_df = df.copy()

if len(selected_fields) > 0 and 'Field_of_Study' in df.columns:
    filtered_df = filtered_df[filtered_df['Field_of_Study'].isin(selected_fields)]

if 'University_GPA' in df.columns:
    filtered_df = filtered_df[
        (filtered_df['University_GPA'] >= gpa_range[0]) &
        (filtered_df['University_GPA'] <= gpa_range[1])
    ]

if 'Starting_Salary' in df.columns:
    filtered_df = filtered_df[
        (filtered_df['Starting_Salary'] >= salary_range[0]) &
        (filtered_df['Starting_Salary'] <= salary_range[1])
    ]

if gender_filter != 'All' and 'Gender' in df.columns:
    filtered_df = filtered_df[filtered_df['Gender'] == gender_filter]

with st.container():
    # Main content
    st.title("🎓 Undergraduate Employability in the US (as of February 2025)")
    st.markdown("Analyzing the relationship between academic performance, field of study, and employment outcomes")

    # KPI cards
    st.subheader("Key Performance Indicators")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if 'University_GPA' in filtered_df.columns:
            st.metric("Average CGPA", f"{filtered_df['University_GPA'].mean():.2f}")
        else:
            st.metric("Average CGPA", "N/A")

    with col2:
        if 'Starting_Salary' in filtered_df.columns:
            st.metric("Average Salary", f"${filtered_df['Starting_Salary'].mean():,.0f}")
        else:
            st.metric("Average Salary", "N/A")

    with col3:
        if 'Job_Offers' in filtered_df.columns:
            st.metric("Total Job Offers", filtered_df['Job_Offers'].sum())
        else:
            st.metric("Total Job Offers", "N/A")

    with col4:
        if 'Internships_Completed' in filtered_df.columns:
            st.metric("Total Internships", filtered_df['Internships_Completed'].sum())
        else:
            st.metric("Total Internships", "N/A")

    with col5:
        if 'Projects_Completed' in filtered_df.columns:
            st.metric("Total Projects", filtered_df['Projects_Completed'].sum())
        else:
            st.metric("Total Projects", "N/A")

    # Charts Section
    st.subheader("Data Visualizations")

    tab1, tab2, tab3, tab4 = st.tabs([" 🗂️Field Study Impact", " 🗂️GPA Influence on Job", " 🗂️Gender Disparities", " 🗂️Internship ROI"])

    with tab1:

        st.subheader("Objective 1: Analyze Field-of-Study Impact on Career Outcomes")
        st.text("")
        # First Row of Charts
        col1, col2 = st.columns(2)

        with col1:
            if 'Field_of_Study' in filtered_df.columns:
                st.markdown("#### Percentage of Courses Majored in US")
                field_counts = filtered_df['Field_of_Study'].value_counts()
                fig = px.pie(field_counts, 
                            values=field_counts.values, 
                            names=field_counts.index,
                            hole=0.3)
                st.plotly_chart(fig, use_container_width=True)
                with st.expander("📌 Interpretation Guide", expanded=False):
                    st.markdown("""
                    **What this shows:**  
                    • Relative popularity of different fields among graduates  
                    **How to use it:**  
                    • Larger slices = More common majors  
                    • Compare STEM vs Humanities proportions  
                    **Pro Tip:**  
                    • Click slices to isolate specific fields  
                    """)
            else:
                st.warning("Field_of_Study column not found in data")

        with col2:
            if 'Field_of_Study' in filtered_df.columns and 'Starting_Salary' in filtered_df.columns:
                st.markdown("#### Annual Starting Salary by Field")
                fig = px.box(filtered_df, 
                            x='Field_of_Study', 
                            y='Starting_Salary',
                            color='Field_of_Study')
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
                with st.expander("💰 Salary Insights", expanded=False):
                    st.markdown("""
                    **Key Elements:**  
                    • Box width = Salary range for middle 50% of graduates  
                    • Line = Median salary  
                    • Dots = Exceptional cases  
                    **Actionable Takeaways:**  
                    • Fields with taller boxes have wider salary ranges  
                    • Compare STEM vs Business medians  
                    """)
            else:
                st.warning("Required columns for salary analysis not found")

    with tab2:

        st.subheader("Objective 2: Quantify GPA's Influence on Job Acquisition")
        st.text("")
        # Second Row of Charts
        col1, col2 = st.columns(2)

        with col1:
                if 'University_GPA' in filtered_df.columns and 'Job_Offers' in filtered_df.columns:
                    st.markdown("#### GPA Distribution by Number of Job Offers")
                    
                    # Convert Job_Offers to categorical for better grouping
                    filtered_df['Job_Offers_Cat'] = filtered_df['Job_Offers'].astype(str) + " Offer(s)"
                    
                    #Violin plot 
                    fig = px.violin(
                        filtered_df,
                        x='Job_Offers_Cat',
                        y='University_GPA',
                        color='Job_Offers_Cat',
                        box=True,  # Show box plot inside violin
                        title="GPA Distribution by Job Offers"
                    )
                    
                    fig.update_layout(
                        xaxis_title="Number of Job Offers",
                        yaxis_title="University GPA",
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    with st.expander("🎓 GPA vs Offers Guide", expanded=False):
                        st.markdown("""
                        **Violin Plot Features:**  
                        • Width = Density of students at each GPA level  
                        • Inner box = Traditional boxplot statistics  
                        **Career Insights:**  
                        • Thicker sections = Common GPA ranges for each offer count   
                        • Narrow violins = Consistent GPA patterns  
                        • Wide bases = Diverse academic performance  
                        """)
                else:
                    st.warning("Required columns for GPA vs Job Offers analysis not found")

        with col2:
            if 'SAT_Score' in filtered_df.columns:
                st.markdown("#### SAT Score Distribution")
                fig = px.histogram(filtered_df, 
                                x='SAT_Score', 
                                nbins=20,
                                color='Field_of_Study' if 'Field_of_Study' in filtered_df.columns else None)
                st.plotly_chart(fig, use_container_width=True)
                with st.expander("📝 SAT Analysis Notes", expanded=False):
                    st.markdown("""
                    **Patterns to Observe:**  
                    • Left skew = Most students scored high  
                    • Right skew = Many had test-taking challenges  
                    **Admissions Context:**  
                    • Compare peaks between fields  
                    • 1200-1400 = Typical competitive range  
                    **Correlation Check:**  
                    • Filter high SAT scores to see if GPA/salary increases  
                    """)
            else:
                st.warning("SAT_Score column not found in data")

    with tab3:

        st.subheader("Objective 3: Evaluate Gender Disparities in Employment")
        st.text("")
        # Third Row of Charts - Replacements
        col1, col2 = st.columns(2)

        with col1:
            if 'Field_of_Study' in filtered_df.columns and 'Starting_Salary' in filtered_df.columns:
                st.markdown("#### Average Salary by Field of Study")
                avg_salary = filtered_df.groupby('Field_of_Study')['Starting_Salary'].mean().sort_values()
                fig = px.bar(avg_salary, 
                            x=avg_salary.values, 
                            y=avg_salary.index,
                            orientation='h',
                            color=avg_salary.values,
                            color_continuous_scale='Blues',
                            title='Average Starting Salary by Field')
                fig.update_layout(yaxis_title="Field of Study", xaxis_title="Average Salary ($)")
                st.plotly_chart(fig, use_container_width=True)
                with st.expander("💸 Salary Benchmarking", expanded=False):
                    st.markdown("""
                    **Horizontal Bars Show:**  
                    • Exact average salaries per field  
                    • Color intensity = Higher salaries  
                    **Strategic Insights:**  
                    • Longest bars = Most lucrative fields  
                    • Compare adjacent fields (e.g., CS vs Engineering)  
                    **Caveat:**  
                    • Averages can hide entry-level vs senior pay differences  
                    """)
            else:
                st.warning("Required columns for salary analysis not found")

        with col2:
            if 'University_GPA' in filtered_df.columns and 'Starting_Salary' in filtered_df.columns:
                st.markdown("#### GPA vs Salary Correlation")
                fig = px.scatter(filtered_df,
                                x='University_GPA',
                                y='Starting_Salary',
                                color='Field_of_Study' if 'Field_of_Study' in filtered_df.columns else None,
                                trendline="ols",
                                marginal_x="histogram",
                                marginal_y="histogram")
                fig.update_layout(xaxis_title="University GPA", yaxis_title="Starting Salary ($)")
                st.plotly_chart(fig, use_container_width=True)
                with st.expander("📈 Trend Analysis", expanded=False):
                    st.markdown("""
                    **Key Components:**  
                    • Dots = Individual graduates  
                    • Trendline = Overall relationship  
                    • Side histograms = Distribution of each variable  
                    **Career Implications:**  
                    • Steep trend = GPA strongly affects starting pay  
                    • Flat trend = Other factors dominate  
                    **Field Differences:**  
                    • Compare color clusters (different majors)  
                    """)
            else:
                st.warning("Required columns for GPA vs Salary analysis not found")

    with tab4:

        st.subheader("Objective 4: Measure Internship ROI")
        st.text("")
        # Fourth Row of Charts
        col1, col2 = st.columns(2)

        with col1:
            if 'Internships_Completed' in filtered_df.columns and 'Field_of_Study' in filtered_df.columns:
                st.markdown("#### Internship Completion by Field")
                internship_counts = filtered_df.groupby(['Field_of_Study', 'Internships_Completed']).size().reset_index(name='Count')
                fig = px.bar(internship_counts,
                            x='Field_of_Study',
                            y='Count',
                            color='Internships_Completed',
                            barmode='group',
                            title='Internship Completion Count by Field')
                fig.update_layout(xaxis_title="Field of Study", yaxis_title="Number of Students")
                st.plotly_chart(fig, use_container_width=True)
                with st.expander("🛠️ Experience Matters", expanded=False):
                    st.markdown("""
                    **Grouped Bars Reveal:**  
                    • Internship participation rates per field  
                    • Stack height = Total students in each field  
                    **Career Preparation Insights:**  
                    • Fields with more 2+ internship students = Strong industry pipelines  
                    • Low internship fields may rely on academic projects  
                    **Action Item:**  
                    • Compare with salary/job offer charts  
                    """)
            else:
                st.warning("Required columns for internship analysis not found")

        with col2:
            if 'Employment_Status' in filtered_df.columns:
                st.markdown("#### Employment Status Distribution")
                status_counts = filtered_df['Employment_Status'].value_counts()
                fig = px.pie(status_counts,
                            values=status_counts.values,
                            names=status_counts.index,
                            hole=0.4,
                            title='Current Employment Status of Graduates')
                st.plotly_chart(fig, use_container_width=True)
            elif 'Job_Offers' in filtered_df.columns:
                st.markdown("#### Job Offer Distribution")
                fig = px.histogram(filtered_df,
                                x='Job_Offers',
                                nbins=10,
                                color='Field_of_Study' if 'Field_of_Study' in filtered_df.columns else None,
                                title='Distribution of Job Offers Received')
                st.plotly_chart(fig, use_container_width=True)
                with st.expander("🏆 Outcomes Breakdown", expanded=False):
                    st.markdown("""
                    **Pie Chart Shows:**  
                    • Immediate post-graduation outcomes  
                    **Critical Metrics:**  
                    • Full-Time % = Quick employment rate  
                    • Unemployed % = Potential issues  
                    **Deep Dive:**  
                    • Filter by field to see which majors struggle  
                    • Compare with internship participation  
                    """)
            else:
                st.warning("No employment-related columns found in data")

    # Raw data view
    st.subheader("Filtered Data Preview")
    st.dataframe(filtered_df.head(100), height=300)

    # Add some explanatory text
    st.markdown("""
    ### Insights:
    - Explore how different fields of study compare in terms of employment outcomes
    - Filter data using the sidebar to focus on specific student groups
    - Hover over charts for detailed information
    - Missing visualizations indicate required columns not found in the data
    """)

    # Add download button for filtered data
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download filtered data as CSV",
        data=csv,
        file_name="filtered_employability_data.csv",
        mime="text/csv"
    )