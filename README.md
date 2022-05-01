# dreamcandies-extraction-tool

## Table of contents 

- General info
- Setup
- Development process

## General info
The input of the tool is the customer sample input file and the expected output from the tool is three smaller files 
containing extracted customer data from the full extraction files.

## Setup
Run this project by using python3 command:

`python3 extract_data.py` 

The input files needs to be placed in the following path:

`dreamcandies-extraction-tool/input` 

The input directory contains the customer sample `CUSTOMER_SAMPLE` and the three full extraction files `CUSTOMER.CSV, INVOICE.CSV, INVOICE_ITEM.CSV` 

Three smaller files `customer.csv, invoice.csv, invoice_item.csv` will be produced in the output directory:

`dreamcandies-extraction-tool/output` 

## Development process

Since OOP was required for the developed tool 7 classes was created. 

### Intuitive classes: Customer, Invoice, Item
Three of these are intuitive classes that represent the three entities provided, the Customer, the Invoice and the Item.
Each intuitive class corresponds to a table in the database from which the files are derived.
Our tool uses these classes for writing in the output files by creating objects in order to:
- to support the respective data types for each field 
- to obtain reusability 

### Abstract classes: Table, CustomerTable, InvoiceTable, ItemTable
The main functions of the developed service are reading, filtering and writing in files.
A generic object type was created in order to support repetitive processes by taking advantage of the OOP as well.
A master Table class is used to cover the "write" method, which is the same for all files.
Three subclasses that inherit the Table class are used for "read" and "filter" methods.
The CustomerTable class includes an init method that reads a file and filters that file with the customers sample provided.
Similarly, the InvoiceTable class includes an init method that reads a file and filters that file with the customers sample provided.
And finally the ItemsTable class includes an init method that reads a file and filters that file with the invoice sample extracted in the previous step.

### Sets 
Set data structure was selected in order to obtain performance.
In python, set is the most suitable data structure for searching, as it uses a hashtable as its underlying data structure.
List data structure was also used for testing purposes. The execution time when creating a list from the 1000 record input file was 18.5 seconds as opposed to using a set for which the corresponding execution time was 0.74 seconds