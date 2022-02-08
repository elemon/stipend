select 
    
	students.id as "Student#",
	name as "Genius",
	sum(credit) as "Credit",
	sum(debit) as "Debit",
	sum(credit-debit) as "Total Due" 
		from stipends join  
			students on students.id = student_id 
				group by students.id 
					order by name; 