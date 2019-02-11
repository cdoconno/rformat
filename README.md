# rformat
Set and row based result filter and formatter

## Overview
rformat is a nested list proccessor that helps manage:
  * multiple sets or lists
  * ordered output
  * column functions
  * default values
  
Based on a config, it reformats and returns data in a new structure. rformat can be used as a runtime formatter, with a config being supplied at time of call, or it can be preconfigured, passing along new result sets to the configured rformat object. rformat can be incorporated into a stream processor for pipelining.  
 
## Example
rformat excels when you have a standard query result format or a denormalized row, but different consumers require custom views. This turns the formatting into a config based operation instead of an explicit release to the underlying data server. 

Consider the following data structure you might receive when requesting a report with multiple sections:
```
report = [
  [
    { "_id": 123, "first": "Jane", "middle": None, "last": "Smith"}
  ],
  [
    { "_id": 201, "account_no": "2984039756", "acct_type": "Checking", "name": "Checking", "branch_id": "1024309",  "branch_name": "Chase North Clybourn",  "address": "2790 N Clybourn Ave", "balance": 4280.80, "open_date": "20060512T00:00:00Z" },
    { "_id": 202, "account_no": "4528929834", "acct_type": "Savings", "name": "Rainy Day",  "branch_id": "3490002", "branch_name": "Chase Lakeview", "address": "3215 N Lincoln", "balance": 23802.27, "opened_on": "20030305T00:00:00Z"}
  ],
  [
    { "_id": 10980, "account_no": "2984039756", "acct_type": "Checking", "name": "Checking", "branch_id": "1024309",  "branch_name": "Chase North Clybourn",  "address": "2790 N Clybourn Ave", "debit_credit": "debit", "amt": 430.30 },
    { "_id": 10981, "account_no": "4528929834", "acct_type": "Savings", "name": "Rainy Day Fund",  "branch_id": "3490002", "branch_name": "Chase Lakeview", "address": "3215 N Lincoln", "debit_credit": "credit", "amt": 1250.00 },
    { "_id": 10982, "account_no": "2984039756", "acct_type": "Checking", "name": "Checking", "branch_id": "1024309",  "branch_name": "Chase North Clybourn",  "address": "2790 N Clybourn Ave", "debit_credit": "debit", "amt": 102.12 },
    { "_id": 10984, "account_no": "2984039756", "acct_type": "Checking", "name": "Checking", "branch_id": "1024309",  "branch_name": "Chase North Clybourn",  "address": "2790 N Clybourn Ave", "debit_credit": "debit", "amt": 17.65 }
  ]
]
```
Using the rformat config below, we show only the fields we care about, and reorder compared to our config
```
set0:
    0: 
        col: first
        alias: first_name
    1:
        col: last
        alias: last_name
set1:
    0:
        col: acct_type
        alias: type
        format: 
            - type: string
              func: upper
            - type: string
              func: format
              tmpl: "{0} Account"
    1:
        col: account
        alias: name 
    2:
        col: account_number
        alias: account_no 
    3:  
        col: opened_on
        alias: opened
        formats:
            - type: date
              from: "%Y%m%dT%H%M%SZ" 
              to: "%Y-%m-%d"
set3:
    0:
        col: _id
        alias: transaction_id
    1:
        col: account_no
        alias: account_number
    2:
        col: debit_credit
        format:
           - type: mapping
             maps: 
                from: "credit", to: "CREDIT (+)"
                from: "debit", to: "DEBIT  (-)"
    3:  
         alias: amount
         col: amt 
```
And then data is returned in the following structure, which can be passed directly to whatever is responsible for writing the data. 
```
[
  [
    { "first_name": "Jane", "last_name": "Smith"}
  ],
  [ 
    { type": "CHECKING Account", "account": "Checking", "account_number": "2984039756", "opened": "2006-05-12"},
    { type": "SAVINGS Account", "account": "Rainy Day", "account_number": "4528929834", "opened": "2003-03-05"}
  ],
  [
    { "transaction_id": 10980, "account_number": "2984039756", "debit_credit": "DEBIT  (-)", "amount": 430.30 },
    { "transaction_id": 10981, "account_number": "4528929834", "debit_credit": "CREDIT (+)", "amount": 1250.00 },
    { "transaction_id": 10982, "account_number": "2984039756", "debit_credit": "DEBIT  (-)", "amount": 102.12 },
    { "transaction_id": 10984, "account_number": "2984039756", "debit_credit": "DEBIT  (-)", "amount": 17.65 }
  ]
]
```
The ordermap config uses integer and float keys for ordering.

