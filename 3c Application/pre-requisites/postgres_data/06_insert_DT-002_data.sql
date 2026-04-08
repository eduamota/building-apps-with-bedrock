-- SQL script to insert sample data for machine DT-002 into PostgreSQL tables.
-- Assumes the tables were created using the script in postgres_create_tables (with SERIAL keys).
-- Ensure the Machines table already contains the record for 'DT-002'.

-- Insert Operational Data for DT-002 (March 2025)
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, material_moved_cubic_meters, distance_traveled_km, maintenance_flag)
VALUES
('DT-002', '2025-03-01', 10.0, 1230.0, 1.7, 6350.0, 142.0, FALSE),
('DT-002', '2025-03-02', 9.7, 1190.0, 1.7, 6150.0, 137.0, FALSE),
('DT-002', '2025-03-03', 10.3, 1260.0, 1.8, 6600.0, 148.0, FALSE),
('DT-002', '2025-03-04', 10.1, 1240.0, 1.8, 6400.0, 143.0, FALSE),
('DT-002', '2025-03-05', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE),
('DT-002', '2025-03-06', 10.0, 1230.0, 1.7, 6350.0, 142.0, FALSE),
('DT-002', '2025-03-07', 0.0, 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('DT-002', '2025-03-08', 6.0, 740.0, 1.0, 3800.0, 85.0, FALSE),
('DT-002', '2025-03-09', 0.0, 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('DT-002', '2025-03-10', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE),
('DT-002', '2025-03-11', 10.3, 1260.0, 1.8, 6600.0, 148.0, FALSE),
('DT-002', '2025-03-12', 9.9, 1220.0, 1.7, 6300.0, 140.0, FALSE),
('DT-002', '2025-03-13', 10.1, 1240.0, 1.8, 6400.0, 143.0, FALSE),
('DT-002', '2025-03-14', 10.0, 1230.0, 1.7, 6350.0, 142.0, FALSE),
('DT-002', '2025-03-15', 6.1, 750.0, 1.1, 3850.0, 86.0, FALSE),
('DT-002', '2025-03-16', 0.0, 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('DT-002', '2025-03-17', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE),
('DT-002', '2025-03-18', 10.1, 1240.0, 1.8, 6400.0, 143.0, FALSE),
('DT-002', '2025-03-19', 9.8, 1200.0, 1.7, 6200.0, 138.0, FALSE),
('DT-002', '2025-03-20', 10.0, 1230.0, 1.7, 6350.0, 142.0, FALSE),
('DT-002', '2025-03-21', 10.3, 1260.0, 1.8, 6600.0, 148.0, FALSE),
('DT-002', '2025-03-22', 6.2, 760.0, 1.1, 3900.0, 88.0, FALSE),
('DT-002', '2025-03-23', 0.0, 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('DT-002', '2025-03-24', 10.1, 1240.0, 1.8, 6400.0, 143.0, FALSE),
('DT-002', '2025-03-25', 10.0, 1230.0, 1.7, 6350.0, 142.0, FALSE),
('DT-002', '2025-03-26', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE),
('DT-002', '2025-03-27', 9.9, 1220.0, 1.7, 6300.0, 140.0, FALSE),
('DT-002', '2025-03-28', 10.1, 1240.0, 1.8, 6400.0, 143.0, FALSE),
('DT-002', '2025-03-29', 6.0, 740.0, 1.0, 3800.0, 85.0, FALSE),
('DT-002', '2025-03-30', 0.0, 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('DT-002', '2025-03-31', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE);

-- Insert Operational Data for DT-002 (April 2025)
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, material_moved_cubic_meters, distance_traveled_km, maintenance_flag)
VALUES
('DT-002', '2025-04-01', 10.0, 1230.0, 1.7, 6350.0, 142.0, FALSE),
('DT-002', '2025-04-02', 10.1, 1240.0, 1.8, 6400.0, 143.0, FALSE),
('DT-002', '2025-04-03', 10.3, 1260.0, 1.8, 6600.0, 148.0, FALSE),
('DT-002', '2025-04-04', 9.9, 1220.0, 1.7, 6300.0, 140.0, FALSE),
('DT-002', '2025-04-05', 6.1, 750.0, 1.1, 3850.0, 86.0, FALSE),
('DT-002', '2025-04-06', 0.0, 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('DT-002', '2025-04-07', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE),
('DT-002', '2025-04-08', 10.0, 1230.0, 1.7, 6350.0, 142.0, FALSE),
('DT-002', '2025-04-09', 10.1, 1240.0, 1.8, 6400.0, 143.0, FALSE),
('DT-002', '2025-04-10', 9.8, 1200.0, 1.7, 6200.0, 138.0, FALSE),
('DT-002', '2025-04-11', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE),
('DT-002', '2025-04-12', 6.0, 740.0, 1.0, 3800.0, 85.0, FALSE),
('DT-002', '2025-04-13', 0.0, 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('DT-002', '2025-04-14', 10.1, 1240.0, 1.8, 6400.0, 143.0, FALSE),
('DT-002', '2025-04-15', 10.3, 1260.0, 1.8, 6600.0, 148.0, FALSE),
('DT-002', '2025-04-16', 0.0, 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('DT-002', '2025-04-17', 0.0, 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('DT-002', '2025-04-18', 10.0, 1230.0, 1.7, 6350.0, 142.0, FALSE),
('DT-002', '2025-04-19', 6.2, 760.0, 1.1, 3900.0, 88.0, FALSE),
('DT-002', '2025-04-20', 0.0, 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('DT-002', '2025-04-21', 10.1, 1240.0, 1.8, 6400.0, 143.0, FALSE),
('DT-002', '2025-04-22', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE),
('DT-002', '2025-04-23', 10.0, 1230.0, 1.7, 6350.0, 142.0, FALSE),
('DT-002', '2025-04-24', 9.9, 1220.0, 1.7, 6300.0, 140.0, FALSE),
('DT-002', '2025-04-25', 10.3, 1260.0, 1.8, 6600.0, 148.0, FALSE),
('DT-002', '2025-04-26', 6.1, 750.0, 1.1, 3850.0, 86.0, FALSE),
('DT-002', '2025-04-27', 0.0, 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('DT-002', '2025-04-28', 10.0, 1230.0, 1.7, 6350.0, 142.0, FALSE),
('DT-002', '2025-04-29', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE),
('DT-002', '2025-04-30', 10.1, 1240.0, 1.8, 6400.0, 143.0, FALSE);

-- Insert Maintenance Events for DT-002
INSERT INTO MaintenanceEvents (machine_id, event_date, event_type, description, parts_replaced, cost, downtime_hours, technician_name)
VALUES
('DT-002', '2025-03-07', 'Preventive Maintenance', 'Regular 250-hour scheduled maintenance', 'Oil filters, fuel filters, air filters', 1750.25, 8.0, 'Rebecca Williams'),
('DT-002', '2025-04-16', 'Preventive Maintenance', 'Regular 500-hour scheduled maintenance', 'Oil filters, fuel filters, air filters, transmission filters', 2650.50, 16.0, 'Carlos Martinez'),
('DT-002', '2025-04-17', 'Repair', 'Steering system inspection and repair', 'Steering pump, hydraulic lines', 1950.75, 8.0, 'Carlos Martinez');

-- Insert Alert Events for DT-002
INSERT INTO AlertEvents (machine_id, alert_date, alert_type, severity, description, resolved, resolution_date, resolution_notes)
VALUES
('DT-002', '2025-03-06 08:35:42', 'Transmission Temperature Warning', 'Warning', 'Elevated transmission fluid temperature', TRUE, '2025-03-06 09:20:15', 'Allowed system to cool and inspected cooling system'),
('DT-002', '2025-03-06 16:48:19', 'Engine Performance Warning', 'Warning', 'Reduced engine power detected', TRUE, '2025-03-07 10:15:40', 'Addressed during scheduled maintenance'),
('DT-002', '2025-04-12 12:30:55', 'Tire Pressure Warning', 'Warning', 'Front left tire pressure below threshold', TRUE, '2025-04-12 13:45:30', 'Inflated tire to proper pressure and inspected for leaks'),
('DT-002', '2025-04-15 09:22:18', 'Steering System Warning', 'Critical', 'Increased resistance in steering system', TRUE, '2025-04-17 14:30:45', 'Repaired steering pump during maintenance');

-- End of script for DT-002 data
