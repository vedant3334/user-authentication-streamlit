import streamlit as st
import sqlite3
import os
from datetime import datetime

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(page_title="NGO Media & Communications", layout="wide")

# ==================================================
# DEMO ADMIN CREDENTIALS (INTERNSHIP USE ONLY)
# ==================================================
ADMIN_USER = "admin"
ADMIN_PASS = "password123"

# ==================================================
# DATABASE
# ==================================================
def get_db():
    return sqlite3.connect("media_alt.db", check_same_thread=False)

conn = get_db()
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS press_release (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    headline TEXT,
    content TEXT,
    published_on TEXT,
    is_active INTEGER DEFAULT 1
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS media_link (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    outlet TEXT,
    link TEXT,
    is_active INTEGER DEFAULT 1
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS gallery (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path TEXT,
    uploaded_on TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS video_media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    embed_url TEXT
)
""")

conn.commit()

# ==================================================
# SESSION STATE
# ==================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ==================================================
# LOGIN COMPONENT
# ==================================================
def login_panel():
    st.subheader("Admin Access")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Sign In"):
        if u == ADMIN_USER and p == ADMIN_PASS:
            st.session_state.logged_in = True
            st.success("Login successful")
        else:
            st.error("Invalid credentials")

# ==================================================
# PUBLIC MEDIA PAGE
# ==================================================
def public_media():
    st.title("Media & Communications")

    st.markdown("""
    This section showcases official announcements, news coverage,
    photos from the field, and videos documenting our NGO’s impact.
    """)

    # Press Releases
    st.header("Press Releases")
    cur.execute("SELECT headline, content, published_on FROM press_release WHERE is_active=1 ORDER BY published_on DESC")
    data = cur.fetchall()

    if data:
        for d in data:
            st.subheader(d[0])
            st.write(d[1])
            st.caption(f"Published on: {d[2]}")
            st.divider()
    else:
        st.info("No press releases published yet.")

    # Media Links
    st.header("In the News")
    cur.execute("SELECT outlet, link FROM media_link WHERE is_active=1")
    news = cur.fetchall()

    if news:
        for n in news:
            st.markdown(f"- **{n[0]}**: [Read more]({n[1]})")
    else:
        st.info("No external media articles available.")

    # Gallery
    st.header("Photo Gallery")
    cur.execute("SELECT file_path FROM gallery")
    imgs = [i[0] for i in cur.fetchall()]
    if imgs:
        st.image(imgs, width=220)
    else:
        st.info("Gallery is empty.")

    # Videos
    st.header("Videos")
    cur.execute("SELECT embed_url FROM video_media")
    vids = cur.fetchall()
    if vids:
        for v in vids:
            st.video(v[0])
    else:
        st.info("No videos added yet.")

# ==================================================
# ADMIN DASHBOARD
# ==================================================
def admin_panel():
    st.title("Media Management Dashboard")
    tabs = st.tabs(["Press", "News", "Gallery", "Videos"])

    # Press
    with tabs[0]:
        st.subheader("Publish Press Release")
        h = st.text_input("Headline")
        c = st.text_area("Content")
        if st.button("Publish"):
            cur.execute("INSERT INTO press_release VALUES (NULL, ?, ?, ?, 1)",
                        (h, c, datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
            st.success("Press release published")

    # News
    with tabs[1]:
        st.subheader("Add Media Article")
        o = st.text_input("Media Outlet")
        l = st.text_input("Article Link")
        if st.button("Add Article"):
            cur.execute("INSERT INTO media_link VALUES (NULL, ?, ?, 1)", (o, l))
            conn.commit()
            st.success("Media link added")

    # Gallery
    with tabs[2]:
        st.subheader("Upload Photo")
        img = st.file_uploader("Select Image", type=["jpg", "png", "jpeg"])
        if img:
            os.makedirs("uploads_alt", exist_ok=True)
            path = f"uploads_alt/{img.name}"
            with open(path, "wb") as f:
                f.write(img.getbuffer())
            cur.execute("INSERT INTO gallery VALUES (NULL, ?, ?)",
                        (path, datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
            st.success("Image uploaded")

    # Videos
    with tabs[3]:
        st.subheader("Add Video URL")
        v = st.text_input("YouTube / Embed URL")
        if st.button("Save Video"):
            cur.execute("INSERT INTO video_media VALUES (NULL, ?)", (v,))
            conn.commit()
            st.success("Video saved")

# ==================================================
# NAVIGATION
# ==================================================
choice = st.sidebar.selectbox("Menu", ["Public Media Page", "Admin Panel"])

if choice == "Public Media Page":
    public_media()
else:
    if st.session_state.logged_in:
        admin_panel()
    else:
        login_panel()
