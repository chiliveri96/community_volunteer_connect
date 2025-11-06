-- DROP DATABASE IF EXISTS community_volunteer_connect;
CREATE DATABASE community_volunteer_connect;
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

CREATE TABLE volunteer_activities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    volunteer_id INT NOT NULL,
    activity_id INT NOT NULL,
	joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'Pending',
    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (volunteer_id) REFERENCES volunteers(id) ON DELETE CASCADE,
    FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE CASCADE
);

CREATE TABLE activity_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    volunteer_id INT NOT NULL,
    activity_id INT NOT NULL,
    status ENUM('pending','accepted','rejected') NOT NULL DEFAULT 'pending',
    request_note TEXT,
    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (volunteer_id) REFERENCES volunteers(id) ON DELETE CASCADE,
    FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE CASCADE,
    CONSTRAINT uq_request UNIQUE (volunteer_id, activity_id) -- prevent duplicate pending requests
);

CREATE TABLE volunteer_activity (
    id INT AUTO_INCREMENT PRIMARY KEY,
    volunteer_id INT NOT NULL,
    activity_id INT NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (volunteer_id) REFERENCES volunteers(id) ON DELETE CASCADE,
    FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE CASCADE,
    CONSTRAINT uq_vol_activity UNIQUE (volunteer_id, activity_id) -- prevent duplicates
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







describe skill;
describe organizations;
describe organization_contact;
describe volunteers;
describe volunteer_contact;
describe activities;
describe activity_skill;
describe volunteer_skill;
describe activity_requests;
describe volunteer_activities;
describe organization_user;

select *from organizations;
select *from volunteers;
select*from volunteer_activities;
select *from activities;
select *from volunteer_activity_requests;


SELECT id, volunteer_id, activity_id, status
FROM volunteer_activity_requests;

