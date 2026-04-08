-- SQL script to insert sample data for machine MC-003 into PostgreSQL tables.
-- Assumes the tables were created using the script in postgres_create_tables (with SERIAL keys).
-- Ensure the Machines table already contains the record for 'MC-003'.

-- Insert Operational Data for MC-003 (March 2025)
-- Note: Mobile Cranes have loads_lifted, weight_lifted_tons, max_load_tons columns
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, loads_lifted, weight_lifted_tons, max_load_tons, maintenance_flag)
VALUES
('MC-003', '2025-03-01', 7.5, 225.0, 2.5, 15, 600.0, 115.0, FALSE),
('MC-003', '2025-03-02', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('MC-003', '2025-03-03', 7.8, 234.0, 2.6, 15, 620.0, 125.0, FALSE),
('MC-003', '2025-03-04', 7.6, 228.0, 2.5, 15, 605.0, 120.0, FALSE),
('MC-003', '2025-03-05', 8.0, 240.0, 2.7, 16, 640.0, 130.0, FALSE),
('MC-003', '2025-03-06', 7.7, 231.0, 2.5, 15, 610.0, 122.0, FALSE),
('MC-003', '2025-03-07', 7.5, 225.0, 2.5, 15, 600.0, 118.0, FALSE),
('MC-003', '2025-03-08', 4.3, 129.0, 1.4, 9, 345.0, 110.0, FALSE),
('MC-003', '2025-03-09', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('MC-003', '2025-03-10', 7.6, 228.0, 2.5, 15, 605.0, 120.0, FALSE),
('MC-003', '2025-03-11', 7.9, 237.0, 2.6, 15, 630.0, 128.0, FALSE),
('MC-003', '2025-03-12', 7.7, 231.0, 2.5, 15, 610.0, 122.0, FALSE),
('MC-003', '2025-03-13', 7.8, 234.0, 2.6, 15, 620.0, 125.0, FALSE),
('MC-003', '2025-03-14', 7.6, 228.0, 2.5, 15, 605.0, 120.0, FALSE),
('MC-003', '2025-03-15', 4.4, 132.0, 1.4, 9, 350.0, 112.0, FALSE),
('MC-003', '2025-03-16', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('MC-003', '2025-03-17', 7.7, 231.0, 2.5, 15, 610.0, 122.0, FALSE),
('MC-003', '2025-03-18', 7.4, 222.0, 2.4, 15, 590.0, 115.0, FALSE),
('MC-003', '2025-03-19', 8.0, 240.0, 2.7, 16, 640.0, 130.0, FALSE),
('MC-003', '2025-03-20', 7.8, 234.0, 2.6, 15, 620.0, 125.0, FALSE),
('MC-003', '2025-03-21', 7.7, 231.0, 2.5, 15, 610.0, 122.0, FALSE),
('MC-003', '2025-03-22', 4.2, 126.0, 1.4, 8, 340.0, 105.0, FALSE),
('MC-003', '2025-03-23', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('MC-003', '2025-03-24', 0.0, 0.0, 0.0, 0, 0.0, 0.0, TRUE), -- Maintenance day
('MC-003', '2025-03-25', 0.0, 0.0, 0.0, 0, 0.0, 0.0, TRUE), -- Maintenance day
('MC-003', '2025-03-26', 7.6, 228.0, 2.5, 15, 605.0, 120.0, FALSE),
('MC-003', '2025-03-27', 7.9, 237.0, 2.6, 15, 630.0, 128.0, FALSE),
('MC-003', '2025-03-28', 7.7, 231.0, 2.5, 15, 610.0, 122.0, FALSE),
('MC-003', '2025-03-29', 4.3, 129.0, 1.4, 9, 345.0, 110.0, FALSE),
('MC-003', '2025-03-30', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('MC-003', '2025-03-31', 7.6, 228.0, 2.5, 15, 605.0, 120.0, FALSE);

-- Insert Operational Data for MC-003 (April 2025)
INSERT INTO OperationalData (machine_id, operation_date, hours_operated, fuel_consumed_liters, idle_time_hours, loads_lifted, weight_lifted_tons, max_load_tons, maintenance_flag)
VALUES
('MC-003', '2025-04-01', 7.8, 234.0, 2.6, 15, 620.0, 125.0, FALSE),
('MC-003', '2025-04-02', 7.7, 231.0, 2.5, 15, 610.0, 122.0, FALSE),
('MC-003', '2025-04-03', 7.5, 225.0, 2.5, 15, 600.0, 118.0, FALSE),
('MC-003', '2025-04-04', 8.0, 240.0, 2.7, 16, 640.0, 130.0, FALSE),
('MC-003', '2025-04-05', 4.4, 132.0, 1.4, 9, 350.0, 112.0, FALSE),
('MC-003', '2025-04-06', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('MC-003', '2025-04-07', 7.6, 228.0, 2.5, 15, 605.0, 120.0, FALSE),
('MC-003', '2025-04-08', 7.8, 234.0, 2.6, 15, 620.0, 125.0, FALSE),
('MC-003', '2025-04-09', 7.7, 231.0, 2.5, 15, 610.0, 122.0, FALSE),
('MC-003', '2025-04-10', 7.9, 237.0, 2.6, 15, 630.0, 128.0, FALSE),
('MC-003', '2025-04-11', 7.6, 228.0, 2.5, 15, 605.0, 120.0, FALSE),
('MC-003', '2025-04-12', 4.3, 129.0, 1.4, 9, 345.0, 110.0, FALSE),
('MC-003', '2025-04-13', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('MC-003', '2025-04-14', 7.5, 225.0, 2.5, 15, 600.0, 118.0, FALSE),
('MC-003', '2025-04-15', 7.7, 231.0, 2.5, 15, 610.0, 122.0, FALSE),
('MC-003', '2025-04-16', 7.8, 234.0, 2.6, 15, 620.0, 125.0, FALSE),
('MC-003', '2025-04-17', 7.6, 228.0, 2.5, 15, 605.0, 120.0, FALSE),
('MC-003', '2025-04-18', 8.0, 240.0, 2.7, 16, 640.0, 130.0, FALSE),
('MC-003', '2025-04-19', 4.2, 126.0, 1.4, 8, 340.0, 105.0, FALSE),
('MC-003', '2025-04-20', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('MC-003', '2025-04-21', 7.7, 231.0, 2.5, 15, 610.0, 122.0, FALSE),
('MC-003', '2025-04-22', 8.0, 240.0, 2.7, 16, 640.0, 130.0, FALSE),
('MC-003', '2025-04-23', 7.8, 234.0, 2.6, 15, 620.0, 125.0, FALSE),
('MC-003', '2025-04-24', 7.7, 231.0, 2.5, 15, 610.0, 122.0, FALSE),
('MC-003', '2025-04-25', 7.5, 225.0, 2.5, 15, 600.0, 118.0, FALSE),
('MC-003', '2025-04-26', 4.3, 129.0, 1.4, 9, 345.0, 110.0, FALSE),
('MC-003', '2025-04-27', 0.0, 0.0, 0.0, 0, 0.0, 0.0, FALSE), -- Weekend/Off
('MC-003', '2025-04-28', 0.0, 0.0, 0.0, 0, 0.0, 0.0, TRUE), -- Maintenance day
('MC-003', '2025-04-29', 0.0, 0.0, 0.0, 0, 0.0, 0.0, TRUE), -- Maintenance day
('MC-003', '2025-04-30', 7.6, 228.0, 2.5, 15, 605.0, 120.0, FALSE);

-- Insert Maintenance Events for MC-003
INSERT INTO MaintenanceEvents (machine_id, event_date, event_type, description, parts_replaced, cost, downtime_hours, technician_name)
VALUES
('MC-003', '2025-03-24', 'Preventive Maintenance', 'Regular 250-hour scheduled maintenance', 'Oil filters, fuel filters, air filters', 2250.50, 16.0, 'Ethan Wilson'),
('MC-003', '2025-03-25', 'Repair', 'Hydraulic system repair', 'Hydraulic pump, seals', 3050.75, 16.0, 'Ethan Wilson'),
('MC-003', '2025-04-28', 'Preventive Maintenance', 'Regular 500-hour scheduled maintenance', 'Oil filters, fuel filters, air filters, hydraulic filters', 2750.25, 16.0, 'Sophia Taylor'),
('MC-003', '2025-04-29', 'Inspection', 'Boom inspection and certification', 'Boom extension cables', 1750.50, 8.0, 'Sophia Taylor');

-- Insert Alert Events for MC-003
INSERT INTO AlertEvents (machine_id, alert_date, alert_type, severity, description, resolved, resolution_date, resolution_notes)
VALUES
('MC-003', '2025-03-15 09:42:15', 'Boom Extension Warning', 'Warning', 'Uneven movement in boom extension', TRUE, '2025-03-15 11:20:30', 'Lubricated boom extension mechanism and scheduled for inspection'),
('MC-003', '2025-03-23 13:28:42', 'Hydraulic System Warning', 'Critical', 'Hydraulic pressure drop in main circuit', TRUE, '2025-03-24 10:15:55', 'Addressed during scheduled maintenance'),
('MC-003', '2025-04-18 10:35:27', 'Swing Brake Warning', 'Warning', 'Reduced performance in swing brake system', TRUE, '2025-04-18 12:40:15', 'Adjusted brake system and scheduled for detailed inspection'),
('MC-003', '2025-04-27 15:22:48', 'Low Coolant Level', 'Critical', 'Coolant level below minimum threshold', TRUE, '2025-04-28 09:45:30', 'Added coolant and addressed during scheduled maintenance');

-- End of script for MC-003 data
