# Issues
## Duplicate Assignments
investigating the teacher's issue and likely adding a db constraint...

1. try to find any dupes (eg any assignment records that have the same activity, enrollment, and piece as at least 1 other) looks like about 4552 rn
    select concat_ws('-', assns.activity_id, assns.enrollment_id, assns.piece_id) as uid, assns.* from assignments_assignment assns 
    where concat_ws('-', assns.activity_id, assns.enrollment_id, assns.piece_id) in (
      select concat_ws('-', aa.activity_id, aa.enrollment_id, aa.piece_id) as uuid
      from assignments_assignment aa 
      group by concat_ws('-', aa.activity_id, aa.enrollment_id, aa.piece_id)
      having count(*) > 1
    )
1. find those that have no submissions (total count rn of 4525)
    select concat_ws('-', assns.activity_id, assns.enrollment_id, assns.piece_id) as uid, assns.* from assignments_assignment assns 
    where concat_ws('-', assns.activity_id, assns.enrollment_id, assns.piece_id) in (
      select concat_ws('-', aa.activity_id, aa.enrollment_id, aa.piece_id) as uuid
      from assignments_assignment aa 
      group by concat_ws('-', aa.activity_id, aa.enrollment_id, aa.piece_id)
      having count(*) > 1
    ) and assns.id not in (select ss.assignment_id from submissions_submission ss) order by uid desc
1. select concat_ws('-', assns.activity_id, assns.enrollment_id, assns.piece_id) as uid, assns.* from assignments_assignment assns 
where concat_ws('-', assns.activity_id, assns.enrollment_id, assns.piece_id) in (
	select concat_ws('-', aa.activity_id, aa.enrollment_id, aa.piece_id) as uuid
	from assignments_assignment aa 
	group by concat_ws('-', aa.activity_id, aa.enrollment_id, aa.piece_id)
	having count(*) > 1
)  order by uid desc
