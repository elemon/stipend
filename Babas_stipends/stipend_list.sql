select name,credit,debit,stipends.comment from stipends join students on students.id = student_id order by name;