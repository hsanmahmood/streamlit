<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Streamlit Task Manager & Code Viewer</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Chart.js for analytics visualization -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        streamlitRed: '#FF4B4B',
                        streamlitDarkBg: '#0E1117',
                        streamlitDarkSec: '#262730',
                        streamlitLightBg: '#FFFFFF',
                        streamlitLightSec: '#F0F2F6',
                    }
                }
            }
        }
    </script>
    <style>
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.05);
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(150, 150, 150, 0.4);
            border-radius: 4px;
        }
        .code-block {
            font-family: 'Courier New', Courier, monospace;
            tab-size: 4;
        }
    </style>
</head>
<body class="bg-streamlitLightBg dark:bg-streamlitDarkBg text-gray-800 dark:text-gray-100 min-h-screen flex flex-col font-sans transition-colors duration-200">

    <header class="border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-streamlitDarkSec px-6 py-3 flex justify-between items-center shadow-sm">
        <div class="flex items-center space-x-3">
            <div class="w-7 h-7 rounded bg-streamlitRed flex items-center justify-center text-white font-bold text-lg">
                <i class="fa-solid fa-crown text-xs"></i>
            </div>
            <h1 class="text-xl font-bold tracking-tight">TaskFlow Pro <span class="text-xs bg-streamlitRed text-white px-2 py-0.5 rounded-full font-normal">Streamlit App</span></h1>
        </div>
        
        <div class="flex items-center space-x-4">
            <!-- Mode Toggle Tabs -->
            <div class="flex bg-gray-100 dark:bg-gray-800 p-1 rounded-lg border border-gray-200 dark:border-gray-700 text-sm">
                <button id="tab-app-btn" onclick="switchMainTab('app')" class="px-4 py-1.5 rounded-md font-medium bg-white dark:bg-streamlitDarkSec text-streamlitRed shadow-sm transition">
                    <i class="fa-solid fa-desktop mr-1.5"></i>Interactive App UI
                </button>
                <button id="tab-code-btn" onclick="switchMainTab('code')" class="px-4 py-1.5 rounded-md font-medium text-gray-600 dark:text-gray-300 hover:text-streamlitRed transition">
                    <i class="fa-solid fa-code mr-1.5"></i>Python Code (streamlit run)
                </button>
            </div>

            <!-- Dark/Light Mode Switcher -->
            <button id="theme-toggle" onclick="toggleDarkMode()" class="p-2 rounded-lg bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-600 dark:text-gray-300 transition">
                <i id="theme-toggle-icon" class="fa-solid fa-moon"></i>
            </button>
        </div>
    </header>

    <!-- MAIN APP WRAPPER -->
    <div id="main-container" class="flex-1 flex overflow-hidden">

        <aside id="streamlit-sidebar" class="w-80 border-r border-gray-200 dark:border-gray-800 bg-streamlitLightSec dark:bg-streamlitDarkSec p-5 overflow-y-auto flex flex-col justify-between">
            <div class="space-y-6">
                <!-- Sidebar Header -->
                <div class="border-b border-gray-300 dark:border-gray-700 pb-3">
                    <h2 class="font-semibold text-lg text-gray-700 dark:text-gray-200 flex items-center">
                        <i class="fa-solid fa-sliders mr-2 text-streamlitRed"></i> Controls & Filters
                    </h2>
                </div>

                <!-- Add New Task Section -->
                <div class="bg-white dark:bg-gray-800/60 p-4 rounded-xl border border-gray-200 dark:border-gray-700/60 shadow-sm space-y-3">
                    <h3 class="font-medium text-sm text-streamlitRed uppercase tracking-wider">➕ Create New Task</h3>
                    
                    <div>
                        <label class="text-xs text-gray-500 dark:text-gray-400 block mb-1">Task Title</label>
                        <input type="text" id="task-title-input" placeholder="e.g., Prepare Q3 Report" class="w-full text-sm px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-streamlitRed">
                    </div>

                    <div class="grid grid-cols-2 gap-2">
                        <div>
                            <label class="text-xs text-gray-500 dark:text-gray-400 block mb-1">Category</label>
                            <select id="task-category-input" class="w-full text-sm px-2.5 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-streamlitRed">
                                <option value="Work">💼 Work</option>
                                <option value="Personal">🏡 Personal</option>
                                <option value="Urgent">🔥 Urgent</option>
                                <option value="Study">📚 Study</option>
                            </select>
                        </div>
                        <div>
                            <label class="text-xs text-gray-500 dark:text-gray-400 block mb-1">Priority</label>
                            <select id="task-priority-input" class="w-full text-sm px-2.5 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-streamlitRed">
                                <option value="High">🔴 High</option>
                                <option value="Medium" selected>🟡 Medium</option>
                                <option value="Low">🟢 Low</option>
                            </select>
                        </div>
                    </div>

                    <div>
                        <label class="text-xs text-gray-500 dark:text-gray-400 block mb-1">Due Date</label>
                        <input type="date" id="task-date-input" class="w-full text-sm px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-streamlitRed">
                    </div>

                    <button onclick="addTask()" class="w-full bg-streamlitRed hover:bg-red-600 text-white font-medium py-2 px-4 rounded-lg transition text-sm flex items-center justify-center space-x-2 shadow-md">
                        <i class="fa-solid fa-plus"></i>
                        <span>Add Task</span>
                    </button>
                </div>

                <!-- Filters Section -->
                <div class="space-y-3">
                    <h3 class="font-medium text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wider">Filter Tasks</h3>
                    
                    <div>
                        <label class="text-xs text-gray-500 dark:text-gray-400 block mb-1">Search Keywords</label>
                        <div class="relative">
                            <i class="fa-solid fa-magnifying-glass absolute left-3 top-2.5 text-xs text-gray-400"></i>
                            <input type="text" id="search-input" oninput="applyFilters()" placeholder="Search title..." class="w-full text-sm pl-8 pr-3 py-1.5 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-streamlitRed">
                        </div>
                    </div>

                    <div>
                        <label class="text-xs text-gray-500 dark:text-gray-400 block mb-1">Filter by Status</label>
                        <select id="filter-status" onchange="applyFilters()" class="w-full text-sm px-3 py-1.5 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-streamlitRed">
                            <option value="All">All Statuses</option>
                            <option value="Pending">Pending</option>
                            <option value="In Progress">In Progress</option>
                            <option value="Completed">Completed</option>
                        </select>
                    </div>

                    <div>
                        <label class="text-xs text-gray-500 dark:text-gray-400 block mb-1">Filter by Category</label>
                        <select id="filter-category" onchange="applyFilters()" class="w-full text-sm px-3 py-1.5 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-streamlitRed">
                            <option value="All">All Categories</option>
                            <option value="Work">💼 Work</option>
                            <option value="Personal">🏡 Personal</option>
                            <option value="Urgent">🔥 Urgent</option>
                            <option value="Study">📚 Study</option>
                        </select>
                    </div>
                </div>
            </div>

            <div class="mt-6 pt-4 border-t border-gray-300 dark:border-gray-700 text-xs text-gray-500 dark:text-gray-400 text-center">
                Streamlit v1.38.0 • Python 3.11
            </div>
        </aside>

        <main id="app-view" class="flex-1 p-6 overflow-y-auto bg-streamlitLightBg dark:bg-streamlitDarkBg">
            
            <!-- Metrics Row (Streamlit st.metric) -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                <div class="bg-white dark:bg-streamlitDarkSec p-4 rounded-xl border border-gray-200 dark:border-gray-700/80 shadow-sm">
                    <span class="text-xs font-medium text-gray-500 dark:text-gray-400">Total Tasks</span>
                    <div class="text-2xl font-bold mt-1 text-gray-800 dark:text-gray-100" id="metric-total">0</div>
                    <span class="text-xs text-blue-500"><i class="fa-solid fa-list mr-1"></i>Active list items</span>
                </div>
                <div class="bg-white dark:bg-streamlitDarkSec p-4 rounded-xl border border-gray-200 dark:border-gray-700/80 shadow-sm">
                    <span class="text-xs font-medium text-gray-500 dark:text-gray-400">Pending Tasks</span>
                    <div class="text-2xl font-bold mt-1 text-amber-500" id="metric-pending">0</div>
                    <span class="text-xs text-amber-500/80"><i class="fa-solid fa-clock mr-1"></i>Awaiting action</span>
                </div>
                <div class="bg-white dark:bg-streamlitDarkSec p-4 rounded-xl border border-gray-200 dark:border-gray-700/80 shadow-sm">
                    <span class="text-xs font-medium text-gray-500 dark:text-gray-400">In Progress</span>
                    <div class="text-2xl font-bold mt-1 text-indigo-500" id="metric-progress">0</div>
                    <span class="text-xs text-indigo-500/80"><i class="fa-solid fa-spinner mr-1"></i>Currently active</span>
                </div>
                <div class="bg-white dark:bg-streamlitDarkSec p-4 rounded-xl border border-gray-200 dark:border-gray-700/80 shadow-sm">
                    <span class="text-xs font-medium text-gray-500 dark:text-gray-400">Completed</span>
                    <div class="text-2xl font-bold mt-1 text-emerald-500" id="metric-completed">0</div>
                    <span class="text-xs text-emerald-500/80" id="metric-completion-rate"><i class="fa-solid fa-check-circle mr-1"></i>0% completion</span>
                </div>
            </div>

            <!-- Charts Section (Streamlit Visuals) -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <div class="bg-white dark:bg-streamlitDarkSec p-5 rounded-xl border border-gray-200 dark:border-gray-700/80 shadow-sm">
                    <h3 class="text-sm font-semibold mb-3 text-gray-700 dark:text-gray-300 flex items-center">
                        <i class="fa-solid fa-chart-pie text-streamlitRed mr-2"></i> Status Breakdown
                    </h3>
                    <div class="h-48 relative flex items-center justify-center">
                        <canvas id="statusChart"></canvas>
                    </div>
                </div>
                <div class="bg-white dark:bg-streamlitDarkSec p-5 rounded-xl border border-gray-200 dark:border-gray-700/80 shadow-sm">
                    <h3 class="text-sm font-semibold mb-3 text-gray-700 dark:text-gray-300 flex items-center">
                        <i class="fa-solid fa-chart-bar text-streamlitRed mr-2"></i> Category Distribution
                    </h3>
                    <div class="h-48 relative flex items-center justify-center">
                        <canvas id="categoryChart"></canvas>
                    </div>
                </div>
            </div>

            <!-- Task List Section (Streamlit st.dataframe / custom list) -->
            <div class="bg-white dark:bg-streamlitDarkSec rounded-xl border border-gray-200 dark:border-gray-700/80 shadow-sm overflow-hidden">
                <div class="p-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center bg-gray-50/50 dark:bg-gray-800/30">
                    <h3 class="font-semibold text-base flex items-center">
                        <i class="fa-solid fa-tasks text-streamlitRed mr-2"></i> Task Inventory
                    </h3>
                    <button onclick="clearCompleted()" class="text-xs text-gray-500 hover:text-streamlitRed transition flex items-center">
                        <i class="fa-solid fa-trash-can mr-1"></i> Clear Completed
                    </button>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full text-left text-sm">
                        <thead class="bg-gray-100 dark:bg-gray-800/80 text-gray-600 dark:text-gray-400 uppercase text-xs">
                            <tr>
                                <th class="py-3 px-4">Task</th>
                                <th class="py-3 px-4">Category</th>
                                <th class="py-3 px-4">Priority</th>
                                <th class="py-3 px-4">Due Date</th>
                                <th class="py-3 px-4">Status</th>
                                <th class="py-3 px-4 text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody id="task-table-body" class="divide-y divide-gray-200 dark:divide-gray-700">
                            <!-- Tasks populated dynamically -->
                        </tbody>
                    </table>
                </div>
            </div>
        </main>

        <main id="code-view" class="hidden flex-1 p-6 overflow-y-auto bg-slate-900 text-gray-100">
            <div class="max-w-5xl mx-auto space-y-4">
                <div class="flex justify-between items-center bg-slate-800 p-4 rounded-xl border border-slate-700">
                    <div>
                        <h2 class="text-lg font-bold text-white flex items-center">
                            <i class="fa-brands fa-python text-yellow-400 mr-2 text-xl"></i> `app.py` - Ready to Run
                        </h2>
                        <p class="text-xs text-gray-400 mt-0.5">Copy this code and execute locally using <code class="bg-slate-900 px-1.5 py-0.5 rounded text-streamlitRed">streamlit run app.py</code></p>
                    </div>
                    <button onclick="copyCode()" class="bg-streamlitRed hover:bg-red-600 text-white text-xs font-semibold px-4 py-2 rounded-lg transition flex items-center space-x-2">
                        <i class="fa-solid fa-copy"></i>
                        <span id="copy-btn-text">Copy Python Code</span>
                    </button>
                </div>

                <div class="relative bg-slate-950 p-4 rounded-xl border border-slate-800 overflow-x-auto">
                    <pre><code id="streamlit-code-content" class="code-block text-xs text-green-400 leading-relaxed">
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# 1. Page Configuration
st.set_page_config(
    page_title="TaskFlow Pro - Streamlit To-Do App",
    page_icon="✅",
    layout="wide"
)

