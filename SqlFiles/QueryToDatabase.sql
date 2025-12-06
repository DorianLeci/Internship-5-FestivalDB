SELECT *
FROM workshop w
JOIN festival f ON f.festival_id = w.festival_id

WHERE LOWER(w.difficulty::text) = LOWER('NAPREDNA')
  AND (EXTRACT(YEAR FROM f.start_date) = 2025 OR EXTRACT(YEAR FROM f.end_date) = 2025)
ORDER BY current_enrolled DESC
LIMIT 10;



SELECT pe.name AS performer_name,f.name AS festival_name,s.name AS stage_name,lower(p.performance_period) AS performance_start
FROM performance p
JOIN festival_performer fp ON fp.festival_performer_id=p.festival_performer_id
JOIN performer pe ON pe.performer_id=fp.performer_id
JOIN stage s ON s.stage_id=p.stage_id
JOIN festival f ON f.festival_id=s.festival_id

WHERE p.expected_visitors>10000
LIMIT 100;



SELECT *FROM festival
WHERE (EXTRACT(YEAR FROM start_date) = 2025 OR EXTRACT(YEAR FROM end_date) = 2025)
LIMIT 100;



SELECT * FROM workshop
WHERE LOWER(difficulty::text)=LOWER('NAPREDNA')
ORDER BY current_enrolled DESC
LIMIT 10;



SELECT *FROM workshop
WHERE duration>=INTERVAL '4 hours'
ORDER BY duration DESC
LIMIT 100;




SELECT *FROM workshop
WHERE prior_knowledge_required=true
ORDER BY current_enrolled DESC
LIMIT 100;



SELECT 
	mentor_id,
	COALESCE(m.performer_id,m.staff_id) AS person_id,
	COALESCE(s.name,p.name) AS name,
	COALESCE(m.birth_date,s.birth_date) AS birth_date,
	m.expertise_area,m.years_of_experience
FROM mentor m

LEFT JOIN staff s ON m.staff_id=s.staff_id
LEFT JOIN performer p ON m.performer_id=p.performer_id
WHERE m.years_of_experience>10
LIMIT 100;




SELECT 
	mentor_id,
	COALESCE(m.performer_id,m.staff_id) AS person_id,
	COALESCE(s.name,p.name) AS name,
	COALESCE(m.birth_date,s.birth_date) AS birth_date,
	m.expertise_area,m.years_of_experience
	
FROM mentor m
LEFT JOIN staff s ON m.staff_id=s.staff_id
LEFT JOIN performer p ON m.performer_id=p.performer_id
WHERE EXTRACT(YEAR FROM m.birth_date)>1985
LIMIT 100;




SELECT v.visitor_id,v.name AS visitor_name,v.surname AS visitor_surname,v.email,v.birth_date,c.city_id,c.name AS city_name,c.postal_code
FROM visitor v
JOIN city c ON c.city_id=v.city_id
WHERE c.name='Split'
LIMIT 100;



SELECT v.visitor_id,v.name AS visitor_name,v.surname AS visitor_surname,v.email,v.birth_date,c.city_id,c.name AS city_name,c.postal_code
FROM visitor v
JOIN city c ON c.city_id=v.city_id
WHERE v.email LIKE '%@gmail.com'
LIMIT 100;



SELECT v.visitor_id,v.name AS visitor_name,v.surname AS visitor_surname,v.email,v.birth_date
FROM visitor v
WHERE AGE(v.birth_date)<INTERVAL '25 years'
LIMIT 100;



SELECT t.ticket_id,i.price,ti.ticket_type,ti.description FROM ticket t
JOIN ticket_type ti ON ti.ticket_type_id=t.ticket_type_id
JOIN order_item i ON i.ticket_id=t.ticket_id

WHERE i.price>120
ORDER BY i.price DESC
LIMIT 100;



SELECT t.ticket_id,i.price,ti.ticket_type,ti.description FROM ticket t
JOIN ticket_type ti ON ti.ticket_type_id=t.ticket_type_id
JOIN order_item i ON i.ticket_id=t.ticket_id

WHERE LOWER(ti.ticket_type::text)=LOWER('VIP')
ORDER BY i.price DESC
LIMIT 100;



SELECT t.ticket_id,i.price,ti.ticket_type,ti.description,ti.validity FROM ticket t
JOIN ticket_type ti ON ti.ticket_type_id=t.ticket_type_id
JOIN order_item i ON i.ticket_id=t.ticket_id

WHERE LOWER(ti.ticket_type::text)=LOWER('FESTIVALSKA') AND LOWER(ti.validity::text)=LOWER('CIJELI_FESTIVAL')
ORDER BY i.price DESC
LIMIT 100;


SELECT *FROM staff
WHERE has_safety_training=true
LIMIT 100;



