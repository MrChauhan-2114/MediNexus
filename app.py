import streamlit as st
import pandas as pd

from database import get_connection

from datetime import datetime, date

st.set_page_config(
    page_title="MediNexus",
    page_icon="🏥",
    layout="wide"
)

# MediNexus Header
st.markdown("""
<div style="
    padding: 25px 30px;
    border-radius: 15px;
    background: linear-gradient(90deg, #0f4c75, #3282b8);
    color: white;
    margin-bottom: 25px;
">
    <h1 style="margin: 0;">🏥 MediNexus</h1>
    <p style="font-size: 18px; margin-top: 8px;">
        Advanced Healthcare Management & Analytics Platform
    </p>
</div>
""", unsafe_allow_html=True)

try:
    conn = get_connection()
    cursor = conn.cursor()

    # Patients
    cursor.execute("SELECT COUNT(*) FROM patients")
    total_patients = cursor.fetchone()[0]

    # Doctors
    cursor.execute("SELECT COUNT(*) FROM doctors")
    total_doctors = cursor.fetchone()[0]

    # Appointments
    cursor.execute("SELECT COUNT(*) FROM appointments")
    total_appointments = cursor.fetchone()[0]

    # Revenue
    cursor.execute("SELECT COALESCE(SUM(total_amount), 0) FROM billing")
    total_Revenue = cursor.fetchone()[0]

    cursor.close()
    conn.close()

except Exception as e:
    total_patients = 0
    total_doctors = 0
    total_appointments = 0
    total_Revenue = 0
    st.error(f"Database Error: {e}") 

# Premium Dashboard Cards

