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
rformat excels when you have a standard query result format or a denormalized row, but different consumers require custom changes. This turns the formatting into a config based operation instead of an explicit release to the underlying data server. 

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
         column: { first_name: first }
         format:
    1:
         column: { last_name: last }
         format:
set1:
    0:
         column: { type: acct_type }
         format:
    1:
         column: { account: name }
         format:
    2:
         column: { account_number: account_no }
         format:
    3:  
         column: { opened: opened_on }
         format:
             date: {from: "%Y%m%dT%H%M%SZ" to: "%Y-%m-%d"}
set3:
    0:
         column: { transaction_id: _id }
         format:
    1:
         column: { account_number: account_no }
         format:
    2:
         column: { debit_credit: debit_credit }
         format:
             string-replace: [
                            {from: "credit", to: "CREDIT (+)"},
                            {from: "debit", to: "DEBIT  (-)"}
             ]
    3:  
         column: { amount: amt }
         format:
```
And then data is returned in the following structure, which can be passed directly to whatever is responsible for writing the data. 
```
[
  [
    { "first_name": "Jane", "last_name": "Smith"}
  ],
  [ 
    { type": "Checking", "account": "Checking", "account_number": "2984039756", "opened": "2006-05-12"},
    { type": "Savings", "account": "Rainy Day", "account_number": "4528929834", "opened": "2003-03-05"}
  ],
  [
    { "transaction_id": 10980, "account_number": "2984039756", "debit_credit": "DEBIT  (-)", "amount": 430.30 },
    { "transaction_id": 10981, "account_number": "4528929834", "debit_credit": "CREDIT (+)", "amount": 1250.00 },
    { "transaction_id": 10982, "account_number": "2984039756", "debit_credit": "DEBIT  (-)", "amount": 102.12 },
    { "transaction_id": 10984, "account_number": "2984039756", "debit_credit": "DEBIT  (-)", "amount": 17.65 }
  ]
]
```
