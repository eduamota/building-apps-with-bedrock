-- SQL script to insert sample data for machine MC-001 into PostgreSQL tables.
-- Assumes the tables were created using the script in postgres_create_tables (with SERIAL keys).
-- Ensure the Machines table already contains the record for 'MC-001'.

-- Insert Operational Data for MC-001 (March 2025)
-- Note: Mobile Cranes have loads_lifted, weight_lifted_tons, max_load_tons columns
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, loads_lifted, weight_lifted_tons, max_load_tons, maintenance_flag)
VALUES
('MC-001', '2025-03-01', 7.5, 225.0, 2.5, 15, 600.0, 120.0, FALSE),
('MC-001', '2025-03-02', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('MC-001', '2025-03-03', 8.0, 240.0, 2.7, 16, 640.0, 130.0, FALSE),
('MC-001', '2025-03-04', 7.8, 234.0, 2.6, 15, 620.0, 125.0, FALSE),
('MC-001', '2025-03-05', 8.2, 246.0, 2.8, 16, 650.0, 135.0, FALSE),
('MC-001', '2025-03-06', 7.9, 237.0, 2.6, 15, 630.0, 128.0, FALSE),
('MC-001', '2025-03-07', 7.7, 231.0, 2.5, 15, 610.0, 122.0, FALSE),
('MC-001', '2025-03-08', 4.5, 135.0, 1.5, 9, 360.0, 115.0, FALSE),
('MC-001', '2025-03-09', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('MC-001', '2025-03-10', 7.8, 234.0, 2.6, 15, 620.0, 125.0, FALSE),
('MC-001', '2025-03-11', 8.1, 243.0, 2.7, 16, 645.0, 132.0, FALSE),
('MC-001', '2025-03-12', 7.9, 237.0, 2.6, 15, 630.0, 128.0, FALSE),
('MC-001', '2025-03-13', 8.0, 240.0, 2.7, 16, 640.0, 130.0, FALSE),
('MC-001', '2025-03-14', 0.0, 0.0, 0.0, 0, 0.0, 0.0, TRUE), -- Maintenance day
('MC-001', '2025-03-15', 4.6, 138.0, 1.5, 9, 365.0, 118.0, FALSE),
('MC-001', '2025-03-16', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('MC-001', '2025-03-17', 0.0, 0.0, 0.0, 0, 0.0, 0.0, TRUE), -- Maintenance day
('MC-001', '2025-03-18', 7.6, 228.0, 2.5, 15, 605.0, 120.0, FALSE),
('MC-001', '2025-03-19', 8.2, 246.0, 2.8, 16, 650.0, 135.0, FALSE),
('MC-001', '2025-03-20', 7.8, 234.0, 2.6, 15, 620.0, 125.0, FALSE),
('MC-001', '2025-03-21', 7.9, 237.0, 2.6, 15, 630.0, 128.0, FALSE),
('MC-001', '2025-03-22', 4.4, 132.0, 1.4, 9, 350.0, 110.0, FALSE),
('MC-001', '2025-03-23', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('MC-001', '2025-03-24', 8.0, 240.0, 2.7, 16, 640.0, 130.0, FALSE),
('MC-001', '2025-03-25', 7.7, 231.0, 2.5, 15, 610.0, 122.0, FALSE),
('MC-001', '2025-03-26', 7.8, 234.0, 2.6, 15, 620.0, 125.0, FALSE),
('MC-001', '2025-03-27', 8.1, 243.0, 2.7, 16, 645.0, 132.0, FALSE),
('MC-001', '2025-03-28', 7.9, 237.0, 2.6, 15, 630.0, 128.0, FALSE),
('MC-001', '2025-03-29', 4.5, 135.0, 1.5, 9, 360.0, 115.0, FALSE),
('MC-001', '2025-03-30', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('MC-001', '2025-03-31', 7.8, 234.0, 2.6, 15, 620.0, 125.0, FALSE);

-- Insert Operational Data for MC-001 (April 2025)
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, loads_lifted, weight_lifted_tons, max_load_tons, maintenance_flag)
VALUES
('MC-001', '2025-04-01', 8.0, 240.0, 2.7, 16, 640.0, 130.0, FALSE),
('MC-001', '2025-04-02', 7.9, 237.0, 2.6, 15, 630.0, 128.0, FALSE),
('MC-001', '2025-04-03', 7.7, 231.0, 2.5, 15, 610.0, 122.0, FALSE),
('MC-001', '2025-04-04', 8.2, 246.0, 2.8, 16, 650.0, 135.0, FALSE),
('MC-001', '2025-04-05', 4.6, 138.0, 1.5, 9, 365.0, 118.0, FALSE),
('MC-001', '2025-04-06', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('MC-001', '2025-04-07', 7.8, 234.0, 2.6, 15, 620.0, 125.0, FALSE),
('MC-001', '2025-04-08', 8.0, 240.0, 2.7, 16, 640.0, 130.0, FALSE),
('MC-001', '2025-04-09', 7.9, 237.0, 2.6, 15, 630.0, 128.0, FALSE),
('MC-001', '2025-04-10', 8.1, 243.0, 2.7, 16, 645.0, 132.0, FALSE),
('MC-001', '2025-04-11', 7.8, 234.0, 2.6, 15, 620.0, 125.0, FALSE),
('MC-001', '2025-04-12', 4.5, 135.0, 1.5, 9, 360.0, 115.0, FALSE),
('MC-001', '2025-04-13', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('MC-001', '2025-04-14', 7.7, 231.0, 2.5, 15, 610.0, 122.0, FALSE),
('MC-001', '2025-04-15', 7.9, 237.0, 2.6, 15, 630.0, 128.0, FALSE),
('MC-001', '2025-04-16', 8.0, 240.0, 2.7, 16, 640.0, 130.0, FALSE),
('MC-001', '2025-04-17', 7.8, 234.0, 2.6, 15, 620.0, 125.0, FALSE),
('MC-001', '2025-04-18', 0.0, 0.0, 0.0, 0, 0.0, 0.0, TRUE), -- Maintenance day
('MC-001', '2025-04-19', 4.4, 132.0, 1.4, 9, 350.0, 110.0, FALSE),
('MC-001', '2025-04-20', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('MC-001', '2025-04-21', 7.9, 237.0, 2.6, 15, 630.0, 128.0, FALSE),
('MC-001', '2025-04-22', 8.2, 246.0, 2.8, 16, 650.0, 135.0, FALSE),
('MC-001', '2025-04-23', 0.0, 0.0, 0.0, 0, 0.0, 0.0, TRUE), -- Maintenance day
('MC-001', '2025-04-24', 8.0, 240.0, 2.7, 16, 640.0, 130.0, FALSE),
('MC-001', '2025-04-25', 7.8, 234.0, 2.6, 15, 620.0, 125.0, FALSE),
('MC-001', '2025-04-26', 4.5, 135.0, 1.5, 9, 360.0, 115.0, FALSE),
('MC-001', '2025-04-27', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('MC-001', '2025-04-28', 7.9, 237.0, 2.6, 15, 630.0, 128.0, FALSE),
('MC-001', '2025-04-29', 8.1, 243.0, 2.7, 16, 645.0, 132.0, FALSE),
('MC-001', '2025-04-30', 7.8, 234.0, 2.6, 15, 620.0, 125.0, FALSE);

-- Insert Maintenance Events for MC-001
INSERT INTO MaintenanceEvents (machine_id, event_date, event_type, description, parts_replaced, cost, downtime_hours, technician_name)
VALUES
('MC-001', '2025-03-14', 'Preventive Maintenance', 'Regular 250-hour scheduled maintenance', 'Oil filters, fuel filters, air filters', 2250.75, 16.0, 'Amanda Garcia'),
('MC-001', '2025-03-17', 'Repair', 'Repair of boom extension system', 'Hydraulic seals, extension cables', 3150.50, 16.0, 'Amanda Garcia'),
('MC-001', '2025-04-18', 'Preventive Maintenance', 'Regular 500-hour scheduled maintenance', 'Oil filters, fuel filters, air filters, hydraulic filters', 2850.25, 8.0, 'Christopher Jackson'),
('MC-001', '2025-04-23', 'Inspection', 'Annual safety inspection and certification', 'Load test certification', 1950.75, 16.0, 'Christopher Jackson');

-- Insert Alert Events for MC-001
INSERT INTO AlertEvents (machine_id, alert_date, alert_type, severity, description, resolved, resolution_date, resolution_notes)
VALUES
('MC-001', '2025-03-07 07:55:33', 'Outrigger Pressure Warning', 'Warning', 'Uneven pressure detected in outrigger system', TRUE, '2025-03-07 09:30:45', 'Recalibrated outrigger pressure sensors'),
('MC-001', '2025-03-13 14:22:18', 'Boom Extension Warning', 'Critical', 'Abnormal resistance in boom extension', TRUE, '2025-03-14 11:45:30', 'Addressed during scheduled maintenance'),
('MC-001', '2025-04-05 11:48:27', 'Wind Speed Warning', 'Warning', 'Operation near maximum allowable wind speed', TRUE, '2025-04-05 12:20:15', 'Temporarily paused operation until wind conditions improved'),
('MC-001', '2025-04-17 09:38:42', 'Hydraulic System Warning', 'Critical', 'Potential contamination in main hydraulic system', TRUE, '2025-04-18 14:55:33', 'Flushed hydraulic system and replaced filters during maintenance');

-- End of script for MC-001 data
