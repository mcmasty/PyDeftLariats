



### **🧠 What PyDeftLariats Does**

- **Abstracts PyHamcrest matchers into field-based matchers**, allowing structured matching against dictionary-style data records (e.g., rows in a dataset or events in a stream).
- **Provides reusable, composable matchers** for specific field keys and types: text, numbers, existence, dictionaries, etc.
- **Enables rule-style matching logic** to be implemented declaratively and extensibly.
* * *



### Example Usage

Extract specific records from the Coingecko API using PyDeftLariats.



- assuming you have jq installed

- One Record form the Coingecko API
```
{
  "name": "Mogo Inc.",
  "symbol": "NASDAQ:MOGO",
  "country": "CA",
  "total_holdings": 18,
  "total_entry_value_usd": 595494,
  "total_current_value_usd": 391423,
  "percentage_of_total_supply": 0
}
```


- Use jq to extract the record from the Coingecko API and stream to deft
- `deft` is the command line tool for PyDeftLariats

**Goal**: return all records that match any of the following criteria:
- `symbol` is `OTCMKTS:FRMO`
- `total_holdings` is greater than or equal to `1000`
- `percentage_of_total_supply` is greater than or equal to `0.1`

how that gets created in code... the Python code for `example-coingecko` fuction is:

```python
    ...
    field_key = 'symbol'
    filter_one = EqualTo(field_key)
    target_value = 'OTCMKTS:FRMO'

    filter_two = NumberComparer('total_holdings', MatcherType.GREATER_THAN_EQUAL_TO)
    filter_three = NumberComparer('percentage_of_total_supply', MatcherType.GREATER_THAN_EQUAL_TO)
    for x in data:
        if any([filter_one.is_match(target_value, x),
                filter_two.is_match(1000, x),
                filter_three.is_match(0.1, x),
                ]):
            click.echo(f"Data Filter hit for record:\n{x}\n\n")
```

Running from the command line:


``` 
curl 'https://api.coingecko.com/api/v3/companies/public_treasury/bitcoin' |  jq '.companies[]' | deft example-coingecko
```



Comparers:    
- EqualTo  
- TextComparer  
- NumberComparer  
- Exists  
- Anything  
- Nothing  


---

# Random Stuff  

### Additional Documentation

I am playing with MyST for documentation

Thus, visit [https://pydeftlariats.readthedocs.io/](https://pydeftlariats.readthedocs.io/) for more information.
