CREATE FUNCTION auto_period() RETURNS TRIGGER AS $$
BEGIN
	SELECT DATERANGE(f.start_time,f.end_time,'[]')
	INTO NEW.festival_period
	FROM festival f
	WHERE f.festival_id=NEW.festival_id;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_auto_period
BEFORE INSERT ON festival_performer
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
BEFORE INSERT ON ticket_type
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

	