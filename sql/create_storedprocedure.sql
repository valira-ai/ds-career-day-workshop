-- PROCEDURE: public.storelisting()

-- DROP PROCEDURE IF EXISTS public.storelisting();

CREATE OR REPLACE PROCEDURE public.storelisting(
	)
LANGUAGE 'plpgsql'
AS $BODY$
begin
    WITH listing_preprocessed AS (
		SELECT ci."city_id",
			rt."room_type_id",
			n."neighbourhood_id",
			r."longitude",
			r."latitude",
			r."price",
			r."minimum_nights",
			r."id" AS listing_given_id,
			pt."property_type_id",
			r."accommodates",
			r."bathrooms",
			r."bedrooms",
			r."beds",
			bt."bed_type_id",
			cp."cancel_policy_id",
			r."features",
			r."amenities"
		FROM raw AS r
		LEFT JOIN neighbourhood AS n ON r."neighbourhood" = n."neighbourhood_name"
		LEFT JOIN city AS ci ON r."city" = ci."city_name"
		LEFT JOIN roomtype AS rt ON r."room_type" = rt."room_type_name"
		LEFT JOIN propertytype AS pt ON r."property_type" = pt."property_type_name"
		LEFT JOIN cancelpolicy AS cp ON r."cancel_policy" = cp."cancel_policy_name"
		LEFT JOIN bedtype AS bt ON r."bed_type" = bt."bed_type_name"
	)
	
	INSERT INTO listing("city_id", "room_type_id", "neighbourhood_id",
					   "longitude", "latitude", "price", "minimum_nights",
					   "listing_given_id", "property_type_id", "accommodates",
					   "bathrooms", "bedrooms", "beds", "bed_type_id", "cancel_policy_id",
					   "features", "amenities")
	SELECT * FROM listing_preprocessed

    

    commit;
end;
$BODY$;
ALTER PROCEDURE public.storelisting()
    OWNER TO postgres;
