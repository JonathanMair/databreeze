# Databreeze

Databreeze is a python package that provides utilities to simplify common data science operations.

Currently contains the following functions, more planned soon!

## databreeze.dictionary_utils.drill_down()

Iterates through a list of (possibly nested) dictionaries attempting to drill down to find a value using a list of hierarchical dictionary keys. Returns a list containing the values found, or, where any key in the chain is missing, a supplied default (defaults to `None`). Also works with a single dictionary, in which case it returns a single value.

### Parameters

- data: dictionary or list of dictionaries in which the values are to be found
- keys_: list of hierarchically ordered keys that will be used to drill down to the desired value
- value_if_none: value to append to the list returned representing missing values, defaults to `None`

### Returns
 
- value or a list of values representing the result from each dictionary supplied in `data`


### Usage

Consider the following nested dictionaries: these have two levels, but could be any level of nesting:

```
d = {"name": "Tony", "contact": {"phone": 878787878, "city": "Madrid"}}
e = {"name": "Marta", "contact": {"city": "Madrid"}}
```

Pass the possibly nested dictionary and the list of keys to the function and it will drill down:

```
from databreeze.dictionary_utils import drill_down

drill_down(d, ["contact", "phone"])
```
```
878787878
```

```
drill_down(d, ["name"])
```
```
'Tony'
```

### Rationale

An important part of data science workflows is extracting information from the nested formats often provided by database APIs into two-dimensional formats so that it can be used with tools such as [numpy](https://github.com/numpy/numpy) and [pandas](https://github.com/pandas-dev/pandas). 

Such data is commonly provided in a text format such as json, which is easily converted into a composite of python lists and dictionaries. 

If it reaches a point in the chain of keys where the key doesn't exist, the error is caught and
`None`is returned

```
drill_down(e, ["contact", "phone"]) is None
```
```
True
```

Pass a list of dictionaries, get a list of values or `value_if_none` if the Key is missing:

```
drill_down([d, e], ["contact", "phone"], value_if_none="Missing Data")
```
```
[878787878, 'Missing Data']
```



However, public APIs often provide data in an irregular format, in the sense that each row can have different fields. This information is often provided in json format that is easily transformed into a python dictionary.  

Consider a very simple example of a list of data items. 

```
people_data = [
    {"name": "Mandu", "job": "Dev"}, 
    {"name": "Jin", "phone": "0798709896"}
]
```

If we know that we want to extract the "name" field, that can be done in a straightforward way, since the field is present for every record: 

```
names = [record["name"] for record in people_data]
print(names)
```


```
['Mandu', 'Jin']
```



However, if we try this for a field that is not present for every record, like this: 


```
names = [record["job"] for record in people_data]
```
Then when the list comprehension comes tries to get ["job"] for the second record, a `KeyError` is thrown. 

```
----> 1 jobs = [record["job"] for record in people_data]
      2 jobs

KeyError: 'job'
```

To avoid this, it is necessary to check each record to ensure the field is present. 

``` 
jobs = [record["job"] if "job" in record.keys() else None for record in people_data]
```

``` 
['Dev', None]
``` 

This is only slightly inconvenient but it quickly becomes more complex when the data involves nested dictionaries with inconsistent fields. To take a very simple example: 

``` 
people_data = [
    {"name": "Eric", "contact": {"address": "29, Acacia Road"}},
    {"name": "Mary"},
    {"name": "Salva", "contact": {"email": "salva@slv.com"}}
]
``` 
In this case it is necessary to check that each level exists. One way of doing this would be: 

``` 
contacts = [
    record["contact"] if "contact" in record.keys() else None for record in people_data
]

addresses = [
    None if contact is None 
    else contact["address"] if "address" in contact.keys() 
    else None 
    for contact in contacts
]

emails = [
    None if contact is None else contact["email"] if "email" in contact.keys() 
    else None 
    for contact in contacts
]
``` 
which yields: 
``` 
addresses: ['29, Acacia Road', None, None]
emails: [None, None, 'salva@slv.com']
``` 
Clearly, when parsing typical complex data structures, checking for missing fields in deeply nested dictionaries quickly becomes very cumbersome.  

Using drill_down(), the same can be achieved using much less code:

``` 
addresses = drill_down(people_data, ["contact", "address"])
emails = drill_down(people_data, ["contact", "email"])
``` 



