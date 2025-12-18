import streamlit as st
import sqlite3

# ================= DATABASE SETUP =================
def get_connection():
    return sqlite3.connect("ngo_profile.db", check_same_thread=False)

conn = get_connection()
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS ngo_intro (content TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS ngo_values (value TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS ngo_projects (project TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS ngo_members (name TEXT, role TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS ngo_achievements (info TEXT)")
conn.commit()

# ================= DEFAULT DATA =================
def insert_defaults():
    if cur.execute("SELECT COUNT(*) FROM ngo_intro").fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO ngo_intro VALUES ('We are a non-profit organization dedicated to community upliftment.')"
        )

    if cur.execute("SELECT COUNT(*) FROM ngo_values").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO ngo_values VALUES (?)",
            [("Transparency",), ("Empathy",), ("Accountability",)]
        )

    if cur.execute("SELECT COUNT(*) FROM ngo_projects").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO ngo_projects VALUES (?)",
            [("Women Empowerment",), ("Rural Healthcare",), ("Youth Skill Development",)]
        )

    if cur.execute("SELECT COUNT(*) FROM ngo_members").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO ngo_members VALUES (?, ?)",
            [("Neha Patil", "Director"), ("Rahul Joshi", "Operations Head")]
        )

    if cur.execute("SELECT COUNT(*) FROM ngo_achievements").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO ngo_achievements VALUES (?)",
            [("5,000+ lives impacted",), ("60+ community drives completed",)]
        )

    conn.commit()

insert_defaults()

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ================= UI CONFIG =================
st.set_page_config("NGO Profile System", layout="wide")
st.title("NGO Profile Management System")

page = st.sidebar.radio(
    "Menu",
    ["NGO Overview", "Admin Panel"]
)

# ================= USER VIEW =================
def ngo_overview():
    st.header("Who We Are")

    st.write(cur.execute("SELECT content FROM ngo_intro").fetchone()[0])

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Our Core Values")
        for v in cur.execute("SELECT value FROM ngo_values"):
            st.markdown(f"✔ {v[0]}")

    with col2:
        st.subheader("Key Projects")
        for p in cur.execute("SELECT project FROM ngo_projects"):
            st.markdown(f"📌 {p[0]}")

    st.subheader("Leadership Team")
    for m in cur.execute("SELECT name, role FROM ngo_members"):
        st.write(f"**{m[0]}** — {m[1]}")

    st.subheader("Our Impact")
    for a in cur.execute("SELECT info FROM ngo_achievements"):
        st.markdown(f"⭐ {a[0]}")

    st.info("Together, we can make a difference.")
    st.button("Become a Volunteer")
    st.button("Support Our Work")

# ================= ADMIN PANEL =================
def admin_panel():
    if not st.session_state.logged_in:
        st.subheader("Admin Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username == "admin" and password == "ngo123":
                st.session_state.logged_in = True
                st.success("Login successful")
            else:
                st.error("Incorrect credentials")

    if st.session_state.logged_in:
        st.subheader("Admin Dashboard")

        intro = st.text_area(
            "Edit NGO Introduction",
            cur.execute("SELECT content FROM ngo_intro").fetchone()[0]
        )

        if st.button("Save Introduction"):
            cur.execute("DELETE FROM ngo_intro")
            cur.execute("INSERT INTO ngo_intro VALUES (?)", (intro,))
            conn.commit()
            st.success("Introduction updated")

        value = st.text_input("Add Core Value")
        if st.button("Add Value"):
            cur.execute("INSERT INTO ngo_values VALUES (?)", (value,))
            conn.commit()
            st.success("Value added")

        project = st.text_input("Add Project")
        if st.button("Add Project"):
            cur.execute("INSERT INTO ngo_projects VALUES (?)", (project,))
            conn.commit()
            st.success("Project added")

        member = st.text_input("Member Name")
        role = st.text_input("Member Role")
        if st.button("Add Member"):
            cur.execute(
                "INSERT INTO ngo_members VALUES (?, ?)",
                (member, role)
            )
            conn.commit()
            st.success("Team member added")

# ================= ROUTING =================
if page == "NGO Overview":
    ngo_overview()
else:
    admin_panel()
