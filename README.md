# opencorporates API Profile

Creation date: 02/05/18 10:51:58 PM

@author Eric Bolton <edbltn@gmail.com>

## Query 1: Search for companies incorporated in Bermuda

The opencorporates API lets users perform searches of their database and returns the results in JSON format. To test this feature, I used the following query:

'https://api.opencorporates.com/v0.4/companies/search?jurisdiction_code=bm'

To generate this query, I modified code by Nikhil Kumar at [Geeks for Geeks](https://www.geeksforgeeks.org/get-post-requests-using-python/). The link provides a useful explanation for how to perform GET requests.

```python
import requests

# Set up token and URL
api_token = # YOUR API TOKEN HERE
search_url = 'https://api.opencorporates.com/v0.4/companies/search'

# Set up parameters
country_code = 'bm'
date_range = '1995-01-01:2000-01-01'

data_params = {
    'api_token':api_token,
    'incorporation_date':date_range,
    'jurisdiction_code':country_code
}

# Perform and process get request
r = requests.get(url = search_url, params=data_params)
print(r.status_code)

data = r.json()
```

The API token (which can be obtained through a short application at https://opencorporates.com/api_accounts/new) enables enhanced usage of the API, such as searching based on an entity's incorporation date, which we're doing in this case

'incorporation_date' enables users to limit results to firms within a specified date range, such as '1995-01-01:2000-01-01.'

The request returns the following response:

```
{'api_version': '0.4', 'results': {'companies': [<companies>], 'page': 1, 'per_page': 30, 'total_pages': 233, 'total_count': 6967}}
```

For brevity, the 30 companies displayed in the 'companies' array are excluded.

The response contains the total number of companies, which tells us in this case that there were 6967 companies incorporated in Bermuda between January 1st, 1995 and January 1st, 2000. It also contains first page of 30 companies. By setting parameters for 'per_page' and 'page,' one can change which page the request returns, and how many companies to display.

To examine this object further, we can use the fact that JSON objects have type "dict" in Python to define the following function, 'printkeys,' which will print a JSON Object's keys in markdown:

```python
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
```

I'm choosing to print the keys of only the first element of any list that the recursion tree encounters, for simplicity's sake. This is because some lists have objects whose properties differ from each other, which leads their keys to differ.


Now we need only call:

```python
printkeys(data,0)
```

This yields the following markdown list:

* api_version
* results
  * companies
      * company
        * name
        * company_number
        * jurisdiction_code
        * incorporation_date
        * dissolution_date
        * company_type
        * registry_url
        * branch
        * branch_status
        * inactive
        * current_status
        * created_at
        * updated_at
        * retrieved_at
        * opencorporates_url
        * previous_names
        * source
          * publisher
          * url
          * retrieved_at
        * registered_address
        * registered_address_in_full
        * restricted_for_marketing
        * native_company_number
  * page
  * per_page
  * total_pages
  * total_count

Many of the potentially interesting entries in company, such as 'branch,' 'branch_status,' and 'company_type' are unfortunately often left empty.

However, some useful entries stand out:
* **incorporation_date** tells you when the company was incorporated.
* **jurisdiction_code** in general, this gives the country in which the company was incorporated in 2-letter [ISO country code](http://www.nationsonline.org/oneworld/country_code_list.htm) format. However, smaller entities are also categorized as jurisdictions, such as U.S. states. In this case, the relevant code is given by the [ISO 3166-2](https://en.wikipedia.org/wiki/ISO_3166-2) subcountry code. [Here](https://en.wikipedia.org/wiki/ISO_3166-2:US) is the relevant list for the U.S.
* **source** gives details as to where and when the information was obtained.
* **company_number** tells us how to find a company within the database, so we can drill down on specific companies. For example, Bunge Ltd., an agrobusiness corporation incorporated in Bermuda, has a company_number of '20791'.

## Query 2: Bunge Ltd.'s Statements

To get the statements for a specific company, one can write a query with the following example format:
```
'https://api.opencorporates.com/v0.4/companies/bm/20791/statements'
```
I generated this query with the following code:

```python
import requests

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
```

The query requires the jurisdiction code and company ID for a given company, which can be obtained from the response to a search for a company. The response to a statement query looks like this:

```
{'api_version': '0.4', 'results': {'statements': [<statements>], 'page': 1, 'per_page': 30, 'total_pages': 1, 'total_count': 16}}
```

The 16 statements, which I've excluded in the response above, are themselves massive and confusing JSON objects, such as this one:

```
{'statement': {'id': 437589035, 'data_type': 'control_statement', 'properties': {'control_level': 'unknown', 'control_mechanisms': [{'mechanism_type': 'share_ownership', 'mechanism_properties': {'exercised_via': None, 'percentage_of_shares': {'minimum': 75, 'maximum': 100, 'exclusive_minimum': True, 'exclusive_maximum': False}}, 'source_description': 'The person holds, directly or indirectly, more than 75% of the shares in the company.'}], 'controlling_entities': [{'entity_type': 'company', 'entity_properties': {'jurisdiction': 'Bermuda', 'company_number': '20791', 'company_type': 'Limited Liability Company', 'name': 'Bunge Limited', 'all_attributes': {'uid': '/company/05913290/persons-with-significant-control/corporate-entity/9VbVi-T72fse--W3ig-8cwOqS8g'}, 'registered_address': {'country': 'Usa', 'locality': 'White Plains', 'postal_code': '10606', 'region': 'Ny', 'street_address': '50 Main Street'}}}], 'other_attributes': {'etag': '67c7da42d470c2097f77c53ce0d11180976acc39', 'ceased_on': None, 'notified_on': '2016-04-06'}, 'retrieved_at': '2016-09-21T13:58:03+00:00', 'subject_entity': {'entity_properties': {'company_number': '05913290', 'jurisdiction_code': 'gb'}, 'entity_type': 'company'}, 'uid': '/company/05913290/persons-with-significant-control/corporate-entity/9VbVi-T72fse--W3ig-8cwOqS8g'}, 'opencorporates_url': 'https://opencorporates.com/statements/437589035', 'start_date': '2016-04-06', 'start_date_type': '<', 'end_date': None, 'end_date_type': None, 'sample_date': '2016-04-06', 'predicate': 'controls', 'subject_entities': [{'entity_type': 'company', 'id': 3796775, 'name': 'Bunge Limited', 'opencorporates_url': 'https://opencorporates.com/companies/bm/20791', 'company_number': '20791', 'jurisdiction_code': 'bm'}], 'object_entities': [{'entity_type': 'company', 'id': 717757, 'name': 'CLIMATE CHANGE CAPITAL CARBON MANAGED ACCOUNT LIMITED', 'opencorporates_url': 'https://opencorporates.com/companies/gb/05913290', 'company_number': '05913290', 'jurisdiction_code': 'gb'}], 'sources': [{'source_url': 'http://download.companieshouse.gov.uk/en_pscdata.html', 'confidence': 90, 'source_type': 'external', 'actor_type': 'bot', 'log_message': None, 'created_at': '2016-10-09T23:35:56+00:00'}]}}
```

However, calling printkeys gives more clarity, yielding the following markdown list:

* api_version
* results
  * statements
      * statement
        * id
        * data_type
        * properties
          * control_level
          * control_mechanisms
              * mechanism_type
              * mechanism_properties
                * exercised_via
                * percentage_of_shares
                  * minimum
                  * maximum
                  * exclusive_minimum
                  * exclusive_maximum
              * source_description
          * controlling_entities
              * entity_type
              * entity_properties
                * jurisdiction
                * company_number
                * company_type
                * name
                * all_attributes
                  * uid
                * registered_address
                  * country
                  * locality
                  * postal_code
                  * region
                  * street_address
          * other_attributes
            * etag
            * ceased_on
            * notified_on
          * retrieved_at
          * subject_entity
            * entity_properties
              * company_number
              * jurisdiction_code
            * entity_type
          * uid
        * opencorporates_url
        * start_date
        * start_date_type
        * end_date
        * end_date_type
        * sample_date
        * predicate
        * subject_entities
            * entity_type
            * id
            * name
            * opencorporates_url
            * company_number
            * jurisdiction_code
        * object_entities
            * entity_type
            * id
            * name
            * opencorporates_url
            * company_number
            * jurisdiction_code
        * sources
            * source_url
            * confidence
            * source_type
            * actor_type
            * log_message
            * created_at
  * page
  * per_page
  * total_pages
  * total_count

This list provides some interesting details.

First, it's important to note that in the case of statements, the 'properties' key depends on the 'data_type'. Since the first element of the 'statements' list had type 'control_statment', we are seeing the keys that a control statement object would have.

However, all statements include 'subject_entities' and 'object_entities' fields, which gives details about the companies the statement concerns.

Control statements give details about who controls what, and how:
* **control_mechanisms** is a list of objects whose attributes describe the means and level of control. In this case, the 'mechanism_type' is 'share_ownership', so the properties include a estimated range for the percentage of shares owned.
* **controlling_entities** is a list of objects whose attributes describe the entity in control, such as whether the entity is a company, and if it is, the company number within the opencorporates database.
* **subject_entity** (not to be confused with 'subject_entities,' which belongs to all statements) describes the entity being controlled.

For example, the JSON object that our sample query returned lists 'Bunge Limited' in the array of 'controlling_entities', and describes the control mechanism under the 'control_mechanisms' field as ownership of a greater than 75% stake in 'CLIMATE CHANGE CAPITAL CARBON MANAGED ACCOUNT LIMITED,' listed under 'object_entities'.

## Query 3: Search for Michael Bloomberg

Finally, opencorporate's API lets you search for officers within companies. Let's try to find Michael Bloomberg:

```
'https://api.opencorporates.com/v0.4/officers/search?jurisdiction_code=us_ny&q=bloomberg'
```

I generated this query with the following code:

```python
import requests

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
```

Here, I'm doing a keyword search for 'michael+bloomberg' using the 'q' parameter, and restricting my results to the jurisdiction 'us_ny' - that is New York state.

The API's officer search lets you drill down even more and search for people with specific positions, such as 'CEO,' but this is a new feature, and the naming convention for positions vary wildly, so it typically doesn't return many interesting results.

Here is the result for our search:

```
{'api_version': '0.4', 'results': {'page': 1, 'per_page': 30, 'total_pages': 1, 'total_count': 2, 'officers': [<officers>]}}
```

Here are the two officers that our search returned:

```
[{'officer': {'id': 225418939, 'uid': None, 'name': 'MICHAEL BLOOMBERG', 'jurisdiction_code': 'us_ny', 'position': 'chief executive officer', 'retrieved_at': '2018-01-23T03:26:17+00:00', 'opencorporates_url': 'https://opencorporates.com/officers/225418939', 'start_date': None, 'end_date': None, 'occupation': None, 'current_status': None, 'inactive': False, 'company': {'name': 'MARLBOROUGH ASSOCIATES, INC.', 'jurisdiction_code': 'us_ny', 'company_number': '1297997', 'opencorporates_url': 'https://opencorporates.com/companies/us_ny/1297997'}}}, {'officer': {'id': 225078260, 'uid': None, 'name': 'MICHAEL BLOOMBERG', 'jurisdiction_code': 'us_ny', 'position': 'chief executive officer', 'retrieved_at': '2016-07-07T13:41:08+00:00', 'opencorporates_url': 'https://opencorporates.com/officers/225078260', 'start_date': None, 'end_date': None, 'occupation': None, 'current_status': None, 'inactive': True, 'company': {'name': 'BLOOMBERG ASIA INC.', 'jurisdiction_code': 'us_ny', 'company_number': '1210780', 'opencorporates_url': 'https://opencorporates.com/companies/us_ny/1210780'}}}]
```

For more clarity, here's the markdown list for the JSON object returned by our search:

* api_version
* results
  * page
  * per_page
  * total_pages
  * total_count
  * officers
      * officer
        * id
        * uid
        * name
        * jurisdiction_code
        * position
        * retrieved_at
        * opencorporates_url
        * start_date
        * end_date
        * occupation
        * current_status
        * inactive
        * company
          * name
          * jurisdiction_code
          * company_number
          * opencorporates_url

Sadly, many of the useful fields are often left empty, such as 'start_date' and 'end_date.' However, it is possible to find information about the company the officer works at, as well as the name and position of the officer.

In this case, our search returned two officers, both named 'MICHAEL BLOOMBERG,' and one of which is the 'chief executive officer' of 'MARLBOROUGH Associates, Inc.' and the other of which is the 'chief executive officer' of 'BLOOMBERG ASIA INC.' This is enough to tell us that the second one is the Michael Bloomberg that we all know.