revenue_crore = total_Revenue / 10000000

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div style="
        background:white;
        padding:25px;
        border-radius:15px;
        border:1px solid #e5e7eb;
        box-shadow:0 4px 15px rgba(0,0,0,0.08);
        text-align:center;
    ">
        <div style="font-size:30px;">👥</div>
        <div style="color:#64748b;font-size:15px;">Total Patients</div>
        <div style="font-size:30px;font-weight:700;color:#111827;">{total_patients:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="
        background:white;
        padding:25px;
        border-radius:15px;
        border:1px solid #e5e7eb;
        box-shadow:0 4px 15px rgba(0,0,0,0.08);
        text-align:center;
    ">
        <div style="font-size:30px;">👨‍⚕️</div>
        <div style="color:#64748b;font-size:15px;">Total Doctors</div>
        <div style="font-size:30px;font-weight:700;color:#111827;">{total_doctors:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="
        background:white;
        padding:25px;
        border-radius:15px;
        border:1px solid #e5e7eb;
        box-shadow:0 4px 15px rgba(0,0,0,0.08);
        text-align:center;
    ">
        <div style="font-size:30px;">📅</div>
        <div style="color:#64748b;font-size:15px;">Appointments</div>
        <div style="font-size:30px;font-weight:700;color:#111827;">{total_appointments:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="
        background:white;
        padding:25px;
        border-radius:15px;
        border:1px solid #e5e7eb;
        box-shadow:0 4px 15px rgba(0,0,0,0.08);
        text-align:center;
    ">
        <div style="font-size:30px;">💰</div>
        <div style="color:#64748b;font-size:15px;">Total Revenue</div>
        <div style="font-size:30px;font-weight:700;color:#111827;">₹{revenue_crore:,.2f} Cr</div>
    </div>
    """, unsafe_allow_html=True)



st.markdown("---")




# Navigation
st.sidebar.markdown("""
<div style="
    padding: 18px 10px;
    margin-bottom: 20px;
    text-align: center;
">
    <div style="font-size: 38px;">🏥</div>
    <div style="
        font-size: 25px;
        font-weight: 700;
        color: #2563eb;
    ">
        MediNexus
    </div>
    <div style="
        font-size: 12px;
        color: #64748b;
        margin-top: 4px;
    ">
        Healthcare Management
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧭 Navigation")

menu = st.sidebar.selectbox(
    "Navigate",
    [
        "Dashboard",
        "Patients",
        "Doctors",
        "Appointments",
    #    "Medical Records",
        "Prescriptions",
        "Medicines",
        "Billing",
  #      "Insurance",
     #   "Analytics"
    ]
)

st.write(f"### {menu}")
if menu == "Dashboard":

        # Appointment Analytics
    st.markdown("## 📊 Appointment Analytics")
    st.caption("Appointment status overview")

    try:
        conn = get_connection()

        query = """
        SELECT status, COUNT(*) AS total
        FROM appointments
        GROUP BY status
        ORDER BY total DESC
        """

        appointment_data = pd.read_sql(query, conn)
        conn.close()

        col1, col2 = st.columns([1, 2])

        with col1:
            st.dataframe(
                appointment_data,
                use_container_width=True,
                hide_index=True
            )

        with col2:
            chart_data = appointment_data.set_index("status")
            st.bar_chart(chart_data["total"])

    except Exception as e:
        st.error(f"Unable to load appointment analytics: {e}")


    st.markdown("## 📅 Recent Appointments")
    st.caption("Latest patient appointments from the hospital database")

    try:
        conn = get_connection()

        query = """
         SELECT
            a.appointment_id AS ID,
            p.patient_name AS Patient,
            d.doctor_name AS Doctor,
            a.appointment_date AS Date,
            a.status AS Status
        FROM appointments a
        JOIN patients p
            ON a.patient_id = p.patient_id
        JOIN doctors d
            ON a.doctor_id = d.doctor_id
        ORDER BY a.appointment_date DESC
        LIMIT 10
        """

        recent_appointments = pd.read_sql(query, conn)

        conn.close()

        st.dataframe(
            recent_appointments,
            use_container_width=True,
            hide_index=True
        )

    except Exception as e:
        st.error(f"Unable to load appointments: {e}")

elif menu == "Patients":
    st.write("Patient Management")
    st.markdown("## 👤 Patients")
    st.caption("Patient Management")
    st.markdown("### 🔍 Search Patients")

    search = st.text_input(
        "Search by patient name or city",
        placeholder="Enter patient name or city..."
    )

    try:
        conn = get_connection()

        query = """
        SELECT
            patient_id AS ID,
            patient_name AS Patient,
            date_of_birth AS DOB,
            gender AS Gender,
            city AS City
        FROM patients
        WHERE patient_name LIKE %s
           OR city LIKE %s
        ORDER BY patient_id DESC
        """

        search_value = f"%{search}%"

        patients_data = pd.read_sql(
            query,
            conn,
            params=(search_value, search_value)
        )

        conn.close()

        st.markdown("### 👥 Patient List")

        st.dataframe(
            patients_data,
            use_container_width=True,
            hide_index=True
        )

    except Exception as e:
        st.error(f"Unable to load patients: {e}")

        # =========================================================
    # EDIT PATIENT
    # =========================================================

    st.markdown("### ✏️ Edit Patient")

    edit_search = st.text_input(
        "Search patient to edit",
        placeholder="Enter patient name or patient ID...",
        key="edit_patient_search"
    )

    if edit_search.strip():

        try:
            conn = get_connection()

            edit_search_value = f"%{edit_search.strip()}%"

            edit_patient_query = """
            SELECT
                patient_id,
                patient_name,
                date_of_birth,
                gender,
                city,
                blood_group,
                registration_date
            FROM patients
            WHERE patient_name LIKE %s
               OR CAST(patient_id AS CHAR) LIKE %s
            ORDER BY patient_id DESC
            LIMIT 50
            """

            edit_patients = pd.read_sql(
                edit_patient_query,
                conn,
                params=(edit_search_value, edit_search_value)
            )

            conn.close()

            if not edit_patients.empty:

                edit_patients["display"] = (
                    edit_patients["patient_id"].astype(str)
                    + " - "
                    + edit_patients["patient_name"]
                )

                selected_edit_patient = st.selectbox(
                    "Select patient",
                    edit_patients["display"].tolist(),
                    key="selected_edit_patient"
                )

                selected_edit_patient_id = int(
                    selected_edit_patient.split(" - ")[0]
                )

                selected_patient_data = edit_patients[
                    edit_patients["patient_id"] ==
                    selected_edit_patient_id
                ].iloc[0]

                with st.form("edit_patient_form"):

                    col1, col2 = st.columns(2)

                    with col1:

                        edit_name = st.text_input(
                            "Patient Name",
                            value=str(
                                selected_patient_data["patient_name"]
                            )
                        )

                        edit_dob = st.date_input(
                            "Date of Birth",
                            value=pd.to_datetime(
                                selected_patient_data["date_of_birth"]
                            ).date()
                        )

                        gender_options = [
                            "Male",
                            "Female",
                            "Other"
                        ]

                        current_gender = str(
                            selected_patient_data["gender"]
                        )

                        edit_gender = st.selectbox(
                            "Gender",
                            gender_options,
                            index=(
                                gender_options.index(current_gender)
                                if current_gender in gender_options
                                else 0
                            )
                        )

                    with col2:

                        edit_city = st.text_input(
                            "City",
                            value=str(
                                selected_patient_data["city"]
                            )
                        )

                        blood_groups = [
                            "A+", "A-", "B+", "B-",
                            "AB+", "AB-", "O+", "O-"
                        ]

                        current_blood_group = str(
                            selected_patient_data["blood_group"]
                        )

                        edit_blood_group = st.selectbox(
                            "Blood Group",
                            blood_groups,
                            index=(
                                blood_groups.index(
                                    current_blood_group
                                )
                                if current_blood_group in blood_groups
                                else 0
                            )
                        )

                    edit_registration_date = st.date_input(
                        "Registration Date",
                        value=pd.to_datetime(
                            selected_patient_data[
                                "registration_date"
                            ]
                        ).date()
                    )

                    update_patient = st.form_submit_button(
                        "💾 Update Patient"
                    )

                if update_patient:

                    if (
                        edit_name.strip() == ""
                        or edit_city.strip() == ""
                    ):
                        st.warning(
                            "Please enter Patient Name and City."
                        )

                    else:

                        try:
                            conn = get_connection()
                            cursor = conn.cursor()

                            update_query = """
                            UPDATE patients
                            SET
                                patient_name = %s,
                                date_of_birth = %s,
                                gender = %s,
                                city = %s,
                                blood_group = %s,
                                registration_date = %s
                            WHERE patient_id = %s
                            """

                            cursor.execute(
                                update_query,
                                (
                                    edit_name.strip(),
                                    edit_dob,
                                    edit_gender,
                                    edit_city.strip(),
                                    edit_blood_group,
                                    edit_registration_date,
                                    selected_edit_patient_id
                                )
                            )

                            conn.commit()

                            cursor.close()
                            conn.close()

                            st.success(
                                "✅ Patient updated successfully!"
                            )

                            

                        except Exception as e:

                            st.error(
                                f"Unable to update patient: {e}"
                            )

            else:
                st.info(
                    "No patient found. Try another name or ID."
                )

        except Exception as e:

            st.error(
                f"Unable to search patients: {e}"
            )
         

    
    st.markdown("### ➕ Add New Patient")
    

    with st.form("add_patient_form"):

        col1, col2 = st.columns(2)

        with col1:
            patient_name = st.text_input("Patient Name")
            date_of_birth = st.date_input("Date of Birth")
            gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"]
            )

        with col2:
            city = st.text_input("City")
            blood_group = st.selectbox(
                "Blood Group",
                ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
            )
        registration_date = st.date_input("Registration Date")
        
        add_patient = st.form_submit_button( "➕ Add Patient")    
    
    
# Process form submission AFTER the form
    if add_patient:

        if patient_name.strip() == "" or city.strip() == "":
            st.warning("Please enter Patient Name and City.")

        else:
            try:
                conn = get_connection()
                cursor = conn.cursor()

                query = """
                INSERT INTO patients
                (
                    patient_name,
                    date_of_birth,
                    gender,
                    city,
                    blood_group,
                    registration_date
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """

                cursor.execute(
                    query,
                    (
                        patient_name,
                        date_of_birth,
                        gender,
                        city,
                        blood_group,
                        registration_date
                    )
                )

                conn.commit()

                cursor.close()
                conn.close()

                st.success("✅ Patient added successfully!")
            except Exception as e:
                st.error(f"Unable to add patient: {e}")
                

    st.markdown("### 🗑️ Delete Patient")

    delete_search = st.text_input(
        "Search patient to delete",
        placeholder="Enter patient name or patient ID...",
        key="delete_patient_search"
    )

    if delete_search.strip():

        try:
            conn = get_connection()

            delete_search_value = f"%{delete_search.strip()}%"

            delete_patient_query = """
            SELECT
                patient_id,
                patient_name,
                city,
                gender
            FROM patients
            WHERE patient_name LIKE %s
            OR CAST(patient_id AS CHAR) LIKE %s
            ORDER BY patient_id DESC
            LIMIT 50
            """

            delete_patients = pd.read_sql(
                delete_patient_query,
                conn,
                params=(delete_search_value, delete_search_value)
            )

            conn.close()

            if not delete_patients.empty:

                delete_patients["display"] = (
                    delete_patients["patient_id"].astype(str)
                    + " - "
                    + delete_patients["patient_name"]
                    + " - "
                    + delete_patients["city"]
                )

                selected_delete_patient = st.selectbox(
                    "Select patient to delete",
                    delete_patients["display"].tolist(),
                    key="selected_delete_patient"
                )

                selected_delete_patient_id = int(
                    selected_delete_patient.split(" - ")[0]
                )

                st.warning(
                    "⚠️ Deleting a patient is permanent. "
                    "Please confirm before deleting."
                )

                confirm_delete = st.checkbox(
                    "I confirm that I want to delete this patient.",
                    key="confirm_delete_patient"
                )

                if st.button(
                    "🗑️ Delete Patient",
                    key="delete_patient_button"
                ):

                    if not confirm_delete:

                        st.warning(
                            "Please confirm deletion first."
                        )

                    else:

                        try:
                            conn = get_connection()
                            cursor = conn.cursor()

                            # Check linked records
                            check_query = """
                            SELECT
                                (SELECT COUNT(*)
                                 FROM appointments
                                 WHERE patient_id = %s) AS appointments_count,

                                (SELECT COUNT(*)
                                 FROM billing
                                 WHERE patient_id = %s) AS billing_count,

                                (SELECT COUNT(*)
                                FROM medical_records
                                WHERE patient_id = %s) AS records_count,

                                (SELECT COUNT(*)
                                 FROM prescriptions
                                 WHERE patient_id = %s) AS prescriptions_count
                            """

                            cursor.execute(
                                check_query,
                                (
                                    selected_delete_patient_id,
                                    selected_delete_patient_id,
                                    selected_delete_patient_id,
                                    selected_delete_patient_id
                                )
                            )

                            linked_data = cursor.fetchone()

                            if any(linked_data):

                                cursor.close()
                                conn.close()

                                st.error(
                                    "❌ This patient cannot be deleted because "
                                    "linked medical records exist "
                                    "(appointments, billing, medical records, "
                                    "or prescriptions)."
                                )

                            else:

                                delete_query = """
                                DELETE FROM patients
                                WHERE patient_id = %s
                                """

                                cursor.execute(
                                    delete_query,
                                    (selected_delete_patient_id,)
                                )

                                conn.commit()

                                cursor.close()
                                conn.close()

                                st.success(
                                    "✅ Patient deleted successfully!"
                                )

                        except Exception as e:

                            st.error(
                                f"Unable to delete patient: {e}"
                            )

            else:

                st.info(
                    "No patient found. Try another name or ID."
                )

        except Exception as e:

            st.error(
                f"Unable to search patients: {e}"
            ) 

                
 
       
        

    
elif menu == "Doctors":
    

    st.title("👨‍⚕️ Doctors Management")

    # =========================================================
    # LOAD DEPARTMENTS
    # =========================================================
    conn = get_connection()

    try:
        department_query = """
            SELECT
                department_id,
                department_name
            FROM departments
            ORDER BY department_id
        """

        departments_df = pd.read_sql(
            department_query,
            conn
        )

    except Exception as e:

        st.error(f"❌ Error loading departments: {e}")
        departments_df = pd.DataFrame()

    finally:
        conn.close()


    # Create Department Name → Department ID mapping
    if not departments_df.empty:

        department_map = dict(
            zip(
                departments_df["department_name"],
                departments_df["department_id"]
            )
        )

        department_names = departments_df[
            "department_name"
        ].tolist()

    else:

        department_map = {}
        department_names = []


    # =========================================================
    # 1. SEARCH / VIEW DOCTORS
    # =========================================================
    st.subheader("🔍 Search Doctors")

    search_doctor = st.text_input(
        "Search by Doctor Name or Specialization",
        key="search_doctor"
    )

    conn = get_connection()

    try:

        query = """
            SELECT
                d.doctor_id,
                d.doctor_name,
                d.department_id,
                dept.department_name AS department,
                d.specialization,
                d.experience_years,
                d.consultation_fee
            FROM doctors d
            LEFT JOIN departments dept
                ON d.department_id = dept.department_id
            WHERE d.doctor_name LIKE %s
               OR d.specialization LIKE %s
               OR dept.department_name LIKE %s
            ORDER BY d.doctor_id DESC
            LIMIT 100
        """

        search_value = f"%{search_doctor}%"

        doctors_df = pd.read_sql(
            query,
            conn,
            params=(
                search_value,
                search_value,
                search_value
            )
        )

        st.dataframe(
            doctors_df,
            use_container_width=True,
            hide_index=True
        )

    except Exception as e:

        st.error(
            f"❌ Error loading doctors: {e}"
        )

    finally:
        conn.close()


    st.divider()


    # =========================================================
    # 2. ADD NEW DOCTOR
    # =========================================================
    st.subheader("➕ Add New Doctor")

    if not department_names:

        st.error(
            "❌ No departments found. "
            "Please add departments first."
        )

    else:

        with st.form("add_doctor_form"):

            # -------------------------------------------------
            # Doctor Name
            # -------------------------------------------------
            doctor_name = st.text_input(
                "Doctor Name"
            )

            # -------------------------------------------------
            # Specialization
            # -------------------------------------------------
            specialization = st.selectbox(
                "Specialization",
                department_names
            )

            # Automatically get Department ID
            selected_department_id = department_map[
                specialization
            ]

            # -------------------------------------------------
            # Department (Automatic)
            # -------------------------------------------------
            st.text_input(
                "Department",
                value=specialization,
                disabled=True
            )

            # -------------------------------------------------
            # Experience + Fee
            # -------------------------------------------------
            col1, col2 = st.columns(2)

            with col1:

                experience_years = st.number_input(
                    "Experience (Years)",
                    min_value=0,
                    step=1
                )

            with col2:

                consultation_fee = st.number_input(
                    "Consultation Fee",
                    min_value=0.0,
                    step=100.0
                )

            add_doctor = st.form_submit_button(
                "➕ Add Doctor"
            )


        if add_doctor:

            if not doctor_name.strip():

                st.error(
                    "⚠️ Doctor name is required."
                )

            else:

                conn = get_connection()
                cursor = conn.cursor()

                try:

                    query = """
                        INSERT INTO doctors
                        (
                            doctor_name,
                            department_id,
                            specialization,
                            experience_years,
                            consultation_fee
                        )
                        VALUES (%s, %s, %s, %s, %s)
                    """

                    cursor.execute(
                        query,
                        (
                            doctor_name.strip(),
                            selected_department_id,
                            specialization,
                            experience_years,
                            consultation_fee
                        )
                    )

                    conn.commit()

                    st.success(
                        f"✅ Doctor added successfully! "
                        f"Department: {specialization}"
                    )

                except Exception as e:

                    conn.rollback()

                    st.error(
                        f"❌ Error adding doctor: {e}"
                    )

                finally:

                    cursor.close()
                    conn.close()


    st.divider()


    # =========================================================
    # 3. EDIT DOCTOR
    # =========================================================
    st.subheader("✏️ Edit Doctor")

    edit_search = st.text_input(
        "Search Doctor by Name or Doctor ID",
        key="edit_doctor_search"
    )

    if edit_search.strip():

        conn = get_connection()

        try:

            query = """
                SELECT
                    d.doctor_id,
                    d.doctor_name,
                    d.department_id,
                    dept.department_name AS department,
                    d.specialization,
                    d.experience_years,
                    d.consultation_fee
                FROM doctors d
                LEFT JOIN departments dept
                    ON d.department_id = dept.department_id
                WHERE d.doctor_name LIKE %s
                   OR CAST(d.doctor_id AS CHAR) LIKE %s
                ORDER BY d.doctor_id
                LIMIT 50
            """

            search_value = f"%{edit_search}%"

            edit_df = pd.read_sql(
                query,
                conn,
                params=(
                    search_value,
                    search_value
                )
            )

        except Exception as e:

            st.error(
                f"❌ Error searching doctors: {e}"
            )

            edit_df = pd.DataFrame()

        finally:
            conn.close()


        if edit_df.empty:

            st.warning(
                "⚠️ No doctors found."
            )

        else:

            doctor_options = edit_df[
                "doctor_id"
            ].tolist()

            selected_doctor_id = st.selectbox(
                "Select Doctor",
                doctor_options,
                format_func=lambda x:
                    f"Doctor ID {x} - "
                    f"{edit_df.loc[edit_df['doctor_id'] == x, 'doctor_name'].iloc[0]}",
                key="edit_doctor_select"
            )

            selected_doctor = edit_df[
                edit_df["doctor_id"] == selected_doctor_id
            ].iloc[0]


            with st.form("edit_doctor_form"):

                new_doctor_name = st.text_input(
                    "Doctor Name",
                    value=str(
                        selected_doctor["doctor_name"]
                    )
                )


                # -------------------------------------------------
                # Existing specialization
                # -------------------------------------------------
                existing_specialization = str(
                    selected_doctor["specialization"]
                )

                if existing_specialization in department_names:

                    default_index = department_names.index(
                        existing_specialization
                    )

                else:

                    default_index = 0


                new_specialization = st.selectbox(
                    "Specialization",
                    department_names,
                    index=default_index
                )


                # Automatically determine department ID
                new_department_id = department_map[
                    new_specialization
                ]


                # Automatically show department
                st.text_input(
                    "Department",
                    value=new_specialization,
                    disabled=True,
                    key="edit_department_display"
                )


                col1, col2 = st.columns(2)

                with col1:

                    new_experience_years = st.number_input(
                        "Experience (Years)",
                        min_value=0,
                        value=int(
                            selected_doctor["experience_years"]
                        ),
                        step=1
                    )

                with col2:

                    new_consultation_fee = st.number_input(
                        "Consultation Fee",
                        min_value=0.0,
                        value=float(
                            selected_doctor["consultation_fee"]
                        ),
                        step=100.0
                    )


                update_doctor = st.form_submit_button(
                    "💾 Update Doctor"
                )


            if update_doctor:

                if not new_doctor_name.strip():

                    st.error(
                        "⚠️ Doctor name is required."
                    )

                else:

                    conn = get_connection()
                    cursor = conn.cursor()

                    try:

                        query = """
                            UPDATE doctors
                            SET
                                doctor_name = %s,
                                department_id = %s,
                                specialization = %s,
                                experience_years = %s,
                                consultation_fee = %s
                            WHERE doctor_id = %s
                        """

                        cursor.execute(
                            query,
                            (
                                new_doctor_name.strip(),
                                new_department_id,
                                new_specialization,
                                new_experience_years,
                                new_consultation_fee,
                                selected_doctor_id
                            )
                        )

                        conn.commit()

                        st.success(
                            "✅ Doctor updated successfully!"
                        )

                    except Exception as e:

                        conn.rollback()

                        st.error(
                            f"❌ Error updating doctor: {e}"
                        )

                    finally:

                        cursor.close()
                        conn.close()


    st.divider()


    # =========================================================
    # 4. DELETE DOCTOR
    # =========================================================
    st.subheader("🗑️ Delete Doctor")

    delete_search = st.text_input(
        "Search Doctor by Name or Doctor ID",
        key="delete_doctor_search"
    )


    if delete_search.strip():

        conn = get_connection()

        try:

            query = """
                SELECT
                    d.doctor_id,
                    d.doctor_name,
                    d.department_id,
                    dept.department_name AS department,
                    d.specialization,
                    d.experience_years,
                    d.consultation_fee
                FROM doctors d
                LEFT JOIN departments dept
                    ON d.department_id = dept.department_id
                WHERE d.doctor_name LIKE %s
                   OR CAST(d.doctor_id AS CHAR) LIKE %s
                ORDER BY d.doctor_id
                LIMIT 50
            """

            search_value = f"%{delete_search}%"

            delete_df = pd.read_sql(
                query,
                conn,
                params=(
                    search_value,
                    search_value
                )
            )

        except Exception as e:

            st.error(
                f"❌ Error searching doctors: {e}"
            )

            delete_df = pd.DataFrame()

        finally:
            conn.close()


        if delete_df.empty:

            st.warning(
                "⚠️ No doctors found."
            )

        else:

            doctor_options = delete_df[
                "doctor_id"
            ].tolist()

            selected_delete_id = st.selectbox(
                "Select Doctor to Delete",
                doctor_options,
                format_func=lambda x:
                    f"Doctor ID {x} - "
                    f"{delete_df.loc[delete_df['doctor_id'] == x, 'doctor_name'].iloc[0]}",
                key="delete_doctor_select"
            )


            selected_delete_doctor = delete_df[
                delete_df["doctor_id"] == selected_delete_id
            ].iloc[0]


            st.warning(
                f"⚠️ You are about to delete "
                f"Doctor ID {selected_delete_id} - "
                f"{selected_delete_doctor['doctor_name']}"
            )


            confirm_delete = st.checkbox(
                "I confirm that I want to delete this doctor.",
                key="confirm_delete_doctor"
            )


            if st.button(
                "🗑️ Delete Doctor",
                key="delete_doctor_button"
            ):

                if not confirm_delete:

                    st.error(
                        "⚠️ Please confirm the deletion first."
                    )

                else:

                    conn = get_connection()
                    cursor = conn.cursor()

                    try:

                        # -------------------------------------------------
                        # Check Appointments
                        # -------------------------------------------------
                        cursor.execute(
                            """
                            SELECT COUNT(*)
                            FROM appointments
                            WHERE doctor_id = %s
                            """,
                            (selected_delete_id,)
                        )

                        appointment_count = cursor.fetchone()[0]


                        # -------------------------------------------------
                        # Check Medical Records
                        # -------------------------------------------------
                        cursor.execute(
                            """
                            SELECT COUNT(*)
                            FROM medical_records
                            WHERE doctor_id = %s
                            """,
                            (selected_delete_id,)
                        )

                        medical_record_count = cursor.fetchone()[0]


                        # -------------------------------------------------
                        # Check Prescriptions
                        # -------------------------------------------------
                        cursor.execute(
                            """
                            SELECT COUNT(*)
                            FROM prescriptions
                            WHERE doctor_id = %s
                            """,
                            (selected_delete_id,)
                        )

                        prescription_count = cursor.fetchone()[0]


                        total_links = (
                            appointment_count
                            + medical_record_count
                            + prescription_count
                        )


                        if total_links > 0:

                            st.error(
                                "❌ This doctor cannot be deleted "
                                "because records are linked to this doctor."
                            )

                            if appointment_count > 0:

                                st.warning(
                                    f"Appointments linked: "
                                    f"{appointment_count}"
                                )

                            if medical_record_count > 0:

                                st.warning(
                                    f"Medical records linked: "
                                    f"{medical_record_count}"
                                )

                            if prescription_count > 0:

                                st.warning(
                                    f"Prescriptions linked: "
                                    f"{prescription_count}"
                                )


                        else:

                            cursor.execute(
                                """
                                DELETE FROM doctors
                                WHERE doctor_id = %s
                                """,
                                (selected_delete_id,)
                            )

                            conn.commit()

                            st.success(
                                "✅ Doctor deleted successfully!"
                            )

                    except Exception as e:

                        conn.rollback()

                        st.error(
                            f"❌ Error deleting doctor: {e}"
                        )

                    finally:

                        cursor.close()
                        conn.close()
    

elif menu == "Appointments":
 
 # ============================================================
# APPOINTMENTS MODULE
# ============================================================


    st.title("📅 Appointment Management")

    # ========================================================
    # APPOINTMENT SECTION
    # ========================================================

    appointment_section = st.radio(
        "Appointment Section",
        [
            "📋 View Appointments",
            "➕ Add Appointment",
            "✏️ Edit Appointment",
            "🗑️ Delete Appointment"
        ],
        horizontal=True,
        key="appointment_section"
    )


    # ========================================================
    # 1. VIEW APPOINTMENTS
    # ========================================================

    if appointment_section == "📋 View Appointments":

        st.subheader("📋 Appointment Records")

        search_text = st.text_input(
            "🔎 Search Appointment",
            placeholder=(
                "Search by Patient Name, Doctor Name "
                "or Appointment ID..."
            ),
            key="view_appointment_search"
        )

        conn = None

        try:

            conn = get_connection()

            # ------------------------------------------------
            # SEARCH MODE
            # ------------------------------------------------

            if search_text.strip():

                search_text_clean = search_text.strip()

                # If user entered a number, search exact
                # appointment ID first.
                if search_text_clean.isdigit():

                    query = """
                        SELECT
                            a.appointment_id,
                            a.appointment_date,
                            a.appointment_type,
                            a.status,
                            a.reason,

                            p.patient_id,
                            p.patient_name,

                            d.doctor_id,
                            d.doctor_name,
                            d.specialization,

                            dep.department_name

                        FROM appointments a

                        LEFT JOIN patients p
                            ON a.patient_id = p.patient_id

                        LEFT JOIN doctors d
                            ON a.doctor_id = d.doctor_id

                        LEFT JOIN departments dep
                            ON d.department_id = dep.department_id

                        WHERE a.appointment_id = %s

                        ORDER BY
                            a.appointment_id DESC

                        LIMIT 100
                    """

                    appointments_df = pd.read_sql(
                        query,
                        conn,
                        params=(int(search_text_clean),)
                    )

                else:

                    search_value = f"%{search_text_clean}%"

                    query = """
                        SELECT
                            a.appointment_id,
                            a.appointment_date,
                            a.appointment_type,
                            a.status,
                            a.reason,

                            p.patient_id,
                            p.patient_name,

                            d.doctor_id,
                            d.doctor_name,
                            d.specialization,

                            dep.department_name

                        FROM appointments a

                        LEFT JOIN patients p
                            ON a.patient_id = p.patient_id

                        LEFT JOIN doctors d
                            ON a.doctor_id = d.doctor_id

                        LEFT JOIN departments dep
                            ON d.department_id = dep.department_id

                        WHERE
                            p.patient_name LIKE %s
                            OR d.doctor_name LIKE %s

                        ORDER BY
                            a.appointment_date DESC,
                            a.appointment_id DESC

                        LIMIT 100
                    """

                    appointments_df = pd.read_sql(
                        query,
                        conn,
                        params=(
                            search_value,
                            search_value
                        )
                    )

            # ------------------------------------------------
            # NORMAL MODE
            # Only latest 50 records are loaded.
            # ------------------------------------------------

            else:

                query = """
                    SELECT
                        a.appointment_id,
                        a.appointment_date,
                        a.appointment_type,
                        a.status,
                        a.reason,

                        p.patient_id,
                        p.patient_name,

                        d.doctor_id,
                        d.doctor_name,
                        d.specialization,

                        dep.department_name

                    FROM appointments a

                    LEFT JOIN patients p
                        ON a.patient_id = p.patient_id

                    LEFT JOIN doctors d
                        ON a.doctor_id = d.doctor_id

                    LEFT JOIN departments dep
                        ON d.department_id = dep.department_id

                    ORDER BY
                        a.appointment_date DESC,
                        a.appointment_id DESC

                    LIMIT 50
                """

                appointments_df = pd.read_sql(
                    query,
                    conn
                )

        except Exception as e:

            st.error(
                f"❌ Error loading appointments: {e}"
            )

            appointments_df = pd.DataFrame()

        finally:

            if conn is not None:
                conn.close()


        if appointments_df.empty:

            if search_text.strip():

                st.warning(
                    "No appointment found. "
                    "Try another patient name, doctor name "
                    "or appointment ID."
                )

            else:

                st.info(
                    "No appointments found."
                )

        else:

            display_df = appointments_df[
                [
                    "appointment_id",
                    "appointment_date",
                    "patient_id",
                    "patient_name",
                    "doctor_name",
                    "specialization",
                    "department_name",
                    "appointment_type",
                    "status",
                    "reason"
                ]
            ].copy()

            display_df.columns = [
                "Appointment ID",
                "Date",
                "Patient ID",
                "Patient Name",
                "Doctor",
                "Specialization",
                "Department",
                "Appointment Type",
                "Status",
                "Reason"
            ]

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                f"Showing {len(display_df)} appointment record(s)."
            )


    # ========================================================
    # 2. ADD APPOINTMENT
    # ========================================================

    elif appointment_section == "➕ Add Appointment":

        st.subheader("➕ Add New Appointment")

        # ====================================================
        # PATIENT TYPE
        # ====================================================

        patient_mode = st.radio(
            "Patient Type",
            [
                "Existing Patient",
                "New Patient"
            ],
            horizontal=True,
            key="appointment_patient_mode"
        )

        selected_patient_id = None

        # ====================================================
        # EXISTING PATIENT
        # ====================================================

        if patient_mode == "Existing Patient":

            st.markdown("### 👤 Patient Information")

            patient_search = st.text_input(
                "🔎 Search Patient by Name or ID",
                placeholder=(
                    "Enter patient name or patient ID..."
                ),
                key="appointment_patient_search"
            )

            patients_df = pd.DataFrame()

            conn = None

            try:

                conn = get_connection()

                if patient_search.strip():

                    search_value = (
                        f"%{patient_search.strip()}%"
                    )

                    patients_df = pd.read_sql(
                        """
                        SELECT
                            patient_id,
                            patient_name,
                            date_of_birth,
                            gender,
                            city,
                            blood_group
                        FROM patients
                        WHERE
                            patient_name LIKE %s
                            OR CAST(patient_id AS CHAR) LIKE %s
                        ORDER BY patient_name
                        LIMIT 50
                        """,
                        conn,
                        params=(
                            search_value,
                            search_value
                        )
                    )

                else:

                    # Only load a small number when no search
                    # is entered. This prevents loading 100k rows.
                    patients_df = pd.read_sql(
                        """
                        SELECT
                            patient_id,
                            patient_name,
                            date_of_birth,
                            gender,
                            city,
                            blood_group
                        FROM patients
                        ORDER BY patient_id DESC
                        LIMIT 25
                        """,
                        conn
                    )

            except Exception as e:

                st.error(
                    f"❌ Error loading patients: {e}"
                )

            finally:

                if conn is not None:
                    conn.close()


            if patients_df.empty:

                st.warning(
                    "No patient found. "
                    "Please search by patient name or ID."
                )

            else:

                patient_ids = patients_df[
                    "patient_id"
                ].astype(int).tolist()


                def patient_display(patient_id):

                    row = patients_df[
                        patients_df["patient_id"] == patient_id
                    ]

                    if row.empty:
                        return f"Patient ID: {patient_id}"

                    patient_name = row.iloc[0][
                        "patient_name"
                    ]

                    if pd.isna(patient_name):
                        patient_name = "Unknown Patient"

                    return (
                        f"{patient_name} "
                        f"(ID: {patient_id})"
                    )


                selected_patient_id = st.selectbox(
                    "👤 Select Patient",
                    patient_ids,
                    format_func=patient_display,
                    key="appointment_existing_patient"
                )


                # ------------------------------------------------
                # SELECTED PATIENT DETAILS
                # ------------------------------------------------

                selected_patient = patients_df[
                    patients_df["patient_id"]
                    == selected_patient_id
                ].iloc[0]

                st.markdown(
                    "### 👤 Selected Patient Details"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.text_input(
                        "Patient ID",
                        value=str(
                            selected_patient["patient_id"]
                        ),
                        disabled=True,
                        key=(
                            f"selected_patient_id_"
                            f"{selected_patient_id}"
                        )
                    )

                with col2:

                    patient_name_value = (
                        selected_patient["patient_name"]
                    )

                    if pd.isna(patient_name_value):
                        patient_name_value = ""

                    st.text_input(
                        "Patient Name",
                        value=str(patient_name_value),
                        disabled=True,
                        key=(
                            f"selected_patient_name_"
                            f"{selected_patient_id}"
                        )
                    )

                with col3:

                    gender_value = (
                        selected_patient["gender"]
                    )

                    if pd.isna(gender_value):
                        gender_value = ""

                    st.text_input(
                        "Gender",
                        value=str(gender_value),
                        disabled=True,
                        key=(
                            f"selected_patient_gender_"
                            f"{selected_patient_id}"
                        )
                    )

                col1, col2, col3 = st.columns(3)

                with col1:

                    dob_value = (
                        selected_patient["date_of_birth"]
                    )

                    if pd.isna(dob_value):
                        dob_value = ""

                    st.text_input(
                        "Date of Birth",
                        value=str(dob_value),
                        disabled=True,
                        key=(
                            f"selected_patient_dob_"
                            f"{selected_patient_id}"
                        )
                    )

                with col2:

                    city_value = (
                        selected_patient["city"]
                    )

                    if pd.isna(city_value):
                        city_value = ""

                    st.text_input(
                        "City",
                        value=str(city_value),
                        disabled=True,
                        key=(
                            f"selected_patient_city_"
                            f"{selected_patient_id}"
                        )
                    )

                with col3:

                    blood_group_value = (
                        selected_patient["blood_group"]
                    )

                    if pd.isna(blood_group_value):
                        blood_group_value = ""

                    st.text_input(
                        "Blood Group",
                        value=str(blood_group_value),
                        disabled=True,
                        key=(
                            f"selected_patient_blood_"
                            f"{selected_patient_id}"
                        )
                    )


        # ====================================================
        # NEW PATIENT
        # ====================================================

        else:

            st.markdown(
                "### 👤 New Patient Information"
            )

            col1, col2 = st.columns(2)

            with col1:

                new_patient_name = st.text_input(
                    "Patient Name *",
                    key="new_appointment_patient_name"
                )

                new_patient_dob = st.date_input(
                    "Date of Birth *",
                    value=date.today(),
                    min_value=date(1900, 1, 1),
                    max_value=date.today(),
                    key="new_appointment_patient_dob"
                )

                new_patient_gender = st.selectbox(
                    "Gender *",
                    [
                        "Male",
                        "Female",
                        "Other"
                    ],
                    key="new_appointment_patient_gender"
                )

            with col2:

                new_patient_city = st.text_input(
                    "City",
                    key="new_appointment_patient_city"
                )

                new_patient_blood_group = st.selectbox(
                    "Blood Group",
                    [
                        "A+",
                        "A-",
                        "B+",
                        "B-",
                        "AB+",
                        "AB-",
                        "O+",
                        "O-",
                        "Unknown"
                    ],
                    key="new_appointment_patient_blood"
                )


        # ====================================================
        # DOCTOR INFORMATION
        # ====================================================

        st.markdown(
            "### 👨‍⚕️ Doctor Information"
        )

        doctors_df = pd.DataFrame()

        conn = None

        try:

            conn = get_connection()

            doctors_df = pd.read_sql(
                """
                SELECT
                    d.doctor_id,
                    d.doctor_name,
                    d.specialization,
                    d.consultation_fee,
                    d.department_id,
                    dep.department_name

                FROM doctors d

                LEFT JOIN departments dep
                    ON d.department_id = dep.department_id

                ORDER BY d.doctor_name
                """,
                conn
            )

        except Exception as e:

            st.error(
                f"❌ Error loading doctors: {e}"
            )

        finally:

            if conn is not None:
                conn.close()


        selected_doctor_id = None
        selected_doctor = None

        if doctors_df.empty:

            st.warning(
                "No doctors available. "
                "Please add a doctor first."
            )

        else:

            doctor_ids = doctors_df[
                "doctor_id"
            ].astype(int).tolist()


            def doctor_display(doctor_id):

                row = doctors_df[
                    doctors_df["doctor_id"] == doctor_id
                ]

                if row.empty:
                    return f"Doctor ID: {doctor_id}"

                doctor_name = row.iloc[0][
                    "doctor_name"
                ]

                specialization = row.iloc[0][
                    "specialization"
                ]

                if pd.isna(doctor_name):
                    doctor_name = "Unknown Doctor"

                if pd.isna(specialization):
                    specialization = "General"

                return (
                    f"{doctor_name} - "
                    f"{specialization} "
                    f"(ID: {doctor_id})"
                )


            selected_doctor_id = st.selectbox(
                "👨‍⚕️ Select Doctor",
                doctor_ids,
                format_func=doctor_display,
                key="appointment_doctor"
            )


            # =================================================
            # CRITICAL FIX
            # Get department from THE SELECTED DOCTOR
            # =================================================

            selected_doctor = doctors_df[
                doctors_df["doctor_id"]
                == selected_doctor_id
            ].iloc[0]


            selected_department_id = (
                selected_doctor["department_id"]
            )

            selected_department_name = (
                selected_doctor["department_name"]
            )


            if pd.isna(selected_department_name):

                selected_department_name = (
                    "Not Assigned"
                )

            else:

                selected_department_name = str(
                    selected_department_name
                )


            # -------------------------------------------------
            # DYNAMIC KEY IS IMPORTANT
            # This prevents old department such as Surgery
            # from staying in the widget.
            # -------------------------------------------------

            st.text_input(
                "Department",
                value=selected_department_name,
                disabled=True,
                key=(
                    f"appointment_department_"
                    f"{int(selected_doctor_id)}"
                )
            )


            # Optional useful information
            col1, col2 = st.columns(2)

            with col1:

                st.caption(
                    f"Department ID: "
                    f"{int(selected_department_id)}"
                    if not pd.isna(selected_department_id)
                    else "Department ID: Not Assigned"
                )

            with col2:

                consultation_fee = (
                    selected_doctor[
                        "consultation_fee"
                    ]
                )

                if pd.isna(consultation_fee):
                    consultation_fee = 0

                st.caption(
                    f"Consultation Fee: ₹{consultation_fee}"
                )


        # ====================================================
        # APPOINTMENT INFORMATION
        # ====================================================

        st.markdown(
            "### 📅 Appointment Information"
        )

        col1, col2 = st.columns(2)

        with col1:

            appointment_date = st.date_input(
                "Appointment Date *",
                value=date.today(),
                min_value=date.today(),
                key="new_appointment_date"
            )

            appointment_type = st.selectbox(
                "Appointment Type",
                [
                    "General Consultation",
                    "Follow-up",
                    "Emergency",
                    "Routine Check-up",
                    "Specialist Consultation",
                    "Diagnostic",
                    "Surgery Consultation"
                ],
                key="new_appointment_type"
            )

        with col2:

            appointment_status = st.selectbox(
                "Status",
                [
                    "Scheduled",
                    "Confirmed",
                    "Completed",
                    "Cancelled",
                    "No Show"
                ],
                key="new_appointment_status"
            )

            appointment_reason = st.text_area(
                "Reason / Symptoms",
                placeholder=(
                    "Enter reason for appointment..."
                ),
                key="new_appointment_reason"
            )


        # ====================================================
        # CREATE APPOINTMENT
        # ====================================================

        add_appointment = st.button(
            "➕ Create Appointment",
            use_container_width=True,
            key="create_appointment_button"
        )


        if add_appointment:

            # ------------------------------------------------
            # VALIDATION
            # ------------------------------------------------

            if selected_doctor_id is None:

                st.error(
                    "❌ Please select a doctor."
                )

            elif (
                patient_mode == "Existing Patient"
                and selected_patient_id is None
            ):

                st.error(
                    "❌ Please select a patient."
                )

            elif (
                patient_mode == "New Patient"
                and not new_patient_name.strip()
            ):

                st.error(
                    "❌ Please enter the patient name."
                )

            else:

                conn = None
                cursor = None

                try:

                    conn = get_connection()
                    cursor = conn.cursor()


                    # ========================================
                    # EXISTING PATIENT
                    # ========================================

                    if patient_mode == "Existing Patient":

                        cursor.execute(
                            """
                            INSERT INTO appointments
                            (
                                patient_id,
                                doctor_id,
                                appointment_date,
                                appointment_type,
                                status,
                                reason
                            )
                            VALUES
                            (
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s
                            )
                            """,
                            (
                                int(selected_patient_id),
                                int(selected_doctor_id),
                                appointment_date,
                                appointment_type,
                                appointment_status,
                                appointment_reason
                            )
                        )

                        appointment_id = cursor.lastrowid


                    # ========================================
                    # NEW PATIENT
                    # ========================================

                    else:

                        cursor.execute(
                            """
                            INSERT INTO patients
                            (
                                patient_name,
                                date_of_birth,
                                gender,
                                city,
                                blood_group,
                                registration_date
                            )
                            VALUES
                            (
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s
                            )
                            """,
                            (
                                new_patient_name.strip(),
                                new_patient_dob,
                                new_patient_gender,
                                new_patient_city.strip(),
                                new_patient_blood_group,
                                date.today()
                            )
                        )

                        new_patient_id = (
                            cursor.lastrowid
                        )


                        cursor.execute(
                            """
                            INSERT INTO appointments
                            (
                                patient_id,
                                doctor_id,
                                appointment_date,
                                appointment_type,
                                status,
                                reason
                            )
                            VALUES
                            (
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s
                            )
                            """,
                            (
                                int(new_patient_id),
                                int(selected_doctor_id),
                                appointment_date,
                                appointment_type,
                                appointment_status,
                                appointment_reason
                            )
                        )

                        appointment_id = (
                            cursor.lastrowid
                        )


                    conn.commit()

                    st.success(
                        "✅ Appointment created successfully! "
                        f"Appointment ID: {appointment_id}"
                    )

                except Exception as e:

                    if conn is not None:
                        conn.rollback()

                    st.error(
                        f"❌ Error creating appointment: {e}"
                    )

                finally:

                    if cursor is not None:
                        cursor.close()

                    if conn is not None:
                        conn.close()


    # ========================================================
    # 3. EDIT APPOINTMENT
    # ========================================================

    elif appointment_section == "✏️ Edit Appointment":

        st.subheader("✏️ Edit Appointment")

        edit_search = st.text_input(
            "🔎 Search Appointment",
            placeholder=(
                "Patient name, Doctor name "
                "or Appointment ID..."
            ),
            key="edit_appointment_search"
        )

        edit_df = pd.DataFrame()

        if edit_search.strip():

            conn = None

            try:

                conn = get_connection()

                search_text_clean = edit_search.strip()

                if search_text_clean.isdigit():

                    edit_df = pd.read_sql(
                        """
                        SELECT
                            a.appointment_id,
                            a.patient_id,
                            a.doctor_id,
                            a.appointment_date,
                            a.appointment_type,
                            a.status,
                            a.reason,

                            p.patient_name,

                            d.doctor_name,
                            d.specialization,

                            dep.department_name

                        FROM appointments a

                        LEFT JOIN patients p
                            ON a.patient_id = p.patient_id

                        LEFT JOIN doctors d
                            ON a.doctor_id = d.doctor_id

                        LEFT JOIN departments dep
                            ON d.department_id = dep.department_id

                        WHERE a.appointment_id = %s

                        ORDER BY a.appointment_id DESC

                        LIMIT 100
                        """,
                        conn,
                        params=(int(search_text_clean),)
                    )

                else:

                    search_value = (
                        f"%{search_text_clean}%"
                    )

                    edit_df = pd.read_sql(
                        """
                        SELECT
                            a.appointment_id,
                            a.patient_id,
                            a.doctor_id,
                            a.appointment_date,
                            a.appointment_type,
                            a.status,
                            a.reason,

                            p.patient_name,

                            d.doctor_name,
                            d.specialization,

                            dep.department_name

                        FROM appointments a

                        LEFT JOIN patients p
                            ON a.patient_id = p.patient_id

                        LEFT JOIN doctors d
                            ON a.doctor_id = d.doctor_id

                        LEFT JOIN departments dep
                            ON d.department_id = dep.department_id

                        WHERE
                            p.patient_name LIKE %s
                            OR d.doctor_name LIKE %s

                        ORDER BY a.appointment_id DESC

                        LIMIT 100
                        """,
                        conn,
                        params=(
                            search_value,
                            search_value
                        )
                    )

            except Exception as e:

                st.error(
                    f"❌ Error searching appointments: {e}"
                )

            finally:

                if conn is not None:
                    conn.close()


        else:

            st.info(
                "🔎 Enter a patient name, doctor name "
                "or appointment ID to edit an appointment."
            )


        if not edit_df.empty:

            appointment_ids = (
                edit_df["appointment_id"]
                .astype(int)
                .tolist()
            )


            def edit_appointment_display(
                appointment_id
            ):

                row = edit_df[
                    edit_df["appointment_id"]
                    == appointment_id
                ]

                if row.empty:
                    return (
                        f"Appointment ID: "
                        f"{appointment_id}"
                    )

                patient_name = row.iloc[0][
                    "patient_name"
                ]

                doctor_name = row.iloc[0][
                    "doctor_name"
                ]

                if pd.isna(patient_name):
                    patient_name = "Unknown Patient"

                if pd.isna(doctor_name):
                    doctor_name = "Unknown Doctor"

                return (
                    f"#{appointment_id} - "
                    f"{patient_name} → "
                    f"{doctor_name}"
                )


            selected_appointment_id = st.selectbox(
                "Select Appointment",
                appointment_ids,
                format_func=edit_appointment_display,
                key="edit_appointment_selector"
            )


            selected_appointment = edit_df[
                edit_df["appointment_id"]
                == selected_appointment_id
            ].iloc[0]


            # =================================================
            # CURRENT PATIENT
            # =================================================

            st.markdown("### 👤 Patient")

            current_patient_id = int(
                selected_appointment["patient_id"]
            )


            conn = None
            current_patient_df = pd.DataFrame()

            try:

                conn = get_connection()

                current_patient_df = pd.read_sql(
                    """
                    SELECT
                        patient_id,
                        patient_name,
                        date_of_birth,
                        gender,
                        city,
                        blood_group
                    FROM patients
                    WHERE patient_id = %s
                    """,
                    conn,
                    params=(current_patient_id,)
                )

            except Exception as e:

                st.error(
                    f"❌ Error loading current patient: {e}"
                )

            finally:

                if conn is not None:
                    conn.close()


            if not current_patient_df.empty:

                current_patient = (
                    current_patient_df.iloc[0]
                )

                current_patient_name = (
                    current_patient["patient_name"]
                )

                if pd.isna(current_patient_name):
                    current_patient_name = (
                        "Unknown Patient"
                    )

                st.info(
                    f"Current Patient: "
                    f"{current_patient_name} "
                    f"(ID: {current_patient_id})"
                )


            # ------------------------------------------------
            # Optional patient change
            # ------------------------------------------------

            change_patient_search = st.text_input(
                "🔎 Change Patient "
                "(optional - search by name or ID)",
                placeholder=(
                    "Leave empty to keep current patient..."
                ),
                key=(
                    f"edit_patient_search_"
                    f"{selected_appointment_id}"
                )
            )


            edit_patient_id = current_patient_id


            if change_patient_search.strip():

                conn = None
                patient_search_df = pd.DataFrame()

                try:

                    conn = get_connection()

                    search_value = (
                        f"%{change_patient_search.strip()}%"
                    )

                    patient_search_df = pd.read_sql(
                        """
                        SELECT
                            patient_id,
                            patient_name
                        FROM patients
                        WHERE
                            patient_name LIKE %s
                            OR CAST(patient_id AS CHAR) LIKE %s
                        ORDER BY patient_name
                        LIMIT 50
                        """,
                        conn,
                        params=(
                            search_value,
                            search_value
                        )
                    )

                except Exception as e:

                    st.error(
                        f"❌ Error searching patients: {e}"
                    )

                finally:

                    if conn is not None:
                        conn.close()


                if not patient_search_df.empty:

                    patient_ids = (
                        patient_search_df["patient_id"]
                        .astype(int)
                        .tolist()
                    )


                    def edit_patient_display(
                        patient_id
                    ):

                        row = patient_search_df[
                            patient_search_df["patient_id"]
                            == patient_id
                        ]

                        if row.empty:
                            return (
                                f"Patient ID: "
                                f"{patient_id}"
                            )

                        name = row.iloc[0][
                            "patient_name"
                        ]

                        if pd.isna(name):
                            name = "Unknown Patient"

                        return (
                            f"{name} "
                            f"(ID: {patient_id})"
                        )


                    edit_patient_id = st.selectbox(
                        "Select New Patient",
                        patient_ids,
                        format_func=edit_patient_display,
                        key=(
                            f"edit_patient_selector_"
                            f"{selected_appointment_id}"
                        )
                    )

                else:

                    st.warning(
                        "No matching patient found. "
                        "Current patient will be retained."
                    )


            # =================================================
            # DOCTOR
            # =================================================

            st.markdown("### 👨‍⚕️ Doctor")

            conn = None
            doctors_df = pd.DataFrame()

            try:

                conn = get_connection()

                doctors_df = pd.read_sql(
                    """
                    SELECT
                        d.doctor_id,
                        d.doctor_name,
                        d.specialization,
                        d.department_id,
                        dep.department_name

                    FROM doctors d

                    LEFT JOIN departments dep
                        ON d.department_id = dep.department_id

                    ORDER BY d.doctor_name
                    """,
                    conn
                )

            except Exception as e:

                st.error(
                    f"❌ Error loading doctors: {e}"
                )

            finally:

                if conn is not None:
                    conn.close()


            edit_doctor_id = None

            if not doctors_df.empty:

                doctor_ids = (
                    doctors_df["doctor_id"]
                    .astype(int)
                    .tolist()
                )

                current_doctor_id = int(
                    selected_appointment["doctor_id"]
                )


                if current_doctor_id in doctor_ids:

                    doctor_index = doctor_ids.index(
                        current_doctor_id
                    )

                else:

                    doctor_index = 0


                def edit_doctor_display(
                    doctor_id
                ):

                    row = doctors_df[
                        doctors_df["doctor_id"]
                        == doctor_id
                    ]

                    if row.empty:
                        return (
                            f"Doctor ID: "
                            f"{doctor_id}"
                        )

                    name = row.iloc[0][
                        "doctor_name"
                    ]

                    specialization = row.iloc[0][
                        "specialization"
                    ]

                    if pd.isna(name):
                        name = "Unknown Doctor"

                    if pd.isna(specialization):
                        specialization = "General"

                    return (
                        f"{name} - "
                        f"{specialization} "
                        f"(ID: {doctor_id})"
                    )


                edit_doctor_id = st.selectbox(
                    "Select Doctor",
                    doctor_ids,
                    index=doctor_index,
                    format_func=edit_doctor_display,
                    key=(
                        f"edit_appointment_doctor_"
                        f"{selected_appointment_id}"
                    )
                )


                # =============================================
                # CRITICAL DEPARTMENT FIX FOR EDIT
                # =============================================

                selected_edit_doctor = doctors_df[
                    doctors_df["doctor_id"]
                    == edit_doctor_id
                ].iloc[0]


                edit_department = (
                    selected_edit_doctor[
                        "department_name"
                    ]
                )


                if pd.isna(edit_department):

                    edit_department = "Not Assigned"

                else:

                    edit_department = str(
                        edit_department
                    )


                st.text_input(
                    "Department",
                    value=edit_department,
                    disabled=True,
                    key=(
                        f"edit_department_"
                        f"{selected_appointment_id}_"
                        f"{int(edit_doctor_id)}"
                    )
                )


            # =================================================
            # APPOINTMENT DETAILS
            # =================================================

            st.markdown(
                "### 📅 Appointment Details"
            )


            current_date = selected_appointment[
                "appointment_date"
            ]


            if pd.isna(current_date):

                current_date = date.today()

            elif hasattr(current_date, "date"):

                current_date = current_date.date()


            appointment_types = [
                "General Consultation",
                "Follow-up",
                "Emergency",
                "Routine Check-up",
                "Specialist Consultation",
                "Diagnostic",
                "Surgery Consultation"
            ]


            current_type = selected_appointment[
                "appointment_type"
            ]


            if pd.isna(current_type):

                current_type = appointment_types[0]

            else:

                current_type = str(current_type)


            if current_type not in appointment_types:

                appointment_types.append(
                    current_type
                )


            status_options = [
                "Scheduled",
                "Confirmed",
                "Completed",
                "Cancelled",
                "No Show"
            ]


            current_status = selected_appointment[
                "status"
            ]


            if pd.isna(current_status):

                current_status = status_options[0]

            else:

                current_status = str(
                    current_status
                )


            if current_status not in status_options:

                status_options.append(
                    current_status
                )


            current_reason = selected_appointment[
                "reason"
            ]


            if pd.isna(current_reason):

                current_reason = ""

            else:

                current_reason = str(
                    current_reason
                )


            col1, col2 = st.columns(2)

            with col1:

                edit_date = st.date_input(
                    "Appointment Date",
                    value=current_date,
                    key=(
                        f"edit_appointment_date_"
                        f"{selected_appointment_id}"
                    )
                )

                edit_type = st.selectbox(
                    "Appointment Type",
                    appointment_types,
                    index=appointment_types.index(
                        current_type
                    ),
                    key=(
                        f"edit_appointment_type_"
                        f"{selected_appointment_id}"
                    )
                )

            with col2:

                edit_status = st.selectbox(
                    "Status",
                    status_options,
                    index=status_options.index(
                        current_status
                    ),
                    key=(
                        f"edit_appointment_status_"
                        f"{selected_appointment_id}"
                    )
                )

                edit_reason = st.text_area(
                    "Reason / Symptoms",
                    value=current_reason,
                    key=(
                        f"edit_appointment_reason_"
                        f"{selected_appointment_id}"
                    )
                )


            # =================================================
            # UPDATE
            # =================================================

            update_appointment = st.button(
                "💾 Update Appointment",
                use_container_width=True,
                key=(
                    f"update_appointment_"
                    f"{selected_appointment_id}"
                )
            )


            if update_appointment:

                if edit_doctor_id is None:

                    st.error(
                        "❌ Please select a doctor."
                    )

                else:

                    conn = None
                    cursor = None

                    try:

                        conn = get_connection()
                        cursor = conn.cursor()


                        cursor.execute(
                            """
                            UPDATE appointments

                            SET
                                patient_id = %s,
                                doctor_id = %s,
                                appointment_date = %s,
                                appointment_type = %s,
                                status = %s,
                                reason = %s

                            WHERE appointment_id = %s
                            """,
                            (
                                int(edit_patient_id),
                                int(edit_doctor_id),
                                edit_date,
                                edit_type,
                                edit_status,
                                edit_reason,
                                int(
                                    selected_appointment_id
                                )
                            )
                        )


                        conn.commit()


                        st.success(
                            f"✅ Appointment "
                            f"#{selected_appointment_id} "
                            f"updated successfully."
                        )

                    except Exception as e:

                        if conn is not None:
                            conn.rollback()

                        st.error(
                            f"❌ Error updating appointment: {e}"
                        )

                    finally:

                        if cursor is not None:
                            cursor.close()

                        if conn is not None:
                            conn.close()


        elif edit_search.strip():

            st.info(
                "No appointment found. "
                "Try another search."
            )


    # ========================================================
    # 4. DELETE APPOINTMENT
    # ========================================================

    else:

        st.subheader("🗑️ Delete Appointment")

        delete_search = st.text_input(
            "🔎 Search Appointment to Delete",
            placeholder=(
                "Patient name, Doctor name "
                "or Appointment ID..."
            ),
            key="delete_appointment_search"
        )


        delete_df = pd.DataFrame()


        if delete_search.strip():

            conn = None

            try:

                conn = get_connection()

                search_text_clean = (
                    delete_search.strip()
                )


                if search_text_clean.isdigit():

                    delete_df = pd.read_sql(
                        """
                        SELECT
                            a.appointment_id,
                            a.patient_id,
                            a.doctor_id,
                            a.appointment_date,
                            a.appointment_type,
                            a.status,
                            a.reason,

                            p.patient_name,

                            d.doctor_name,
                            d.specialization,

                            dep.department_name

                        FROM appointments a

                        LEFT JOIN patients p
                            ON a.patient_id = p.patient_id

                        LEFT JOIN doctors d
                            ON a.doctor_id = d.doctor_id

                        LEFT JOIN departments dep
                            ON d.department_id = dep.department_id

                        WHERE a.appointment_id = %s

                        LIMIT 100
                        """,
                        conn,
                        params=(int(search_text_clean),)
                    )

                else:

                    search_value = (
                        f"%{search_text_clean}%"
                    )

                    delete_df = pd.read_sql(
                        """
                        SELECT
                            a.appointment_id,
                            a.patient_id,
                            a.doctor_id,
                            a.appointment_date,
                            a.appointment_type,
                            a.status,
                            a.reason,

                            p.patient_name,

                            d.doctor_name,
                            d.specialization,

                            dep.department_name

                        FROM appointments a

                        LEFT JOIN patients p
                            ON a.patient_id = p.patient_id

                        LEFT JOIN doctors d
                            ON a.doctor_id = d.doctor_id

                        LEFT JOIN departments dep
                            ON d.department_id = dep.department_id

                        WHERE
                            p.patient_name LIKE %s
                            OR d.doctor_name LIKE %s

                        ORDER BY a.appointment_id DESC

                        LIMIT 100
                        """,
                        conn,
                        params=(
                            search_value,
                            search_value
                        )
                    )

            except Exception as e:

                st.error(
                    f"❌ Error searching appointments: {e}"
                )

            finally:

                if conn is not None:
                    conn.close()


        else:

            st.info(
                "🔎 Enter a patient name, doctor name "
                "or appointment ID to find an appointment."
            )


        if not delete_df.empty:

            appointment_ids = (
                delete_df["appointment_id"]
                .astype(int)
                .tolist()
            )


            def delete_appointment_display(
                appointment_id
            ):

                row = delete_df[
                    delete_df["appointment_id"]
                    == appointment_id
                ]

                if row.empty:

                    return (
                        f"Appointment ID: "
                        f"{appointment_id}"
                    )

                patient_name = row.iloc[0][
                    "patient_name"
                ]

                doctor_name = row.iloc[0][
                    "doctor_name"
                ]

                if pd.isna(patient_name):
                    patient_name = "Unknown Patient"

                if pd.isna(doctor_name):
                    doctor_name = "Unknown Doctor"

                return (
                    f"#{appointment_id} - "
                    f"{patient_name} → "
                    f"{doctor_name}"
                )


            selected_delete_id = st.selectbox(
                "Select Appointment",
                appointment_ids,
                format_func=delete_appointment_display,
                key="delete_appointment_selector"
            )


            selected_delete = delete_df[
                delete_df["appointment_id"]
                == selected_delete_id
            ].iloc[0]


            # =================================================
            # SHOW APPOINTMENT
            # =================================================

            st.markdown(
                "### ⚠️ Appointment Selected for Deletion"
            )


            col1, col2, col3 = st.columns(3)

            with col1:

                st.write(
                    "**Appointment ID:**",
                    selected_delete["appointment_id"]
                )

            with col2:

                st.write(
                    "**Patient:**",
                    selected_delete["patient_name"]
                )

            with col3:

                st.write(
                    "**Doctor:**",
                    selected_delete["doctor_name"]
                )


            col1, col2, col3 = st.columns(3)

            with col1:

                st.write(
                    "**Department:**",
                    selected_delete["department_name"]
                )

            with col2:

                st.write(
                    "**Date:**",
                    selected_delete["appointment_date"]
                )

            with col3:

                st.write(
                    "**Status:**",
                    selected_delete["status"]
                )


            st.write(
                "**Appointment Type:**",
                selected_delete["appointment_type"]
            )


            if not pd.isna(
                selected_delete["reason"]
            ):

                st.write(
                    "**Reason:**",
                    selected_delete["reason"]
                )


            # =================================================
            # DELETE BUTTON
            # =================================================

            delete_appointment = st.button(
                "🗑️ Delete Appointment",
                use_container_width=True,
                key=(
                    f"delete_appointment_button_"
                    f"{selected_delete_id}"
                )
            )


            if delete_appointment:

                conn = None
                cursor = None

                try:

                    conn = get_connection()
                    cursor = conn.cursor()

                    appointment_id = int(
                        selected_delete_id
                    )


                    # =========================================
                    # CHECK BILLING
                    # =========================================

                    cursor.execute(
                        """
                        SELECT COUNT(*)
                        FROM billing
                        WHERE appointment_id = %s
                        """,
                        (appointment_id,)
                    )

                    billing_count = (
                        cursor.fetchone()[0]
                    )


                    # =========================================
                    # CHECK MEDICAL RECORDS
                    # =========================================

                    cursor.execute(
                        """
                        SELECT COUNT(*)
                        FROM medical_records
                        WHERE appointment_id = %s
                        """,
                        (appointment_id,)
                    )

                    medical_count = (
                        cursor.fetchone()[0]
                    )


                    # =========================================
                    # CHECK PRESCRIPTIONS
                    # =========================================

                    cursor.execute(
                        """
                        SELECT COUNT(*)
                        FROM prescriptions
                        WHERE appointment_id = %s
                        """,
                        (appointment_id,)
                    )

                    prescription_count = (
                        cursor.fetchone()[0]
                    )


                    # =========================================
                    # PREVENT DELETE IF LINKED
                    # =========================================

                    if billing_count > 0:

                        st.error(
                            "❌ Cannot delete this appointment "
                            "because it is linked to billing records."
                        )

                    elif medical_count > 0:

                        st.error(
                            "❌ Cannot delete this appointment "
                            "because it is linked to medical records."
                        )

                    elif prescription_count > 0:

                        st.error(
                            "❌ Cannot delete this appointment "
                            "because it is linked to prescriptions."
                        )

                    else:

                        cursor.execute(
                            """
                            DELETE FROM appointments
                            WHERE appointment_id = %s
                            """,
                            (appointment_id,)
                        )

                        conn.commit()

                        st.success(
                            f"✅ Appointment "
                            f"#{appointment_id} "
                            f"deleted successfully."
                        )

                except Exception as e:

                    if conn is not None:
                        conn.rollback()

                    st.error(
                        f"❌ Error deleting appointment: {e}"
                    )

                finally:

                    if cursor is not None:
                        cursor.close()

                    if conn is not None:
                        conn.close()


        elif delete_search.strip():

            st.info(
                "No appointment found. "
                "Try another patient name, "
                "doctor name or appointment ID."
            )
 
 
 
#elif menu == "Medical Records":
  #  st.write("Medical Records")

elif menu == "Prescriptions":
    st.write("Prescription Management")

elif menu == "Medicines":
    st.write("Medicine Management")

elif menu == "Billing":
    st.write("Billing & Payments")

#elif menu == "Insurance":
  #  st.write("Insurance Management")

#elif menu == "Analytics":
 #   st.write("Advanced Healthcare Analytics")