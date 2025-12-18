import streamlit as st
import sqlite3
import os
from datetime import date

# ---------- DATABASE ----------
conn = sqlite3.connect("ngo_v3.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    status TEXT,
    start_date TEXT,
    end_date TEXT,
    location TEXT,
    image TEXT
)
""")
conn.commit()

# ---------- IMAGE FOLDER ----------
if not os.path.exists("uploads"):
    os.mkdir("uploads")

# ---------- APP TITLE ----------
st.set_page_config(page_title="NGO Project System")
st.title("🌍 NGO Project Management System")

tab1, tab2, tab3 = st.tabs(["📂 Projects", "➕ Add Project", "🗑 Manage"])

# ==================================================
# ================= VIEW PROJECTS ==================
# ==================================================
with tab1:
    st.subheader("Our Projects")

    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "Ongoing", "Completed", "Upcoming"]
    )

    if status_filter == "All":
        cur.execute("SELECT * FROM projects")
    else:
        cur.execute("SELECT * FROM projects WHERE status=?", (status_filter,))

    projects = cur.fetchall()

    if not projects:
        st.info("No projects found")
    else:
        for p in projects:
            st.markdown(f"### {p[1]}")
            st.write(p[2])
            st.write("📍 Location:", p[6])
            st.write("📌 Status:", p[3])
            st.write("📅 Duration:", p[4], "to", p[5])

            if p[7]:
                st.image(p[7], width=300)

            st.divider()

# ==================================================
# ================= ADD PROJECT ====================
# ==================================================
with tab2:
    st.subheader("Add New Project")

    title = st.text_input("Project Title")
    desc = st.text_area("Description")
    status = st.selectbox("Status", ["Ongoing", "Completed", "Upcoming"])
    start = st.date_input("Start Date", date.today())
    end = st.date_input("End Date", date.today())
    location = st.text_input("Location")
    image = st.file_uploader("Upload Image", ["jpg", "png", "jpeg"])

    if st.button("Save Project"):
        img_path = ""
        if image:
            img_path = f"uploads/{image.name}"
            with open(img_path, "wb") as f:
                f.write(image.read())

        cur.execute(
            "INSERT INTO projects VALUES (NULL,?,?,?,?,?,?,?)",
            (title, desc, status, str(start), str(end), location, img_path)
        )
        conn.commit()
        st.success("Project added successfully")

# ==================================================
# ================= DELETE PROJECT =================
# ==================================================
with tab3:
    st.subheader("Delete Project")

    cur.execute("SELECT id, title FROM projects")
    items = cur.fetchall()

    if items:
        project_map = {i[1]: i[0] for i in items}
        selected = st.selectbox("Select Project", project_map.keys())

        if st.button("Delete"):
            cur.execute("DELETE FROM projects WHERE id=?", (project_map[selected],))
            conn.commit()
            st.success("Project deleted")
    else:
        st.info("No projects available")

# ---------- FOOTER ----------
st.caption("Internship Project | Streamlit + SQLite")
