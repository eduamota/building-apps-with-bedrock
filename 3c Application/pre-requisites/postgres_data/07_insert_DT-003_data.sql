-- SQL script to insert sample data for machine DT-003 into PostgreSQL tables.
-- Assumes the tables were created using the script in postgres_create_tables (with SERIAL keys).
-- Ensure the Machines table already contains the record for 'DT-003'.

-- Insert Operational Data for DT-003 (March 2025)
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, material_moved_cubic_meters, distance_traveled_km, maintenance_flag)
VALUES
('DT-003', '2025-03-01', 10.1, 1240.0, 1.8, 6400.0, 143.0, FALSE),
('DT-003', '2025-03-02', 9.8, 1200.0, 1.7, 6200.0, 138.0, FALSE),
('DT-003', '2025-03-03', 10.4, 1270.0, 1.8, 6700.0, 150.0, FALSE),
('DT-003', '2025-03-04', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE),
('DT-003', '2025-03-05', 10.3, 1260.0, 1.8, 6600.0, 148.0, FALSE),
('DT-003', '2025-03-06', 10.1, 1240.0, 1.8, 6400.0, 143.0, FALSE),
('DT-003', '2025-03-07', 10.0, 1230.0, 1.7, 6350.0, 142.0, FALSE),
('DT-003', '2025-03-08', 6.1, 750.0, 1.1, 3850.0, 86.0, FALSE),
('DT-003', '2025-03-09', 0.0, 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('DT-003', '2025-03-10', 10.3, 1260.0, 1.8, 6600.0, 148.0, FALSE),
('DT-003', '2025-03-11', 10.4, 1270.0, 1.8, 6700.0, 150.0, FALSE),
('DT-003', '2025-03-12', 10.0, 1230.0, 1.7, 6350.0, 142.0, FALSE),
('DT-003', '2025-03-13', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE),
('DT-003', '2025-03-14', 10.1, 1240.0, 1.8, 6400.0, 143.0, FALSE),
('DT-003', '2025-03-15', 6.2, 760.0, 1.1, 3900.0, 88.0, FALSE),
('DT-003', '2025-03-16', 0.0, 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('DT-003', '2025-03-17', 10.3, 1260.0, 1.8, 6600.0, 148.0, FALSE),
('DT-003', '2025-03-18', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE),
('DT-003', '2025-03-19', 9.9, 1220.0, 1.7, 6300.0, 140.0, FALSE),
('DT-003', '2025-03-20', 0.0, 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('DT-003', '2025-03-21', 0.0, 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('DT-003', '2025-03-22', 6.3, 770.0, 1.1, 4000.0, 90.0, FALSE),
('DT-003', '2025-03-23', 0.0, 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('DT-003', '2025-03-24', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE),
('DT-003', '2025-03-25', 10.1, 1240.0, 1.8, 6400.0, 143.0, FALSE),
('DT-003', '2025-03-26', 10.3, 1260.0, 1.8, 6600.0, 148.0, FALSE),
('DT-003', '2025-03-27', 10.0, 1230.0, 1.7, 6350.0, 142.0, FALSE),
('DT-003', '2025-03-28', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE),
('DT-003', '2025-03-29', 6.1, 750.0, 1.1, 3850.0, 86.0, FALSE),
('DT-003', '2025-03-30', 0.0, 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('DT-003', '2025-03-31', 10.3, 1260.0, 1.8, 6600.0, 148.0, FALSE);

-- Insert Operational Data for DT-003 (April 2025)
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, material_moved_cubic_meters, distance_traveled_km, maintenance_flag)
VALUES
('DT-003', '2025-04-01', 10.1, 1240.0, 1.8, 6400.0, 143.0, FALSE),
('DT-003', '2025-04-02', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE),
('DT-003', '2025-04-03', 10.4, 1270.0, 1.8, 6700.0, 150.0, FALSE),
('DT-003', '2025-04-04', 10.0, 1230.0, 1.7, 6350.0, 142.0, FALSE),
('DT-003', '2025-04-05', 6.2, 760.0, 1.1, 3900.0, 88.0, FALSE),
('DT-003', '2025-04-06', 0.0, 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('DT-003', '2025-04-07', 10.3, 1260.0, 1.8, 6600.0, 148.0, FALSE),
('DT-003', '2025-04-08', 10.1, 1240.0, 1.8, 6400.0, 143.0, FALSE),
('DT-003', '2025-04-09', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE),
('DT-003', '2025-04-10', 9.9, 1220.0, 1.7, 6300.0, 140.0, FALSE),
('DT-003', '2025-04-11', 10.3, 1260.0, 1.8, 6600.0, 148.0, FALSE),
('DT-003', '2025-04-12', 6.1, 750.0, 1.1, 3850.0, 86.0, FALSE),
('DT-003', '2025-04-13', 0.0, 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('DT-003', '2025-04-14', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE),
('DT-003', '2025-04-15', 10.4, 1270.0, 1.8, 6700.0, 150.0, FALSE),
('DT-003', '2025-04-16', 10.1, 1240.0, 1.8, 6400.0, 143.0, FALSE),
('DT-003', '2025-04-17', 10.0, 1230.0, 1.7, 6350.0, 142.0, FALSE),
('DT-003', '2025-04-18', 10.3, 1260.0, 1.8, 6600.0, 148.0, FALSE),
('DT-003', '2025-04-19', 6.3, 770.0, 1.1, 4000.0, 90.0, FALSE),
('DT-003', '2025-04-20', 0.0, 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('DT-003', '2025-04-21', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE),
('DT-003', '2025-04-22', 10.3, 1260.0, 1.8, 6600.0, 148.0, FALSE),
('DT-003', '2025-04-23', 10.1, 1240.0, 1.8, 6400.0, 143.0, FALSE),
('DT-003', '2025-04-24', 10.0, 1230.0, 1.7, 6350.0, 142.0, FALSE),
('DT-003', '2025-04-25', 0.0, 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('DT-003', '2025-04-26', 6.2, 760.0, 1.1, 3900.0, 88.0, FALSE),
('DT-003', '2025-04-27', 0.0, 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('DT-003', '2025-04-28', 10.1, 1240.0, 1.8, 6400.0, 143.0, FALSE),
('DT-003', '2025-04-29', 10.3, 1260.0, 1.8, 6600.0, 148.0, FALSE),
('DT-003', '2025-04-30', 10.2, 1250.0, 1.8, 6500.0, 145.0, FALSE);

-- Insert Maintenance Events for DT-003
INSERT INTO MaintenanceEvents (machine_id, event_date, event_type, description, parts_replaced, cost, downtime_hours, technician_name)
VALUES
('DT-003', '2025-03-20', 'Preventive Maintenance', 'Regular 250-hour scheduled maintenance', 'Oil filters, fuel filters, air filters', 1850.50, 16.0, 'Maria Gonzalez'),
('DT-003', '2025-03-21', 'Repair', 'Electrical system inspection and repair', 'Battery cables, alternator belt', 1250.25, 8.0, 'Maria Gonzalez'),
('DT-003', '2025-04-25', 'Preventive Maintenance', 'Regular 500-hour scheduled maintenance', 'Oil filters, fuel filters, air filters, transmission filters', 2750.75, 16.0, 'Anthony Wilson');

-- Insert Alert Events for DT-003
INSERT INTO AlertEvents (machine_id, alert_date, alert_type, severity, description, resolved, resolution_date, resolution_notes)
VALUES
('DT-003', '2025-03-12 07:45:33', 'Electrical System Warning', 'Warning', 'Battery charging system performance degraded', TRUE, '2025-03-12 09:20:15', 'Tightened connections and tested alternator output'),
('DT-003', '2025-03-19 15:38:27', 'Brake System Warning', 'Critical', 'Uneven braking performance detected', TRUE, '2025-03-20 11:50:40', 'Inspected brake system during scheduled maintenance'),
('DT-003', '2025-04-15 10:22:56', 'Engine Oil Pressure Warning', 'Warning', 'Engine oil pressure fluctuation detected', TRUE, '2025-04-15 11:45:18', 'Changed engine oil and filter ahead of schedule'),
('DT-003', '2025-04-24 13:15:42', 'Exhaust System Warning', 'Warning', 'Elevated exhaust temperature detected', TRUE, '2025-04-25 09:30:55', 'Inspected exhaust system during scheduled maintenance');

-- End of script for DT-003 data
