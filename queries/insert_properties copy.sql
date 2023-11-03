INSERT INTO dbt_source.property_ptnf (
                        ID, DATASOURCE, UNIT_NUMBER, ADDRESS, CITY, STATE, ZIP, COUNTY, latitude, longitude,
                        TYPE, SUBTYPE, TITLE, DESCRIPTION, PARCEL_NUMBER, BEDS, BATHS, FULLBATHS, HALFBATHS, AREASQFT,
                        LOTSQFT, YEAR_BUILT, DISPLAY_ADDRESS, DISPLAY_LISTING, MLS_NUMBER, STATUS, SALEDATE, SALEPRICE,
                        LISTDATE, ORIG_LISTPRICE, CURR_LISTPRICE, DAYS_ON_MARKET, DATE_PRICE_ADJUST, LISTING_URL,
                        VTOUR_URL, MODIF_TIMESTAMP, EXPIRY_DATE, MISC, PHOTO_COUNT, VIDEO_COUNT, PHOTO_MODIF_DATE,
                        VIDEO_MODIF_DATE, DIST_SCHOOL, ELEM_SCHOOL, MIDL_SCHOOL, HIGH_SCHOOL, NABRHD_NAME, NABRHD_DESC,
                        NEARBY_URL, IDENTIFIER, GEOLEVEL, MAIN_PHOTO, PRICE_CHANGE, STATUS_CHANGE, BROKER_CODE,
                        BROKER_NAME, OFFICE_LISTING_YN, EXTRA1, EXTRA2, EXTRA3, EXTRA4, EXTRA5, POSTINGUSER_ID
                    )
                    VALUES (
                        %(ID)s, %(DATASOURCE)s, %(UNIT_NUMBER)s, %(ADDRESS)s, %(CITY)s, %(STATE)s, %(ZIP)s,
                        %(COUNTY)s, %(latitude)s, %(longitude)s, %(TYPE)s, %(SUBTYPE)s, %(TITLE)s, %(DESCRIPTION)s,
                        %(PARCEL_NUMBER)s, %(BEDS)s, %(BATHS)s, %(FULLBATHS)s, %(HALFBATHS)s, %(AREASQFT)s, %(LOTSQFT)s,
                        %(YEAR_BUILT)s, %(DISPLAY_ADDRESS)s, %(DISPLAY_LISTING)s, %(MLS_NUMBER)s, %(STATUS)s, %(SALEDATE)s,
                        %(SALEPRICE)s, %(LISTDATE)s, %(ORIG_LISTPRICE)s, %(CURR_LISTPRICE)s, %(DAYS_ON_MARKET)s,
                        %(DATE_PRICE_ADJUST)s, %(LISTING_URL)s, %(VTOUR_URL)s, %(MODIF_TIMESTAMP)s, %(EXPIRY_DATE)s,
                        %(MISC)s, %(PHOTO_COUNT)s, %(VIDEO_COUNT)s, %(PHOTO_MODIF_DATE)s, %(VIDEO_MODIF_DATE)s,
                        %(DIST_SCHOOL)s, %(ELEM_SCHOOL)s, %(MIDL_SCHOOL)s, %(HIGH_SCHOOL)s, %(NABRHD_NAME)s,
                        %(NABRHD_DESC)s, %(NEARBY_URL)s, %(IDENTIFIER)s, %(GEOLEVEL)s, %(MAIN_PHOTO)s,
                        %(PRICE_CHANGE)s, %(STATUS_CHANGE)s, %(BROKER_CODE)s, %(BROKER_NAME)s, %(OFFICE_LISTING_YN)s,
                        %(EXTRA1)s, %(EXTRA2)s, %(EXTRA3)s, %(EXTRA4)s, %(EXTRA5)s, %(POSTINGUSER_ID)s
                    )