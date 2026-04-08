-- SQL script to insert sample data for machine MC-002 into PostgreSQL tables.
-- Assumes the tables were created using the script in postgres_create_tables (with SERIAL keys).
-- Ensure the Machines table already contains the record for 'MC-002'.

-- Insert Operational Data for MC-002 (March 2025)
-- Note: Mobile Cranes have loads_lifted, weight_lifted_tons, max_load_tons columns
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, loads_lifted, weight_lifted_tons, max_load_tons, maintenance_flag)
VALUES
('MC-002', '2025-03-01', 7.6, 228.0, 2.5, 15, 605.0, 118.0, FALSE),
('MC-002', '2025-03-02', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('MC-002', '2025-03-03', 7.9, 237.0, 2.6, 15, 630.0, 128.0, FALSE),
('MC-002', '2025-03-04', 7.7, 231.0, 2.5, 15, 610.0, 122.0, FALSE),
('MC-002', '2025-03-05', 8.1, 243.0, 2.7, 16, 645.0, 132.0, FALSE),
('MC-002', '2025-03-06', 7.8, 234.0, 2.6, 15, 620.0, 125.0, FALSE),
('MC-002', '2025-03-07', 7.6, 228.0, 2.5, 15, 605.0, 120.0, FALSE),
('MC-002', '2025-03-08', 4.4, 132.0, 1.4, 9, 350.0, 112.0, FALSE),
('MC-002', '2025-03-09', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('MC-002', '2025-03-10', 7.7, 231.0, 2.5, 15, 610.0, 122.0, FALSE),
('MC-002', '2025-03-11', 8.0, 240.0, 2.7, 16, 640.0, 130.0, FALSE),
('MC-002', '2025-03-12', 7.8, 234.0, 2.6, 15, 620.0, 125.0, FALSE),
('MC-002', '2025-03-13', 7.9, 237.0, 2.6, 15, 630.0, 128.0, FALSE),
('MC-002', '2025-03-14', 7.7, 231.0, 2.5, 15, 610.0, 122.0, FALSE),
('MC-002', '2025-03-15', 4.5, 135.0, 1.5, 9, 360.0, 116.0, FALSE),
('MC-002', '2025-03-16', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('MC-002', '2025-03-17', 7.8, 234.0, 2.6, 15, 620.0, 125.0, FALSE),
('MC-002', '2025-03-18', 7.5, 225.0, 2.5, 15, 600.0, 120.0, FALSE),
('MC-002', '2025-03-19', 8.1, 243.0, 2.7, 16, 645.0, 132.0, FALSE),
('MC-002', '2025-03-20', 0.0, 0.0, 0.0, 0, 0.0, 0.0, TRUE), -- Maintenance day
('MC-002', '2025-03-21', 0.0, 0.0, 0.0, 0, 0.0, 0.0, TRUE), -- Maintenance day
('MC-002', '2025-03-22', 4.3, 129.0, 1.4, 9, 345.0, 108.0, FALSE),
('MC-002', '2025-03-23', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('MC-002', '2025-03-24', 7.9, 237.0, 2.6, 15, 630.0, 128.0, FALSE),
('MC-002', '2025-03-25', 7.6, 228.0, 2.5, 15, 605.0, 120.0, FALSE),
('MC-002', '2025-03-26', 7.7, 231.0, 2.5, 15, 610.0, 122.0, FALSE),
('MC-002', '2025-03-27', 8.0, 240.0, 2.7, 16, 640.0, 130.0, FALSE),
('MC-002', '2025-03-28', 7.8, 234.0, 2.6, 15, 620.0, 125.0, FALSE),
('MC-002', '2025-03-29', 4.4, 132.0, 1.4, 9, 350.0, 112.0, FALSE),
('MC-002', '2025-03-30', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('MC-002', '2025-03-31', 7.7, 231.0, 2.5, 15, 610.0, 122.0, FALSE);

-- Insert Operational Data for MC-002 (April 2025)
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, loads_lifted, weight_lifted_tons, max_load_tons, maintenance_flag)
VALUES
('MC-002', '2025-04-01', 7.9, 237.0, 2.6, 15, 630.0, 128.0, FALSE),
('MC-002', '2025-04-02', 7.8, 234.0, 2.6, 15, 620.0, 125.0, FALSE),
('MC-002', '2025-04-03', 7.6, 228.0, 2.5, 15, 605.0, 120.0, FALSE),
('MC-002', '2025-04-04', 8.1, 243.0, 2.7, 16, 645.0, 132.0, FALSE),
('MC-002', '2025-04-05', 4.5, 135.0, 1.5, 9, 360.0, 116.0, FALSE),
('MC-002', '2025-04-06', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('MC-002', '2025-04-07', 7.7, 231.0, 2.5, 15, 610.0, 122.0, FALSE),
('MC-002', '2025-04-08', 7.9, 237.0, 2.6, 15, 630.0, 128.0, FALSE),
('MC-002', '2025-04-09', 7.8, 234.0, 2.6, 15, 620.0, 125.0, FALSE),
('MC-002', '2025-04-10', 8.0, 240.0, 2.7, 16, 640.0, 130.0, FALSE),
('MC-002', '2025-04-11', 7.7, 231.0, 2.5, 15, 610.0, 122.0, FALSE),
('MC-002', '2025-04-12', 4.4, 132.0, 1.4, 9, 350.0, 112.0, FALSE),
('MC-002', '2025-04-13', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('MC-002', '2025-04-14', 7.6, 228.0, 2.5, 15, 605.0, 120.0, FALSE),
('MC-002', '2025-04-15', 7.8, 234.0, 2.6, 15, 620.0, 125.0, FALSE),
('MC-002', '2025-04-16', 7.9, 237.0, 2.6, 15, 630.0, 128.0, FALSE),
('MC-002', '2025-04-17', 7.7, 231.0, 2.5, 15, 610.0, 122.0, FALSE),
('MC-002', '2025-04-18', 8.1, 243.0, 2.7, 16, 645.0, 132.0, FALSE),
('MC-002', '2025-04-19', 4.3, 129.0, 1.4, 9, 345.0, 108.0, FALSE),
('MC-002', '2025-04-20', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('MC-002', '2025-04-21', 7.8, 234.0, 2.6, 15, 620.0, 125.0, FALSE),
('MC-002', '2025-04-22', 8.1, 243.0, 2.7, 16, 645.0, 132.0, FALSE),
('MC-002', '2025-04-23', 7.9, 237.0, 2.6, 15, 630.0, 128.0, FALSE),
('MC-002', '2025-04-24', 0.0, 0.0, 0.0, 0, 0.0, 0.0, TRUE), -- Maintenance day
('MC-002', '2025-04-25', 0.0, 0.0, 0.0, 0, 0.0, 0.0, TRUE), -- Maintenance day
('MC-002', '2025-04-26', 4.4, 132.0, 1.4, 9, 350.0, 112.0, FALSE),
('MC-002', '2025-04-27', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('MC-002', '2025-04-28', 7.8, 234.0, 2.6, 15, 620.0, 125.0, FALSE),
('MC-002', '2025-04-29', 8.0, 240.0, 2.7, 16, 640.0, 130.0, FALSE),
('MC-002', '2025-04-30', 7.7, 231.0, 2.5, 15, 610.0, 122.0, FALSE);

-- Insert Maintenance Events for MC-002
INSERT INTO MaintenanceEvents (machine_id, event_date, event_type, description, parts_replaced, cost, downtime_hours, technician_name)
VALUES
('MC-002', '2025-03-20', 'Preventive Maintenance', 'Regular 250-hour scheduled maintenance', 'Oil filters, fuel filters, air filters', 2150.25, 16.0, 'Joshua Martin'),
('MC-002', '2025-03-21', 'Repair', 'Outrigger system repair', 'Hydraulic cylinder seals', 1850.75, 8.0, 'Joshua Martin'),
('MC-002', '2025-04-24', 'Preventive Maintenance', 'Regular 500-hour scheduled maintenance', 'Oil filters, fuel filters, air filters, hydraulic filters', 2650.50, 16.0, 'Olivia Anderson'),
('MC-002', '2025-04-25', 'Inspection', 'Load testing and certification', 'Cable inspection', 1650.25, 8.0, 'Olivia Anderson');

-- Insert Alert Events for MC-002
INSERT INTO AlertEvents (machine_id, alert_date, alert_type, severity, description, resolved, resolution_date, resolution_notes)
VALUES
('MC-002', '2025-03-12 10:25:18', 'Hydraulic System Warning', 'Warning', 'Low hydraulic fluid level detected', TRUE, '2025-03-12 11:45:30', 'Added hydraulic fluid and inspected for leaks'),
('MC-002', '2025-03-19 15:50:42', 'Outrigger Pressure Warning', 'Critical', 'Uneven pressure detected in outrigger system', TRUE, '2025-03-20 09:30:15', 'Recalibrated outrigger pressure sensors during maintenance'),
('MC-002', '2025-04-15 08:35:27', 'Cable Inspection Warning', 'Warning', 'Cable wear approaching inspection threshold', TRUE, '2025-04-15 10:15:50', 'Inspected and lubricated cables, scheduled replacement'),
('MC-002', '2025-04-23 14:20:33', 'Engine Oil Pressure Warning', 'Warning', 'Engine oil pressure below optimal range', TRUE, '2025-04-24 11:30:45', 'Changed oil and filter during scheduled maintenance');

-- End of script for MC-002 data
