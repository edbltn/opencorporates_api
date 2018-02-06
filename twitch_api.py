import requests

# Implemented during Investigative Techniques with Susan McGregor
# Adapted from:
# https://www.geeksforgeeks.org/get-post-requests-using-python/

# Useful functions
# Prints the key hierarchy of the JSON Object sub_data
def printkeys(sub_data,level):
    indent = "* "

    # Set up indentation
    for i in range(0, level):
        indent = "  " + indent

    # Check that the data has type dict
    if type(sub_data) == dict:

        # Now recurse on each of its keys
        for key in sub_data.keys():
            markdown = indent + key
            print(markdown)
            printkeys(sub_data[key],level+1)

    # If data is a list, recurse on first element of the list
    if type(sub_data)== list:
        if sub_data: # check that list is not empty
            printkeys(sub_data[0],level+1)

# Query 1
# Set up token and URL
#api_token = # YOUR API TOKEN HERE
search_url = 'https://api.opencorporates.com/v0.4/companies/search'

# Set up parameters
country_code = 'bm'
date_range = '1995-01-01:2000-01-01'

data_params = {
    #'api_token':api_token,
    #'incorporation_date':date_range,
    'jurisdiction_code':country_code
}

# Perform and process get request
r = requests.get(url = search_url, params=data_params)
print(r.status_code)

data = r.json()

# Query 2
# Set up URL
bunge_id = '20791'
bunge_country = 'bm' # jurisdiction code

statements_url = \
'https://api.opencorporates.com/v0.4/companies/{}/{}/statements'\
.format(bunge_country, bunge_id)

# Perform and process get request
r = requests.get(url = statements_url, params={})
print(r.status_code)

data = r.json()

# Query 3
# Set up URL
officer_url = 'https://api.opencorporates.com/v0.4/officers/search'

# Set up parameters
data_params = {
    'jurisdiction_code':'us_ny',
    'q':'michael+bloomberg'
}

# Perform and process get request
r = requests.get(url = officer_url, params=data_params)
print(r.status_code)

data = r.json()
