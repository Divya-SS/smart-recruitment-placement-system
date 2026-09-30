-- ==========================================================
-- SMART RECRUITMENT & PLACEMENT MANAGEMENT SYSTEM (SRPMS)
-- Database DDL Schema (MySQL 8.0 / InnoDB)
-- ==========================================================

CREATE DATABASE IF NOT EXISTS `recruitment_db`
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE `recruitment_db`;

-- Disable foreign key checks during creation
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------------------------------------
-- 1. Table: roles
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(30) NOT NULL UNIQUE,
  `description` VARCHAR(150) NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_roles_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------
-- 2. Table: users
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `role_id` INT NOT NULL,
  `full_name` VARCHAR(100) NOT NULL,
  `email` VARCHAR(120) NOT NULL UNIQUE,
  `password_hash` VARCHAR(255) NOT NULL,
  `phone` VARCHAR(20) NULL,
  `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `idx_users_email` (`email`),
  INDEX `idx_users_role_id` (`role_id`),
  CONSTRAINT `fk_users_role` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------
-- 3. Table: skills
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `skills`;
CREATE TABLE `skills` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(60) NOT NULL UNIQUE,
  `category` VARCHAR(50) NULL,
  INDEX `idx_skills_name` (`name`),
  INDEX `idx_skills_category` (`category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------
-- 4. Table: candidates
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `candidates`;
CREATE TABLE `candidates` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `first_name` VARCHAR(60) NOT NULL,
  `last_name` VARCHAR(60) NOT NULL,
  `email` VARCHAR(120) NOT NULL UNIQUE,
  `phone` VARCHAR(20) NOT NULL,
  `location` VARCHAR(100) NOT NULL,
  `experience_years` DECIMAL(4,1) NOT NULL DEFAULT 0.0,
  `highest_qualification` VARCHAR(100) NOT NULL,
  `current_company` VARCHAR(120) NULL,
  `current_ctc` DECIMAL(10,2) NULL,
  `expected_ctc` DECIMAL(10,2) NULL,
  `resume_url` VARCHAR(255) NULL,
  `status` ENUM('AVAILABLE', 'SHORTLISTED', 'INTERVIEWING', 'PLACED', 'INACTIVE') NOT NULL DEFAULT 'AVAILABLE',
  `created_by` INT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `idx_candidates_email` (`email`),
  INDEX `idx_candidates_location` (`location`),
  INDEX `idx_candidates_status` (`status`),
  CONSTRAINT `fk_candidates_creator` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------
-- 5. Table: candidate_skills (Junction)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `candidate_skills`;
CREATE TABLE `candidate_skills` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `candidate_id` INT NOT NULL,
  `skill_id` INT NOT NULL,
  `proficiency` ENUM('BEGINNER', 'INTERMEDIATE', 'EXPERT') NOT NULL DEFAULT 'INTERMEDIATE',
  UNIQUE KEY `uq_candidate_skill` (`candidate_id`, `skill_id`),
  INDEX `idx_cs_candidate` (`candidate_id`),
  INDEX `idx_cs_skill` (`skill_id`),
  CONSTRAINT `fk_cs_candidate` FOREIGN KEY (`candidate_id`) REFERENCES `candidates` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_cs_skill` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------
-- 6. Table: companies
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `companies`;
CREATE TABLE `companies` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(120) NOT NULL UNIQUE,
  `website` VARCHAR(150) NULL,
  `industry` VARCHAR(80) NULL,
  `location` VARCHAR(100) NOT NULL,
  `contact_person_name` VARCHAR(100) NOT NULL,
  `contact_person_email` VARCHAR(120) NOT NULL,
  `contact_person_phone` VARCHAR(20) NOT NULL,
  `status` ENUM('ACTIVE', 'INACTIVE') NOT NULL DEFAULT 'ACTIVE',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `idx_companies_name` (`name`),
  INDEX `idx_companies_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------
