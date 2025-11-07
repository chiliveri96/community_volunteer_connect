-- DROP DATABASE IF EXISTS community_volunteer_connect;
-- CREATE DATABASE community_volunteer_connect;
USE community_volunteer_connect;

CREATE TABLE volunteers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    skills VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE organizations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    organization_name VARCHAR(120) NOT NULL,
    contact_person VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL UNIQUE,
    address VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE activities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    organization_id INT NOT NULL,
    organization_name VARCHAR(200) NOT NULL,
    activity_name VARCHAR(200) NOT NULL,
    purpose TEXT,
    activity_date DATE,
    activity_time TIME,
    address VARCHAR(255),
    volunteers_required INT,
    volunteer_skills VARCHAR(255),
    contact VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE
);

CREATE TABLE volunteer_activity_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    volunteer_id INT NOT NULL,
    activity_id INT NOT NULL,
    status ENUM('pending','accepted','rejected') not null DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (volunteer_id) REFERENCES volunteers(id) ON DELETE CASCADE,
    FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE CASCADE
);

ALTER TABLE volunteer_activity_requests 
MODIFY status ENUM('pending','approved','rejected') NOT NULL DEFAULT 'pending';

SELECT id, volunteer_id, activity_id, status
FROM volunteer_activity_requests;




describe organizations;
describe volunteers;
describe activities;
describe volunteer_activities;

select *from organizations ;
select *from volunteers;
select *from activities;
select *from volunteer_activity_requests;


-- DDL (Data Definition Language) CREATE DATABASE,DROP DATABASE,USE,CREATE TABLE,PRIMARY KEY,FOREIGN KEY,REFERENCES,AUTO_INCREMENT,UNIQUE,NOT NULL,DEFAULT,ENUM,CHECK,ON DELETE CASCADE

-- DML (Data Manipulation Language) INSERT INTO,SELECT,UPDATE,DELETE,JOIN,WHERE,VALUES,FROM,SET
SELECT VERSION();
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Akhil369';
FLUSH PRIVILEGES;

SELECT user, host, plugin FROM mysql.user WHERE user='root';


SELECT user, host, plugin FROM mysql.user WHERE user='root';
