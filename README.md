# PythonREDISJSON

1) Active Vs Sold Graph for last 1 year
- We need an API for Active Properties Vs Sold Properties for last 12 Months
This is the MySQL Query
select count(*), status,listdate,EXTRACT(YEAR FROM listdate),EXTRACT(MONTH FROM listdate),type from property_ptnf where status IN ('Active', 'Price Change', 'Extended', 'New', 'Under Agreement', 'Reactivated', 'Back on Market', 'Pending') and City='Denver' group by EXTRACT(YEAR FROM listdate),EXTRACT(MONTH FROM listdate);


2) Status wise Count
- Select Count(*),Status from property_ptnf group by status.
No Of Active Property Processed Daily/Weeekly?Monthly Which Should include Folowing Status 
