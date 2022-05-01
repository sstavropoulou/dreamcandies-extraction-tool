import csv
import datetime


class Customer:
    """ Represents a customer.
    Includes an init function that describes
    the fields required to identify a customer.
    Includes an  iter method  for creating objects
    which can be iterated one element at a time.
    The csv.writer will iterate through a Customer object
    to get the cells in a row, thus trigger the __iter__ method"""

    def __init__(self, code, firstname, lastname):
        self.code = code
        self.firstname = firstname
        self.lastname = lastname

    def __iter__(self):
        return iter([self.code, self.firstname, self.lastname])


class Invoice:
    """ Represents an invoice.
    Includes an init function that describes
    the fields required to identify an invoice.
    Includes an  iter method  for creating objects
    which can be iterated one element at a time.
    The csv.writer will iterate through an Invoice object
    to get the cells in a row, thus trigger the __iter__ method"""

    def __init__(self, customer, code, amount, date):
        self.customer = customer
        self.code = code
        self.amount = float(amount)
        self.date = datetime.datetime.strptime(date, '%d-%b-%Y')

    def __iter__(self):
        return iter([self.customer, self.code, self.amount,
                     datetime.datetime.strftime(self.date, '%d-%b-%Y')])


class Item:
    """ Represents an invoice item.
       Includes an init function that describes
       the fields required to identify an invoice item.
       Includes an  iter method  for creating objects
       which can be iterated one element at a time.
       The csv.writer will iterate through an Item object
       to get the cells in a row, thus trigger the __iter__ method"""

    def __init__(self, invoice, code, amount, quantity):
        self.invoice = invoice
        self.code = code
        self.amount = float(amount)
        self.quantity = int(quantity)

    def __iter__(self):
        return iter([self.invoice, self.code, self.amount, self.quantity])


class Table:
    """Abstract class that represents a generic table.
    Includes the write_csv method that takes a filename as input
    and writes the respective rows to that file"""

    def __init__(self, filename):
        raise NotImplementedError("Should have implemented this")

    def write_csv(self, filename):
        with open(filename, "w") as stream:
            writer = csv.writer(stream, delimiter=',', quoting=csv.QUOTE_ALL)
            writer.writerow(self.header)
            writer.writerows(self.items)
            stream.close()

    def print(self):
        print(self.header, self.items)


class CustomerTable(Table):
    """ Subclass that inherits from class Table.
    Represents a CustomerTable.
    Reads from a Customer file and filters it with the customer sample."""

    def __init__(self, filename, customer_sample):
        with open(filename, 'r') as csv_file:
            reader = csv.reader(csv_file, quotechar='"', delimiter=',',
                                quoting=csv.QUOTE_ALL, skipinitialspace=True)
            self.header = next(reader)
            self.items = set()
            for code, firstname, lastname in reader:
                if code in customer_sample:
                    self.items.add(Customer(code, firstname, lastname))
            csv_file.close()


class InvoiceTable(Table):
    """ Subclass that inherits from class Table.
    Represents an InvoiceTable.
    Reads from an Invoice file and filters it with the customer sample.
    Returns an invoice code set with the filtered invoice codes"""

    def __init__(self, filename, customer_sample):
        with open(filename, 'r') as csv_file:
            reader = csv.reader(csv_file, quotechar='"', delimiter=',',
                                quoting=csv.QUOTE_ALL, skipinitialspace=True)
            self.header = next(reader)
            self.items = set()
            self.codes = set()
            for customer, code, amount, date in reader:
                if customer in customer_sample:
                    self.items.add(Invoice(customer, code, amount, date))
                    self.codes.add(code)
            csv_file.close()


class ItemTable(Table):
    """Subclass that inherits from class Table.
    Represents an ItemTable.
    Reads from an Item file and filters it with the invoice code sample returned by InvoiceTable object."""

    def __init__(self, filename, invoice_sample):
        with open(filename, 'r') as csv_file:
            reader = csv.reader(csv_file, quotechar='"', delimiter=',',
                                quoting=csv.QUOTE_ALL, skipinitialspace=True)
            self.header = next(reader)
            self.items = set()
            for invoice, code, amount, quantity in reader:
                if invoice in invoice_sample:
                    self.items.add(Item(invoice, code, amount, quantity))
            csv_file.close()


def main():
    customer_sample = set()
    with open("input/CUSTOMER_SAMPLE.CSV", newline='') as csv_file:
        reader = csv.reader(csv_file, quotechar='"', delimiter=',',
                            quoting=csv.QUOTE_ALL, skipinitialspace=True)
        next(reader, None)  # Skip the header.
        for row in reader:
            customer_sample.add(row[0])
    csv_file.close()

    customer_table = CustomerTable('input/CUSTOMER.CSV', customer_sample)
    customer_table.write_csv('output/customer.csv')

    invoice_table = InvoiceTable('input/INVOICE.CSV', customer_sample)
    invoice_table.write_csv("output/invoice.csv")

    item_table = ItemTable('input/INVOICE_ITEM.CSV', invoice_table.codes)
    item_table.write_csv("output/invoice_item.csv")


if __name__ == '__main__':
    main()
