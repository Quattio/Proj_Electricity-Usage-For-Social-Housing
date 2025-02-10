import argparse

def parse_mysql_args():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('--extractVariables', nargs='+', help='The variables you want to extract from the data    base, used in "SELECT".')
    parser.add_argument('--table', help='The table you want to extract variables.', default='cic_stats')
    parser.add_argument('--installationId', help='Clientid is cic-UUID', default=None)

    parser.add_argument('--query', help='Another option to extract data, directly from written query', default=None)

    return parser





