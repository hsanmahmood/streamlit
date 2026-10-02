import streamlit as st
import datetime

# ---------------------------------------------------------
# Page Config
# ---------------------------------------------------------
st.set_page_config(page_title="Simple To-Do", page_icon="📝", layout="centered")

# ---------------------------------------------------------
# State Initialization
# ---------------------------------------------------------
if "todos" not in st.session_state:
    st.session_state.todos = [
        {"id": 1, "task": "Learn Streamlit basics", "done": True, "priority": "High"},
        {"id": 2, "task": "Build lightweight experimental app", "done": False, "priority": "Medium"},
    ]

if "next_id" not in st.session_state:
    st.session_state.next_id = 3

# ---------------------------------------------------------
# Sidebar: Add New Task
# ---------------------------------------------------------
st.sidebar.header("➕ Add New Task")

with st.sidebar.form("new_task_form", clear_on_submit=True):
    task_input = st.text_input("Task Description")
    priority_input = st.selectbox("Priority", ["High", "Medium", "Low"])
    submitted = st.form_submit_button("Add Task")

    if submitted:
        if task_input.strip():
            st.session_state.todos.append({
                "id": st.session_state.next_id,
                "task": task_input.strip(),
                "done": False,
                "priority": priority_input
            })
            st.session_state.next_id += 1
            st.rerun()
        else:
            st.warning("Please enter a task.")

# ---------------------------------------------------------
# Main Page UI
# ---------------------------------------------------------
st.title("📝 Simple To-Do App")

# Simple Metrics
total = len(st.session_state.todos)
completed = sum(1 for item in st.session_state.todos if item["done"])
pending = total - completed

c1, c2, c3 = st.columns(3)
c1.metric("Total", total)
c2.metric("Pending", pending)
c3.metric("Completed", completed)

st.divider()

# Progress Bar
if total > 0:
    st.progress(completed / total)

st.subheader("Your Tasks")

if not st.session_state.todos:
    st.info("No tasks yet! Add one using the sidebar.")
else:
    # Render tasks
    for idx, item in enumerate(st.session_state.todos):
        col_check, col_text, col_badge, col_del = st.columns([0.8, 5, 2, 1])

        # Toggle status
        with col_check:
            is_done = st.checkbox("", value=item["done"], key=f"check_{item['id']}")
            if is_done != item["done"]:
                st.session_state.todos[idx]["done"] = is_done
                st.rerun()

        # Display text with strikethrough if done
        with col_text:
            if item["done"]:
                st.markdown(f"~~{item['task']}~~")
            else:
                st.write(item["task"])

        # Display priority badge
        with col_badge:
            st.caption(f"P: **{item['priority']}**")

        # Delete button
        with col_del:
            if st.button("❌", key=f"del_{item['id']}"):
                st.session_state.todos = [t for t in st.session_state.todos if t["id"] != item["id"]]
                st.rerun()

# ---------------------------------------------------------
# Danger Zone / Clear All
# ---------------------------------------------------------
st.divider()
if st.button("🗑️ Clear All Tasks"):
    st.session_state.todos = []
    st.rerun()
