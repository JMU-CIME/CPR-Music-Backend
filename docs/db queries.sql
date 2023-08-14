-- teleband
-- get the data nathan and student need from teleband
--  1. identify which users are teachers in the dataset
select * from teachers where id > 13 and id not in (21,23,24,25,26);
--  2. get the students for those teachers
select * from students where teacher_id > 13 and teacher_id not in (21,23,24,25,26);
--  3. get all the business
select s.id, s.teacher_id, s.grade, s.created_at, s.updated_at, sa.*, a.*, asa.*, asb.*
from students s 
join student_assignments sa on sa.student_id = s.id 
join assignments a on a.id = sa.assignment_id
join active_storage_attachments asa on asa.record_id = sa.id
join active_storage_blobs asb on asb.id = asa.blob_id 
where s.teacher_id > 13 and s.teacher_id not in (21,23,24,25,26) and asa.record_type = 'StudentAssignment';
-- musiccpr