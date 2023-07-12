import sys

# Use this file to write your queries. Submit this file in Brightspace after finishing your homework.

#TODO: Write your username and answer to each query as a string in the return statements in the functions below. 
# Do not change the function names. 

#Your resulting tables should have the attributes in the same order as appeared in the sample answers. 

#Make sure to test that python prints out the strings (your username and SQL queries) correctly.

#usage: python hw1.py or python3 hw1.py

def username():
	return "pate1854"
    
def query1():
	return """SELECT place.id AS id, place.name as name, host.host_name, room.room_type, place.price, neighbourhood.name as neighbourhood, area.area
    FROM place
    JOIN host USING(host_id)
    JOIN room USING(room_type_id)
    JOIN neighbourhood USING(neighbourhood_id)
    JOIN area USING(area_id)
    WHERE neighbourhood LIKE 'Harlem';
	"""

def query2():
	return """SELECT place.id, place.name, host.host_name, room.room_type, price, longitude, latitude
    FROM place
    JOIN host USING(host_id)
    JOIN room USING(room_type_id)
    WHERE (longitude BETWEEN -73.99 AND -73.97)
    AND (latitude BETWEEN 40.75 AND 40.77);
	"""

def query3():
	return """SELECT DISTINCT minimum_nights
    FROM place
    ORDER BY minimum_nights asc;
	"""
	
def query4():
	return """SELECT AVG(price) AS avg_price, COUNT(id) as place_count, MAX(price) as max_price, MIN(price) as min_price
	FROM place;
	"""

def query5():
	return """SELECT AVG(price) AS avg_price, COUNT(id) as place_count, MAX(price) as max_price, MIN(price) as min_price
   FROM place
   JOIN neighbourhood USING(neighbourhood_id)
   WHERE neighbourhood.name LIKE 'Harlem';
	"""

def query6():
	return """

	"""

def query7():
	return """

	"""

def query8():
	return """

	"""

def query9():
	return """

	"""

#Do not edit below

def main():
	query_options = {1: query1(), 2: query2(), 3: query3(), 4: query4(), 5: query5(), 6: query6(), 7: query7(), 8: query8(), 
		9: query9()}
	
	if len(sys.argv) == 1:
		if username() == "username":
			print("Make sure to change the username function to return your username.")
			return
		else:
			print(username())
		for query in query_options.values():
			print(query)
	elif len(sys.argv) == 2:
		if sys.argv[1] == "username":
			print(username())
		else:
			print(query_options[int(sys.argv[1])])

	
if __name__ == "__main__":
   main()
