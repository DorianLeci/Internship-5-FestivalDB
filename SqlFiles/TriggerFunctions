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
	