\c medical_assistant;

CREATE TABLE IF NOT EXISTS patients (
    id SERIAL PRIMARY KEY,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    birth_date DATE NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS medications (
    id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    dosage VARCHAR(100) NOT NULL,
    frequency VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_patients_cpf ON patients(cpf);
CREATE INDEX idx_medications_patient_id ON medications(patient_id);

-- Test data: Patients
INSERT INTO patients (cpf, name, birth_date, phone, email) VALUES
('12345678901', 'Maria Silva', '1985-03-15', '11999887766', 'maria.silva@email.com'),
('23456789012', 'João Santos', '1972-08-22', '11988776655', 'joao.santos@email.com'),
('34567890123', 'Ana Oliveira', '1990-12-01', '11977665544', 'ana.oliveira@email.com'),
('45678901234', 'Carlos Ferreira', '1968-05-10', '11966554433', 'carlos.ferreira@email.com'),
('56789012345', 'Beatriz Costa', '1995-07-28', '11955443322', 'beatriz.costa@email.com');

-- Test data: Medications
INSERT INTO medications (patient_id, name, dosage, frequency, start_date, end_date, notes) VALUES
-- Maria Silva (diabetes and hypertension)
(1, 'Metformin', '850mg', 'Twice daily', '2023-01-15', NULL, 'Take after meals'),
(1, 'Losartan', '50mg', 'Once daily', '2023-01-15', NULL, 'Take in the morning'),

-- João Santos (hypertension and cholesterol)
(2, 'Atenolol', '25mg', 'Once daily', '2022-06-10', NULL, 'Take in the morning on empty stomach'),
(2, 'Simvastatin', '20mg', 'Once daily', '2022-06-10', NULL, 'Take at night'),
(2, 'Aspirin', '100mg', 'Once daily', '2022-06-10', NULL, 'Take after lunch'),

-- Ana Oliveira (anxiety)
(3, 'Escitalopram', '10mg', 'Once daily', '2024-02-01', NULL, 'Take in the morning'),
(3, 'Clonazepam', '0.5mg', 'As needed', '2024-02-01', '2024-05-01', 'Maximum once daily for anxiety episodes'),

-- Carlos Ferreira (diabetes, hypertension, thyroid)
(4, 'NPH Insulin', '20UI', 'Twice daily', '2020-03-20', NULL, 'Inject subcutaneously before breakfast and dinner'),
(4, 'Regular Insulin', '10UI', 'Three times daily', '2020-03-20', NULL, 'Inject before main meals'),
(4, 'Enalapril', '10mg', 'Twice daily', '2020-03-20', NULL, 'Take every 12 hours'),
(4, 'Levothyroxine', '50mcg', 'Once daily', '2019-08-15', NULL, 'Take on empty stomach, 30min before breakfast'),

-- Beatriz Costa (migraine)
(5, 'Topiramate', '25mg', 'Twice daily', '2024-06-01', NULL, 'Migraine prevention'),
(5, 'Sumatriptan', '50mg', 'As needed', '2024-06-01', NULL, 'Take at onset of migraine, maximum twice daily');
