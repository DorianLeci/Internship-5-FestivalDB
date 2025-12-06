CREATE OR REPLACE FUNCTION auto_period() RETURNS TRIGGER AS $$
BEGIN
	IF TG_OP='INSERT' OR NEW.festival_id IS DISTINCT FROM OLD.festival_id THEN
		SELECT DATERANGE(f.start_date,f.end_date,'[]')
		INTO NEW.festival_period
		FROM festival f
		WHERE f.festival_id=NEW.festival_id;
		
	END IF;
	
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE TRIGGER trg_auto_period
BEFORE INSERT OR UPDATE ON festival_performer
FOR EACH ROW
EXECUTE FUNCTION auto_period();

CREATE OR REPLACE TRIGGER trg_auto_period_staff
BEFORE INSERT OR UPDATE ON festival_staff
FOR EACH ROW
EXECUTE FUNCTION auto_period();


CREATE OR REPLACE FUNCTION  auto_ticket_validity() RETURNS TRIGGER AS $$
BEGIN

	IF NEW.ticket_type IN ('jednodnevna','promo') THEN
		NEW.validity:='jedan_dan';
		
	ELSEIF NEW.ticket_type IN ('VIP','festivalska','kamp') THEN
		NEW.validity:='cijeli_festival';
		
	END IF;

	RETURN NEW;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE TRIGGER trg_auto_ticket_validity
BEFORE INSERT OR UPDATE ON ticket_type
FOR EACH ROW
EXECUTE FUNCTION auto_ticket_validity();


CREATE OR REPLACE FUNCTION check_ticket_purchase_time() RETURNS TRIGGER AS $$

DECLARE 
	purchase_time TIMESTAMP;
	festival_range tsrange;

BEGIN
	SELECT o.time_of_purchase
	INTO purchase_time
	FROM orders o
	WHERE o.order_id=NEW.order_id;
	
	SELECT tsrange(f.start_date::timestamp,f.end_date::timestamp+interval '1 day','[]')
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
	SET 
	total_price=(
		SELECT SUM(i.price*i.quantity) 
		FROM order_item i
		WHERE i.order_id=NEW.order_id
	),
	amount=(
		SELECT SUM(i.quantity)
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
	SELECT f.capacity
	INTO festival_capacity
	FROM festival f
	WHERE f.festival_id=NEW.festival_id;
	
	IF NEW.capacity>(festival_capacity) THEN
		RAISE EXCEPTION 'Kapacitet (%) ne može biti veći od kapaciteta festivala. (%)',NEW.capacity,festival.capacity;

	END IF;

	RETURN NEW;

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
	SELECT current_enrolled,capacity 
	INTO curr_enrollment_count,workshop_capacity
	FROM workshop w
	WHERE w.workshop_id=NEW.workshop_id;
	
	IF NEW.status IN ('prijavljen','ceka_na_potvrdu') THEN
		IF curr_enrollment_count>workshop_capacity THEN
				RAISE EXCEPTION 'Radionica je popunjena do kraja (kapacitet: %)',workshop_capacity;

		END IF;

		UPDATE workshop w
		SET current_enrolled=current_enrolled+1
		WHERE workshop_id=NEW.workshop_id;
		
	END IF;

	RETURN NEW;
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_check_capacity
BEFORE INSERT ON visitor_workshop
FOR EACH ROW
EXECUTE FUNCTION check_workshop_capacity();


CREATE OR REPLACE FUNCTION set_festival_status() RETURNS TRIGGER AS $$
BEGIN
	IF NEW.start_date>CURRENT_DATE THEN
		NEW.status='Planiran';

	ELSIF NEW.start_date<=CURRENT_DATE AND NEW.end_date>=CURRENT_DATE THEN
		NEW.status='Aktivan';
	ELSE
		NEW.status='Zavrsen';

	END IF;
	RETURN NEW;

END
$$ LANGUAGE plpgsql;
	
CREATE OR REPLACE TRIGGER trg_festival_status
BEFORE INSERT OR UPDATE ON festival
FOR EACH ROW
EXECUTE FUNCTION set_festival_status();


CREATE OR REPLACE FUNCTION calculate_band_members() RETURNS TRIGGER AS $$
DECLARE
	member_count INT;
	target_band_id INT;
BEGIN
	IF TG_OP='DELETE' THEN
		target_band_id=OLD.band_id;
	ELSE
		target_band_id=NEW.band_id;
	END IF;
	
	SELECT COUNT(*)
	INTO member_count
	FROM performer p
	WHERE p.type='Band_Member' AND p.band_id=target_band_id;

	UPDATE band b
	SET num_of_members=member_count
	WHERE b.band_id=target_band_id;
	
	RETURN NEW;

END
$$ LANGUAGE plpgsql;


CREATE OR REPLACE TRIGGER trg_calculate_band_members
AFTER INSERT OR DELETE ON performer
FOR EACH ROW
EXECUTE FUNCTION calculate_band_members();


CREATE OR REPLACE FUNCTION performance_period_check() RETURNS TRIGGER AS $$
DECLARE
  	festival_period_local TSRANGE;
BEGIN
	SELECT tsrange(lower(fp.festival_period)::timestamp,upper(fp.festival_period)::timestamp+ interval '1 day','[]')
	INTO festival_period_local
	FROM festival_performer fp
	WHERE fp.festival_performer_id=NEW.festival_performer_id;

	IF NOT NEW.performance_period <@ festival_period_local THEN
		RAISE EXCEPTION 'Nastup mora biti unutar trajanja festivala (%)',festival_period_local;
	END IF;
	
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_performance_period_check
BEFORE INSERT OR UPDATE ON performance
FOR EACH ROW
EXECUTE FUNCTION performance_period_check();


CREATE OR REPLACE FUNCTION performance_overlap_performer() RETURNS TRIGGER AS $$
DECLARE
	target_performer_id INT;
	count INT;
BEGIN
	SELECT performer_id
	INTO target_performer_id
	FROM festival_performer fp
	WHERE fp.festival_performer_id=NEW.festival_performer_id;
	
	SELECT COUNT(*)
	INTO count
	FROM performance p 
	JOIN festival_performer fp on fp.festival_performer_id=p.festival_performer_id
	WHERE fp.performer_id=target_performer_id
	 AND p.performance_period && NEW.performance_period;

	IF count>0 THEN
		RAISE EXCEPTION 'Izvođač već ima nastup nastup za uneseno vrijeme %',NEW.performance_period;
	END IF;

	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_performance_overlap_performer
BEFORE INSERT OR UPDATE ON performance
FOR EACH ROW
EXECUTE FUNCTION performance_overlap_performer();
