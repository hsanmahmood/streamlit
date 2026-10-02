import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="TaskFlow Pro",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom CSS (Properly escaped for Streamlit markdown)
# ---------------------------------------------------------
st.markdown(r"""
    <style>
        /* Modern Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.05);
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 4px;
        }
        
        /* Task Cards Layout */
        .task-card {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        }
        .task-high {
            border-left: 5px solid #ff4b4b;
        }
        .task-medium {
            border-left: 5px solid #ffa100;
        }
        .task-low {
            border-left: 5px solid #00c853;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {
            "id": 1,
            "title": "Design App Architecture",
            "category": "Work",
            "priority": "High",
            "due_date": datetime.date.today(),
            "status": "In Progress"
        },
        {
            "id": 2,
            "title": "Buy Groceries for the week",
            "category": "Personal",
            "priority": "Low",
            "due_date": datetime.date.today() + datetime.timedelta(days=1),
            "status": "Pending"
        },
        {
            "id": 3,
            "title": "30-min Evening Run",
            "category": "Health",
            "priority": "Medium",
            "due_date": datetime.date.today(),
            "status": "Completed"
        }
    ]

if "next_id" not in st.session_state:
    st.session_state.next_id = 4

# Helper function to delete task
def delete_task(task_id):
    st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != task_id]

# Helper function to update task status
def update_status(task_id, new_status):
    for task in st.session_state.tasks:
        if task["id"] == task_id:
            task["status"] = new_status
            break

# ---------------------------------------------------------
# Sidebar Header & Add Task Form
# ---------------------------------------------------------
with st.sidebar:
    st.title("📌 Task Manager")
    st.caption("Organize your work and life efficiently.")
    
    st.divider()
    st.subheader("➕ Add New Task")
    
    with st.form("add_task_form", clear_on_submit=True):
        new_title = st.text_input("Task Title", placeholder="e.g. Finish quarterly report")
        new_category = st.selectbox("Category", ["Work", "Personal", "Health", "Finance", "Other"])
        new_priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        new_due_date = st.date_input("Due Date", value=datetime.date.today())
        
        submitted = st.form_submit_button("Add Task", use_container_width=True)
        if submitted:
            if new_title.strip() == "":
                st.error("Please enter a task title!")
            else:
                new_task = {
                    "id": st.session_state.next_id,
                    "title": new_title.strip(),
                    "category": new_category,
                    "priority": new_priority,
                    "due_date": new_due_date,
                    "status": "Pending"
                }
                st.session_state.tasks.append(new_task)
                st.session_state.next_id += 1
                st.success("Task added successfully!")
                st.rerun()

    st.divider()
    st.markdown("**Quick Filters**")
    filter_status = st.multiselect(
        "Filter by Status",
        options=["Pending", "In Progress", "Completed"],
        default=["Pending", "In Progress", "Completed"]
    )
    filter_category = st.multiselect(
        "Filter by Category",
        options=["Work", "Personal", "Health", "Finance", "Other"],
        default=["Work", "Personal", "Health", "Finance", "Other"]
    )

# ---------------------------------------------------------
# Main Page Metrics Dashboard
# ---------------------------------------------------------
st.title("✅ TaskFlow Dashboard")

df = pd.DataFrame(st.session_state.tasks)

if not df.empty:
    total_tasks = len(df)
    completed_tasks = len(df[df["status"] == "Completed"])
    in_progress_tasks = len(df[df["status"] == "In Progress"])
    pending_tasks = len(df[df["status"] == "Pending"])
    completion_rate = round((completed_tasks / total_tasks) * 100, 1) if total_tasks > 0 else 0
else:
    total_tasks, completed_tasks, in_progress_tasks, pending_tasks, completion_rate = 0, 0, 0, 0, 0

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Total Tasks", total_tasks)
m2.metric("Pending", pending_tasks)
m3.metric("In Progress", in_progress_tasks)
m4.metric("Completed", completed_tasks)
m5.metric("Completion Rate", f"{completion_rate}%")

st.divider()

# ---------------------------------------------------------
# Task List View & Analytics Tabs
# ---------------------------------------------------------
tab_list, tab_analytics = st.tabs(["📋 Task List", "📊 Analytics"])

with tab_list:
    # Filter tasks based on sidebar controls
    filtered_tasks = [
        t for t in st.session_state.tasks
        if t["status"] in filter_status and t["category"] in filter_category
    ]

    if not filtered_tasks:
        st.info("No tasks found. Try adjusting your filters or add a new task from the sidebar.")
    else:
        for task in filtered_tasks:
            priority_class = f"task-{task['priority'].lower()}"
            
            with st.container():
                col_info, col_status, col_action = st.columns([5, 2, 1])
                
                with col_info:
                    st.markdown(f"### {task['title']}")
                    st.caption(f"📁 Category: **{task['category']}** | 🔥 Priority: **{task['priority']}** | 📅 Due: **{task['due_date']}**")
                
                with col_status:
                    current_idx = ["Pending", "In Progress", "Completed"].index(task["status"])
                    new_st = st.selectbox(
                        "Status",
                        options=["Pending", "In Progress", "Completed"],
                        index=current_idx,
                        key=f"status_{task['id']}"
                    )
                    if new_st != task["status"]:
                        update_status(task["id"], new_st)
                        st.rerun()

                with col_action:
                    st.write("") # Alignment spacing
                    if st.button("🗑️ Delete", key=f"del_{task['id']}", use_container_width=True):
                        delete_task(task["id"])
                        st.rerun()
                
                st.divider()

with tab_analytics:
    if df.empty:
        st.info("Add tasks to view analytics visualization.")
    else:
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("Task Status Distribution")
            status_counts = df["status"].value_counts().reset_index()
            status_counts.columns = ["Status", "Count"]
            fig1 = px.pie(
                status_counts,
                names="Status",
                values="Count",
                color="Status",
                color_discrete_map={
                    "Pending": "#FFA100",
                    "In Progress": "#29B6F6",
                    "Completed": "#66BB6A"
                },
                hole=0.4
            )
            st.plotly_chart(fig1, use_container_width=True)

        with col_chart2:
            st.subheader("Tasks by Category")
            cat_counts = df["category"].value_counts().reset_index()
            cat_counts.columns = ["Category", "Count"]
            fig2 = px.bar(
                cat_counts,
                x="Category",
                y="Count",
                color="Category",
                text="Count"
            )
            st.plotly_chart(fig2, use_container_width=True)
