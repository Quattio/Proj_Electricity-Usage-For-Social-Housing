import argparse
import Mysql as mysql_loader
import Clickhouse as clickhouse_loader
import S3 as S3_loader
import Redis as redis_loader
import Snowflake as snowflake_loader
import time

def main():


    # Parser Argument
    parser = argparse.ArgumentParser(description='QuattDataLoader main parser')
    subparsers = parser.add_subparsers(dest='subpackage', help='Subpackage to use')

    clickhouse_parser = subparsers.add_parser('clickhouse', help='Options for Clickhouse')
    clickhouse_args = clickhouse_loader.clickhouse_argparse.parse_clickhouse_args()
    for action in clickhouse_args._actions:
        clickhouse_parser._add_action(action)

    snowflake_parser = subparsers.add_parser('snowflake', help='Options for Snowflake')
    snowflake_args = snowflake_loader.snowflake_argparse.parse_snowflake_args()
    for action in snowflake_args._actions:
        snowflake_parser._add_action(action)

    mysql_parser = subparsers.add_parser('mysql', help='Options for MySQL')
    mysql_args = mysql_loader.mysql_argparse.parse_mysql_args()
    for action in mysql_args._actions:
        mysql_parser._add_action(action)

    s3_parser = subparsers.add_parser('s3', help='Options for S3')
    s3_args =  S3_loader.boto3_argparse.parse_boto3_args()  
    for action in s3_args._actions:
        s3_parser._add_action(action)

    redis_parser = subparsers.add_parser('redis', help='Options for redis')
    redis_args =  redis_loader.redis_argparse.parse_redis_args()  
    for action in redis_args._actions:
        redis_parser._add_action(action)

    args = parser.parse_args()


    # Load Data
    if args.subpackage == 's3':
        s3_instance = S3_loader.Boto3()
        S3_loader.action_s3(s3_instance, args)
    elif args.subpackage == 'clickhouse':
        extractedData = clickhouse_loader.connect_clickhouse(args)
    elif args.subpackage == 'snowflake':
        extractedData = snowflake_loader.connect_snowflake(args)
    elif args.subpackage == 'mysql':
        extractedData = mysql_loader.connect_mysql(args)
    elif args.subpackage == 'redis':
        extractedData = redis_loader.connect_redis(args)


    # Analysis
    #### Your Analysis Part
    

    # Save
    if args.subpackage in ('clickhouse', 'mysql', 'snowflake'):
        print(extractedData)
        # extractedData.to_csv("Data/extractedData_" + str(args.subpackage) + ".csv", index=False )    
    else:
        print(extractedData)

if __name__ == "__main__":
    time_start=time.time()
    main()
    time_end=time.time()
    print('Running Time: ', (time_end-time_start)/60,'mins')



