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
	return """SELECT * 
    FROM (
    	SELECT name FROM neighbourhood
    	UNION 
    	SELECT area.area AS name FROM area
	)
    WHERE name LIKE 'B%';
	"""

def query7():
	return """SELECT DISTINCT area
    FROM area
    WHERE area NOT IN (
    	SELECT DISTINCT area.area
    	FROM place
    	JOIN neighbourhood USING(neighbourhood_id)
    	JOIN area USING(area_id)
    	JOIN room USING(room_type_id)
    	WHERE room.room_type LIKE 'Entire%'
	)
    ORDER BY area asc;
	"""

def query8():
	return """WITH joinedPlace(name, neighbourhood, room_type_id, number_of_reviews, price) AS (
    	SELECT place.name, neighbourhood.name as neighbourhood, place.room_type_id, place.number_of_reviews, place.price
		FROM place
    	JOIN neighbourhood USING(neighbourhood_id)
	)
    SELECT A.name, A.price, B.name, B.price
    FROM joinedPlace A, joinedPlace B
    WHERE A.neighbourhood = B.neighbourhood
    	AND A.room_type_id = B.room_type_id
    	AND A.number_of_reviews = B.number_of_reviews
    	AND A.price < B.price;
	"""

def query9():
	return """WITH joinedPlace(id, neighbourhood, room_type, price) AS (
		SELECT place.id, neighbourhood.name as neighbourhood, place.room_type_id, place.price
		FROM place
		JOIN neighbourhood USING(neighbourhood_id)
	)
	SELECT DISTINCT A.id AS place1_id, B.id AS place2_id, C.id as place3_id, A.price, A.room_type as room_type_id
	FROM joinedPlace A, joinedPlace B, joinedPlace C
	WHERE A.price < 100
	AND ((A.id < B.id) AND (B.id < C.id))
	AND ((A.price = B.price) AND (B.price = C.price))
	AND ((A.room_type = B.room_type) AND (B.room_type = C.room_type))
	AND ((A.neighbourhood <> B.neighbourhood)
		AND (B.neighbourhood <> C.neighbourhood) 
		AND (A.neighbourhood <> C.neighbourhood));
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
