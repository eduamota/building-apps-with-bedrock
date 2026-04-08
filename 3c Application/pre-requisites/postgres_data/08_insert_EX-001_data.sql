-- SQL script to insert sample data for machine EX-001 into PostgreSQL tables.
-- Assumes the tables were created using the script in postgres_create_tables (with SERIAL keys).
-- Ensure the Machines table already contains the record for 'EX-001'.

-- Insert Operational Data for EX-001 (March 2025)
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, material_moved_cubic_meters, maintenance_flag)
VALUES
('EX-001', '2025-03-01', 9.5, 570.0, 1.5, 4200.0, FALSE),
('EX-001', '2025-03-02', 9.3, 558.0, 1.4, 4100.0, FALSE),
('EX-001', '2025-03-03', 9.7, 582.0, 1.6, 4300.0, FALSE),
('EX-001', '2025-03-04', 9.6, 576.0, 1.5, 4250.0, FALSE),
('EX-001', '2025-03-05', 9.8, 588.0, 1.6, 4350.0, FALSE),
('EX-001', '2025-03-06', 9.4, 564.0, 1.5, 4150.0, FALSE),
('EX-001', '2025-03-07', 9.2, 552.0, 1.4, 4050.0, FALSE),
('EX-001', '2025-03-08', 5.6, 336.0, 0.9, 2500.0, FALSE),
('EX-001', '2025-03-09', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('EX-001', '2025-03-10', 9.5, 570.0, 1.5, 4200.0, FALSE),
('EX-001', '2025-03-11', 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('EX-001', '2025-03-12', 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('EX-001', '2025-03-13', 9.6, 576.0, 1.5, 4250.0, FALSE),
('EX-001', '2025-03-14', 9.7, 582.0, 1.6, 4300.0, FALSE),
('EX-001', '2025-03-15', 5.8, 348.0, 0.9, 2550.0, FALSE),
('EX-001', '2025-03-16', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('EX-001', '2025-03-17', 9.4, 564.0, 1.5, 4150.0, FALSE),
('EX-001', '2025-03-18', 9.5, 570.0, 1.5, 4200.0, FALSE),
('EX-001', '2025-03-19', 9.6, 576.0, 1.5, 4250.0, FALSE),
('EX-001', '2025-03-20', 9.3, 558.0, 1.4, 4100.0, FALSE),
('EX-001', '2025-03-21', 9.2, 552.0, 1.4, 4050.0, FALSE),
('EX-001', '2025-03-22', 5.5, 330.0, 0.8, 2450.0, FALSE),
('EX-001', '2025-03-23', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('EX-001', '2025-03-24', 9.4, 564.0, 1.5, 4150.0, FALSE),
('EX-001', '2025-03-25', 9.6, 576.0, 1.5, 4250.0, FALSE),
('EX-001', '2025-03-26', 9.5, 570.0, 1.5, 4200.0, FALSE),
('EX-001', '2025-03-27', 9.7, 582.0, 1.6, 4300.0, FALSE),
('EX-001', '2025-03-28', 9.4, 564.0, 1.5, 4150.0, FALSE),
('EX-001', '2025-03-29', 5.7, 342.0, 0.9, 2500.0, FALSE),
('EX-001', '2025-03-30', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('EX-001', '2025-03-31', 9.6, 576.0, 1.5, 4250.0, FALSE);

-- Insert Operational Data for EX-001 (April 2025)
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, material_moved_cubic_meters, maintenance_flag)
VALUES
('EX-001', '2025-04-01', 9.5, 570.0, 1.5, 4200.0, FALSE),
('EX-001', '2025-04-02', 9.6, 576.0, 1.5, 4250.0, FALSE),
('EX-001', '2025-04-03', 9.8, 588.0, 1.6, 4350.0, FALSE),
('EX-001', '2025-04-04', 9.7, 582.0, 1.6, 4300.0, FALSE),
('EX-001', '2025-04-05', 5.5, 330.0, 0.8, 2450.0, FALSE),
('EX-001', '2025-04-06', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('EX-001', '2025-04-07', 9.4, 564.0, 1.5, 4150.0, FALSE),
('EX-001', '2025-04-08', 9.5, 570.0, 1.5, 4200.0, FALSE),
('EX-001', '2025-04-09', 9.3, 558.0, 1.4, 4100.0, FALSE),
('EX-001', '2025-04-10', 9.6, 576.0, 1.5, 4250.0, FALSE),
('EX-001', '2025-04-11', 9.7, 582.0, 1.6, 4300.0, FALSE),
('EX-001', '2025-04-12', 5.6, 336.0, 0.9, 2500.0, FALSE),
('EX-001', '2025-04-13', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('EX-001', '2025-04-14', 9.5, 570.0, 1.5, 4200.0, FALSE),
('EX-001', '2025-04-15', 9.4, 564.0, 1.5, 4150.0, FALSE),
('EX-001', '2025-04-16', 9.6, 576.0, 1.5, 4250.0, FALSE),
('EX-001', '2025-04-17', 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('EX-001', '2025-04-18', 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('EX-001', '2025-04-19', 5.7, 342.0, 0.9, 2500.0, FALSE),
('EX-001', '2025-04-20', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('EX-001', '2025-04-21', 9.6, 576.0, 1.5, 4250.0, FALSE),
('EX-001', '2025-04-22', 9.7, 582.0, 1.6, 4300.0, FALSE),
('EX-001', '2025-04-23', 9.5, 570.0, 1.5, 4200.0, FALSE),
('EX-001', '2025-04-24', 9.4, 564.0, 1.5, 4150.0, FALSE),
('EX-001', '2025-04-25', 9.3, 558.0, 1.4, 4100.0, FALSE),
('EX-001', '2025-04-26', 5.6, 336.0, 0.9, 2500.0, FALSE),
('EX-001', '2025-04-27', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('EX-001', '2025-04-28', 9.5, 570.0, 1.5, 4200.0, FALSE),
('EX-001', '2025-04-29', 9.7, 582.0, 1.6, 4300.0, FALSE),
('EX-001', '2025-04-30', 9.6, 576.0, 1.5, 4250.0, FALSE);

-- Insert Maintenance Events for EX-001
INSERT INTO MaintenanceEvents (machine_id, event_date, event_type, description, parts_replaced, cost, downtime_hours, technician_name)
VALUES
('EX-001', '2025-03-11', 'Preventive Maintenance', 'Regular 250-hour scheduled maintenance', 'Oil filters, fuel filters, air filters', 1450.50, 16.0, 'Jennifer Lee'),
('EX-001', '2025-03-12', 'Repair', 'Repair of bucket cylinder', 'Hydraulic seals, O-rings', 1950.75, 8.0, 'Jennifer Lee'),
('EX-001', '2025-04-17', 'Preventive Maintenance', 'Regular 500-hour scheduled maintenance', 'Oil filters, fuel filters, air filters, hydraulic filters', 2450.25, 16.0, 'Thomas Brown'),
('EX-001', '2025-04-18', 'Inspection', 'Thorough inspection of undercarriage', 'Track pad bolts', 850.50, 8.0, 'Thomas Brown');

-- Insert Alert Events for EX-001
INSERT INTO AlertEvents (machine_id, alert_date, alert_type, severity, description, resolved, resolution_date, resolution_notes)
VALUES
('EX-001', '2025-03-05 11:12:45', 'Hydraulic Pressure Warning', 'Warning', 'Fluctuating hydraulic pressure in boom circuit', TRUE, '2025-03-05 13:25:30', 'Cleared contamination from pressure relief valve'),
('EX-001', '2025-03-10 15:38:22', 'Swing Bearing Temperature Warning', 'Warning', 'Elevated temperature in swing bearing', TRUE, '2025-03-11 09:15:45', 'Added lubricant and addressed during scheduled maintenance'),
('EX-001', '2025-04-02 09:27:18', 'Bucket Cylinder Warning', 'Warning', 'Reduced speed in bucket cylinder extension', TRUE, '2025-04-02 10:40:33', 'Adjusted hydraulic flow control valve'),
('EX-001', '2025-04-16 14:05:52', 'Engine Performance Warning', 'Critical', 'Engine power reduction due to high exhaust temperature', TRUE, '2025-04-18 11:30:27', 'Cleaned exhaust system and replaced sensors during maintenance');

-- End of script for EX-001 data