# 2. Session State Initialization
if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {"Task": "Finalize Q4 Budget Report", "Category": "Work", "Priority": "High", "Due Date": "2026-10-15", "Status": "In Progress"},
        {"Task": "Grocery Shopping", "Category": "Personal", "Priority": "Medium", "Due Date": "2026-10-05", "Status": "Pending"},
        {"Task": "Server Security Patch Update", "Category": "Urgent", "Priority": "High", "Due Date": "2026-10-03", "Status": "Completed"}
    ]

# 3. Sidebar Inputs & Filters
st.sidebar.title("⚡ Task Controls")

# Form to add new task
with st.sidebar.form("new_task_form", clear_on_submit=True):
    st.subheader("➕ Add New Task")
    task_name = st.text_input("Task Name")
    category = st.selectbox("Category", ["Work", "Personal", "Urgent", "Study"])
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    due_date = st.date_input("Due Date", date.today())
    submit = st.form_submit_button("Add Task")

    if submit and task_name:
        new_task = {
            "Task": task_name,
            "Category": category,
            "Priority": priority,
            "Due Date": str(due_date),
            "Status": "Pending"
        }
        st.session_state.tasks.append(new_task)
        st.sidebar.success("Task added successfully!")

# Filters
st.sidebar.divider()
st.sidebar.subheader("🔍 Filters")
search_term = st.sidebar.text_input("Search Tasks")
filter_status = st.sidebar.selectbox("Filter Status", ["All", "Pending", "In Progress", "Completed"])
filter_category = st.sidebar.selectbox("Filter Category", ["All", "Work", "Personal", "Urgent", "Study"])

