import streamlit as st

st.set_page_config(page_title="Care & Support NGO", layout="wide")

# ---------------- SESSION STATE INITIALIZATION ----------------
if "vision" not in st.session_state:
    st.session_state.vision = "To support communities and promote social well-being."

if "mission" not in st.session_state:
    st.session_state.mission = "Providing education, health support, and basic needs."

if "statistics" not in st.session_state:
    st.session_state.statistics = [
        ("Families Supported", "900+"),
        ("Volunteers Joined", "120+"),
        ("Programs Conducted", "25+")
    ]

if "initiatives" not in st.session_state:
    st.session_state.initiatives = [
        "Child Education Support",
        "Health Awareness Programs",
        "Food Donation Drives"
    ]

# ---------------- SIDEBAR ----------------
page = st.sidebar.selectbox(
    "Navigation",
    ["Home Page", "Admin Dashboard"]
)

# ---------------- HOME PAGE ----------------
if page == "Home Page":
    st.title("Care & Support NGO")

    st.subheader("Vision")
    st.write(st.session_state.vision)

    st.subheader("Mission")
    st.write(st.session_state.mission)

    st.subheader("Our Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric(st.session_state.statistics[0][0], st.session_state.statistics[0][1])
    col2.metric(st.session_state.statistics[1][0], st.session_state.statistics[1][1])
    col3.metric(st.session_state.statistics[2][0], st.session_state.statistics[2][1])

    st.subheader("Our Initiatives")
    for item in st.session_state.initiatives:
        st.write("•", item)

    st.markdown("---")
    st.write("📧 Contact: caresupport@ngo.org")

# ---------------- ADMIN DASHBOARD ----------------
elif page == "Admin Dashboard":
    st.title("Admin Dashboard")

    st.subheader("Edit Vision & Mission")
    new_vision = st.text_area("Vision", st.session_state.vision)
    new_mission = st.text_area("Mission", st.session_state.mission)

    if st.button("Update Vision & Mission"):
        st.session_state.vision = new_vision
        st.session_state.mission = new_mission
        st.success("Vision and Mission updated")

    st.subheader("Update Statistics")
    updated_stats = []

    for title, value in st.session_state.statistics:
        new_value = st.text_input(title, value)
        updated_stats.append((title, new_value))

    if st.button("Save Statistics"):
        st.session_state.statistics = updated_stats
        st.success("Statistics updated")

    st.subheader("Add New Initiative")
    new_init = st.text_input("Initiative Name")

    if st.button("Add Initiative"):
        if new_init:
            st.session_state.initiatives.append(new_init)
            st.success("Initiative added")