-- View: public.vw_airbnb

-- DROP VIEW public.vw_airbnb;

CREATE OR REPLACE VIEW public.vw_airbnb
 AS
 SELECT ci.city_name,
 	ci.center_longitude,
	ci.center_latitude,
    rt.room_type_name,
    n.neighbourhood_name,
    l.longitude,
    l.latitude,
    l.price,
    l.minimum_nights,
    l.listing_given_id,
    pt.property_type_name,
    l.accommodates,
    l.bathrooms,
    l.bedrooms,
    l.beds,
    bt.bed_type_name,
    cp.cancel_policy_name,
    l.features,
    l.amenities
   FROM listing l
     LEFT JOIN neighbourhood n ON l.neighbourhood_id = n.neighbourhood_id
     LEFT JOIN city ci ON l.city_id = ci.city_id
     LEFT JOIN roomtype rt ON l.room_type_id = rt.room_type_id
     LEFT JOIN propertytype pt ON l.property_type_id = pt.property_type_id
     LEFT JOIN cancelpolicy cp ON l.cancel_policy_id = cp.cancel_policy_id
     LEFT JOIN bedtype bt ON l.bed_type_id = bt.bed_type_id;

ALTER TABLE public.vw_airbnb
    OWNER TO postgres;

