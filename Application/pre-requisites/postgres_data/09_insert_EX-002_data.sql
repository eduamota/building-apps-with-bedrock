-- SQL script to insert sample data for machine EX-002 into PostgreSQL tables.
-- Assumes the tables were created using the script in postgres_create_tables (with SERIAL keys).
-- Ensure the Machines table already contains the record for 'EX-002'.

-- Insert Operational Data for EX-002 (March 2025)
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, material_moved_cubic_meters, maintenance_flag)
VALUES
('EX-002', '2025-03-01', 9.4, 564.0, 1.5, 4150.0, FALSE),
('EX-002', '2025-03-02', 9.2, 552.0, 1.4, 4050.0, FALSE),
('EX-002', '2025-03-03', 9.6, 576.0, 1.5, 4250.0, FALSE),
('EX-002', '2025-03-04', 9.5, 570.0, 1.5, 4200.0, FALSE),
('EX-002', '2025-03-05', 9.7, 582.0, 1.6, 4300.0, FALSE),
('EX-002', '2025-03-06', 9.3, 558.0, 1.4, 4100.0, FALSE),
('EX-002', '2025-03-07', 9.1, 546.0, 1.4, 4000.0, FALSE),
('EX-002', '2025-03-08', 5.5, 330.0, 0.8, 2450.0, FALSE),
('EX-002', '2025-03-09', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('EX-002', '2025-03-10', 9.4, 564.0, 1.5, 4150.0, FALSE),
('EX-002', '2025-03-11', 9.6, 576.0, 1.5, 4250.0, FALSE),
('EX-002', '2025-03-12', 9.5, 570.0, 1.5, 4200.0, FALSE),
('EX-002', '2025-03-13', 9.7, 582.0, 1.6, 4300.0, FALSE),
('EX-002', '2025-03-14', 9.3, 558.0, 1.4, 4100.0, FALSE),
('EX-002', '2025-03-15', 5.7, 342.0, 0.9, 2500.0, FALSE),
('EX-002', '2025-03-16', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('EX-002', '2025-03-17', 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('EX-002', '2025-03-18', 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('EX-002', '2025-03-19', 9.5, 570.0, 1.5, 4200.0, FALSE),
('EX-002', '2025-03-20', 9.2, 552.0, 1.4, 4050.0, FALSE),
('EX-002', '2025-03-21', 9.4, 564.0, 1.5, 4150.0, FALSE),
('EX-002', '2025-03-22', 5.4, 324.0, 0.8, 2400.0, FALSE),
('EX-002', '2025-03-23', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('EX-002', '2025-03-24', 9.3, 558.0, 1.4, 4100.0, FALSE),
('EX-002', '2025-03-25', 9.5, 570.0, 1.5, 4200.0, FALSE),
('EX-002', '2025-03-26', 9.4, 564.0, 1.5, 4150.0, FALSE),
('EX-002', '2025-03-27', 9.6, 576.0, 1.5, 4250.0, FALSE),
('EX-002', '2025-03-28', 9.3, 558.0, 1.4, 4100.0, FALSE),
('EX-002', '2025-03-29', 5.6, 336.0, 0.9, 2500.0, FALSE),
('EX-002', '2025-03-30', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('EX-002', '2025-03-31', 9.5, 570.0, 1.5, 4200.0, FALSE);

-- Insert Operational Data for EX-002 (April 2025)
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, material_moved_cubic_meters, maintenance_flag)
VALUES
('EX-002', '2025-04-01', 9.4, 564.0, 1.5, 4150.0, FALSE),
('EX-002', '2025-04-02', 9.5, 570.0, 1.5, 4200.0, FALSE),
('EX-002', '2025-04-03', 9.7, 582.0, 1.6, 4300.0, FALSE),
('EX-002', '2025-04-04', 9.6, 576.0, 1.5, 4250.0, FALSE),
('EX-002', '2025-04-05', 5.4, 324.0, 0.8, 2400.0, FALSE),
('EX-002', '2025-04-06', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('EX-002', '2025-04-07', 9.3, 558.0, 1.4, 4100.0, FALSE),
('EX-002', '2025-04-08', 9.4, 564.0, 1.5, 4150.0, FALSE),
('EX-002', '2025-04-09', 9.2, 552.0, 1.4, 4050.0, FALSE),
('EX-002', '2025-04-10', 9.5, 570.0, 1.5, 4200.0, FALSE),
('EX-002', '2025-04-11', 9.6, 576.0, 1.5, 4250.0, FALSE),
('EX-002', '2025-04-12', 5.5, 330.0, 0.8, 2450.0, FALSE),
('EX-002', '2025-04-13', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('EX-002', '2025-04-14', 9.4, 564.0, 1.5, 4150.0, FALSE),
('EX-002', '2025-04-15', 9.3, 558.0, 1.4, 4100.0, FALSE),
('EX-002', '2025-04-16', 9.5, 570.0, 1.5, 4200.0, FALSE),
('EX-002', '2025-04-17', 9.6, 576.0, 1.5, 4250.0, FALSE),
('EX-002', '2025-04-18', 9.4, 564.0, 1.5, 4150.0, FALSE),
('EX-002', '2025-04-19', 5.6, 336.0, 0.9, 2500.0, FALSE),
('EX-002', '2025-04-20', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('EX-002', '2025-04-21', 9.5, 570.0, 1.5, 4200.0, FALSE),
('EX-002', '2025-04-22', 9.6, 576.0, 1.5, 4250.0, FALSE),
('EX-002', '2025-04-23', 9.4, 564.0, 1.5, 4150.0, FALSE),
('EX-002', '2025-04-24', 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('EX-002', '2025-04-25', 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('EX-002', '2025-04-26', 5.5, 330.0, 0.8, 2450.0, FALSE),
('EX-002', '2025-04-27', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('EX-002', '2025-04-28', 9.4, 564.0, 1.5, 4150.0, FALSE),
('EX-002', '2025-04-29', 9.6, 576.0, 1.5, 4250.0, FALSE),
('EX-002', '2025-04-30', 9.5, 570.0, 1.5, 4200.0, FALSE);

-- Insert Maintenance Events for EX-002
INSERT INTO MaintenanceEvents (machine_id, event_date, event_type, description, parts_replaced, cost, downtime_hours, technician_name)
VALUES
('EX-002', '2025-03-17', 'Preventive Maintenance', 'Regular 250-hour scheduled maintenance', 'Oil filters, fuel filters, air filters', 1550.25, 16.0, 'Daniel Brown'),
('EX-002', '2025-03-18', 'Repair', 'Hydraulic cylinder repair', 'Hydraulic seals, O-rings', 1250.50, 8.0, 'Daniel Brown'),
('EX-002', '2025-04-24', 'Preventive Maintenance', 'Regular 500-hour scheduled maintenance', 'Oil filters, fuel filters, air filters, hydraulic filters', 2350.75, 16.0, 'Samantha Lee'),
('EX-002', '2025-04-25', 'Inspection', 'Boom and stick inspection', 'Boom pins, bushings', 950.25, 8.0, 'Samantha Lee');

-- Insert Alert Events for EX-002
INSERT INTO AlertEvents (machine_id, alert_date, alert_type, severity, description, resolved, resolution_date, resolution_notes)
VALUES
('EX-002', '2025-03-10 09:25:15', 'Swing Bearing Temperature Warning', 'Warning', 'Elevated temperature in swing bearing', TRUE, '2025-03-10 10:40:30', 'Added lubricant and monitored temperature'),
('EX-002', '2025-03-16 14:50:42', 'Hydraulic System Warning', 'Warning', 'Hydraulic oil contamination detected', TRUE, '2025-03-17 09:15:25', 'Addressed during scheduled maintenance'),
('EX-002', '2025-04-14 11:30:18', 'Track Tension Warning', 'Warning', 'Left track tension below optimal range', TRUE, '2025-04-14 13:20:45', 'Adjusted track tension to manufacturer specifications'),
('EX-002', '2025-04-23 08:45:52', 'Boom Cylinder Warning', 'Critical', 'Pressure drop detected in boom cylinder circuit', TRUE, '2025-04-24 15:30:20', 'Repaired hydraulic seals during scheduled maintenance');

-- End of script for EX-002 data
