-- 00_create_tables.sql
-- Date: 2025-05-02
-- Description: Creates the necessary tables for machine operational data using PostgreSQL syntax.

-- Drop tables if they exist (optional, for clean runs during testing)
DROP TABLE IF EXISTS AlertEvents;
DROP TABLE IF EXISTS MaintenanceEvents;
DROP TABLE IF EXISTS OperationalData;
DROP TABLE IF EXISTS Machines;

-- Machines table to store basic information about each machine
CREATE TABLE Machines (
    machine_id VARCHAR(20) PRIMARY KEY,
    machine_type VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    serial_number VARCHAR(50) NOT NULL UNIQUE, -- Added UNIQUE constraint
    manufacture_date DATE NOT NULL,
    acquisition_date DATE NOT NULL
);

-- OperationalData table to store daily operational metrics
CREATE TABLE OperationalData (
    data_id SERIAL PRIMARY KEY, -- Use SERIAL for auto-incrementing ID in PostgreSQL
    machine_id VARCHAR(20) NOT NULL REFERENCES Machines(machine_id), -- Inline FOREIGN KEY
    operation_date DATE NOT NULL,
    hours_operated DECIMAL(8,2) NOT NULL,
    fuel_consumed_liters DECIMAL(8,2) NOT NULL,
    idle_time_hours DECIMAL(8,2) NOT NULL,
    material_moved_cubic_meters DECIMAL(10,2),  -- For bulldozers, dump trucks, excavators
    distance_traveled_km DECIMAL(8,2),          -- For dump trucks
    loads_lifted INT,                           -- For forklifts and cranes
    weight_lifted_tons DECIMAL(10,2),           -- For forklifts and cranes
    max_load_tons DECIMAL(10,2),                -- For forklifts and cranes
    maintenance_flag BOOLEAN DEFAULT FALSE,
    UNIQUE(machine_id, operation_date) -- Added UNIQUE constraint to prevent duplicate daily entries per machine
);

-- MaintenanceEvents table to store maintenance activities
CREATE TABLE MaintenanceEvents (
    event_id SERIAL PRIMARY KEY, -- Use SERIAL for auto-incrementing ID in PostgreSQL
    machine_id VARCHAR(20) NOT NULL REFERENCES Machines(machine_id), -- Inline FOREIGN KEY
    event_date DATE NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    description TEXT,
    parts_replaced TEXT,
    cost DECIMAL(10,2),
    downtime_hours DECIMAL(8,2),
    technician_name VARCHAR(100)
);

-- AlertEvents table to store machine alerts and warnings
CREATE TABLE AlertEvents (
    alert_id SERIAL PRIMARY KEY, -- Use SERIAL for auto-incrementing ID in PostgreSQL
    machine_id VARCHAR(20) NOT NULL REFERENCES Machines(machine_id), -- Inline FOREIGN KEY
    alert_date TIMESTAMP NOT NULL,
    alert_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    description TEXT,
    resolved BOOLEAN DEFAULT FALSE,
    resolution_date TIMESTAMP,
    resolution_notes TEXT
);

-- Add Indexes for performance (optional but recommended)
CREATE INDEX idx_operationaldata_machine_date ON OperationalData (machine_id, operation_date);
CREATE INDEX idx_maintenanceevents_machine_date ON MaintenanceEvents (machine_id, event_date);
CREATE INDEX idx_alertevents_machine_date ON AlertEvents (machine_id, alert_date);
CREATE INDEX idx_alertevents_resolved ON AlertEvents (resolved);