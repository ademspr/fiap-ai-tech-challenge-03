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
-- Maria Silva (diabetes e hipertensão)
(1, 'Metformina', '850mg', '2x ao dia', '2023-01-15', NULL, 'Tomar após refeições'),
(1, 'Losartana', '50mg', '1x ao dia', '2023-01-15', NULL, 'Tomar pela manhã'),

-- João Santos (hipertensão e colesterol)
(2, 'Atenolol', '25mg', '1x ao dia', '2022-06-10', NULL, 'Tomar pela manhã em jejum'),
(2, 'Sinvastatina', '20mg', '1x ao dia', '2022-06-10', NULL, 'Tomar à noite'),
(2, 'AAS', '100mg', '1x ao dia', '2022-06-10', NULL, 'Tomar após almoço'),

-- Ana Oliveira (ansiedade)
(3, 'Escitalopram', '10mg', '1x ao dia', '2024-02-01', NULL, 'Tomar pela manhã'),
(3, 'Clonazepam', '0.5mg', 'Se necessário', '2024-02-01', '2024-05-01', 'Máximo 1x ao dia para crises'),

-- Carlos Ferreira (diabetes, hipertensão, tireoide)
(4, 'Insulina NPH', '20UI', '2x ao dia', '2020-03-20', NULL, 'Aplicar subcutâneo antes do café e jantar'),
(4, 'Insulina Regular', '10UI', '3x ao dia', '2020-03-20', NULL, 'Aplicar antes das refeições principais'),
(4, 'Enalapril', '10mg', '2x ao dia', '2020-03-20', NULL, 'Tomar 12/12h'),
(4, 'Levotiroxina', '50mcg', '1x ao dia', '2019-08-15', NULL, 'Tomar em jejum, 30min antes do café'),

-- Beatriz Costa (enxaqueca)
(5, 'Topiramato', '25mg', '2x ao dia', '2024-06-01', NULL, 'Prevenção de enxaqueca'),
(5, 'Sumatriptana', '50mg', 'Se necessário', '2024-06-01', NULL, 'Tomar no início da crise, máximo 2x ao dia');
