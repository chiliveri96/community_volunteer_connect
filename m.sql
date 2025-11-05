


USE community_volunteer_connect;

/*-- community_connect_schema.sql
  DROP DATABASE IF EXISTS community_volunteer_connect;
CREATE DATABASE community_volunteer_connect CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE community_volunteer_connect;

-- Skills (lookup) -- reusable for volunteers & activities
CREATE TABLE skill (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- Organizations
DROP TABLE IF EXISTS organizations;

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








-- Organization contact methods (one org can have many contact rows: phone, email, person)
CREATE TABLE organization_contact (
    id INT AUTO_INCREMENT PRIMARY KEY,
    organization_id INT NOT NULL,
    contact_type ENUM('phone','email','person','other') NOT NULL,
    contact_value VARCHAR(255) NOT NULL,
    is_primary TINYINT(1) DEFAULT 0,
    CONSTRAINT uq_org_contact UNIQUE (organization_id, contact_type, contact_value),
    FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_org_contact_org ON organization_contact(organization_id);


-- Volunteer contact methods (phone, email, etc.). multiple allowed => normalized to its own table
CREATE TABLE volunteer_contact (
    id INT AUTO_INCREMENT PRIMARY KEY,
    volunteer_id INT NOT NULL,
    contact_type ENUM('phone','email','other') NOT NULL,
    contact_value VARCHAR(255) NOT NULL,
    is_primary TINYINT(1) DEFAULT 0,
    CONSTRAINT uq_vol_contact UNIQUE (volunteer_id, contact_type, contact_value),
    FOREIGN KEY (volunteer_id) REFERENCES volunteer(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_vol_contact_vol ON volunteer_contact(volunteer_id);


-- Activities posted by organizations
/*CREATE TABLE activities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    organization_id INT NOT NULL,
    activity_name VARCHAR(200) NOT NULL,
    description TEXT,
    activity_date DATE NOT NULL,
    activity_time TIME,
    location VARCHAR(255),
    volunteers_required INT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE
) ENGINE=InnoDB;

ALTER TABLE activities ADD COLUMN volunteer_skills VARCHAR(255);
ALTER TABLE activities ADD COLUMN contact VARCHAR(255);



CREATE INDEX idx_activity_org_date ON activity(organization_id, activity_date);

-- Skills required by an activity (many-to-many)
CREATE TABLE activity_skill (
    activity_id INT NOT NULL,
    skill_id INT NOT NULL,
    PRIMARY KEY (activity_id, skill_id),
    FOREIGN KEY (activity_id) REFERENCES activity(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skill(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_activityskill_skill ON activity_skill(skill_id);

-- Skills a volunteer has (many-to-many)
CREATE TABLE volunteer_skill (
    volunteer_id INT NOT NULL,
    skill_id INT NOT NULL,
    PRIMARY KEY (volunteer_id, skill_id),
    FOREIGN KEY (volunteer_id) REFERENCES volunteer(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skill(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_volunteerskill_skill ON volunteer_skill(skill_id);

-- Activity join requests (pending system) — volunteer requests to join
CREATE TABLE activity_request (
    id INT AUTO_INCREMENT PRIMARY KEY,
    volunteer_id INT NOT NULL,
    activity_id INT NOT NULL,
    status ENUM('pending','accepted','rejected') NOT NULL DEFAULT 'pending',
    request_note TEXT,
    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (volunteer_id) REFERENCES volunteer(id) ON DELETE CASCADE,
    FOREIGN KEY (activity_id) REFERENCES activity(id) ON DELETE CASCADE,
    CONSTRAINT uq_request UNIQUE (volunteer_id, activity_id) -- prevent duplicate pending requests
) ENGINE=InnoDB;

CREATE INDEX idx_request_activity ON activity_request(activity_id);

-- Accepted volunteer-activity mappings (final accepted participants)
CREATE TABLE volunteer_activity (
    id INT AUTO_INCREMENT PRIMARY KEY,
    volunteer_id INT NOT NULL,
    activity_id INT NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (volunteer_id) REFERENCES volunteer(id) ON DELETE CASCADE,
    FOREIGN KEY (activity_id) REFERENCES activity(id) ON DELETE CASCADE,
    CONSTRAINT uq_vol_activity UNIQUE (volunteer_id, activity_id) -- prevent duplicates
) ENGINE=InnoDB;

CREATE INDEX idx_vol_activity_activity ON volunteer_activity(activity_id);

-- Optional: track organization admins / contact persons (if you want logins separate)
CREATE TABLE organization_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    organization_id INT NOT NULL,
    name VARCHAR(120) NOT NULL,
    role VARCHAR(50) DEFAULT 'admin',
    email VARCHAR(120),
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organization(id) ON DELETE CASCADE,
    CONSTRAINT uq_org_user_email UNIQUE (organization_id, email)
) ENGINE=InnoDB;

CREATE INDEX idx_orguser_org ON organization_user(organization_id);

-- Recommended helper indexes (if needed)
CREATE INDEX idx_activity_date ON activity(activity_date);
CREATE INDEX idx_volunteer_created ON volunteer(created_at);

-- Example seed for skill table (optional)
-- INSERT INTO skill (name) VALUES ('First Aid'), ('Teaching'), ('Event Management'), ('Cleaning'), ('Gardening')
-- ON DUPLICATE KEY UPDATE name=name;



DROP TABLE IF EXISTS volunteer_activities;
/*

CREATE TABLE volunteers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    skills VARCHAR(255),
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
INSERT INTO volunteer_activities (volunteer_id, activity_id) VALUES (3, 1);

SELECT id, full_name, email FROM volunteers;
SELECT id, activity_name FROM activities;
INSERT INTO volunteers (full_name,  phone, email, password_hash)
VALUES ('Akhil', '9876543210', 'akhil@gmail.com', 'testhash');


describe skill;
describe organizations;
describe organization_contact;
describe volunteers;
describe volunteer_contact;
describe activities;
describe activity_skill;
describe volunteer_skill;
describe activity_request;
describe volunteer_activities;
describe organization_user;

select *from organizations;
select *from volunteers;
select*from volunteer_activities;
select *from activities;
*/
select *from organizations;
