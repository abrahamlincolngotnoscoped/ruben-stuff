import mysql.connector
from mysql.connector import Error
import prettytable


def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="HospitalDB"
        )
        return connection
    except Error as e:
        print("Error connecting to the database:", e)
        return None


def create_tables(connection):
    cursor = connection.cursor()
    
    tables = [
    """
    CREATE TABLE IF NOT EXISTS Patients (
        PatientID INT AUTO_INCREMENT PRIMARY KEY,
        FirstName VARCHAR(50),
        LastName VARCHAR(50),
        DateOfBirth DATE,
        Gender ENUM('Male', 'Female', 'Other'),
        Allergies TEXT,
        MedicalHistory TEXT,
        RoomNumber INT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Admissions (
        AdmissionID INT AUTO_INCREMENT PRIMARY KEY,
        PatientID INT,
        AdmissionDate DATE,
        DischargeDate DATE,
        AdmittingPhysician VARCHAR(100),
        ReasonForAdmission TEXT,
        FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS MedicalStaff (
        StaffID INT AUTO_INCREMENT PRIMARY KEY,
        FirstName VARCHAR(50),
        LastName VARCHAR(50),
        Role VARCHAR(100),
        LicensingInfo VARCHAR(100),
        WorkSchedule TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Policies (
        PolicyID INT AUTO_INCREMENT PRIMARY KEY,
        PolicyName VARCHAR(100),
        PolicyText TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Billing (
        BillingID INT AUTO_INCREMENT PRIMARY KEY,
        PatientID INT,
        InsuranceProvider VARCHAR(100),
        BillingAmount DECIMAL(10, 2),
        PaymentStatus ENUM('Paid', 'Unpaid'),
        FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
    )
    """,
    """
CREATE TABLE IF NOT EXISTS MedicalImages (
    ImageID INT AUTO_INCREMENT PRIMARY KEY,
    PatientID INT,
    ImageType VARCHAR(50),
    ImageData LONGBLOB,
    Report TEXT,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
)
""",
"""
CREATE TABLE IF NOT EXISTS LabResults (
    ResultID INT AUTO_INCREMENT PRIMARY KEY,
    PatientID INT,
    TestType VARCHAR(50),
    ResultValue VARCHAR(100),
    TestDate DATE,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
)
""",
"""
CREATE TABLE IF NOT EXISTS Medications (
    MedicationID INT AUTO_INCREMENT PRIMARY KEY,
    PatientID INT,
    MedicationName VARCHAR(100),
    Dosage VARCHAR(50),
    PrescriptionDate DATE,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
)
""",
"""
CREATE TABLE IF NOT EXISTS Appointments (
    AppointmentID INT AUTO_INCREMENT PRIMARY KEY,
    PatientID INT,
    AppointmentDate DATETIME,
    PhysicianName VARCHAR(100),
    Status ENUM('Scheduled', 'Canceled', 'Attended'),
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
)
""",
"""
CREATE TABLE IF NOT EXISTS Inventory (
    ItemID INT AUTO_INCREMENT PRIMARY KEY,
    ItemName VARCHAR(100),
    Quantity INT,
    UnitPrice DECIMAL(10, 2),
    Description TEXT
)
""",
"""
CREATE TABLE IF NOT EXISTS Suppliers (
    SupplierID INT AUTO_INCREMENT PRIMARY KEY,
    SupplierName VARCHAR(100),
    ContactName VARCHAR(100),
    Phone VARCHAR(20),
    Email VARCHAR(100)
)
"""
]


    for table in tables:
        cursor.execute(table)
    
    cursor.close()


def check_and_create_database_tables():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
        )

        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS HospitalDB")
        cursor.close()

        connection.database = "HospitalDB"
        create_tables(connection)
        return connection
    except Error as e:
        print("Error connecting to the database:", e)
        return None



