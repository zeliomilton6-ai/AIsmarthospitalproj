import streamlit as st
import pandas as pd
import sqlite3
import numpy as np
from datetime import date, time, datetime
from sklearn.ensemble import RandomForestRegressor

st.set_page_config(page_title="MEDI AI Smart Hospital", page_icon="🏥", layout="wide")
DEPARTMENTS = {"General Medicine": 3, "Paediatrics": 2, "Maternity": 2, "Surgery": 2, "Dental": 1, "Laboratory": 2}

# Demo database only. Do not enter real patient information.
conn = sqlite3.connect("hospital.db", check_same_thread=False)
conn.execute("""CREATE TABLE IF NOT EXISTS appointments (
id INTEGER PRIMARY KEY AUTOINCREMENT, patient_name TEXT, department TEXT,
doctor TEXT, appointment_date TEXT, appointment_time TEXT, created_at TEXT)""")
conn.commit()

@st.cache_resource
def train_model():
    np.random.seed(42)
    data = pd.DataFrame({
        "queue": np.random.randint(0, 30, 1000),
        "doctors": np.random.randint(1, 5, 1000),
        "duration": np.random.randint(10, 31, 1000)
    })
    data["wait"] = (data.queue * data.duration / data.doctors +
                    np.random.normal(0, 3, 1000)).clip(lower=0)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(data[["queue", "doctors", "duration"]], data.wait)
    return model

model = train_model()
def records():
    return pd.read_sql_query(
        "SELECT * FROM appointments ORDER BY appointment_date, appointment_time", conn
    )

st.title("🏥 MEDI AI — SMART HOSPITAL")
st.write("Appointment management and experimental waiting-time estimation.")
st.warning("Educational prototype. Use fictional data only. Waiting-time estimates use simulated data and are not validated for real hospital use or clinical decisions.")

df = records()
a, b, c = st.columns(3)
a.metric("Appointments", len(df))
b.metric("Departments", len(DEPARTMENTS))
c.metric("Demo doctors", sum(DEPARTMENTS.values()))

page = st.sidebar.selectbox("Menu", ["Dashboard", "Register Appointment", "Waiting Time Prediction", "Appointment Records"])

if page == "Dashboard":
    st.header("Welcome to MEDI AI")
    st.subheader("Departments")
    for name, count in DEPARTMENTS.items():
        st.write(f"🏥 {name} — {count} demo doctors")
    if not df.empty:
        st.subheader("Appointments")
        st.dataframe(df, use_container_width=True, hide_index=True)

elif page == "Register Appointment":
    st.header("📅 Register an appointment")
    with st.form("booking"):
        patient = st.text_input("Patient name or demo ID")
        department = st.selectbox("Department", list(DEPARTMENTS))
        doctor = st.text_input("Doctor name or ID")
        day = st.date_input("Appointment date", min_value=date.today())
        hour = st.time_input("Appointment time", value=time(9, 0))
        submitted = st.form_submit_button("Book appointment")
    if submitted:
        if not patient.strip() or not doctor.strip():
            st.error("Enter a patient demo ID and doctor name or ID.")
        else:
            conflict = conn.execute(
                "SELECT COUNT(*) FROM appointments WHERE doctor=? AND appointment_date=? AND appointment_time=?",
                (doctor.strip(), day.isoformat(), hour.strftime("%H:%M"))
            ).fetchone()[0]
            if conflict:
                st.error("This doctor already has an appointment at that time.")
            else:
                conn.execute(
                    "INSERT INTO appointments (patient_name, department, doctor, appointment_date, appointment_time, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (patient.strip(), department, doctor.strip(), day.isoformat(),
                     hour.strftime("%H:%M"), datetime.now().isoformat(timespec="seconds"))
                )
                conn.commit()
                st.success("Appointment successfully registered.")

elif page == "Waiting Time Prediction":
    st.header("🤖 Experimental waiting-time estimator")
    dept = st.selectbox("Department", list(DEPARTMENTS))
    queue = st.number_input("Patients currently waiting", 0, 200, 5)
    doctors = st.number_input("Doctors available", 1, 20, DEPARTMENTS[dept])
    duration = st.slider("Average consultation duration (minutes)", 5, 60, 20)
    if st.button("Estimate waiting time"):
        estimate = max(0, round(float(model.predict([[queue, doctors, duration]])[0])))
        st.success(f"Estimated waiting time: approximately {estimate} minutes")
        st.caption("Based on synthetic demonstration data. Do not use for triage or clinical decisions.")

elif page == "Appointment Records":
    st.header("📋 Appointment records")
    df = records()
    if df.empty:
        st.info("No appointments registered yet.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)
        record_id = st.number_input("Appointment ID to cancel", min_value=1, step=1)
        if st.button("Cancel appointment"):
            result = conn.execute("DELETE FROM appointments WHERE id=?", (record_id,))
            conn.commit()
            if result.rowcount:
                st.success("Appointment cancelled.")
                st.rerun()
            else:
                st.error("Appointment ID not found.")

st.divider()
st.caption("MEDI AI Smart Hospital | Educational prototype")
