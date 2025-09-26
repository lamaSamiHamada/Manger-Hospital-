
import streamlit as st
from hospital import Patient, Doctor, Appointment, HospitalManagementSystem
from datetime import datetime
import pandas as pd

# Predefined lists
COMMON_DISEASES = [
    "Flu", "Diabetes", "Hypertension", "Asthma", "Covid-19", 
    "Allergy", "Cancer", "Heart Disease", "Migraine", "Fracture"
]

MEDICAL_SPECIALTIES = [
    "Cardiology", "Neurology", "Dermatology", "Pediatrics", "Orthopedics",
    "Psychiatry", "Radiology", "General Surgery", "Internal Medicine", "Ophthalmology"
]

# Initialize system
if 'system' not in st.session_state:
    st.session_state.system = HospitalManagementSystem()

system = st.session_state.system

st.set_page_config(page_title="Hospital Management", layout="centered")

st.title("🏥 Hospital Management System")

menu = st.sidebar.selectbox("Navigation", [
    "Add Patient", "Add Doctor", "Create Appointment", 
    "View All", "Export to CSV"
])

def convert_to_csv(data, columns):
    df = pd.DataFrame(data, columns=columns)
    return df.to_csv(index=False).encode("utf-8")

if menu == "Add Patient":
    st.subheader("➕ Add Patient")
    with st.form("patient_form"):
        pid = st.text_input("Patient ID")
        name = st.text_input("Name")
        age = st.number_input("Age", 0, 120)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        disease = st.selectbox("Disease", COMMON_DISEASES)
        submitted = st.form_submit_button("Add Patient")
        if submitted:
            if pid and name and gender and disease and age is not None:
                patient = Patient(pid, name, age, gender, disease)
                system.add_patient(patient)
                st.success(f"✅ Patient {name} added.")
            else:
                st.error("❌ Please fill in all fields.")

elif menu == "Add Doctor":
    st.subheader("➕ Add Doctor")
    with st.form("doctor_form"):
        did = st.text_input("Doctor ID")
        name = st.text_input("Name")
        age = st.number_input("Age", 25, 100)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        specialty = st.selectbox("Specialty", MEDICAL_SPECIALTIES)
        submitted = st.form_submit_button("Add Doctor")
        if submitted:
            if did and name and gender and specialty and age is not None:
                doctor = Doctor(did, name, age, gender, specialty)
                system.add_doctor(doctor)
                st.success(f"✅ Doctor {name} added.")
            else:
                st.error("❌ Please fill in all fields.")

elif menu == "Create Appointment":
    st.subheader("📅 Create Appointment")
    if not system.patients or not system.doctors:
        st.warning("⚠️ Add at least one patient and doctor first.")
    else:
        with st.form("appointment_form"):
            aid = st.text_input("Appointment ID")
            date = st.date_input("Date")
            patient = st.selectbox("Select Patient", system.patients, format_func=lambda p: f"{p.name} ({p.person_id})")
            doctor = st.selectbox("Select Doctor", system.doctors, format_func=lambda d: f"{d.name} ({d.person_id})")
            submitted = st.form_submit_button("Create Appointment")
            if submitted:
                if aid and patient and doctor and date:
                    appt = Appointment(aid, patient, doctor, date)
                    system.create_appointment(appt)
                    st.success(f"✅ Appointment created between {patient.name} and Dr. {doctor.name}.")
                else:
                    st.error("❌ Please fill in all fields.")

elif menu == "View All":
    st.subheader("📋 Patients")
    for p in system.patients:
        st.text(p.display_info())

    st.subheader("🩺 Doctors")
    for d in system.doctors:
        st.text(d.display_info())

    st.subheader("📅 Appointments")
    for a in system.appointments:
        st.text(a.display_info())

elif menu == "Export to CSV":
    st.subheader("📤 Export Data")

    if system.patients:
        patient_data = [[p.person_id, p.name, p.age, p.gender, p.disease] for p in system.patients]
        patient_csv = convert_to_csv(patient_data, ["ID", "Name", "Age", "Gender", "Disease"])
        st.download_button("⬇️ Download Patients CSV", patient_csv, "patients.csv", "text/csv")

    if system.doctors:
        doctor_data = [[d.person_id, d.name, d.age, d.gender, d.specialty] for d in system.doctors]
        doctor_csv = convert_to_csv(doctor_data, ["ID", "Name", "Age", "Gender", "Specialty"])
        st.download_button("⬇️ Download Doctors CSV", doctor_csv, "doctors.csv", "text/csv")

    if system.appointments:
        appt_data = [[a.appt_id, a.patient.name, a.doctor.name, a.date] for a in system.appointments]
        appt_csv = convert_to_csv(appt_data, ["Appointment ID", "Patient", "Doctor", "Date"])
        st.download_button("⬇️ Download Appointments CSV", appt_csv, "appointments.csv", "text/csv")
