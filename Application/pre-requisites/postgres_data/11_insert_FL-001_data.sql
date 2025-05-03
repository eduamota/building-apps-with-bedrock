-- SQL script to insert sample data for machine FL-001 into PostgreSQL tables.
-- Assumes the tables were created using the script in postgres_create_tables (with SERIAL keys).
-- Ensure the Machines table already contains the record for 'FL-001'.

-- Insert Operational Data for FL-001 (March 2025)
-- Note: Forklifts have loads_lifted, weight_lifted_tons, max_load_tons columns
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, loads_lifted, weight_lifted_tons, max_load_tons, maintenance_flag)
VALUES
('FL-001', '2025-03-01', 8.0, 156.0, 2.0, 142, 710.0, 22.5, FALSE),
('FL-001', '2025-03-02', 7.8, 152.0, 1.9, 138, 690.0, 24.0, FALSE),
('FL-001', '2025-03-03', 8.2, 160.0, 2.1, 145, 725.0, 23.5, FALSE),
('FL-001', '2025-03-04', 8.1, 158.0, 2.0, 143, 715.0, 22.0, FALSE),
('FL-001', '2025-03-05', 7.9, 154.0, 2.0, 140, 700.0, 23.0, FALSE),
('FL-001', '2025-03-06', 8.3, 162.0, 2.1, 147, 735.0, 24.5, FALSE),
('FL-001', '2025-03-07', 8.0, 156.0, 2.0, 142, 710.0, 23.0, FALSE),
('FL-001', '2025-03-08', 4.2, 82.0, 1.0, 74, 370.0, 22.0, FALSE),
('FL-001', '2025-03-09', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('FL-001', '2025-03-10', 8.1, 158.0, 2.0, 143, 715.0, 23.5, FALSE),
('FL-001', '2025-03-11', 7.9, 154.0, 2.0, 140, 700.0, 22.5, FALSE),
('FL-001', '2025-03-12', 8.2, 160.0, 2.1, 145, 725.0, 24.0, FALSE),
('FL-001', '2025-03-13', 0.0, 0.0, 0.0, 0, 0.0, 0.0, TRUE), -- Maintenance day
('FL-001', '2025-03-14', 0.0, 0.0, 0.0, 0, 0.0, 0.0, TRUE), -- Maintenance day
('FL-001', '2025-03-15', 4.1, 80.0, 1.0, 72, 360.0, 21.5, FALSE),
('FL-001', '2025-03-16', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('FL-001', '2025-03-17', 8.0, 156.0, 2.0, 142, 710.0, 23.0, FALSE),
('FL-001', '2025-03-18', 7.8, 152.0, 1.9, 138, 690.0, 22.5, FALSE),
('FL-001', '2025-03-19', 8.1, 158.0, 2.0, 143, 715.0, 23.5, FALSE),
('FL-001', '2025-03-20', 8.3, 162.0, 2.1, 147, 735.0, 24.0, FALSE),
('FL-001', '2025-03-21', 8.0, 156.0, 2.0, 142, 710.0, 22.0, FALSE),
('FL-001', '2025-03-22', 4.2, 82.0, 1.0, 74, 370.0, 21.0, FALSE),
('FL-001', '2025-03-23', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('FL-001', '2025-03-24', 7.9, 154.0, 2.0, 140, 700.0, 22.5, FALSE),
('FL-001', '2025-03-25', 8.2, 160.0, 2.1, 145, 725.0, 23.0, FALSE),
('FL-001', '2025-03-26', 8.0, 156.0, 2.0, 142, 710.0, 22.5, FALSE),
('FL-001', '2025-03-27', 7.8, 152.0, 1.9, 138, 690.0, 21.5, FALSE),
('FL-001', '2025-03-28', 8.1, 158.0, 2.0, 143, 715.0, 23.0, FALSE),
('FL-001', '2025-03-29', 4.0, 78.0, 1.0, 71, 355.0, 22.0, FALSE),
('FL-001', '2025-03-30', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('FL-001', '2025-03-31', 8.0, 156.0, 2.0, 142, 710.0, 23.5, FALSE);

-- Insert Operational Data for FL-001 (April 2025)
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, loads_lifted, weight_lifted_tons, max_load_tons, maintenance_flag)
VALUES
('FL-001', '2025-04-01', 8.1, 158.0, 2.0, 143, 715.0, 23.0, FALSE),
('FL-001', '2025-04-02', 8.2, 160.0, 2.1, 145, 725.0, 24.0, FALSE),
('FL-001', '2025-04-03', 7.9, 154.0, 2.0, 140, 700.0, 22.5, FALSE),
('FL-001', '2025-04-04', 8.0, 156.0, 2.0, 142, 710.0, 23.5, FALSE),
('FL-001', '2025-04-05', 4.1, 80.0, 1.0, 72, 360.0, 22.0, FALSE),
('FL-001', '2025-04-06', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('FL-001', '2025-04-07', 7.8, 152.0, 1.9, 138, 690.0, 23.0, FALSE),
('FL-001', '2025-04-08', 8.0, 156.0, 2.0, 142, 710.0, 24.0, FALSE),
('FL-001', '2025-04-09', 8.3, 162.0, 2.1, 147, 735.0, 24.5, FALSE),
('FL-001', '2025-04-10', 8.1, 158.0, 2.0, 143, 715.0, 23.0, FALSE),
('FL-001', '2025-04-11', 7.9, 154.0, 2.0, 140, 700.0, 22.5, FALSE),
('FL-001', '2025-04-12', 4.2, 82.0, 1.0, 74, 370.0, 21.5, FALSE),
('FL-001', '2025-04-13', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('FL-001', '2025-04-14', 8.0, 156.0, 2.0, 142, 710.0, 22.0, FALSE),
('FL-001', '2025-04-15', 8.2, 160.0, 2.1, 145, 725.0, 23.5, FALSE),
('FL-001', '2025-04-16', 7.8, 152.0, 1.9, 138, 690.0, 21.0, FALSE),
('FL-001', '2025-04-17', 8.1, 158.0, 2.0, 143, 715.0, 22.5, FALSE),
('FL-001', '2025-04-18', 0.0, 0.0, 0.0, 0, 0.0, 0.0, TRUE), -- Maintenance day
('FL-001', '2025-04-19', 4.0, 78.0, 1.0, 71, 355.0, 21.0, FALSE),
('FL-001', '2025-04-20', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('FL-001', '2025-04-21', 7.9, 154.0, 2.0, 140, 700.0, 22.0, FALSE),
('FL-001', '2025-04-22', 8.0, 156.0, 2.0, 142, 710.0, 23.0, FALSE),
('FL-001', '2025-04-23', 8.2, 160.0, 2.1, 145, 725.0, 24.0, FALSE),
('FL-001', '2025-04-24', 8.1, 158.0, 2.0, 143, 715.0, 22.5, FALSE),
('FL-001', '2025-04-25', 7.8, 152.0, 1.9, 138, 690.0, 21.5, FALSE),
('FL-001', '2025-04-26', 4.1, 80.0, 1.0, 72, 360.0, 21.0, FALSE),
('FL-001', '2025-04-27', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('FL-001', '2025-04-28', 8.0, 156.0, 2.0, 142, 710.0, 22.5, FALSE),
('FL-001', '2025-04-29', 8.3, 162.0, 2.1, 147, 735.0, 24.5, FALSE),
('FL-001', '2025-04-30', 8.1, 158.0, 2.0, 143, 715.0, 23.0, FALSE);

-- Insert Maintenance Events for FL-001
INSERT INTO MaintenanceEvents (machine_id, event_date, event_type, description, parts_replaced, cost, downtime_hours, technician_name)
VALUES
('FL-001', '2025-03-13', 'Preventive Maintenance', 'Regular 250-hour scheduled maintenance', 'Oil filters, fuel filters, air filters', 950.25, 16.0, 'Jessica Martinez'),
('FL-001', '2025-03-14', 'Repair', 'Repair of hydraulic lift system', 'Hydraulic seals, lift chain', 1350.75, 8.0, 'Jessica Martinez'),
('FL-001', '2025-04-18', 'Preventive Maintenance', 'Regular 500-hour scheduled maintenance', 'Oil filters, fuel filters, air filters, hydraulic filters', 1650.50, 8.0, 'Kevin Wilson');

-- Insert Alert Events for FL-001
INSERT INTO AlertEvents (machine_id, alert_date, alert_type, severity, description, resolved, resolution_date, resolution_notes)
VALUES
('FL-001', '2025-03-06 08:42:15', 'Low Hydraulic Fluid Level', 'Warning', 'Hydraulic fluid level below recommended minimum', TRUE, '2025-03-06 09:15:30', 'Added hydraulic fluid and inspected for leaks'),
('FL-001', '2025-03-12 13:27:48', 'Mast Chain Tension Warning', 'Warning', 'Uneven tension detected in lift chains', TRUE, '2025-03-14 10:22:55', 'Adjusted chain tension during scheduled maintenance'),
('FL-001', '2025-04-08 10:18:33', 'Steering System Warning', 'Warning', 'Increased resistance in steering system', TRUE, '2025-04-08 11:45:20', 'Adjusted steering system and scheduled for detailed inspection'),
('FL-001', '2025-04-17 15:33:42', 'Battery Voltage Warning', 'Warning', 'Battery voltage below optimal range', TRUE, '2025-04-18 09:20:15', 'Replaced battery during scheduled maintenance');

-- End of script for FL-001 data