# 4. Main App Header
st.title("✅ TaskFlow Pro Management Dashboard")
st.caption("A feature-rich, interactive Streamlit task application")

# 5. Data Processing & Metrics
df = pd.DataFrame(st.session_state.tasks)

if not df.empty:
    # Filter Data
    filtered_df = df.copy()
    if search_term:
        filtered_df = filtered_df[filtered_df["Task"].str.contains(search_term, case=False)]
    if filter_status != "All":
        filtered_df = filtered_df[filtered_df["Status"] == filter_status]
    if filter_category != "All":
        filtered_df = filtered_df[filtered_df["Category"] == filter_category]

    # Display Metrics
    col1, col2, col3, col4 = st.columns(4)
    total_tasks = len(df)
    pending_tasks = len(df[df["Status"] == "Pending"])
    progress_tasks = len(df[df["Status"] == "In Progress"])
    completed_tasks = len(df[df["Status"] == "Completed"])
    rate = round((completed_tasks / total_tasks * 100), 1) if total_tasks > 0 else 0

    col1.metric("Total Tasks", total_tasks)
    col2.metric("Pending", pending_tasks, delta_color="inverse")
    col3.metric("In Progress", progress_tasks)
    col4.metric("Completed", completed_tasks, f"{rate}% Rate")

    st.divider()

    # 6. Analytics / Visualizations
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("📊 Status Distribution")
        fig_status = px.pie(df, names="Status", color="Status", 
                            color_discrete_map={"Pending":"#f59e0b", "In Progress":"#6366f1", "Completed":"#10b981"})
        st.plotly_chart(fig_status, use_container_width=True)

    with chart_col2:
        st.subheader("📁 Tasks by Category")
        fig_cat = px.bar(df, x="Category", color="Category", title="Category Counts")
        st.plotly_chart(fig_cat, use_container_width=True)

    st.divider()

    # 7. Interactive Table and Management
    st.subheader("📋 Task Inventory")
    
    # Render interactive status modification
    for idx, row in filtered_df.iterrows():
        c1, c2, c3, c4, c5 = st.columns([3, 1.5, 1.5, 1.5, 1])
        c1.write(f"**{row['Task']}**")
        c2.write(f"`{row['Category']}`")
        c3.write(f"Priority: **{row['Priority']}**")
        c4.write(row['Due Date'])
        
        # Interactive status editor
        new_status = c5.selectbox("", ["Pending", "In Progress", "Completed"], 
                                  index=["Pending", "In Progress", "Completed"].index(row["Status"]), 
                                  key=f"status_{idx}")
        if new_status != row["Status"]:
            st.session_state.tasks[idx]["Status"] = new_status
            st.rerun()

