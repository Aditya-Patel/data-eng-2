import sys

#TODO: Write your username and answer to each query as a string in the return statements 
# in the functions below. Do not change the function names. 

# Write your queries using multi-line strings and use proper indentation to increase readability.

# Your result should have the attributes in the same order as appeared in the sample answers. 

# Make sure to test that python prints out the strings correctly.

# usage: python hw4.py

def username():
	return "YourUsername"
    
def query1():
    return """
           """ 

def query2():
    return """
           """
            
def query3():
    return """
           """ 

def query4():
    return """
           """

def query5():
    return """
           """ 

def query6():
    return """
           """

def query7():
    return """
           """
#Do not edit below

def main():
	query_options = {1: query1(), 2: query2(), 3: query3(), 4: query4(), 
		5: query5(), 6: query6(), 7: query7()}
	
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
