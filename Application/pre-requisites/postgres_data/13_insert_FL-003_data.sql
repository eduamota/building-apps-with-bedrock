-- SQL script to insert sample data for machine FL-003 into PostgreSQL tables.
-- Assumes the tables were created using the script in postgres_create_tables (with SERIAL keys).
-- Ensure the Machines table already contains the record for 'FL-003'.

-- Insert Operational Data for FL-003 (March 2025)
-- Note: Forklifts have loads_lifted, weight_lifted_tons, max_load_tons columns
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, loads_lifted, weight_lifted_tons, max_load_tons, maintenance_flag)
VALUES
('FL-003', '2025-03-01', 7.8, 152.0, 1.9, 138, 690.0, 21.5, FALSE),
('FL-003', '2025-03-02', 7.6, 148.0, 1.8, 134, 670.0, 23.0, FALSE),
('FL-003', '2025-03-03', 8.0, 156.0, 2.0, 142, 710.0, 24.0, FALSE),
('FL-003', '2025-03-04', 7.9, 154.0, 2.0, 140, 700.0, 22.0, FALSE),
('FL-003', '2025-03-05', 7.7, 150.0, 1.9, 136, 680.0, 22.5, FALSE),
('FL-003', '2025-03-06', 8.1, 158.0, 2.0, 143, 715.0, 24.0, FALSE),
('FL-003', '2025-03-07', 7.8, 152.0, 1.9, 138, 690.0, 22.5, FALSE),
('FL-003', '2025-03-08', 4.0, 78.0, 1.0, 71, 355.0, 21.0, FALSE),
('FL-003', '2025-03-09', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('FL-003', '2025-03-10', 7.9, 154.0, 2.0, 140, 700.0, 22.0, FALSE),
('FL-003', '2025-03-11', 7.7, 150.0, 1.9, 136, 680.0, 22.5, FALSE),
('FL-003', '2025-03-12', 8.0, 156.0, 2.0, 142, 710.0, 23.5, FALSE),
('FL-003', '2025-03-13', 8.1, 158.0, 2.0, 143, 715.0, 23.0, FALSE),
('FL-003', '2025-03-14', 7.8, 152.0, 1.9, 138, 690.0, 21.5, FALSE),
('FL-003', '2025-03-15', 3.9, 76.0, 1.0, 69, 345.0, 20.5, FALSE),
('FL-003', '2025-03-16', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('FL-003', '2025-03-17', 7.9, 154.0, 2.0, 140, 700.0, 22.5, FALSE),
('FL-003', '2025-03-18', 7.7, 150.0, 1.9, 136, 680.0, 21.0, FALSE),
('FL-003', '2025-03-19', 0.0, 0.0, 0.0, 0, 0.0, 0.0, TRUE), -- Maintenance day
('FL-003', '2025-03-20', 0.0, 0.0, 0.0, 0, 0.0, 0.0, TRUE), -- Maintenance day
('FL-003', '2025-03-21', 7.8, 152.0, 1.9, 138, 690.0, 22.0, FALSE),
('FL-003', '2025-03-22', 4.0, 78.0, 1.0, 71, 355.0, 21.0, FALSE),
('FL-003', '2025-03-23', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('FL-003', '2025-03-24', 7.7, 150.0, 1.9, 136, 680.0, 21.5, FALSE),
('FL-003', '2025-03-25', 8.0, 156.0, 2.0, 142, 710.0, 23.0, FALSE),
('FL-003', '2025-03-26', 7.8, 152.0, 1.9, 138, 690.0, 22.0, FALSE),
('FL-003', '2025-03-27', 7.6, 148.0, 1.8, 134, 670.0, 20.5, FALSE),
('FL-003', '2025-03-28', 7.9, 154.0, 2.0, 140, 700.0, 22.5, FALSE),
('FL-003', '2025-03-29', 3.8, 74.0, 0.9, 67, 335.0, 20.0, FALSE),
('FL-003', '2025-03-30', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('FL-003', '2025-03-31', 7.8, 152.0, 1.9, 138, 690.0, 22.0, FALSE);

-- Insert Operational Data for FL-003 (April 2025)
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, loads_lifted, weight_lifted_tons, max_load_tons, maintenance_flag)
VALUES
('FL-003', '2025-04-01', 7.9, 154.0, 2.0, 140, 700.0, 22.5, FALSE),
('FL-003', '2025-04-02', 8.0, 156.0, 2.0, 142, 710.0, 23.5, FALSE),
('FL-003', '2025-04-03', 7.7, 150.0, 1.9, 136, 680.0, 22.0, FALSE),
('FL-003', '2025-04-04', 7.8, 152.0, 1.9, 138, 690.0, 23.0, FALSE),
('FL-003', '2025-04-05', 3.9, 76.0, 1.0, 69, 345.0, 21.0, FALSE),
('FL-003', '2025-04-06', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('FL-003', '2025-04-07', 7.6, 148.0, 1.8, 134, 670.0, 21.5, FALSE),
('FL-003', '2025-04-08', 7.8, 152.0, 1.9, 138, 690.0, 22.5, FALSE),
('FL-003', '2025-04-09', 8.1, 158.0, 2.0, 143, 715.0, 24.0, FALSE),
('FL-003', '2025-04-10', 7.9, 154.0, 2.0, 140, 700.0, 22.5, FALSE),
('FL-003', '2025-04-11', 7.7, 150.0, 1.9, 136, 680.0, 22.0, FALSE),
('FL-003', '2025-04-12', 4.0, 78.0, 1.0, 71, 355.0, 20.5, FALSE),
('FL-003', '2025-04-13', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('FL-003', '2025-04-14', 7.8, 152.0, 1.9, 138, 690.0, 21.5, FALSE),
('FL-003', '2025-04-15', 8.0, 156.0, 2.0, 142, 710.0, 23.0, FALSE),
('FL-003', '2025-04-16', 7.6, 148.0, 1.8, 134, 670.0, 20.5, FALSE),
('FL-003', '2025-04-17', 7.9, 154.0, 2.0, 140, 700.0, 22.0, FALSE),
('FL-003', '2025-04-18', 7.8, 152.0, 1.9, 138, 690.0, 22.5, FALSE),
('FL-003', '2025-04-19', 3.8, 74.0, 0.9, 67, 335.0, 20.0, FALSE),
('FL-003', '2025-04-20', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('FL-003', '2025-04-21', 7.9, 154.0, 2.0, 140, 700.0, 22.0, FALSE),
('FL-003', '2025-04-22', 8.1, 158.0, 2.0, 143, 715.0, 24.0, FALSE),
('FL-003', '2025-04-23', 7.8, 152.0, 1.9, 138, 690.0, 21.5, FALSE),
('FL-003', '2025-04-24', 7.7, 150.0, 1.9, 136, 680.0, 22.0, FALSE),
('FL-003', '2025-04-25', 0.0, 0.0, 0.0, 0, 0.0, 0.0, TRUE), -- Maintenance day
('FL-003', '2025-04-26', 3.9, 76.0, 1.0, 69, 345.0, 20.0, FALSE),
('FL-003', '2025-04-27', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('FL-003', '2025-04-28', 7.8, 152.0, 1.9, 138, 690.0, 21.5, FALSE),
('FL-003', '2025-04-29', 8.1, 158.0, 2.0, 143, 715.0, 24.0, FALSE),
('FL-003', '2025-04-30', 7.9, 154.0, 2.0, 140, 700.0, 22.5, FALSE);

-- Insert Maintenance Events for FL-003
INSERT INTO MaintenanceEvents (machine_id, event_date, event_type, description, parts_replaced, cost, downtime_hours, technician_name)
VALUES
('FL-003', '2025-03-19', 'Preventive Maintenance', 'Regular 250-hour scheduled maintenance', 'Oil filters, fuel filters, air filters', 850.25, 8.0, 'Matthew Davis'),
('FL-003', '2025-03-20', 'Repair', 'Hydraulic control valve repair', 'Control valve seals', 1150.50, 16.0, 'Matthew Davis'),
('FL-003', '2025-04-25', 'Preventive Maintenance', 'Regular 500-hour scheduled maintenance', 'Oil filters, fuel filters, air filters, hydraulic filters', 1550.75, 8.0, 'Rachel Kim');

-- Insert Alert Events for FL-003
INSERT INTO AlertEvents (machine_id, alert_date, alert_type, severity, description, resolved, resolution_date, resolution_notes)
VALUES
('FL-003', '2025-03-08 09:45:22', 'Battery Charge Warning', 'Warning', 'Battery charge level below threshold', TRUE, '2025-03-08 10:30:15', 'Charged battery and tested charging system'),
('FL-003', '2025-03-18 14:32:48', 'Fork Alignment Warning', 'Warning', 'Fork alignment deviation detected', TRUE, '2025-03-19 09:20:30', 'Adjusted fork alignment during scheduled maintenance'),
('FL-003', '2025-04-12 11:15:33', 'Hydraulic Pressure Warning', 'Warning', 'Hydraulic pressure fluctuation detected', TRUE, '2025-04-12 13:45:50', 'Inspected hydraulic pump and pressure relief valve'),
('FL-003', '2025-04-24 08:50:27', 'Engine Performance Warning', 'Critical', 'Engine misfire detected', TRUE, '2025-04-25 10:15:42', 'Replaced spark plugs during scheduled maintenance');

-- End of script for FL-003 data
