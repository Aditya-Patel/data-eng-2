import sys

# Use this file to write your queries. Submit this file in Brightspace after finishing your homework.

#TODO: Write your username and answer to each query as a string in the return statements in the functions below. 
# Do not change the function names. 

#Your resulting tables should have the attributes in the same order as appeared in the sample answers. 

#Make sure to test that python prints out the strings (your username and SQL queries) correctly.

#usage: python hw1.py or python3 hw1.py

def username():
	return "o771438"
    
def query1():
	return """
	SELECT b.name as neighbourhood, AVG(a.price) as avg_price, COUNT(a.id) as place_count, MAX(a.price) as max_price, MIN(a.price) as min_price
	FROM place a 
	JOIN neighbourhood b USING(neighbourhood_id) 
	GROUP BY neighbourhood 
	ORDER BY avg_price desc;
	"""

def query2():
	return """
	SELECT b.name as neighbourhood, AVG(a.price) as avg_price, COUNT(a.id) as place_count, MAX(a.price) as max_price, MIN(a.price) as min_price
	FROM place a 
	JOIN neighbourhood b USING(neighbourhood_id)
	GROUP BY neighbourhood
	HAVING place_count >= 4
	ORDER BY avg_price DESC;
   """

def query3():
	return """
	SELECT b.name as neighbourhood, c.room_type, AVG(a.price) as avg_price, COUNT(c.room_type_id) as room_count, MAX(a.price) as max_price, MIN(a.price) as min_price
	FROM place a 
	JOIN neighbourhood b USING(neighbourhood_id) 
	JOIN room c USING(room_type_id)
	GROUP BY neighbourhood, room_type
	ORDER BY AVG(a.price) DESC;
	"""
	
def query4():
	return """
	SELECT b.area, a.name as neighbourhood, c.id, c.name, c.price
	FROM neighbourhood a 
	JOIN area b USING(area_id) 
	LEFT JOIN place c USING(neighbourhood_id)
	WHERE area LIKE 'STATEN%';
	"""

def query5():
	return """
	SELECT a.area, b.name as neighbourhood, COUNT(c.id) as place_count, AVG(c.price) as avg_price
	FROM area a LEFT JOIN neighbourhood b USING(area_id) LEFT JOIN place c USING(neighbourhood_id)
	GROUP BY area, neighbourhood
	HAVING area NOT LIKE 'Brooklyn' 
	AND area NOT LIKE 'Manhattan';
	"""

def query6():
	return """
	SELECT a.area, b.name as neighbourhood, COUNT(c.id) as place_count, AVG(c.price) as avg_price
	FROM area a LEFT JOIN neighbourhood b USING(area_id) LEFT JOIN place c USING(neighbourhood_id)
	GROUP BY area, neighbourhood
	HAVING area NOT LIKE 'Brooklyn' 
	AND area NOT LIKE 'Manhattan' 
	AND place_count >= 2;
	"""

def query7():
	return """
	SELECT b.name AS neighbourhood
	FROM place a JOIN neighbourhood b USING(neighbourhood_id)
	GROUP BY neighbourhood
	HAVING COUNT(a.id) > 5 
	AND MIN(a.price) <= 70;
	"""

def query8():
	return """
	SELECT a.id, a.name, a.price, b.room_type
	FROM place a JOIN room b USING(room_type_id)
	WHERE price = (SELECT MIN(price) FROM place);
	"""

def query9():
	return """
	SELECT a.host_id, b.host_name, COUNT(a.id) as count_places
	FROM place a JOIN host b USING(host_id)
	GROUP BY host_id
	HAVING count_places = (SELECT COUNT(id) FROM place GROUP BY host_id ORDER BY COUNT(id) DESC LIMIT 1);
	"""

def query10():
	return """
	SELECT 'neighbourhood with cheapest price' AS neighborhood, b.name, a.price
	FROM place a JOIN neighbourhood b USING(neighbourhood_id)
	WHERE price = (SELECT MIN(price) FROM place)
	UNION
	SELECT 'neighbourhood with most expensive price' AS neighborhood, b.name, a.price
	FROM place a JOIN neighbourhood b USING(neighbourhood_id)
	WHERE price = (SELECT MAX(price) FROM place);
	"""

#Do not edit below

def main():
	query_options = {1: query1(), 2: query2(), 3: query3(), 4: query4(), 5: query5(), 6: query6(), 7: query7(), 8: query8(), 
		9: query9(), 10: query10()}
	
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
