"""Python Starter Template

"""
import io
import re
from datetime import datetime

def new_trxn():
    return {
        'date': '',
        'description': '',
        'items': [],
    }

def parse_line_item(line):
    stripped_line = line.strip()
    splitted_line = stripped_line.split()

    # the account is from the first character until two whitespace characters
    split_at, _  = re.search(r'\s{2}', stripped_line).span()
    account, other = stripped_line[:split_at], stripped_line[split_at:]

    return {
        'account': account,
        'amount': "".join([ch for ch in other if re.match(r'[0-9\-]', ch)]).strip(),
        'currency': "".join([ch for ch in other if not re.match(r'[0-9\-]', ch)]).strip(),
        'type': 'line_item'
    }

def parse_date(date_input):
    try:
        return datetime.strptime(date_input, '%Y/%m/%d').strftime('%Y-%m-%d')
    except ValueError:
        return datetime.strptime(date_input, '%Y-%m-%d').strftime('%Y-%m-%d')


class Parser():
    def __init__(self, ledger):
        if isinstance(ledger, io.TextIOBase):
            self.ledger_str = ledger.read()
        elif isinstance(ledger, str):
            self.ledger_str = ledger

    def parse(self):
        lines = self.ledger_str.split('\n')

        result = []

        current = new_trxn()
        # initial parse, separate into transactions
        for line in lines:
            if len(line) <= 0:
                if len(current['items']) > 0: 
                    # end current transaction
                    result, current = result+[current], new_trxn()
                continue
            
            if re.match(r'\d', line[0]):
                # if start of line is a number, this is the start of a new transaction
                if len(current['items']) > 0:
                    result, current = result+[current], new_trxn()

                splitted = line.split()
                current['date'] = parse_date(splitted[0])
                current['description'] = " ".join(splitted[1:])

            elif re.match(r'\s', line[0]) and line.strip()[0] == ';':
                # is a comment
                current['items'].append({'type': 'comment', 'text': line.strip()[1:].strip()})
            
            elif re.match(r'\s', line[0]):
                # is a line item
                current['items'].append(parse_line_item(line))
        
        if len(current['items']) > 0:
            result, current = result+[current], new_trxn()

        return result

    def __repr__(self):
        return self.ledger_str
