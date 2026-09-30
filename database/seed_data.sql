-- ==========================================================
-- SMART RECRUITMENT & PLACEMENT MANAGEMENT SYSTEM (SRPMS)
-- Database Seed Data (Roles & Standard Technical Skills)
-- ==========================================================

USE `recruitment_db`;

-- 1. Seed Roles
INSERT INTO `roles` (`id`, `name`, `description`) VALUES
  (1, 'ADMIN', 'Full system access and user management privileges'),
  (2, 'RECRUITER', 'Recruitment pipeline management, candidate tracking, and interviews')
ON DUPLICATE KEY UPDATE `description` = VALUES(`description`);

-- 2. Seed Standard Skills Catalog
INSERT INTO `skills` (`id`, `name`, `category`) VALUES
  (1, 'Python', 'Backend'),
  (2, 'Flask', 'Backend'),
  (3, 'Django', 'Backend'),
  (4, 'FastAPI', 'Backend'),
  (5, 'Java', 'Backend'),
  (6, 'Spring Boot', 'Backend'),
  (7, 'JavaScript', 'Frontend'),
  (8, 'TypeScript', 'Frontend'),
  (9, 'React.js', 'Frontend'),
  (10, 'Vue.js', 'Frontend'),
  (11, 'HTML5', 'Frontend'),
  (12, 'CSS3', 'Frontend'),
  (13, 'TailwindCSS', 'Frontend'),
  (14, 'MySQL', 'Database'),
  (15, 'PostgreSQL', 'Database'),
  (16, 'MongoDB', 'Database'),
  (17, 'Redis', 'Database'),
  (18, 'Git', 'DevOps'),
  (19, 'Docker', 'DevOps'),
  (20, 'Kubernetes', 'DevOps'),
  (21, 'AWS', 'Cloud'),
  (22, 'Azure', 'Cloud'),
  (23, 'REST APIs', 'Architecture'),
  (24, 'GraphQL', 'Architecture')
ON DUPLICATE KEY UPDATE `category` = VALUES(`category`);
