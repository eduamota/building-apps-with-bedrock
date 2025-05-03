-- 01_insert_machines.sql
-- Date: 2025-05-02
-- Description: Inserts the base records for all machines into the Machines table.

-- Sample Bulldozers (BD850)
INSERT INTO Machines (machine_id, machine_type, model, serial_number, manufacture_date, acquisition_date)
VALUES
('BD-001', 'Bulldozer', 'BD850', 'BD850-2024-10001', '2024-01-15', '2024-02-20'),
('BD-002', 'Bulldozer', 'BD850', 'BD850-2024-10002', '2024-01-20', '2024-02-25'),
('BD-003', 'Bulldozer', 'BD850', 'BD850-2024-10003', '2024-01-25', '2024-03-01');

-- Sample Dump Trucks (DT1000)
INSERT INTO Machines (machine_id, machine_type, model, serial_number, manufacture_date, acquisition_date)
VALUES
('DT-001', 'Dump Truck', 'DT1000', 'DT1000-2024-20001', '2024-01-10', '2024-02-15'),
('DT-002', 'Dump Truck', 'DT1000', 'DT1000-2024-20002', '2024-01-12', '2024-02-18'),
('DT-003', 'Dump Truck', 'DT1000', 'DT1000-2024-20003', '2024-01-14', '2024-02-20');

-- Sample Excavators (LE950)
INSERT INTO Machines (machine_id, machine_type, model, serial_number, manufacture_date, acquisition_date)
VALUES
('EX-001', 'Excavator', 'LE950', 'LE950-2024-30001', '2024-01-05', '2024-02-10'),
('EX-002', 'Excavator', 'LE950', 'LE950-2024-30002', '2024-01-08', '2024-02-12'),
('EX-003', 'Excavator', 'LE950', 'LE950-2024-30003', '2024-01-10', '2024-02-15');

-- Sample Forklifts (FL250)
INSERT INTO Machines (machine_id, machine_type, model, serial_number, manufacture_date, acquisition_date)
VALUES
('FL-001', 'Forklift', 'FL250', 'FL250-2024-40001', '2024-01-18', '2024-02-22'),
('FL-002', 'Forklift', 'FL250', 'FL250-2024-40002', '2024-01-20', '2024-02-25'),
('FL-003', 'Forklift', 'FL250', 'FL250-2024-40003', '2024-01-22', '2024-03-01');

-- Sample Mobile Cranes (MC750)
INSERT INTO Machines (machine_id, machine_type, model, serial_number, manufacture_date, acquisition_date)
VALUES
('MC-001', 'Mobile Crane', 'MC750', 'MC750-2024-50001', '2024-01-25', '2024-03-01'),
('MC-002', 'Mobile Crane', 'MC750', 'MC750-2024-50002', '2024-01-28', '2024-03-05'),
('MC-003', 'Mobile Crane', 'MC750', 'MC750-2024-50003', '2024-02-01', '2024-03-10');