# playing with myst  


```{warning}  
This library is under development.

```



working my way through this tutorial


https://youtu.be/qRSb299awB0




assuming you have jq installed


``` 
curl 'https://api.coingecko.com/api/v3/companies/public_treasury/bitcoin' |  jq '.companies[]' | deft example-one
```

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


Big comparers:    
- EqualTo  
- TextComparer  
- NumberComparer  
- Exists  
- Anything  
- Nothing  