
from src.pyledger.parser import Parser

def test_standard_1():
    '''Standard transaction with a comment

    '''

    data = '''2015/05/25 trip to the supermarket
    ; a transaction comment
    expenses:supplies           $10
    assets:checking            $ -10
'''
    my_parser = Parser(data)

    expects = [
        {
            'date': '2015-05-25',
            'description': 'trip to the supermarket',
            'items': [
                {
                    'type': 'comment',
                    'text': 'a transaction comment'
                },
                {
                    'type': 'line_item',
                    'account': 'expenses:supplies',
                    'amount': '10',
                    'currency': '$',
                },
                {
                    'type': 'line_item',
                    'account': 'assets:checking',
                    'amount': '-10',
                    'currency': '$',
                }
            ]
        }
    ]

    assert my_parser.parse() == expects

def test_standard_2():
    '''Standard transaction with some whitespace handling, alternative currency, multi comments

    '''

    data = '''2015/05/25 trip to the supermarket
    ; a transaction comment
    ; another comment
 expenses:supplies & postage           AUD10
    ; yet another comment
 assets:checking            AUD -10
'''
    my_parser = Parser(data)

    expects = [
        {
            'date': '2015-05-25',
            'description': 'trip to the supermarket',
            'items': [
                {
                    'type': 'comment',
                    'text': 'a transaction comment'
                },
                {
                    'type': 'comment',
                    'text': 'another comment'
                },
                {
                    'type': 'line_item',
                    'account': 'expenses:supplies & postage',
                    'amount': '10',
                    'currency': 'AUD',
                },
                {
                    'type': 'comment',
                    'text': 'yet another comment'
                },
                {
                    'type': 'line_item',
                    'account': 'assets:checking',
                    'amount': '-10',
                    'currency': 'AUD',
                }
            ]
        }
    ]

    assert my_parser.parse() == expects

def test_standard_3():
    '''Standard transaction, currency on opposite side

    '''

    data = '''2015/05/25 trip to the supermarket
    expenses:supplies & postage           10 AUD
    assets:checking            -10AUD
'''
    my_parser = Parser(data)

    expects = [
        {
            'date': '2015-05-25',
            'description': 'trip to the supermarket',
            'items': [{
                'type': 'line_item',
                'account': 'expenses:supplies & postage',
                'amount': '10',
                'currency': 'AUD',
            },{
                'type': 'line_item',
                'account': 'assets:checking',
                'amount': '-10',
                'currency': 'AUD',
            }]
        }
    ]

    assert my_parser.parse() == expects



def test_multiple_1():
    '''Multiple Transactions

    '''

    data = '''2015/05/25 trip to the supermarket
    expenses:supplies & postage           AUD10
    assets:checking            AUD -10
2015/05/26 trip to supplier
    expenses:supplies           AUD20
    assets:checking            AUD -20

2015/05/27 trip to supplier 2
    expenses:supplies           AUD20
    assets:checking            AUD -20
'''
    my_parser = Parser(data)

    expects = [
        {
            'date': '2015-05-25',
            'description': 'trip to the supermarket',
            'items': [{
                'type': 'line_item',
                'account': 'expenses:supplies & postage',
                'amount': '10',
                'currency': 'AUD',
            },{
                'type': 'line_item',
                'account': 'assets:checking',
                'amount': '-10',
                'currency': 'AUD',
            }]
        },
        {
            'date': '2015-05-26',
            'description': 'trip to supplier',
            'items': [{
                'type': 'line_item',
                'account': 'expenses:supplies',
                'amount': '20',
                'currency': 'AUD',
            },{
                'type': 'line_item',
                'account': 'assets:checking',
                'amount': '-20',
                'currency': 'AUD',
            }]
        },
        {
            'date': '2015-05-27',
            'description': 'trip to supplier 2',
            'items': [{
                'type': 'line_item',
                'account': 'expenses:supplies',
                'amount': '20',
                'currency': 'AUD',
            },{
                'type': 'line_item',
                'account': 'assets:checking',
                'amount': '-20',
                'currency': 'AUD',
            }]
        }
    ]

    assert my_parser.parse() == expects

