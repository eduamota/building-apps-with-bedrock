-- SQL script to insert sample data for machine FL-002 into PostgreSQL tables.
-- Assumes the tables were created using the script in postgres_create_tables (with SERIAL keys).
-- Ensure the Machines table already contains the record for 'FL-002'.

-- Insert Operational Data for FL-002 (March 2025)
-- Note: Forklifts have loads_lifted, weight_lifted_tons, max_load_tons columns
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, loads_lifted, weight_lifted_tons, max_load_tons, maintenance_flag)
VALUES
('FL-002', '2025-03-01', 7.9, 154.0, 2.0, 140, 700.0, 22.0, FALSE),
('FL-002', '2025-03-02', 7.7, 150.0, 1.9, 136, 680.0, 23.5, FALSE),
('FL-002', '2025-03-03', 8.1, 158.0, 2.0, 143, 715.0, 24.0, FALSE),
('FL-002', '2025-03-04', 8.0, 156.0, 2.0, 142, 710.0, 22.5, FALSE),
('FL-002', '2025-03-05', 7.8, 152.0, 1.9, 138, 690.0, 23.0, FALSE),
('FL-002', '2025-03-06', 8.2, 160.0, 2.1, 145, 725.0, 24.5, FALSE),
('FL-002', '2025-03-07', 7.9, 154.0, 2.0, 140, 700.0, 23.0, FALSE),
('FL-002', '2025-03-08', 4.1, 80.0, 1.0, 72, 360.0, 21.5, FALSE),
('FL-002', '2025-03-09', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('FL-002', '2025-03-10', 8.0, 156.0, 2.0, 142, 710.0, 22.5, FALSE),
('FL-002', '2025-03-11', 7.8, 152.0, 1.9, 138, 690.0, 23.0, FALSE),
('FL-002', '2025-03-12', 8.1, 158.0, 2.0, 143, 715.0, 24.0, FALSE),
('FL-002', '2025-03-13', 8.2, 160.0, 2.1, 145, 725.0, 23.5, FALSE),
('FL-002', '2025-03-14', 7.9, 154.0, 2.0, 140, 700.0, 22.0, FALSE),
('FL-002', '2025-03-15', 4.0, 78.0, 1.0, 71, 355.0, 21.0, FALSE),
('FL-002', '2025-03-16', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('FL-002', '2025-03-17', 0.0, 0.0, 0.0, 0, 0.0, 0.0, TRUE), -- Maintenance day
('FL-002', '2025-03-18', 0.0, 0.0, 0.0, 0, 0.0, 0.0, TRUE), -- Maintenance day
('FL-002', '2025-03-19', 8.0, 156.0, 2.0, 142, 710.0, 23.0, FALSE),
('FL-002', '2025-03-20', 8.2, 160.0, 2.1, 145, 725.0, 24.5, FALSE),
('FL-002', '2025-03-21', 7.9, 154.0, 2.0, 140, 700.0, 22.5, FALSE),
('FL-002', '2025-03-22', 4.1, 80.0, 1.0, 72, 360.0, 21.5, FALSE),
('FL-002', '2025-03-23', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('FL-002', '2025-03-24', 7.8, 152.0, 1.9, 138, 690.0, 22.0, FALSE),
('FL-002', '2025-03-25', 8.1, 158.0, 2.0, 143, 715.0, 23.5, FALSE),
('FL-002', '2025-03-26', 7.9, 154.0, 2.0, 140, 700.0, 22.5, FALSE),
('FL-002', '2025-03-27', 7.7, 150.0, 1.9, 136, 680.0, 21.0, FALSE),
('FL-002', '2025-03-28', 8.0, 156.0, 2.0, 142, 710.0, 23.0, FALSE),
('FL-002', '2025-03-29', 3.9, 76.0, 1.0, 69, 345.0, 21.0, FALSE),
('FL-002', '2025-03-30', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('FL-002', '2025-03-31', 7.9, 154.0, 2.0, 140, 700.0, 22.5, FALSE);

-- Insert Operational Data for FL-002 (April 2025)
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, loads_lifted, weight_lifted_tons, max_load_tons, maintenance_flag)
VALUES
('FL-002', '2025-04-01', 8.0, 156.0, 2.0, 142, 710.0, 23.0, FALSE),
('FL-002', '2025-04-02', 8.1, 158.0, 2.0, 143, 715.0, 24.0, FALSE),
('FL-002', '2025-04-03', 7.8, 152.0, 1.9, 138, 690.0, 22.5, FALSE),
('FL-002', '2025-04-04', 7.9, 154.0, 2.0, 140, 700.0, 23.5, FALSE),
('FL-002', '2025-04-05', 4.0, 78.0, 1.0, 71, 355.0, 21.5, FALSE),
('FL-002', '2025-04-06', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('FL-002', '2025-04-07', 7.7, 150.0, 1.9, 136, 680.0, 22.0, FALSE),
('FL-002', '2025-04-08', 7.9, 154.0, 2.0, 140, 700.0, 23.0, FALSE),
('FL-002', '2025-04-09', 8.2, 160.0, 2.1, 145, 725.0, 24.5, FALSE),
('FL-002', '2025-04-10', 8.0, 156.0, 2.0, 142, 710.0, 23.0, FALSE),
('FL-002', '2025-04-11', 7.8, 152.0, 1.9, 138, 690.0, 22.5, FALSE),
('FL-002', '2025-04-12', 4.1, 80.0, 1.0, 72, 360.0, 21.0, FALSE),
('FL-002', '2025-04-13', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('FL-002', '2025-04-14', 7.9, 154.0, 2.0, 140, 700.0, 22.0, FALSE),
('FL-002', '2025-04-15', 8.1, 158.0, 2.0, 143, 715.0, 23.5, FALSE),
('FL-002', '2025-04-16', 7.7, 150.0, 1.9, 136, 680.0, 21.0, FALSE),
('FL-002', '2025-04-17', 8.0, 156.0, 2.0, 142, 710.0, 22.5, FALSE),
('FL-002', '2025-04-18', 7.9, 154.0, 2.0, 140, 700.0, 23.0, FALSE),
('FL-002', '2025-04-19', 3.9, 76.0, 1.0, 69, 345.0, 20.5, FALSE),
('FL-002', '2025-04-20', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('FL-002', '2025-04-21', 0.0, 0.0, 0.0, 0, 0.0, 0.0, TRUE), -- Maintenance day
('FL-002', '2025-04-22', 0.0, 0.0, 0.0, 0, 0.0, 0.0, TRUE), -- Maintenance day
('FL-002', '2025-04-23', 7.9, 154.0, 2.0, 140, 700.0, 22.0, FALSE),
('FL-002', '2025-04-24', 8.0, 156.0, 2.0, 142, 710.0, 22.5, FALSE),
('FL-002', '2025-04-25', 7.7, 150.0, 1.9, 136, 680.0, 21.0, FALSE),
('FL-002', '2025-04-26', 4.0, 78.0, 1.0, 71, 355.0, 20.5, FALSE),
('FL-002', '2025-04-27', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('FL-002', '2025-04-28', 7.9, 154.0, 2.0, 140, 700.0, 22.0, FALSE),
('FL-002', '2025-04-29', 8.2, 160.0, 2.1, 145, 725.0, 24.5, FALSE),
('FL-002', '2025-04-30', 8.0, 156.0, 2.0, 142, 710.0, 23.0, FALSE);

-- Insert Maintenance Events for FL-002
INSERT INTO MaintenanceEvents (machine_id, event_date, event_type, description, parts_replaced, cost, downtime_hours, technician_name)
VALUES
('FL-002', '2025-03-17', 'Preventive Maintenance', 'Regular 250-hour scheduled maintenance', 'Oil filters, fuel filters, air filters', 850.50, 8.0, 'Sophie Garcia'),
('FL-002', '2025-03-18', 'Repair', 'Mast repair', 'Mast rollers, bearings', 1050.25, 8.0, 'Sophie Garcia'),
('FL-002', '2025-04-21', 'Preventive Maintenance', 'Regular 500-hour scheduled maintenance', 'Oil filters, fuel filters, air filters, hydraulic filters', 1450.75, 16.0, 'Justin Williams'),
('FL-002', '2025-04-22', 'Inspection', 'Fork inspection and certification', 'Fork pins', 750.50, 8.0, 'Justin Williams');

-- Insert Alert Events for FL-002
INSERT INTO AlertEvents (machine_id, alert_date, alert_type, severity, description, resolved, resolution_date, resolution_notes)
VALUES
('FL-002', '2025-03-10 08:30:15', 'Mast Chain Tension Warning', 'Warning', 'Uneven tension detected in lift chains', TRUE, '2025-03-10 09:45:30', 'Adjusted chain tension to manufacturer specifications'),
('FL-002', '2025-03-16 13:42:22', 'Hydraulic System Warning', 'Warning', 'Low hydraulic fluid level detected', TRUE, '2025-03-17 08:50:15', 'Added fluid and inspected for leaks during maintenance'),
('FL-002', '2025-04-08 10:15:48', 'Brake System Warning', 'Critical', 'Reduced braking performance detected', TRUE, '2025-04-08 11:30:25', 'Adjusted brake system and scheduled for detailed inspection'),
('FL-002', '2025-04-20 15:28:33', 'Steering System Warning', 'Warning', 'Increased play in steering mechanism', TRUE, '2025-04-21 10:45:52', 'Addressed during scheduled maintenance');

-- End of script for FL-002 data