def display_patient_info(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Patients")
    patients = cursor.fetchall()
    cursor.close()

    table = PrettyTable()
    table.field_names = ["Patient ID", "First Name", "Last Name", "Date of Birth", "Gender", "Allergies", "Medical History", "Room Number"]

    for patient in patients:
        table.add_row([patient[0], patient[1], patient[2], patient[3], patient[4], patient[5], patient[6], patient[7]])

    print("Patient Information")
    print(table)



    for patient in patients:
        print(f"Patient ID: {patient[0]}")
        print(f"Name: {patient[1]} {patient[2]}")
        print(f"Date of Birth: {patient[3]}")
        print(f"Gender: {patient[4]}")
        print(f"Allergies: {patient[5]}")
        print(f"Medical History: {patient[6]}\n")


def display_admissions(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Admissions")
    admissions = cursor.fetchall()
    cursor.close()

    table = prettytable.PrettyTable(["Admission ID", "Patient ID", "Admission Date", "Discharge Date", "Admitting Physician", "Reason for Admission"])
    for admission in admissions:
        table.add_row(admission)

    print(table)

    for admission in admissions:
        print(f"Admission ID: {admission[0]}")
        print(f"Patient ID: {admission[1]}")
        print(f"Admission Date: {admission[2]}")
        print(f"Discharge Date: {admission[3]}")
        print(f"Admitting Physician: {admission[4]}")
        print(f"Reason for Admission: {admission[5]}\n")


from prettytable import PrettyTable

def view_medical_staff_info(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM MedicalStaff")
    staff = cursor.fetchall()
    cursor.close()

    table = PrettyTable()
    table.field_names = ["Staff ID", "First Name", "Last Name", "Role", "Licensing Info", "Work Schedule"]

    for staff_member in staff:
        table.add_row([staff_member[0], staff_member[1], staff_member[2], staff_member[3], staff_member[4], staff_member[5]])

    print("Medical Staff Information")
    print(table)



def view_policies(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Policies")
    policies = cursor.fetchall()
    cursor.close()

    table = prettytable.PrettyTable(["Policy ID", "Policy Name", "Policy Text"])
    for policy in policies:
        table.add_row(policy)

    print(table)


def edit_policy(connection, policy_id, policy_name, policy_text):
    cursor = connection.cursor()
    sql = """
        UPDATE Policies
        SET PolicyName = %s, PolicyText = %s
        WHERE PolicyID = %s
    """
    values = (policy_name, policy_text, policy_id)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


def remove_policy(connection, policy_id):
    cursor = connection.cursor()
    sql = "DELETE FROM Policies WHERE PolicyID = %s"
    cursor.execute(sql, (policy_id,))
    connection.commit()
    cursor.close()


def assign_room(connection, patient_id, room_number):
    cursor = connection.cursor()
    sql = "UPDATE Patients SET RoomNumber = %s WHERE PatientID = %s"
    values = (room_number, patient_id)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


def view_room_assignments(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT PatientID, FirstName, LastName, RoomNumber FROM Patients WHERE RoomNumber IS NOT NULL")
    room_assignments = cursor.fetchall()
    cursor.close()

    table = prettytable.PrettyTable(["Patient ID", "First Name", "Last Name", "Room Number"])
    for assignment in room_assignments:
        table.add_row(assignment)

    print(table)

    for assignment in room_assignments:
        print(f"Patient ID: {assignment[0]}")
        print(f"Name: {assignment[1]} {assignment[2]}")
        print(f"Room Number: {assignment[3]}\n")


def edit_admission(connection, admission_id, patient_id, admission_date, discharge_date, admitting_physician, reason_for_admission):
    cursor = connection.cursor()
    sql = """
        UPDATE Admissions
        SET PatientID = %s, AdmissionDate = %s, DischargeDate = %s, AdmittingPhysician = %s, ReasonForAdmission = %s
        WHERE AdmissionID = %s
    """
    values = (patient_id, admission_date, discharge_date, admitting_physician, reason_for_admission, admission_id)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


def add_billing(connection, patient_id, insurance_provider, billing_amount, payment_status):
    cursor = connection.cursor()
    sql = """
        INSERT INTO Billing (PatientID, InsuranceProvider, BillingAmount, PaymentStatus)
        VALUES (%s, %s, %s, %s)
    """
    values = (patient_id, insurance_provider, billing_amount, payment_status)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


def edit_billing(connection, billing_id, insurance_provider, billing_amount, payment_status):
    cursor = connection.cursor()
    sql = """
        UPDATE Billing
        SET InsuranceProvider = %s, BillingAmount = %s, PaymentStatus = %s
        WHERE BillingID = %s
    """
    values = (insurance_provider, billing_amount, payment_status, billing_id)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


def remove_billing(connection, billing_id):
    cursor = connection.cursor()
    sql = "DELETE FROM Billing WHERE BillingID = %s"
    cursor.execute(sql, (billing_id,))
    connection.commit()
    cursor.close()


def add_medical_image(connection, patient_id, image_type, image_data, report):
    cursor = connection.cursor()
    sql = """
        INSERT INTO MedicalImages (PatientID, ImageType, ImageData, Report)
        VALUES (%s, %s, %s, %s)
    """
    values = (patient_id, image_type, image_data, report)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


def edit_medical_image(connection, image_id, image_type, report):
    cursor = connection.cursor()
    sql = """
        UPDATE MedicalImages
        SET ImageType = %s, Report = %s
        WHERE ImageID = %s
    """
    values = (image_type, report, image_id)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


def remove_medical_image(connection, image_id):
    cursor = connection.cursor()
    sql = "DELETE FROM MedicalImages WHERE ImageID = %s"
    cursor.execute(sql, (image_id,))
    connection.commit()
    cursor.close()


def add_lab_result(connection, patient_id, test_type, result_value, test_date):
    cursor = connection.cursor()
    sql = """
        INSERT INTO LabResults (PatientID, TestType, ResultValue, TestDate)
        VALUES (%s, %s, %s, %s)
    """
    values = (patient_id, test_type, result_value, test_date)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


def edit_lab_result(connection, result_id, test_type, result_value):
    cursor = connection.cursor()
    sql = """
        UPDATE LabResults
        SET TestType = %s, ResultValue = %s
        WHERE ResultID = %s
    """
    values = (test_type, result_value, result_id)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


def remove_lab_result(connection, result_id):
    cursor = connection.cursor()
    sql = "DELETE FROM LabResults WHERE ResultID = %s"
    cursor.execute(sql, (result_id,))
    connection.commit()
    cursor.close()


def add_medication(connection, patient_id, medication_name, dosage, prescription_date):
    cursor = connection.cursor()
    sql = """
        INSERT INTO Medications (PatientID, MedicationName, Dosage, PrescriptionDate)
        VALUES (%s, %s, %s, %s)
    """
    values = (patient_id, medication_name, dosage, prescription_date)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


def edit_medication(connection, medication_id, medication_name, dosage):
    cursor = connection.cursor()
    sql = """
        UPDATE Medications
        SET MedicationName = %s, Dosage = %s
        WHERE MedicationID = %s
    """
    values = (medication_name, dosage, medication_id)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()



def remove_medication(connection, medication_id):
    cursor = connection.cursor()
    sql = "DELETE FROM Medications WHERE MedicationID = %s"
    cursor.execute(sql, (medication_id,))
    connection.commit()
    cursor.close()


def schedule_appointment(connection, patient_id, staff_id, appointment_date, appointment_time, appointment_type):
    cursor = connection.cursor()
    sql = """
        INSERT INTO Appointments (PatientID, StaffID, AppointmentDate, AppointmentTime, AppointmentType)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (patient_id, staff_id, appointment_date, appointment_time, appointment_type)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


def edit_appointment(connection, appointment_id, appointment_date, appointment_time, appointment_type):
    cursor = connection.cursor()
    sql = """
        UPDATE Appointments
        SET AppointmentDate = %s, AppointmentTime = %s, AppointmentType = %s
        WHERE AppointmentID = %s
    """
    values = (appointment_date, appointment_time, appointment_type, appointment_id)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


def cancel_appointment(connection, appointment_id):
    cursor = connection.cursor()
    sql = "DELETE FROM Appointments WHERE AppointmentID = %s"
    cursor.execute(sql, (appointment_id,))
    connection.commit()
    cursor.close()


def assign_staff_role(connection, staff_id, role):
    cursor = connection.cursor()
    sql = "UPDATE MedicalStaff SET Role = %s WHERE StaffID = %s"
    values = (role, staff_id)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


def edit_staff_information(connection, staff_id, first_name, last_name, role, licensing_info, work_schedule):
    cursor = connection.cursor()
    sql = """
        UPDATE MedicalStaff
        SET FirstName = %s, LastName = %s, Role = %s, LicensingInfo = %s, WorkSchedule = %s
        WHERE StaffID = %s
    """
    values = (first_name, last_name, role, licensing_info, work_schedule, staff_id)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


def remove_staff_member(connection, staff_id):
    cursor = connection.cursor()
    sql = "DELETE FROM MedicalStaff WHERE StaffID = %s"
    cursor.execute(sql, (staff_id,))
    connection.commit()
    cursor.close()


def create_hospital_policy(connection, policy_name, policy_text):
    cursor = connection.cursor()
    sql = """
        INSERT INTO Policies (PolicyName, PolicyText)
        VALUES (%s, %s)
    """
    values = (policy_name, policy_text)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


def remove_policy_procedure(connection, policy_id):
    cursor = connection.cursor()
    sql = "DELETE FROM Policies WHERE PolicyID = %s"
    cursor.execute(sql, (policy_id,))
    connection.commit()
    cursor.close()


def assign_room(connection, patient_id, room_number):
    cursor = connection.cursor()
    sql = "UPDATE Patients SET RoomNumber = %s WHERE PatientID = %s"
    values = (room_number, patient_id)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


def discharge_patient(connection, patient_id, discharge_date):
    cursor = connection.cursor()
    sql = "UPDATE Patients SET DischargeDate = %s WHERE PatientID = %s"
    values = (discharge_date, patient_id)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


from prettytable import PrettyTable

def view_inventory(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Inventory")
    inventory_items = cursor.fetchall()
    cursor.close()

    table = PrettyTable()
    table.field_names = ["Item ID", "Item Name", "Item Description", "Item Quantity", "Item Price"]

    for item in inventory_items:
        table.add_row([item[0], item[1], item[2], item[3], item[4]])

    print("Inventory Items")
    print(table)


    for item in inventory_items:
        print(f"Item ID: {item[0]}")
        print(f"Item Name: {item[1]}")
        print(f"Item Description: {item[2]}")
        print(f"Item Quantity: {item[3]}")
        print(f"Item Price: {item[4]}\n")


def add_inventory_item(connection, item_name, item_description, item_quantity, item_price):
    cursor = connection.cursor()
    sql = """
        INSERT INTO Inventory (ItemName, ItemDescription, ItemQuantity, ItemPrice)
        VALUES (%s, %s, %s, %s)
    """
    values = (item_name, item_description, item_quantity, item_price)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


def edit_inventory_item(connection, item_id, item_name, item_description, item_quantity, item_price):
    cursor = connection.cursor()
    sql = """
        UPDATE Inventory
        SET ItemName = %s, ItemDescription = %s, ItemQuantity = %s, ItemPrice = %s
        WHERE ItemID = %s
    """
    values = (item_name, item_description, item_quantity, item_price, item_id)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


def remove_inventory_item(connection, item_id):
    cursor = connection.cursor()
    sql = "DELETE FROM Inventory WHERE ItemID = %s"
    cursor.execute(sql, (item_id,))
    connection.commit()
    cursor.close()


from prettytable import PrettyTable

def view_supplier_info(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Suppliers")
    suppliers = cursor.fetchall()
    cursor.close()

    table = PrettyTable()
    table.field_names = ["Supplier ID", "Supplier Name", "Supplier Contact", "Supplier Address"]

    for supplier in suppliers:
        table.add_row([supplier[0], supplier[1], supplier[2], supplier[3]])

    print("Supplier Information")
    print(table)


    for supplier in suppliers:
        print(f"Supplier ID: {supplier[0]}")
        print(f"Supplier Name: {supplier[1]}")
        print(f"Supplier Contact: {supplier[2]}")
        print(f"Supplier Address: {supplier[3]}\n")


def add_supplier(connection, supplier_name, supplier_contact, supplier_address):
    cursor = connection.cursor()
    sql = """
        INSERT INTO Suppliers (SupplierName, SupplierContact, SupplierAddress)
        VALUES (%s, %s, %s)
    """
    values = (supplier_name, supplier_contact, supplier_address)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


def edit_supplier_info(connection, supplier_id, supplier_name, supplier_contact, supplier_address):
    cursor = connection.cursor()
    sql = """
        UPDATE Suppliers
        SET SupplierName = %s, SupplierContact = %s, SupplierAddress = %s
        WHERE SupplierID = %s
    """
    values = (supplier_name, supplier_contact, supplier_address, supplier_id)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


def remove_supplier(connection, supplier_id):
    cursor = connection.cursor()
    sql = "DELETE FROM Suppliers WHERE SupplierID = %s"
    cursor.execute(sql, (supplier_id,))
    connection.commit()
    cursor.close()


def patient_check_in(connection, patient_id, check_in_date):
    cursor = connection.cursor()
    sql = "UPDATE Patients SET CheckInDate = %s WHERE PatientID = %s"
    values = (check_in_date, patient_id)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


from prettytable import PrettyTable

def view_quality_assessment(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM QualityAssessments")
    assessments = cursor.fetchall()
    cursor.close()

    table = PrettyTable()
    table.field_names = ["Assessment ID", "Assessment Date", "Assessment Type", "Assessment Description", "Assessment Result"]

    for assessment in assessments:
        table.add_row([assessment[0], assessment[1], assessment[2], assessment[3], assessment[4]])

    print("Quality Assessment Information")
    print(table)


    for assessment in assessments:
        print(f"Assessment ID: {assessment[0]}")
        print(f"Assessment Date: {assessment[1]}")
        print(f"Assessment Type: {assessment[2]}")
        print(f"Assessment Description: {assessment[3]}")
        print(f"Assessment Result: {assessment[4]}\n")


def add_quality_assessment(connection, assessment_date, assessment_type, assessment_description, assessment_result):
    cursor = connection.cursor()
    sql = """
        INSERT INTO QualityAssessments (AssessmentDate, AssessmentType, AssessmentDescription, AssessmentResult)
        VALUES (%s, %s, %s, %s)
    """
    values = (assessment_date, assessment_type, assessment_description, assessment_result)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


def edit_quality_assessment(connection, assessment_id, assessment_date, assessment_type, assessment_description, assessment_result):
    cursor = connection.cursor()
    sql = """
        UPDATE QualityAssessments
        SET AssessmentDate = %s, AssessmentType = %s, AssessmentDescription = %s, AssessmentResult = %s
        WHERE AssessmentID = %s
    """
    values = (assessment_date, assessment_type, assessment_description, assessment_result, assessment_id)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


def remove_quality_assessment(connection, assessment_id):
    cursor = connection.cursor()
    sql = "DELETE FROM QualityAssessments WHERE AssessmentID = %s"
    cursor.execute(sql, (assessment_id,))
    connection.commit()
    cursor.close()


def view_research_projects(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ResearchProjects")
    projects = cursor.fetchall()
    cursor.close()

    table = PrettyTable()
    table.field_names = ["Project ID", "Project Name", "Project Description", "Project Start Date", "Project End Date"]

    for project in projects:
        table.add_row([project[0], project[1], project[2], project[3], project[4]])

    print("Research Projects Information")
    print(table)


def add_research_project(connection, project_name, project_description, project_start_date, project_end_date):
    cursor = connection.cursor()
    sql = """
        INSERT INTO ResearchProjects (ProjectName, ProjectDescription, ProjectStartDate, ProjectEndDate)
        VALUES (%s, %s, %s, %s)
    """
    values = (project_name, project_description, project_start_date, project_end_date)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


def edit_research_project(connection, project_id, project_name, project_description, project_start_date, project_end_date):
    cursor = connection.cursor()
    sql = """
        UPDATE ResearchProjects
        SET ProjectName = %s, ProjectDescription = %s, ProjectStartDate = %s, ProjectEndDate = %s
        WHERE ProjectID = %s
    """
    values = (project_name, project_description, project_start_date, project_end_date, project_id)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


def remove_research_project(connection, project_id):
    cursor = connection.cursor()
    sql = "DELETE FROM ResearchProjects WHERE ProjectID = %s"
    cursor.execute(sql, (project_id,))
    connection.commit()
    cursor.close()


def view_financial_records(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM FinancialRecords")
    records = cursor.fetchall()
    cursor.close()

    table = PrettyTable()
    table.field_names = ["Record ID", "Record Type", "Record Date", "Record Amount"]

    for record in records:
        table.add_row([record[0], record[1], record[2], record[3]])

    print("Financial Records")
    print(table)


def add_financial_record(connection, record_type, record_date, record_amount):
    cursor = connection.cursor()
    sql = """
        INSERT INTO FinancialRecords (RecordType, RecordDate, RecordAmount)
        VALUES (%s, %s, %s)
    """
    values = (record_type, record_date, record_amount)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


def edit_financial_record(connection, record_id, record_type, record_date, record_amount):
    cursor = connection.cursor()
    sql = """
        UPDATE FinancialRecords
        SET RecordType = %s, RecordDate = %s, RecordAmount = %s
        WHERE RecordID = %s
    """
    values = (record_type, record_date, record_amount, record_id)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


def remove_financial_record(connection, record_id):
    cursor = connection.cursor()
    sql = "DELETE FROM FinancialRecords WHERE RecordID = %s"
    cursor.execute(sql, (record_id,))
    connection.commit()
    cursor.close()


def generate_report(connection, report_type, start_date, end_date):
    cursor = connection.cursor()
    sql = "SELECT * FROM FinancialRecords WHERE RecordType = %s AND RecordDate BETWEEN %s AND %s"
    cursor.execute(sql, (report_type, start_date, end_date))
    records = cursor.fetchall()
    cursor.close()

    table = PrettyTable()
    table.field_names = ["Record ID", "Record Type", "Record Date", "Record Amount"]

    for record in records:
        table.add_row([record[0], record[1], record[2], record[3]])

    total_amount = sum(record[3] for record in records)

    print(f"Report Type: {report_type}")
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")
    print(f"Total Amount: {total_amount}")
    print(table)


def user_account_management(connection):
    print("User Account Management is not implemented yet.")




def main_menu(connection):
    while True:
        print("Hospital Management System")
        print("1. Display Patient Information")
        print("2. Add New Patient")
        print("3. Edit Patient Data")
        print("4. Remove Patient")
        print("5. Display Admission and Discharge Records")
        print("6. View Medical Staff Information")
        print("7. View Policy and Procedure Details")
        print("8. Edit Policy and Procedure Details")
        print("9. Remove Policies and Procedures")
        print("10. Assign Room to Patient")
        print("11. View Room Assignments")
        print("12. Edit Admission Records")
        print("13. Add Billing Information")
        print("14. Edit Billing Information")
        print("15. Remove Billing Information")
        print("16. Add Medical Images")
        print("17. Edit Medical Images")
        print("18. Remove Medical Images")
        print("19. Add Lab Results")
        print("20. Edit Lab Results")
        print("21. Remove Lab Results")
        print("22. Add Medications")
        print("23. Edit Medications")
        print("24. Remove Medications")
        print("25. Schedule Appointments")
        print("26. Edit Appointments")
        print("27. Cancel Appointments")
        print("28. Assign Staff Roles")
        print("29. Edit Staff Information")
        print("30. Remove Staff Members")
        print("31. Create Hospital Policies")
        print("32. Remove Policies and Procedures")
        print("33. Assign Rooms")
        print("34. View Room Assignments")
        print("35. Discharge Patients")
        print("36. View Inventory")
        print("37. Add Inventory Items")
        print("38. Edit Inventory Items")
        print("39. Remove Inventory Items")
        print("40. View Supplier Information")
        print("41. Add Suppliers")
        print("42. Edit Supplier Information")
        print("43. Remove Suppliers")
        print("44. Patient Check-in")
        print("45. View Quality Assurance Assessments")
        print("46. Add Quality Assurance Assessments")
        print("47. Edit Quality Assurance Assessments")
        print("48. Remove Quality Assurance Assessments")
        print("49. View Research Projects")
        print("50. Add Research Projects")
        print("51. Edit Research Projects")
        print("52. Remove Research Projects")
        print("53. View Financial Records")
        print("54. Add Financial Records")
        print("55. Edit Financial Records")
        print("56. Remove Financial Records")
        print("57. Generate Reports")
        print("58. User Account Management")
        print("59. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            display_patient_info(connection)
        elif choice == "2":
            
            pass
        elif choice == "3":
            
            pass
        elif choice == "4":
            
            pass
        elif choice == "5":
            display_admissions(connection)
        elif choice == "6":
            view_medical_staff_info(connection)
        elif choice == "7":
            view_policies(connection)
        elif choice == "8":
            
            pass
        elif choice == "9":
            
            pass
        elif choice == "10":
            
            pass
        elif choice == "11":
            view_room_assignments(connection)
        elif choice == "12":
            
            pass
        elif choice == "13":
            
            pass
        elif choice == "14":
            
            pass
        elif choice == "15":
            
            pass
        elif choice == "16":
            
            pass
        elif choice == "17":
            
            pass
        elif choice == "18":
            
            pass
        elif choice == "19":
            
            pass
        elif choice == "20":
            
            pass
        elif choice == "21":
            
            pass
        elif choice == "22":
            
            pass
        elif choice == "23":
            
            pass
        elif choice == "24":
            
            pass
        elif choice == "25":
            
            pass
        elif choice == "26":
            
            pass
        elif choice == "27":
            
            pass
        elif choice == "28":
            
            pass
        elif choice == "29":
            
            pass
        elif choice == "30":
            
            pass
        elif choice == "31":
            
            pass
        elif choice == "32":
            
            pass
        elif choice == "33":
            
            pass
        elif choice == "34":
            
            pass
        elif choice == "35":
            
            pass
        elif choice == "36":
            
            pass
        elif choice == "37":
            
            pass
        elif choice == "38":
            
            pass
        elif choice == "39":
            
            pass
        elif choice == "40":
            
            pass
        elif choice == "41":
            
            pass
        elif choice == "42":
            
            pass
        elif choice == "43":
            
            pass
        elif choice == "44":
            
            pass
        elif choice == "45":
            
            pass
        elif choice == "46":
            
            pass
        elif choice == "47":
            
            pass
        elif choice == "48":
            
            pass
        elif choice == "49":
            
            pass
        elif choice == "50":
            
            pass
        elif choice == "51":
            
            pass
        elif choice == "52":
            
            pass
        elif choice == "53":
            
            pass
        elif choice == "54":
            
            pass
        elif choice == "55":
            
            pass
        elif choice == "56":
            
            pass
        elif choice == "57":
            
            pass
        elif choice == "58":
            
            pass
        elif choice == "59":
            print("Exiting the Hospital Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")
if __name__ == "__main__":
    db_connection = check_and_create_database_tables()
    if db_connection:
        main_menu(db_connection)
        db_connection.close()
