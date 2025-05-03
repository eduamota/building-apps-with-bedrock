-- SQL script to insert sample data for machine EX-003 into PostgreSQL tables.
-- Assumes the tables were created using the script in postgres_create_tables (with SERIAL keys).
-- Ensure the Machines table already contains the record for 'EX-003'.

-- Insert Operational Data for EX-003 (March 2025)
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, material_moved_cubic_meters, maintenance_flag)
VALUES
('EX-003', '2025-03-01', 9.3, 558.0, 1.4, 4100.0, FALSE),
('EX-003', '2025-03-02', 9.1, 546.0, 1.4, 4000.0, FALSE),
('EX-003', '2025-03-03', 9.5, 570.0, 1.5, 4200.0, FALSE),
('EX-003', '2025-03-04', 9.4, 564.0, 1.5, 4150.0, FALSE),
('EX-003', '2025-03-05', 9.6, 576.0, 1.5, 4250.0, FALSE),
('EX-003', '2025-03-06', 9.2, 552.0, 1.4, 4050.0, FALSE),
('EX-003', '2025-03-07', 9.0, 540.0, 1.3, 3950.0, FALSE),
('EX-003', '2025-03-08', 5.4, 324.0, 0.8, 2400.0, FALSE),
('EX-003', '2025-03-09', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('EX-003', '2025-03-10', 9.3, 558.0, 1.4, 4100.0, FALSE),
('EX-003', '2025-03-11', 9.5, 570.0, 1.5, 4200.0, FALSE),
('EX-003', '2025-03-12', 9.4, 564.0, 1.5, 4150.0, FALSE),
('EX-003', '2025-03-13', 9.6, 576.0, 1.5, 4250.0, FALSE),
('EX-003', '2025-03-14', 9.2, 552.0, 1.4, 4050.0, FALSE),
('EX-003', '2025-03-15', 5.6, 336.0, 0.9, 2450.0, FALSE),
('EX-003', '2025-03-16', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('EX-003', '2025-03-17', 9.3, 558.0, 1.4, 4100.0, FALSE),
('EX-003', '2025-03-18', 9.4, 564.0, 1.5, 4150.0, FALSE),
('EX-003', '2025-03-19', 9.6, 576.0, 1.5, 4250.0, FALSE),
('EX-003', '2025-03-20', 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('EX-003', '2025-03-21', 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('EX-003', '2025-03-22', 5.3, 318.0, 0.8, 2350.0, FALSE),
('EX-003', '2025-03-23', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('EX-003', '2025-03-24', 9.2, 552.0, 1.4, 4050.0, FALSE),
('EX-003', '2025-03-25', 9.4, 564.0, 1.5, 4150.0, FALSE),
('EX-003', '2025-03-26', 9.3, 558.0, 1.4, 4100.0, FALSE),
('EX-003', '2025-03-27', 9.5, 570.0, 1.5, 4200.0, FALSE),
('EX-003', '2025-03-28', 9.2, 552.0, 1.4, 4050.0, FALSE),
('EX-003', '2025-03-29', 5.5, 330.0, 0.8, 2400.0, FALSE),
('EX-003', '2025-03-30', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('EX-003', '2025-03-31', 9.4, 564.0, 1.5, 4150.0, FALSE);

-- Insert Operational Data for EX-003 (April 2025)
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, material_moved_cubic_meters, maintenance_flag)
VALUES
('EX-003', '2025-04-01', 9.3, 558.0, 1.4, 4100.0, FALSE),
('EX-003', '2025-04-02', 9.4, 564.0, 1.5, 4150.0, FALSE),
('EX-003', '2025-04-03', 9.6, 576.0, 1.5, 4250.0, FALSE),
('EX-003', '2025-04-04', 9.5, 570.0, 1.5, 4200.0, FALSE),
('EX-003', '2025-04-05', 5.3, 318.0, 0.8, 2350.0, FALSE),
('EX-003', '2025-04-06', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('EX-003', '2025-04-07', 9.2, 552.0, 1.4, 4050.0, FALSE),
('EX-003', '2025-04-08', 9.3, 558.0, 1.4, 4100.0, FALSE),
('EX-003', '2025-04-09', 9.1, 546.0, 1.4, 4000.0, FALSE),
('EX-003', '2025-04-10', 9.4, 564.0, 1.5, 4150.0, FALSE),
('EX-003', '2025-04-11', 9.5, 570.0, 1.5, 4200.0, FALSE),
('EX-003', '2025-04-12', 5.4, 324.0, 0.8, 2400.0, FALSE),
('EX-003', '2025-04-13', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('EX-003', '2025-04-14', 9.3, 558.0, 1.4, 4100.0, FALSE),
('EX-003', '2025-04-15', 9.2, 552.0, 1.4, 4050.0, FALSE),
('EX-003', '2025-04-16', 9.4, 564.0, 1.5, 4150.0, FALSE),
('EX-003', '2025-04-17', 9.5, 570.0, 1.5, 4200.0, FALSE),
('EX-003', '2025-04-18', 9.3, 558.0, 1.4, 4100.0, FALSE),
('EX-003', '2025-04-19', 5.5, 330.0, 0.8, 2400.0, FALSE),
('EX-003', '2025-04-20', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('EX-003', '2025-04-21', 9.4, 564.0, 1.5, 4150.0, FALSE),
('EX-003', '2025-04-22', 9.5, 570.0, 1.5, 4200.0, FALSE),
('EX-003', '2025-04-23', 9.3, 558.0, 1.4, 4100.0, FALSE),
('EX-003', '2025-04-24', 9.2, 552.0, 1.4, 4050.0, FALSE),
('EX-003', '2025-04-25', 9.4, 564.0, 1.5, 4150.0, FALSE),
('EX-003', '2025-04-26', 5.4, 324.0, 0.8, 2400.0, FALSE),
('EX-003', '2025-04-27', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('EX-003', '2025-04-28', 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('EX-003', '2025-04-29', 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('EX-003', '2025-04-30', 9.3, 558.0, 1.4, 4100.0, FALSE);

-- Insert Maintenance Events for EX-003
INSERT INTO MaintenanceEvents (machine_id, event_date, event_type, description, parts_replaced, cost, downtime_hours, technician_name)
VALUES
('EX-003', '2025-03-20', 'Preventive Maintenance', 'Regular 250-hour scheduled maintenance', 'Oil filters, fuel filters, air filters', 1450.75, 16.0, 'Emily Johnson'),
('EX-003', '2025-03-21', 'Repair', 'Track tension system repair', 'Track adjuster, seals', 1150.50, 8.0, 'Emily Johnson'),
('EX-003', '2025-04-28', 'Preventive Maintenance', 'Regular 500-hour scheduled maintenance', 'Oil filters, fuel filters, air filters, hydraulic filters', 2250.25, 16.0, 'Ryan Thompson'),
('EX-003', '2025-04-29', 'Inspection', 'Engine performance inspection', 'Fuel injectors', 1050.75, 8.0, 'Ryan Thompson');

-- Insert Alert Events for EX-003
INSERT INTO AlertEvents (machine_id, alert_date, alert_type, severity, description, resolved, resolution_date, resolution_notes)
VALUES
('EX-003', '2025-03-15 10:18:27', 'Engine Performance Warning', 'Warning', 'Reduced engine power detected', TRUE, '2025-03-15 11:45:50', 'Cleaned air filter and checked fuel quality'),
('EX-003', '2025-03-19 15:42:33', 'Undercarriage Warning', 'Warning', 'Accelerated wear on track components', TRUE, '2025-03-20 10:30:15', 'Scheduled inspection during maintenance'),
('EX-003', '2025-04-12 09:20:45', 'Hydraulic Temperature Warning', 'Warning', 'Elevated hydraulic fluid temperature', TRUE, '2025-04-12 10:15:30', 'Allowed system to cool and inspected cooling components'),
('EX-003', '2025-04-27 14:35:18', 'Low Coolant Level', 'Critical', 'Coolant level below minimum threshold', TRUE, '2025-04-28 09:10:42', 'Added coolant and addressed during scheduled maintenance');

-- End of script for EX-003 data
