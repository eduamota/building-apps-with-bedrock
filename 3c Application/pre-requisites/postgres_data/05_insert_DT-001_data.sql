-- SQL script to insert sample data for machine DT-001 into PostgreSQL tables.
-- Assumes the tables were created using the script in postgres_create_tables (with SERIAL keys).
-- Ensure the Machines table already contains the record for 'DT-001'.

-- Insert Operational Data for DT-001 (March 2025)
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, material_moved_cubic_meters, distance_traveled_km, maintenance_flag)
VALUES
('DT-001', '2025-03-01', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE),
('DT-001', '2025-03-02', 9.8, 1200.0, 1.7, 6200.0, 138.0, FALSE),
('DT-001', '2025-03-03', 10.5, 1280.0, 1.9, 6800.0, 152.0, FALSE),
('DT-001', '2025-03-04', 10.3, 1260.0, 1.8, 6600.0, 148.0, FALSE),
('DT-001', '2025-03-05', 10.1, 1240.0, 1.8, 6400.0, 143.0, FALSE),
('DT-001', '2025-03-06', 9.9, 1220.0, 1.7, 6300.0, 140.0, FALSE),
('DT-001', '2025-03-07', 10.4, 1270.0, 1.8, 6700.0, 150.0, FALSE),
('DT-001', '2025-03-08', 6.2, 760.0, 1.1, 3900.0, 88.0, FALSE),
('DT-001', '2025-03-09', 0.0, 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('DT-001', '2025-03-10', 10.3, 1260.0, 1.8, 6600.0, 148.0, FALSE),
('DT-001', '2025-03-11', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE),
('DT-001', '2025-03-12', 10.0, 1230.0, 1.7, 6350.0, 142.0, FALSE),
('DT-001', '2025-03-13', 9.9, 1220.0, 1.7, 6300.0, 140.0, FALSE),
('DT-001', '2025-03-14', 10.1, 1240.0, 1.8, 6400.0, 143.0, FALSE),
('DT-001', '2025-03-15', 6.0, 740.0, 1.0, 3800.0, 85.0, FALSE),
('DT-001', '2025-03-16', 0.0, 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('DT-001', '2025-03-17', 0.0, 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('DT-001', '2025-03-18', 0.0, 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('DT-001', '2025-03-19', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE),
('DT-001', '2025-03-20', 10.4, 1270.0, 1.8, 6700.0, 150.0, FALSE),
('DT-001', '2025-03-21', 10.3, 1260.0, 1.8, 6600.0, 148.0, FALSE),
('DT-001', '2025-03-22', 6.3, 770.0, 1.1, 4000.0, 90.0, FALSE),
('DT-001', '2025-03-23', 0.0, 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('DT-001', '2025-03-24', 10.1, 1240.0, 1.8, 6400.0, 143.0, FALSE),
('DT-001', '2025-03-25', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE),
('DT-001', '2025-03-26', 10.0, 1230.0, 1.7, 6350.0, 142.0, FALSE),
('DT-001', '2025-03-27', 9.8, 1200.0, 1.7, 6200.0, 138.0, FALSE),
('DT-001', '2025-03-28', 9.9, 1220.0, 1.7, 6300.0, 140.0, FALSE),
('DT-001', '2025-03-29', 6.1, 750.0, 1.1, 3850.0, 86.0, FALSE),
('DT-001', '2025-03-30', 0.0, 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('DT-001', '2025-03-31', 10.0, 1230.0, 1.7, 6350.0, 142.0, FALSE);

-- Insert Operational Data for DT-001 (April 2025)
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, material_moved_cubic_meters, distance_traveled_km, maintenance_flag)
VALUES
('DT-001', '2025-04-01', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE),
('DT-001', '2025-04-02', 10.3, 1260.0, 1.8, 6600.0, 148.0, FALSE),
('DT-001', '2025-04-03', 10.4, 1270.0, 1.8, 6700.0, 150.0, FALSE),
('DT-001', '2025-04-04', 10.1, 1240.0, 1.8, 6400.0, 143.0, FALSE),
('DT-001', '2025-04-05', 6.2, 760.0, 1.1, 3900.0, 88.0, FALSE),
('DT-001', '2025-04-06', 0.0, 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('DT-001', '2025-04-07', 10.0, 1230.0, 1.7, 6350.0, 142.0, FALSE),
('DT-001', '2025-04-08', 9.9, 1220.0, 1.7, 6300.0, 140.0, FALSE),
('DT-001', '2025-04-09', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE),
('DT-001', '2025-04-10', 10.3, 1260.0, 1.8, 6600.0, 148.0, FALSE),
('DT-001', '2025-04-11', 10.1, 1240.0, 1.8, 6400.0, 143.0, FALSE),
('DT-001', '2025-04-12', 6.0, 740.0, 1.0, 3800.0, 85.0, FALSE),
('DT-001', '2025-04-13', 0.0, 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('DT-001', '2025-04-14', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE),
('DT-001', '2025-04-15', 10.0, 1230.0, 1.7, 6350.0, 142.0, FALSE),
('DT-001', '2025-04-16', 9.8, 1200.0, 1.7, 6200.0, 138.0, FALSE),
('DT-001', '2025-04-17', 9.9, 1220.0, 1.7, 6300.0, 140.0, FALSE),
('DT-001', '2025-04-18', 10.1, 1240.0, 1.8, 6400.0, 143.0, FALSE),
('DT-001', '2025-04-19', 6.3, 770.0, 1.1, 4000.0, 90.0, FALSE),
('DT-001', '2025-04-20', 0.0, 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('DT-001', '2025-04-21', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE),
('DT-001', '2025-04-22', 0.0, 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('DT-001', '2025-04-23', 0.0, 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('DT-001', '2025-04-24', 10.0, 1230.0, 1.7, 6350.0, 142.0, FALSE),
('DT-001', '2025-04-25', 10.3, 1260.0, 1.8, 6600.0, 148.0, FALSE),
('DT-001', '2025-04-26', 6.1, 750.0, 1.1, 3850.0, 86.0, FALSE),
('DT-001', '2025-04-27', 0.0, 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('DT-001', '2025-04-28', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE),
('DT-001', '2025-04-29', 10.4, 1270.0, 1.8, 6700.0, 150.0, FALSE),
('DT-001', '2025-04-30', 10.1, 1240.0, 1.8, 6400.0, 143.0, FALSE);

-- Insert Maintenance Events for DT-001
INSERT INTO MaintenanceEvents (machine_id, event_date, event_type, description, parts_replaced, cost, downtime_hours, technician_name)
VALUES
('DT-001', '2025-03-17', 'Preventive Maintenance', 'Regular 250-hour scheduled maintenance', 'Oil filters, fuel filters, air filters', 1850.25, 16.0, 'Sarah Williams'),
('DT-001', '2025-03-18', 'Repair', 'Repair of suspension system', 'Suspension bushings, shock absorber', 2350.75, 8.0, 'Sarah Williams'),
('DT-001', '2025-04-22', 'Preventive Maintenance', 'Regular 500-hour scheduled maintenance', 'Oil filters, fuel filters, air filters, transmission filters', 2850.50, 16.0, 'David Miller'),
('DT-001', '2025-04-23', 'Inspection', 'Thorough inspection of braking system', 'Brake pads', 1250.25, 8.0, 'David Miller');

-- Insert Alert Events for DT-001
INSERT INTO AlertEvents (machine_id, alert_date, alert_type, severity, description, resolved, resolution_date, resolution_notes)
VALUES
('DT-001', '2025-03-10 07:52:34', 'Tire Pressure Warning', 'Warning', 'Rear right tire pressure below threshold', TRUE, '2025-03-10 08:30:15', 'Inflated tire to proper pressure and inspected for leaks'),
('DT-001', '2025-03-16 16:18:27', 'Suspension System Warning', 'Warning', 'Abnormal vibration detected in suspension system', TRUE, '2025-03-18 14:22:45', 'Replaced worn suspension components during maintenance'),
('DT-001', '2025-04-05 10:45:52', 'Transmission Temperature Warning', 'Warning', 'Elevated transmission fluid temperature', TRUE, '2025-04-05 11:30:18', 'Reduced load and allowed system to cool, scheduled inspection'),
('DT-001', '2025-04-21 13:27:33', 'Brake System Warning', 'Critical', 'Reduced braking performance detected', TRUE, '2025-04-23 15:40:55', 'Replaced worn brake pads during scheduled maintenance');

-- End of script for DT-001 data
