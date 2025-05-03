-- SQL script to insert sample data for machine BD-002 into PostgreSQL tables.
-- Assumes the tables were created using the script in postgres_create_tables (with SERIAL keys).
-- Ensure the Machines table already contains the record for 'BD-002'.

-- Insert Operational Data for BD-002 (March 2025)
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, material_moved_cubic_meters, maintenance_flag)
VALUES
('BD-002', '2025-03-01', 8.7, 522.0, 1.2, 12800.0, FALSE),
('BD-002', '2025-03-02', 9.1, 546.0, 1.3, 13400.0, FALSE),
('BD-002', '2025-03-03', 8.9, 534.0, 1.3, 13100.0, FALSE),
('BD-002', '2025-03-04', 8.8, 528.0, 1.3, 12900.0, FALSE),
('BD-002', '2025-03-05', 8.6, 516.0, 1.2, 12600.0, FALSE),
('BD-002', '2025-03-06', 9.0, 540.0, 1.3, 13200.0, FALSE),
('BD-002', '2025-03-07', 8.7, 522.0, 1.2, 12800.0, FALSE),
('BD-002', '2025-03-08', 5.4, 324.0, 0.8, 7900.0, FALSE),
('BD-002', '2025-03-09', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('BD-002', '2025-03-10', 8.9, 534.0, 1.3, 13100.0, FALSE),
('BD-002', '2025-03-11', 8.7, 522.0, 1.2, 12800.0, FALSE),
('BD-002', '2025-03-12', 8.8, 528.0, 1.3, 12900.0, FALSE),
('BD-002', '2025-03-13', 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('BD-002', '2025-03-14', 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('BD-002', '2025-03-15', 5.6, 336.0, 0.8, 8200.0, FALSE),
('BD-002', '2025-03-16', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('BD-002', '2025-03-17', 8.7, 522.0, 1.2, 12800.0, FALSE),
('BD-002', '2025-03-18', 9.0, 540.0, 1.3, 13200.0, FALSE),
('BD-002', '2025-03-19', 8.8, 528.0, 1.3, 12900.0, FALSE),
('BD-002', '2025-03-20', 8.9, 534.0, 1.3, 13100.0, FALSE),
('BD-002', '2025-03-21', 8.6, 516.0, 1.2, 12600.0, FALSE),
('BD-002', '2025-03-22', 5.3, 318.0, 0.8, 7800.0, FALSE),
('BD-002', '2025-03-23', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('BD-002', '2025-03-24', 8.8, 528.0, 1.3, 12900.0, FALSE),
('BD-002', '2025-03-25', 8.7, 522.0, 1.2, 12800.0, FALSE),
('BD-002', '2025-03-26', 8.9, 534.0, 1.3, 13100.0, FALSE),
('BD-002', '2025-03-27', 9.1, 546.0, 1.3, 13400.0, FALSE),
('BD-002', '2025-03-28', 8.8, 528.0, 1.3, 12900.0, FALSE),
('BD-002', '2025-03-29', 5.5, 330.0, 0.8, 8100.0, FALSE),
('BD-002', '2025-03-30', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('BD-002', '2025-03-31', 8.7, 522.0, 1.2, 12800.0, FALSE);

-- Insert Operational Data for BD-002 (April 2025)
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, material_moved_cubic_meters, maintenance_flag)
VALUES
('BD-002', '2025-04-01', 8.9, 534.0, 1.3, 13100.0, FALSE),
('BD-002', '2025-04-02', 9.0, 540.0, 1.3, 13200.0, FALSE),
('BD-002', '2025-04-03', 8.8, 528.0, 1.3, 12900.0, FALSE),
('BD-002', '2025-04-04', 8.6, 516.0, 1.2, 12600.0, FALSE),
('BD-002', '2025-04-05', 5.4, 324.0, 0.8, 7900.0, FALSE),
('BD-002', '2025-04-06', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('BD-002', '2025-04-07', 8.7, 522.0, 1.2, 12800.0, FALSE),
('BD-002', '2025-04-08', 8.9, 534.0, 1.3, 13100.0, FALSE),
('BD-002', '2025-04-09', 9.1, 546.0, 1.3, 13400.0, FALSE),
('BD-002', '2025-04-10', 8.8, 528.0, 1.3, 12900.0, FALSE),
('BD-002', '2025-04-11', 8.7, 522.0, 1.2, 12800.0, FALSE),
('BD-002', '2025-04-12', 5.5, 330.0, 0.8, 8100.0, FALSE),
('BD-002', '2025-04-13', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('BD-002', '2025-04-14', 8.9, 534.0, 1.3, 13100.0, FALSE),
('BD-002', '2025-04-15', 8.8, 528.0, 1.3, 12900.0, FALSE),
('BD-002', '2025-04-16', 8.6, 516.0, 1.2, 12600.0, FALSE),
('BD-002', '2025-04-17', 8.7, 522.0, 1.2, 12800.0, FALSE),
('BD-002', '2025-04-18', 0.0, 0.0, 0.0, 0.0, TRUE), -- Maintenance day
('BD-002', '2025-04-19', 5.3, 318.0, 0.8, 7800.0, FALSE),
('BD-002', '2025-04-20', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('BD-002', '2025-04-21', 8.8, 528.0, 1.3, 12900.0, FALSE),
('BD-002', '2025-04-22', 9.0, 540.0, 1.3, 13200.0, FALSE),
('BD-002', '2025-04-23', 8.9, 534.0, 1.3, 13100.0, FALSE),
('BD-002', '2025-04-24', 8.7, 522.0, 1.2, 12800.0, FALSE),
('BD-002', '2025-04-25', 8.8, 528.0, 1.3, 12900.0, FALSE),
('BD-002', '2025-04-26', 5.6, 336.0, 0.8, 8200.0, FALSE),
('BD-002', '2025-04-27', 0.0, 0.0, 0.0, 0.0, FALSE), -- Weekend/Off
('BD-002', '2025-04-28', 8.7, 522.0, 1.2, 12800.0, FALSE),
('BD-002', '2025-04-29', 8.9, 534.0, 1.3, 13100.0, FALSE),
('BD-002', '2025-04-30', 9.0, 540.0, 1.3, 13200.0, FALSE);

-- Insert Maintenance Events for BD-002
INSERT INTO MaintenanceEvents (machine_id, event_date, event_type, description, parts_replaced, cost, downtime_hours, technician_name)
VALUES
('BD-002', '2025-03-13', 'Preventive Maintenance', 'Regular 250-hour scheduled maintenance', 'Oil filters, fuel filters, air filters', 1275.50, 16.0, 'Eric Smith'),
('BD-002', '2025-03-14', 'Repair', 'Repair of cooling system', 'Radiator hoses, thermostat', 950.75, 8.0, 'Eric Smith'),
('BD-002', '2025-04-18', 'Preventive Maintenance', 'Regular 500-hour scheduled maintenance', 'Oil filters, fuel filters, air filters, hydraulic filters', 2050.25, 8.0, 'Marcus Johnson');

-- Insert Alert Events for BD-002
INSERT INTO AlertEvents (machine_id, alert_date, alert_type, severity, description, resolved, resolution_date, resolution_notes)
VALUES
('BD-002', '2025-03-05 10:25:18', 'Engine Temperature Warning', 'Warning', 'Engine temperature approaching critical threshold', TRUE, '2025-03-05 11:10:45', 'Cleaned radiator and cooling fins to improve airflow'),
('BD-002', '2025-03-12 14:50:42', 'Hydraulic Pressure Warning', 'Warning', 'Fluctuating hydraulic pressure detected', TRUE, '2025-03-13 09:30:15', 'Replaced hydraulic filter during scheduled maintenance'),
('BD-002', '2025-04-05 09:15:33', 'Low Coolant Level', 'Critical', 'Coolant level below minimum threshold', TRUE, '2025-04-05 10:00:22', 'Added coolant and inspected system for leaks'),
('BD-002', '2025-04-17 13:42:56', 'Fuel System Warning', 'Warning', 'Fuel pressure below optimal range', TRUE, '2025-04-18 15:20:40', 'Replaced fuel filter during scheduled maintenance');

-- End of script for BD-002 data