-- 7. Table: jobs
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `jobs`;
CREATE TABLE `jobs` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `company_id` INT NOT NULL,
  `created_by` INT NULL,
  `assigned_recruiter_id` INT NULL,
  `title` VARCHAR(120) NOT NULL,
  `description` TEXT NULL,
  `min_experience_years` DECIMAL(4,1) NOT NULL DEFAULT 0.0,
  `max_experience_years` DECIMAL(4,1) NULL,
  `qualification_required` VARCHAR(100) NULL,
  `location` VARCHAR(100) NOT NULL,
  `job_type` ENUM('FULL_TIME', 'PART_TIME', 'CONTRACT', 'INTERNSHIP') NOT NULL DEFAULT 'FULL_TIME',
  `min_salary` DECIMAL(10,2) NULL,
  `max_salary` DECIMAL(10,2) NULL,
  `openings_count` INT NOT NULL DEFAULT 1,
  `status` ENUM('OPEN', 'ON_HOLD', 'CLOSED') NOT NULL DEFAULT 'OPEN',
  `deadline` DATE NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `idx_jobs_company_id` (`company_id`),
  INDEX `idx_jobs_assigned_recruiter` (`assigned_recruiter_id`),
  INDEX `idx_jobs_title` (`title`),
  INDEX `idx_jobs_status` (`status`),
  CONSTRAINT `fk_jobs_company` FOREIGN KEY (`company_id`) REFERENCES `companies` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_jobs_creator` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_jobs_recruiter` FOREIGN KEY (`assigned_recruiter_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------
-- 8. Table: job_skills (Junction)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `job_skills`;
CREATE TABLE `job_skills` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `job_id` INT NOT NULL,
  `skill_id` INT NOT NULL,
  `is_mandatory` BOOLEAN NOT NULL DEFAULT TRUE,
  UNIQUE KEY `uq_job_skill` (`job_id`, `skill_id`),
  INDEX `idx_js_job` (`job_id`),
  INDEX `idx_js_skill` (`skill_id`),
  CONSTRAINT `fk_js_job` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_js_skill` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------
-- 9. Table: applications
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `applications`;
CREATE TABLE `applications` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `candidate_id` INT NOT NULL,
  `job_id` INT NOT NULL,
  `match_score` DECIMAL(5,2) NOT NULL DEFAULT 0.00,
  `status` ENUM('APPLIED', 'SHORTLISTED', 'INTERVIEW_SCHEDULED', 'SELECTED', 'REJECTED', 'JOINED') NOT NULL DEFAULT 'APPLIED',
  `notes` TEXT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY `uq_candidate_job_app` (`candidate_id`, `job_id`),
  INDEX `idx_app_candidate` (`candidate_id`),
  INDEX `idx_app_job` (`job_id`),
  INDEX `idx_app_status` (`status`),
  CONSTRAINT `fk_app_candidate` FOREIGN KEY (`candidate_id`) REFERENCES `candidates` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_app_job` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------
-- 10. Table: interviews
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `interviews`;
CREATE TABLE `interviews` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `application_id` INT NOT NULL,
  `scheduled_by` INT NULL,
  `interview_round` VARCHAR(60) NOT NULL,
  `scheduled_at` DATETIME NOT NULL,
  `mode` ENUM('ONLINE', 'IN_PERSON', 'TELEPHONIC') NOT NULL DEFAULT 'ONLINE',
  `meeting_link_or_venue` VARCHAR(255) NULL,
  `interviewer_name` VARCHAR(100) NOT NULL,
  `interviewer_email` VARCHAR(120) NULL,
  `status` ENUM('SCHEDULED', 'COMPLETED', 'CANCELLED', 'RESCHEDULED') NOT NULL DEFAULT 'SCHEDULED',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `idx_interviews_application` (`application_id`),
  INDEX `idx_interviews_scheduled_at` (`scheduled_at`),
  INDEX `idx_interviews_status` (`status`),
  CONSTRAINT `fk_interviews_app` FOREIGN KEY (`application_id`) REFERENCES `applications` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_interviews_scheduler` FOREIGN KEY (`scheduled_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------
-- 11. Table: interview_feedback
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `interview_feedback`;
CREATE TABLE `interview_feedback` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `interview_id` INT NOT NULL UNIQUE,
  `technical_rating` INT NOT NULL CHECK (`technical_rating` BETWEEN 1 AND 5),
  `communication_rating` INT NOT NULL CHECK (`communication_rating` BETWEEN 1 AND 5),
  `overall_rating` INT NOT NULL CHECK (`overall_rating` BETWEEN 1 AND 5),
  `comments` TEXT NULL,
  `recommendation` ENUM('STRONG_HIRE', 'HIRE', 'HOLD', 'NO_HIRE') NOT NULL,
  `submitted_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_feedback_interview` FOREIGN KEY (`interview_id`) REFERENCES `interviews` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;
