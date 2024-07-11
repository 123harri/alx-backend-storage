-- Create view need_meeting that lists all students with a score under 80
-- and no last_meeting or last_meeting is more than a month ago

DROP VIEW IF EXISTS need_meeting;

CREATE VIEW need_meeting AS
SELECT name
FROM students
WHERE score < 80
AND (last_meeting IS NULL OR last_meeting < CURDATE() - INTERVAL 1 MONTH);
