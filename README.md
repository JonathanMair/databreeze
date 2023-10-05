# Databreeze

Databreeze is a python package that provides utilities to simplify common data science operations.

Currently contains the following functions, more planned soon!

## databreeze.dictionary_utils.drill_down()

Data scientists often need each item in a series of data to contain the same fields. This allows for the use of tools such as those provided by pandas and numpy.

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

This is only slightly inconvenient but it quickly becomes more complex when the data involves nested dictionaries with inconsistent fields. 

`drill_down()`

