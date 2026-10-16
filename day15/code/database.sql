CREATE DATABASE healthcare_nav;
USE healthcare_nav;

-- appointments
CREATE TABLE IF NOT EXISTS appointments (
    id VARCHAR(20) PRIMARY KEY,
    patient_id VARCHAR(20) NOT NULL,
    doctor VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    time VARCHAR(20) NOT NULL,
    type VARCHAR(100) NOT NULL
);

-- available_slots
CREATE TABLE IF NOT EXISTS available_slots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    time VARCHAR(20) NOT NULL,
    doctor VARCHAR(100) NOT NULL
)

-- invoices
CREATE TABLE IF NOT EXISTS invoices (
    id VARCHAR(30) PRIMARY KEY,
    patient_id VARCHAR(20) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    description VARCHAR(200) NOT NULL
)

-- insurance
CREATE TABLE IF NOT EXISTS insurance (
    policy_number VARCHAR(30) PRIMARY KEY,
    patient_id VARCHAR(20) NOT NULL,
    provider VARCHAR(100) NOT NULL,
    plan_name VARCHAR(100) NOT NULL,
    deductible VARCHAR(50) NOT NULL,
    out_of_pocket_max VARCHAR(50) NOT NULL
)

-- insurance_coverage
CREATE TABLE IF NOT EXISTS insurance_coverage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    policy_number VARCHAR(30) NOT NULL,
    service_type VARCHAR(50) NOT NULL,
    coverage_detail VARCHAR(200) NOT NULL,
    FOREIGN KEY (policy_number) REFERENCES insurance(policy_number)
)

-- medical_records
CREATE TABLE IF NOT EXISTS medical_records (
    id VARCHAR(20) PRIMARY KEY,
    patient_id VARCHAR(20) NOT NULL,
    type VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    title VARCHAR(200) NOT NULL,
    summary TEXT NOT NULL
)

-- insert dummy data for testing
INSERT INTO appointments (id, patient_id, doctor, date, time, type) VALUES 
("APT-001", "PAT-001", "Dr. Smith", "2026-09-25", "10:00 AM", "General Checkup"),
("APT-002", "PAT-001", "Dr. Jones", "2026-10-01", "2:30 PM", "Cardiology"),
("APT-003", "PAT-001", "Dr. Lee", "2026-10-05", "9:00 AM", "Dental Cleaning");

INSERT INTO available_slots (date, time, doctor) VALUES 
("2026-09-26", "9:00 AM", "Dr. Smith"),
("2026-09-26", "11:00 AM", "Dr. Smith"),
("2026-09-27", "10:00 AM", "Dr. Jones"),
("2026-09-28", "3:00 PM", "Dr. Lee"),
("2026-10-02", "9:00 AM", "Dr. Smith");

INSERT INTO invoices (id, patient_id, amount, status, date, description) VALUES
("INV-2026-001", "PAT-001", 150.00, "paid", "2026-08-15", "Office Visit - General Checkup"),
("INV-2026-002", "PAT-001", 320.00, "pending", "2026-09-01", "Lab Work - Blood Panel"),
("INV-2026-003", "PAT-001", 75.00, "overdue", "2026-07-20", "Prescription Refill");

INSERT INTO insurance (policy_number, patient_id, provider, plan_name, deductible, out_of_pocket_max) VALUES
("INS-88421", "PAT-001", "BlueCross Health", "PPO Standard", "$500/year", "$3,000/year");

INSERT INTO insurance_coverage (policy_number, service_type, coverage_detail) VALUES
("INS-88421", "office_visit", "80% after $25 copay"),
("INS-88421", "lab_work", "90% after $15 copay"),
("INS-88421", "imaging", "70% after $30 copay"),
("INS-88421", "prescription", "60% after $10 copay"),
("INS-88421", "emergency", "90% after $50 copay");

INSERT INTO medical_records (id, patient_id, type, date, title, summary) VALUES
("REC-001", "PAT-001", "Lab Report", "2026-08-10", "Complete Blood Count (CBC)", "White blood cells: 6.5 (normal), Red blood cells: 5.1 (normal), Hemoglobin: 14.2 g/dL (normal), Platelets: 250 (normal). All values within normal range."),
("REC-002", "PAT-001", "Lab Report", "2026-07-22", "Lipid Panel", "Total Cholesterol: 215 mg/dL (borderline), LDL: 135 mg/dL (borderline), HDL: 55 mg/dL (normal), Triglycerides: 150 mg/dL (normal). Recommend dietary changes and recheck in 3 months."),
("REC-003", "PAT-001", "Imaging", "2026-06-15", "Chest X-Ray", "No acute findings. Lungs clear bilaterally. Heart size normal. No pleural effusion or pneumothorax."),
("REC-004", "PAT-001", "Discharge Summary", "2026-05-20", "Outpatient Procedure - Minor Skin Biopsy", "Procedure: Punch biopsy of right forearm lesion. Diagnosis: Suspicious mole. Pathology pending. Patient tolerated procedure well. Follow up in 2 weeks for results."),
("REC-005", "PAT-001", "Lab Report", "2026-04-05", "HbA1c Test", "HbA1c: 5.8% (pre-diabetic range). Fasting glucose: 105 mg/dL (slightly elevated). Recommend lifestyle modifications.");