else:
    st.info("No tasks created yet. Use the sidebar to create your first task!")
                    </code></pre>
                </div>
            </div>
        </main>
    </div>

    <script>
        // Default Sample Data
        let tasks = [
            { id: 1, title: "Finalize Q4 Budget Report", category: "Work", priority: "High", dueDate: "2026-10-15", status: "In Progress" },
            { id: 2, title: "Grocery Shopping & Meal Prep", category: "Personal", priority: "Medium", dueDate: "2026-10-05", status: "Pending" },
            { id: 3, title: "Server Security Patch Deployment", category: "Urgent", priority: "High", dueDate: "2026-10-03", status: "Completed" },
            { id: 4, title: "Read Streamlit Documentation", category: "Study", priority: "Low", dueDate: "2026-10-20", status: "Pending" }
        ];

        let filteredTasks = [...tasks];
        let statusChartInstance = null;
        let categoryChartInstance = null;

        // Initialize App
        window.onload = function() {
            // Set default date input to today
            const today = new Date().toISOString().split('T')[0];
            document.getElementById('task-date-input').value = today;
            
            initCharts();
            renderApp();
        };

        // Theme Toggle Functionality
        function toggleDarkMode() {
            const html = document.documentElement;
            const icon = document.getElementById('theme-toggle-icon');
            if (html.classList.contains('dark')) {
                html.classList.remove('dark');
                icon.className = 'fa-solid fa-moon';
            } else {
                html.classList.add('dark');
                icon.className = 'fa-solid fa-sun';
            }
            updateCharts();
        }

        // Tab Switcher
        function switchMainTab(tab) {
            const appView = document.getElementById('app-view');
            const codeView = document.getElementById('code-view');
            const sidebar = document.getElementById('streamlit-sidebar');
            const appBtn = document.getElementById('tab-app-btn');
            const codeBtn = document.getElementById('tab-code-btn');

            if (tab === 'app') {
                appView.classList.remove('hidden');
                codeView.classList.add('hidden');
                sidebar.classList.remove('hidden');
                appBtn.className = "px-4 py-1.5 rounded-md font-medium bg-white dark:bg-streamlitDarkSec text-streamlitRed shadow-sm transition";
                codeBtn.className = "px-4 py-1.5 rounded-md font-medium text-gray-600 dark:text-gray-300 hover:text-streamlitRed transition";
            } else {
                appView.classList.add('hidden');
                codeView.classList.remove('hidden');
                sidebar.classList.add('hidden');
                codeBtn.className = "px-4 py-1.5 rounded-md font-medium bg-white dark:bg-streamlitDarkSec text-streamlitRed shadow-sm transition";
                appBtn.className = "px-4 py-1.5 rounded-md font-medium text-gray-600 dark:text-gray-300 hover:text-streamlitRed transition";
            }
        }

        function addTask() {
            const title = document.getElementById('task-title-input').value.trim();
            const category = document.getElementById('task-category-input').value;
            const priority = document.getElementById('task-priority-input').value;
            const dueDate = document.getElementById('task-date-input').value;

            if (!title) {
                alert("Please enter a task title!");
                return;
            }

            const newTask = {
                id: Date.now(),
                title: title,
                category: category,
                priority: priority,
                dueDate: dueDate,
                status: "Pending"
            };

            tasks.push(newTask);
            document.getElementById('task-title-input').value = '';
            applyFilters();
        }

        function updateTaskStatus(id, newStatus) {
            const task = tasks.find(t => t.id === id);
            if (task) {
                task.status = newStatus;
                applyFilters();
            }
        }

        function deleteTask(id) {
            tasks = tasks.filter(t => t.id !== id);
            applyFilters();
        }

        function clearCompleted() {
            tasks = tasks.filter(t => t.status !== "Completed");
            applyFilters();
        }

        function applyFilters() {
            const search = document.getElementById('search-input').value.toLowerCase();
            const statusFilter = document.getElementById('filter-status').value;
            const catFilter = document.getElementById('filter-category').value;

            filteredTasks = tasks.filter(t => {
                const matchesSearch = t.title.toLowerCase().includes(search);
                const matchesStatus = statusFilter === 'All' || t.status === statusFilter;
                const matchesCategory = catFilter === 'All' || t.category === catFilter;
                return matchesSearch && matchesStatus && matchesCategory;
            });

            renderApp();
        }

        function renderApp() {
            // Render Metrics
            const total = tasks.length;
            const pending = tasks.filter(t => t.status === 'Pending').length;
            const inProgress = tasks.filter(t => t.status === 'In Progress').length;
            const completed = tasks.filter(t => t.status === 'Completed').length;
            const completionRate = total > 0 ? Math.round((completed / total) * 100) : 0;

            document.getElementById('metric-total').innerText = total;
            document.getElementById('metric-pending').innerText = pending;
            document.getElementById('metric-progress').innerText = inProgress;
            document.getElementById('metric-completed').innerText = completed;
            document.getElementById('metric-completion-rate').innerHTML = `<i class="fa-solid fa-check-circle mr-1"></i>${completionRate}% completion rate`;

            // Render Table
            const tbody = document.getElementById('task-table-body');
            tbody.innerHTML = '';

            if (filteredTasks.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="6" class="py-6 text-center text-gray-400">
                            <i class="fa-solid fa-inbox text-2xl mb-2 block"></i>
                            No tasks found matching your filter criteria.
                        </td>
                    </tr>`;
            } else {
                filteredTasks.forEach(task => {
                    const tr = document.createElement('tr');
                    tr.className = "hover:bg-gray-50 dark:hover:bg-gray-800/40 transition";

                    // Priority badges
                    let priorityBadge = '';
                    if (task.priority === 'High') priorityBadge = '<span class="text-xs bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300 px-2 py-0.5 rounded-full font-medium">🔴 High</span>';
                    else if (task.priority === 'Medium') priorityBadge = '<span class="text-xs bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300 px-2 py-0.5 rounded-full font-medium">🟡 Medium</span>';
                    else priorityBadge = '<span class="text-xs bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300 px-2 py-0.5 rounded-full font-medium">🟢 Low</span>';

                    tr.innerHTML = `
                        <td class="py-3 px-4 font-medium text-gray-800 dark:text-gray-200">${task.title}</td>
                        <td class="py-3 px-4"><span class="bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 px-2 py-1 rounded text-xs">${task.category}</span></td>
                        <td class="py-3 px-4">${priorityBadge}</td>
                        <td class="py-3 px-4 text-xs text-gray-500 dark:text-gray-400"><i class="fa-regular fa-calendar mr-1.5"></i>${task.dueDate}</td>
                        <td class="py-3 px-4">
                            <select onchange="updateTaskStatus(${task.id}, this.value)" class="text-xs font-semibold px-2.5 py-1 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 focus:outline-none focus:ring-1 focus:ring-streamlitRed">
                                <option value="Pending" ${task.status === 'Pending' ? 'selected' : ''}>⏳ Pending</option>
                                <option value="In Progress" ${task.status === 'In Progress' ? 'selected' : ''}>🔄 In Progress</option>
                                <option value="Completed" ${task.status === 'Completed' ? 'selected' : ''}>✅ Completed</option>
                            </select>
                        </td>
                        <td class="py-3 px-4 text-right">
                            <button onclick="deleteTask(${task.id})" class="text-gray-400 hover:text-red-500 transition px-2 py-1">
                                <i class="fa-solid fa-trash"></i>
                            </button>
                        </td>
                    `;
                    tbody.appendChild(tr);
                });
            }

            updateCharts();
        }

        function initCharts() {
            const ctxStatus = document.getElementById('statusChart').getContext('2d');
            const ctxCategory = document.getElementById('categoryChart').getContext('2d');

            statusChartInstance = new Chart(ctxStatus, {
                type: 'doughnut',
                data: {
                    labels: ['Pending', 'In Progress', 'Completed'],
                    datasets: [{
                        data: [0, 0, 0],
                        backgroundColor: ['#f59e0b', '#6366f1', '#10b981'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { position: 'bottom' } }
                }
            });

            categoryChartInstance = new Chart(ctxCategory, {
                type: 'bar',
                data: {
                    labels: ['Work', 'Personal', 'Urgent', 'Study'],
                    datasets: [{
                        label: 'Tasks',
                        data: [0, 0, 0, 0],
                        backgroundColor: '#FF4B4B',
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } },
                    plugins: { legend: { display: false } }
                }
            });
        }

        function updateCharts() {
            if (!statusChartInstance || !categoryChartInstance) return;

            const pending = tasks.filter(t => t.status === 'Pending').length;
            const inProgress = tasks.filter(t => t.status === 'In Progress').length;
            const completed = tasks.filter(t => t.status === 'Completed').length;

            statusChartInstance.data.datasets[0].data = [pending, inProgress, completed];
            statusChartInstance.update();

            const categories = ['Work', 'Personal', 'Urgent', 'Study'];
            const catCounts = categories.map(cat => tasks.filter(t => t.category === cat).length);

            categoryChartInstance.data.datasets[0].data = catCounts;
            categoryChartInstance.update();
        }

        // Code Copy Helper
        function copyCode() {
            const codeText = document.getElementById('streamlit-code-content').innerText;
            const textToCopy = codeText.replace(/            
            const textArea = document.createElement("textarea");
            textArea.value = textToCopy;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);

            const btnText = document.getElementById('copy-btn-text');
            btnText.innerText = 'Copied to Clipboard!';
            setTimeout(() => {
                btnText.innerText = 'Copy Python Code';
            }, 2000);
        }
    </script>
</body>
</html>
