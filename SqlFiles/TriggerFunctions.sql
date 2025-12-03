CREATE OR REPLACE FUNCTION auto_period() RETURNS TRIGGER AS $$
BEGIN
	IF TG_OP='INSERT' OR NEW.festival_id IS DISTINCT FROM OLD.festival_id THEN
		SELECT DATERANGE(f.start_time,f.end_time,'[]')
		INTO NEW.festival_period
		FROM festival f
		WHERE f.festival_id=NEW.festival_id;
		
	END IF;
	
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;



CREATE TRIGGER trg_auto_period
BEFORE INSERT OR UPDATE ON festival_performer
FOR EACH ROW
EXECUTE FUNCTION auto_period();

CREATE TRIGGER trg_auto_period_staff
BEFORE INSERT OR UPDATE ON festival_staff
FOR EACH ROW
EXECUTE FUNCTION auto_period();


CREATE OR REPLACE FUNCTION  auto_ticket_validity() RETURNS TRIGGER AS $$
BEGIN

	IF NEW.type_of_ticket IN ('jednodnevna','promo') THEN
		NEW.validity:='jedan_dan';
		
	ELSEIF NEW.type_of_ticket IN ('VIP','festivalska') THEN
		NEW.validity:='cijeli_festival';
		
	END IF;

	RETURN NEW;
END;
$$ LANGUAGE plpgsql;



CREATE TRIGGER trg_auto_ticket_validity
BEFORE INSERT OR UPDATE ON ticket_type
FOR EACH ROW
EXECUTE FUNCTION auto_ticket_validity();


CREATE OR REPLACE FUNCTION check_ticket_purchase_time() RETURNS TRIGGER AS $$

DECLARE 
	purchase_time TIMESTAMP;
	festival_range tsrange;

BEGIN
	SELECT INTO purchase_time
	FROM orders o
	WHERE o.order_id=NEW.order_id;
	
	SELECT tsrange(f.start_date::timestamp,f.end_date::timestamp,'[]')
	INTO festival_range
	FROM festival f
	JOIN ticket t ON t.festival_id=f.festival_id
	WHERE t.ticket_id=NEW.ticket_id;

	IF NOT (festival_range @> purchase_time) THEN 
	RAISE EXCEPTION 'Kupovina mora biti unutar trajanja festivala';
	
	END IF;

	RETURN NEW;
END;

$$ LANGUAGE plpgsql;
	

CREATE OR REPLACE TRIGGER trg_check_ticket_purchase_time
BEFORE INSERT ON order_item
FOR EACH ROW
EXECUTE FUNCTION check_ticket_purchase_time();


CREATE OR REPLACE FUNCTION auto_total_price() RETURNS TRIGGER AS $$

BEGIN

	UPDATE orders o
	SET total_price=(
		SELECT SUM(i.price*i.quantity) 
		FROM order_item i
		WHERE i.order_id=NEW.order_id
	)
	WHERE o.order_id=NEW.order_id;


	RETURN NEW;
END

$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_auto_total_price
AFTER INSERT OR UPDATE ON order_item
FOR EACH ROW
EXECUTE FUNCTION auto_total_price();


CREATE OR REPLACE FUNCTION membership_card_eligibility() RETURNS TRIGGER AS $$
DECLARE
	distinct_festivals INT;
	total_spent NUMERIC;
BEGIN
	SELECT COUNT(DISTINCT t.festival_id)
	INTO distinct_festivals
	FROM order_item oi
	JOIN ticket t on t.ticket_id=oi.ticket_id
	JOIN orders o ON o.order_id=oi.order_id
	WHERE o.visitor_id=NEW.visitor_id;

	SELECT SUM(oi.price*oi.quantity)
	INTO total_spent 
	FROM order_item oi
	JOIN orders o ON o.order_id=oi.order_id
	WHERE o.visitor_id=NEW.visitor_id;

	IF distinct_festivals<=3 OR total_spent<600 THEN
		RAISE EXCEPTION 'Posljetitelj ne može imati člansku iskaznicu (distinct_festivals: %),(total_spent: %)',
		distinct_festivals,total_spent;

	RETURN NEW;
	
	END IF;
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_membership_card_eligibility
BEFORE INSERT ON membership_card
FOR EACH ROW
EXECUTE FUNCTION membership_card_eligibility();



CREATE OR REPLACE FUNCTION check_capacity() RETURNS TRIGGER AS $$
DECLARE
	festival_capacity INT;
BEGIN
	IF NEW.capacity>(SELECT f.capacity INTO festival_capacity 
	FROM festival f 
	WHERE f.festival_id=NEW.festival_id) THEN
		RAISE EXCEPTION 'Kapacitet (%) ne može biti veći od kapaciteta festivala. (%)',NEW.capacity,festival.capacity;

	END IF;

END
$$ LANGUAGE plpgsql;


CREATE OR REPLACE TRIGGER trg_check_capacity_stage
BEFORE INSERT OR UPDATE ON stage
FOR EACH ROW
EXECUTE FUNCTION check_capacity();

CREATE OR REPLACE TRIGGER trg_check_capacity_workshop
BEFORE INSERT OR UPDATE ON workshop
FOR EACH ROW
EXECUTE FUNCTION check_capacity();
		

CREATE OR REPLACE FUNCTION check_workshop_capacity() RETURNS TRIGGER AS $$
DECLARE 
	curr_enrollment_count INT;
	workshop_capacity INT;
BEGIN
	SELECT COUNT(*)
	INTO curr_enrollment_count
	FROM visitor_workshop v
	WHERE v.workshop_id=NEW.workshop_id AND v.status IN ('prijavljen','čeka na povtrdu')

	IF(curr_enrollment_count>=(SELECT capacity INTO workshop_capacity FROM workshop)) THEN
		RAISE EXCEPTION 'Radionica je popunjena do kraja (kapacitet: %)',workshop_capacity;
	END IF;

	RETURN NEW;
END
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_capacity
BEFORE INSERT ON visitor_workshop
FOR EACH ROW
EXECUTE FUNCTION check_workshop_capacity();
	
	