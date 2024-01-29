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


--aug 2 2023

-- oct 23 get alden the respond and connect things
select
uu.id as student_id,
ii.name as instrument,
uu.grade as grade,
cc.owner_id as teacher_id,
aa.id as assignment_id,
p."name" as piece,
pt."name" as part,
actc."name" as activity_category,
actt."name" as activity_type,
ss.submitted as created_at,
sa.file as recording_file,
ss.content as content_response_composition,
sg.tone as tone,
sg.rhythm as rhythm,
sg."expression" as "expression",
ss.id as "submission_id"
from assignments_assignment aa
join courses_enrollment ce on aa.enrollment_id = ce.id
join users_user uu on uu.id = ce.user_id
join instruments_instrument ii on ii.id = ce.instrument_id
join courses_course cc on cc.id = ce.course_id
join assignments_activity asgn_act on aa.activity_id = asgn_act.id
join assignments_activitytype actt on actt.id = asgn_act.activity_type_id
join assignments_activitycategory actc on actc.id = actt.category_id 
join musics_part mp on mp.id = aa.part_id
join musics_piece p on p.id = mp.piece_id
join musics_parttype pt on pt.id = mp.part_type_id
left join submissions_submission ss on ss.assignment_id = aa.id
left join submissions_submissionattachment sa on sa.submission_id = ss.id
left join submissions_grade sg on sg.id = ss.grade_id
where cc.owner_id in (9,10) and actc."name" in ('Respond', 'Connect', 'Connect Green', 'Connect Benjamin', 'Connect Danyew') and ss.content is not null and ss.id in (select max(ss.id)
from assignments_assignment aa 
join assignments_activity asgn_act on aa.activity_id = asgn_act.id
join assignments_activitytype actt on actt.id = asgn_act.activity_type_id
join assignments_activitycategory actc on actc.id = actt.category_id
left join submissions_submission ss on ss.assignment_id = aa.id
left join submissions_submissionattachment sa on sa.submission_id = ss.id
left join submissions_grade sg on sg.id = ss.grade_id
join courses_enrollment ce on ce.id =aa.enrollment_id 
join courses_course cc on cc.id = ce.course_id 
where cc.owner_id in (9,10) and actc."name" in ('Respond', 'Connect', 'Connect Green', 'Connect Benjamin', 'Connect Danyew') and ss.content is not null
group by aa.id)