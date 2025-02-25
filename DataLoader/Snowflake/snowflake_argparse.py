import argparse

def parse_snowflake_args():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('--extractVariables', nargs='+', help='The variables you want to extract from the database, used in "SELECT".')
    parser.add_argument('--table', help='The table you want to extract variables.', default='FIREHOSE_CIC.CIC_STATS.RAW_CIC_STATS_BASE64_1')
    parser.add_argument('--clientid', help='Clientid is cic-UUID', default=None)
    parser.add_argument('--startTime', help='The start of time period for the data taking.', default=None)
    parser.add_argument('--endTime', help='The end of time period for the data taking.', default=None)

    parser.add_argument('--query', help='Another option to extract data, directly from written query', default=None)

    return parser





