import csv
import datetime


class Customer:

    def __init__(self, code, firstname, lastname):
        self.code = code
        self.firstname = firstname
        self.lastname = lastname

    def __iter__(self):
        return iter([self.code, self.firstname, self.lastname])


class Invoice:

    def __init__(self, customer, code, amount, date):
        self.customer = customer
        self.code = code
        self.amount = float(amount)
        self.date = datetime.datetime.strptime(date, '%d-%b-%Y')

    def __iter__(self):
        return iter([self.customer, self.code, self.amount,
                     datetime.datetime.strftime(self.date, '%d-%b-%Y')])


class Item:

    def __init__(self, invoice, code, amount, quantity):
        self.invoice = invoice
        self.code = code
        self.amount = float(amount)
        self.quantity = int(quantity)

    def __iter__(self):
        return iter([self.invoice, self.code, self.amount, self.quantity])


class Table:
    """Some description that tells you it's abstract,
    often listing the methods you're expected to supply."""

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
    """Some description that tells you it's abstract,
    often listing the methods you're expected to supply."""

    def __init__(self, filename, customer_sample):
        with open(filename, 'r') as csv_file:
            reader = csv.reader(csv_file, quotechar='"', delimiter=',',
                                quoting=csv.QUOTE_ALL, skipinitialspace=True)
            self.header = next(reader)
            self.items = set()
            for code, firstname, lastname in reader:
                # print(code, firstname, lastname)
                if code in customer_sample:
                    # print(code)
                    self.items.add(Customer(code, firstname, lastname))
            csv_file.close()


class InvoiceTable(Table):
    """Some description that tells you it's abstract,
    often listing the methods you're expected to supply."""

    def __init__(self, filename, customer_sample):
        with open(filename, 'r') as csv_file:
            reader = csv.reader(csv_file, quotechar='"', delimiter=',',
                                quoting=csv.QUOTE_ALL, skipinitialspace=True)
            self.header = next(reader)
            self.items = set()
            self.codes = set()
            for customer, code, amount, date in reader:
                if customer in customer_sample:
                    # print("customer", code)
                    self.items.add(Invoice(customer, code, amount, date))
                    self.codes.add(code)
            csv_file.close()


class ItemTable(Table):
    """Some description that tells you it's abstract,
    often listing the methods you're expected to supply."""

    def __init__(self, filename, invoice_sample):
        with open(filename, 'r') as csv_file:
            reader = csv.reader(csv_file, quotechar='"', delimiter=',',
                                quoting=csv.QUOTE_ALL, skipinitialspace=True)
            self.header = next(reader)
            self.items = set()
            for invoice, code, amount, quantity in reader:
                # print(invoice, code)
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
