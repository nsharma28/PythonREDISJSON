import json
import psycopg2
import uuid

# PostgreSQL connection parameters
db_params = {
    "host": "16.171.41.170",
    "database": "recolorado_reso",
    "user": "postgres",
    "password": "karanishu",    
}

def insert_property_data(data):
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                insert_sql = """
                    INSERT INTO property_ptnf (
                        TERABITZ_ID, ID, DATASOURCE, UNIT_NUMBER, ADDRESS, CITY, STATE, ZIP, COUNTY, latitude, longitude,
                        TYPE, SUBTYPE, TITLE, DESCRIPTION, PARCEL_NUMBER, BEDS, BATHS, FULLBATHS, HALFBATHS, AREASQFT,
                        LOTSQFT, YEAR_BUILT, DISPLAY_ADDRESS, DISPLAY_LISTING, MLS_NUMBER, STATUS, SALEDATE, SALEPRICE,
                        LISTDATE, ORIG_LISTPRICE, CURR_LISTPRICE, DAYS_ON_MARKET, DATE_PRICE_ADJUST, LISTING_URL,
                        VTOUR_URL, MODIF_TIMESTAMP, EXPIRY_DATE, MISC, PHOTO_COUNT, VIDEO_COUNT, PHOTO_MODIF_DATE,
                        VIDEO_MODIF_DATE, DIST_SCHOOL, ELEM_SCHOOL, MIDL_SCHOOL, HIGH_SCHOOL, NABRHD_NAME, NABRHD_DESC,
                        NEARBY_URL, IDENTIFIER, GEOLEVEL, MAIN_PHOTO, PRICE_CHANGE, STATUS_CHANGE, BROKER_CODE,
                        BROKER_NAME, OFFICE_LISTING_YN, EXTRA1, EXTRA2, EXTRA3, EXTRA4, EXTRA5, POSTINGUSER_ID
                    )
                    VALUES (
                        %(TERABITZ_ID)s, %(ID)s, %(DATASOURCE)s, %(UNIT_NUMBER)s, %(ADDRESS)s, %(CITY)s, %(STATE)s, %(ZIP)s,
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
                """
                # Iterate over the first 50 property items in the data
                for property_item in data[:200]:
                    property_item['TERABITZ_ID'] = str(uuid.uuid4())
                    for field in ['ID', 'DATASOURCE', 'UNIT_NUMBER', 'ADDRESS', 'CITY', 'STATE', 'ZIP', 'COUNTY', 'latitude',
                                  'longitude', 'TYPE', 'SUBTYPE', 'TITLE', 'DESCRIPTION', 'PARCEL_NUMBER', 'BEDS', 'BATHS',
                                  'FULLBATHS', 'HALFBATHS', 'AREASQFT', 'LOTSQFT', 'YEAR_BUILT', 'DISPLAY_ADDRESS',
                                  'DISPLAY_LISTING', 'MLS_NUMBER', 'STATUS', 'SALEDATE', 'SALEPRICE', 'LISTDATE', 'ORIG_LISTPRICE',
                                  'CURR_LISTPRICE', 'DAYS_ON_MARKET', 'DATE_PRICE_ADJUST', 'LISTING_URL', 'VTOUR_URL',
                                  'MODIF_TIMESTAMP', 'EXPIRY_DATE', 'MISC', 'PHOTO_COUNT', 'VIDEO_COUNT', 'PHOTO_MODIF_DATE',
                                  'VIDEO_MODIF_DATE', 'DIST_SCHOOL', 'ELEM_SCHOOL', 'MIDL_SCHOOL', 'HIGH_SCHOOL', 'NABRHD_NAME',
                                  'NABRHD_DESC', 'NEARBY_URL', 'IDENTIFIER', 'GEOLEVEL', 'MAIN_PHOTO', 'PRICE_CHANGE',
                                  'STATUS_CHANGE', 'BROKER_CODE', 'BROKER_NAME', 'OFFICE_LISTING_YN', 'EXTRA1', 'EXTRA2',
                                  'EXTRA3', 'EXTRA4', 'EXTRA5', 'POSTINGUSER_ID']:
                        property_item[field] = property_item.get(field, None)

                cur.executemany(insert_sql, data[:200])  # Insert the first 50 values
                conn.commit()
        print("Data inserted successfully.")
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)

if __name__ == "__main__":
    # Load data from recolorado.json
    with open("C:\\Karan\\internship\\backup\\python\\\internship\\root\\data\\out\\recolorado.json", "r") as json_file:
        data = json.load(json_file)
    
    # Extract the property data from the JSON file
    property_data = [entry["PROPERTY"] for entry in data.values() if "PROPERTY" in entry]

    # Convert "null" strings to Python None values
    for property_item in property_data:
        for key, value in property_item.items():
            if value == "null":
                property_item[key] = None

    # Insert first 5 property data into the database
    insert_property_data(property_data)
