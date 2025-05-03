-- SQL script to insert sample data for machine BD-001 into PostgreSQL tables.
-- Assumes the tables were created using the script in postgres_create_tables (with SERIAL keys).
-- Ensure the Machines table already contains the record for 'BD-001'.

-- Insert Operational Data for BD-001 (March 2025)
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, material_moved_cubic_meters, maintenance_flag)
VALUES
('BD-001', '2025-03-01', 8.5, 510.0, 1.2, 12500.0, FALSE),
('BD-001', '2025-03-02', 9.0, 540.0, 1.3, 13200.0, FALSE),
('BD-001', '2025-03-03', 8.7, 522.0, 1.1, 12800.0, FALSE),
('BD-001', '2025-03-04', 7.5, 450.0, 1.0, 11000.0, FALSE),
('BD-001', '2025-03-05', 8.3, 498.0, 1.2, 12200.0, FALSE),
('BD-001', '2025-03-06', 8.8, 528.0, 1.3, 12900.0, FALSE),
('BD-001', '2025-03-07', 9.2, 552.0, 1.4, 13500.0, FALSE),
('BD-001', '2025-03-08', 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('BD-001', '2025-03-09', 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('BD-001', '2025-03-10', 8.5, 510.0, 1.1, 12500.0, FALSE),
('BD-001', '2025-03-11', 8.7, 522.0, 1.2, 12800.0, FALSE),
('BD-001', '2025-03-12', 8.9, 534.0, 1.3, 13100.0, FALSE),
('BD-001', '2025-03-13', 9.1, 546.0, 1.4, 13400.0, FALSE),
('BD-001', '2025-03-14', 8.8, 528.0, 1.3, 12900.0, FALSE),
('BD-001', '2025-03-15', 5.5, 330.0, 0.8, 8100.0, FALSE),
('BD-001', '2025-03-16', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('BD-001', '2025-03-17', 8.6, 516.0, 1.2, 12600.0, FALSE),
('BD-001', '2025-03-18', 8.7, 522.0, 1.2, 12800.0, FALSE),
('BD-001', '2025-03-19', 8.9, 534.0, 1.3, 13100.0, FALSE),
('BD-001', '2025-03-20', 8.8, 528.0, 1.3, 12900.0, FALSE),
('BD-001', '2025-03-21', 8.5, 510.0, 1.2, 12500.0, FALSE),
('BD-001', '2025-03-22', 5.0, 300.0, 0.7, 7350.0, FALSE),
('BD-001', '2025-03-23', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('BD-001', '2025-03-24', 8.7, 522.0, 1.2, 12800.0, FALSE),
('BD-001', '2025-03-25', 8.6, 516.0, 1.2, 12600.0, FALSE),
('BD-001', '2025-03-26', 8.5, 510.0, 1.2, 12500.0, FALSE),
('BD-001', '2025-03-27', 8.4, 504.0, 1.1, 12300.0, FALSE),
('BD-001', '2025-03-28', 8.6, 516.0, 1.2, 12600.0, FALSE),
('BD-001', '2025-03-29', 5.2, 312.0, 0.8, 7640.0, FALSE),
('BD-001', '2025-03-30', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('BD-001', '2025-03-31', 8.8, 528.0, 1.3, 12900.0, FALSE);

-- Insert Operational Data for BD-001 (April 2025)
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, material_moved_cubic_meters, maintenance_flag)
VALUES
('BD-001', '2025-04-01', 8.7, 522.0, 1.2, 12800.0, FALSE),
('BD-001', '2025-04-02', 8.9, 534.0, 1.3, 13100.0, FALSE),
('BD-001', '2025-04-03', 9.0, 540.0, 1.3, 13200.0, FALSE),
('BD-001', '2025-04-04', 8.8, 528.0, 1.3, 12900.0, FALSE),
('BD-001', '2025-04-05', 5.3, 318.0, 0.8, 7790.0, FALSE),
('BD-001', '2025-04-06', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('BD-001', '2025-04-07', 8.5, 510.0, 1.2, 12500.0, FALSE),
('BD-001', '2025-04-08', 8.7, 522.0, 1.2, 12800.0, FALSE),
('BD-001', '2025-04-09', 8.6, 516.0, 1.2, 12600.0, FALSE),
('BD-001', '2025-04-10', 8.9, 534.0, 1.3, 13100.0, FALSE),
('BD-001', '2025-04-11', 8.7, 522.0, 1.2, 12800.0, FALSE),
('BD-001', '2025-04-12', 5.5, 330.0, 0.8, 8100.0, FALSE),
('BD-001', '2025-04-13', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('BD-001', '2025-04-14', 8.8, 528.0, 1.3, 12900.0, FALSE),
('BD-001', '2025-04-15', 8.7, 522.0, 1.2, 12800.0, FALSE),
('BD-001', '2025-04-16', 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('BD-001', '2025-04-17', 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('BD-001', '2025-04-18', 8.5, 510.0, 1.2, 12500.0, FALSE),
('BD-001', '2025-04-19', 5.2, 312.0, 0.8, 7640.0, FALSE),
('BD-001', '2025-04-20', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('BD-001', '2025-04-21', 8.6, 516.0, 1.2, 12600.0, FALSE),
('BD-001', '2025-04-22', 8.7, 522.0, 1.2, 12800.0, FALSE),
('BD-001', '2025-04-23', 8.9, 534.0, 1.3, 13100.0, FALSE),
('BD-001', '2025-04-24', 8.8, 528.0, 1.3, 12900.0, FALSE),
('BD-001', '2025-04-25', 8.7, 522.0, 1.2, 12800.0, FALSE),
('BD-001', '2025-04-26', 5.4, 324.0, 0.8, 7940.0, FALSE),
('BD-001', '2025-04-27', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('BD-001', '2025-04-28', 8.6, 516.0, 1.2, 12600.0, FALSE),
('BD-001', '2025-04-29', 8.8, 528.0, 1.3, 12900.0, FALSE),
('BD-001', '2025-04-30', 8.7, 522.0, 1.2, 12800.0, FALSE);

-- Insert Maintenance Events for BD-001
INSERT INTO MaintenanceEvents (machine_id, event_date, event_type, description, parts_replaced, cost, downtime_hours, technician_name)
VALUES
('BD-001', '2025-03-08', 'Preventive Maintenance', 'Regular 250-hour scheduled maintenance', 'Oil filters, fuel filters, air filters', 1250.75, 16.0, 'Michael Johnson'),
('BD-001', '2025-03-09', 'Preventive Maintenance', 'Continuation of 250-hour service', 'Hydraulic filters, transmission filters', 980.50, 8.0, 'Michael Johnson'),
('BD-001', '2025-04-16', 'Preventive Maintenance', 'Regular 500-hour scheduled maintenance', 'Oil filters, fuel filters, air filters, hydraulic filters, transmission filters', 2150.25, 16.0, 'Robert Chen'),
('BD-001', '2025-04-17', 'Repair', 'Repair of track tensioner system', 'Track tensioner assembly, seals', 1785.60, 8.0, 'Robert Chen');

-- Insert Alert Events for BD-001
INSERT INTO AlertEvents (machine_id, alert_date, alert_type, severity, description, resolved, resolution_date, resolution_notes)
VALUES
('BD-001', '2025-03-07 09:35:22', 'Low Engine Oil Pressure', 'Critical', 'Engine oil pressure below minimum threshold', TRUE, '2025-03-07 10:15:45', 'Added oil to bring pressure back to normal range'),
('BD-001', '2025-03-15 14:42:18', 'High Hydraulic Fluid Temperature', 'Warning', 'Hydraulic fluid temperature approaching critical threshold', TRUE, '2025-03-15 15:30:12', 'Allowed system to cool down and inspected for potential issues'),
('BD-001', '2025-04-10 11:23:56', 'Track Tension Warning', 'Warning', 'Left track tension below optimal range', TRUE, '2025-04-10 13:05:30', 'Adjusted track tension to manufacturer specifications'),
('BD-001', '2025-04-15 08:17:42', 'Fuel System Warning', 'Warning', 'Potential contamination in fuel system detected', TRUE, '2025-04-17 16:45:22', 'Replaced fuel filters and cleaned fuel system during scheduled maintenance');

-- End of script for BD-001 data
