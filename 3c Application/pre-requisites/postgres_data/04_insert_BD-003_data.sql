-- SQL script to insert sample data for machine BD-003 into PostgreSQL tables.
-- Assumes the tables were created using the script in postgres_create_tables (with SERIAL keys).
-- Ensure the Machines table already contains the record for 'BD-003'.

-- Insert Operational Data for BD-003 (March 2025)
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, material_moved_cubic_meters, maintenance_flag)
VALUES
('BD-003', '2025-03-01', 8.8, 528.0, 1.3, 12900.0, FALSE),
('BD-003', '2025-03-02', 9.2, 552.0, 1.4, 13500.0, FALSE),
('BD-003', '2025-03-03', 9.0, 540.0, 1.3, 13200.0, FALSE),
('BD-003', '2025-03-04', 8.9, 534.0, 1.3, 13100.0, FALSE),
('BD-003', '2025-03-05', 8.7, 522.0, 1.2, 12800.0, FALSE),
('BD-003', '2025-03-06', 9.1, 546.0, 1.3, 13400.0, FALSE),
('BD-003', '2025-03-07', 8.8, 528.0, 1.3, 12900.0, FALSE),
('BD-003', '2025-03-08', 5.5, 330.0, 0.8, 8000.0, FALSE),
('BD-003', '2025-03-09', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('BD-003', '2025-03-10', 9.0, 540.0, 1.3, 13200.0, FALSE),
('BD-003', '2025-03-11', 8.8, 528.0, 1.3, 12900.0, FALSE),
('BD-003', '2025-03-12', 8.9, 534.0, 1.3, 13100.0, FALSE),
('BD-003', '2025-03-13', 8.7, 522.0, 1.2, 12800.0, FALSE),
('BD-003', '2025-03-14', 8.6, 516.0, 1.2, 12600.0, FALSE),
('BD-003', '2025-03-15', 5.7, 342.0, 0.8, 8300.0, FALSE),
('BD-003', '2025-03-16', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('BD-003', '2025-03-17', 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('BD-003', '2025-03-18', 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('BD-003', '2025-03-19', 8.9, 534.0, 1.3, 13100.0, FALSE),
('BD-003', '2025-03-20', 9.1, 546.0, 1.3, 13400.0, FALSE),
('BD-003', '2025-03-21', 8.7, 522.0, 1.2, 12800.0, FALSE),
('BD-003', '2025-03-22', 5.4, 324.0, 0.8, 7900.0, FALSE),
('BD-003', '2025-03-23', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('BD-003', '2025-03-24', 8.9, 534.0, 1.3, 13100.0, FALSE),
('BD-003', '2025-03-25', 8.8, 528.0, 1.3, 12900.0, FALSE),
('BD-003', '2025-03-26', 9.0, 540.0, 1.3, 13200.0, FALSE),
('BD-003', '2025-03-27', 9.2, 552.0, 1.4, 13500.0, FALSE),
('BD-003', '2025-03-28', 8.9, 534.0, 1.3, 13100.0, FALSE),
('BD-003', '2025-03-29', 5.6, 336.0, 0.8, 8200.0, FALSE),
('BD-003', '2025-03-30', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('BD-003', '2025-03-31', 8.8, 528.0, 1.3, 12900.0, FALSE);

-- Insert Operational Data for BD-003 (April 2025)
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, material_moved_cubic_meters, maintenance_flag)
VALUES
('BD-003', '2025-04-01', 9.0, 540.0, 1.3, 13200.0, FALSE),
('BD-003', '2025-04-02', 9.1, 546.0, 1.3, 13400.0, FALSE),
('BD-003', '2025-04-03', 8.9, 534.0, 1.3, 13100.0, FALSE),
('BD-003', '2025-04-04', 8.7, 522.0, 1.2, 12800.0, FALSE),
('BD-003', '2025-04-05', 5.5, 330.0, 0.8, 8000.0, FALSE),
('BD-003', '2025-04-06', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('BD-003', '2025-04-07', 8.8, 528.0, 1.3, 12900.0, FALSE),
('BD-003', '2025-04-08', 9.0, 540.0, 1.3, 13200.0, FALSE),
('BD-003', '2025-04-09', 9.2, 552.0, 1.4, 13500.0, FALSE),
('BD-003', '2025-04-10', 8.9, 534.0, 1.3, 13100.0, FALSE),
('BD-003', '2025-04-11', 8.8, 528.0, 1.3, 12900.0, FALSE),
('BD-003', '2025-04-12', 5.6, 336.0, 0.8, 8200.0, FALSE),
('BD-003', '2025-04-13', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('BD-003', '2025-04-14', 9.0, 540.0, 1.3, 13200.0, FALSE),
('BD-003', '2025-04-15', 8.9, 534.0, 1.3, 13100.0, FALSE),
('BD-003', '2025-04-16', 8.7, 522.0, 1.2, 12800.0, FALSE),
('BD-003', '2025-04-17', 8.8, 528.0, 1.3, 12900.0, FALSE),
('BD-003', '2025-04-18', 9.1, 546.0, 1.3, 13400.0, FALSE),
('BD-003', '2025-04-19', 5.4, 324.0, 0.8, 7900.0, FALSE),
('BD-003', '2025-04-20', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('BD-003', '2025-04-21', 8.9, 534.0, 1.3, 13100.0, FALSE),
('BD-003', '2025-04-22', 9.1, 546.0, 1.3, 13400.0, FALSE),
('BD-003', '2025-04-23', 9.0, 540.0, 1.3, 13200.0, FALSE),
('BD-003', '2025-04-24', 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('BD-003', '2025-04-25', 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('BD-003', '2025-04-26', 5.7, 342.0, 0.8, 8300.0, FALSE),
('BD-003', '2025-04-27', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('BD-003', '2025-04-28', 8.8, 528.0, 1.3, 12900.0, FALSE),
('BD-003', '2025-04-29', 9.0, 540.0, 1.3, 13200.0, FALSE),
('BD-003', '2025-04-30', 9.1, 546.0, 1.3, 13400.0, FALSE);

-- Insert Maintenance Events for BD-003
INSERT INTO MaintenanceEvents (machine_id, event_date, event_type, description, parts_replaced, cost, downtime_hours, technician_name)
VALUES
('BD-003', '2025-03-17', 'Preventive Maintenance', 'Regular 250-hour scheduled maintenance', 'Oil filters, fuel filters, air filters', 1350.50, 16.0, 'Luis Rodriguez'),
('BD-003', '2025-03-18', 'Repair', 'Repair of final drive system', 'Seals, bearings', 1850.25, 8.0, 'Luis Rodriguez'),
('BD-003', '2025-04-24', 'Preventive Maintenance', 'Regular 500-hour scheduled maintenance', 'Oil filters, fuel filters, air filters, hydraulic filters', 2150.75, 16.0, 'Jason Kim'),
('BD-003', '2025-04-25', 'Inspection', 'Undercarriage inspection and measurement', 'Track bolts', 950.50, 8.0, 'Jason Kim');

-- Insert Alert Events for BD-003
INSERT INTO AlertEvents (machine_id, alert_date, alert_type, severity, description, resolved, resolution_date, resolution_notes)
VALUES
('BD-003', '2025-03-08 11:38:27', 'Drive System Warning', 'Warning', 'Abnormal vibration detected in final drive', TRUE, '2025-03-08 13:15:50', 'Adjusted track tension and scheduled for detailed inspection'),
('BD-003', '2025-03-16 15:22:15', 'Low Engine Oil Pressure', 'Critical', 'Engine oil pressure below minimum threshold', TRUE, '2025-03-17 08:45:30', 'Added oil and addressed during scheduled maintenance'),
('BD-003', '2025-04-10 10:05:48', 'Battery Voltage Warning', 'Warning', 'Battery voltage below optimal range', TRUE, '2025-04-10 11:30:15', 'Recharged battery and tested charging system'),
('BD-003', '2025-04-23 14:12:37', 'Undercarriage Wear Warning', 'Warning', 'Accelerated wear detected on track components', TRUE, '2025-04-24 16:35:22', 'Scheduled undercarriage inspection during maintenance');

-- End of script for BD-003 data
