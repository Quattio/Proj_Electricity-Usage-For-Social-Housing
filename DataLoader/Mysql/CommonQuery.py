import pandas as pd


def exampleQuery(cursor):
    cursor.execute("SELECT * FROM cic;") # [9625 rows x 9 columns], Runing Time: 1.3 s


def listDataBases(cursor):
    # DataBases: 'information_schema', 'mysql', 'performance_schema', 'quatt_production', 'sys' 
    cursor.execute("SHOW DATABASES")
    print("SHOW DATABASES:")
    for x in cursor:
        print(x)
    print("\n")


def listTables(cursor):
    # 18 Tables in 'quatt_production': 
    # '_prisma_migrations','cic','cicCommissioning','cicRegistration','cicState',
    # 'energyConsumption','heatPump','heatPumpCommissioning','installation',
    # 'installationNote','installationTariff','installer','settingsUpdate','user',
    # 'userCic','userCicPairRequest','userClient','zipCodesWithEarlyNightPricing',

    ## cic Table: 9625 rows x 9 columns (Update on 16.07.2024)
    # 9 columns: ['id', 'createdAt', 'updatedAt', 'availableWifiNetworks', 'isScanningForWifi', 'lastScannedForWifi', 'wifiConnectionStatus', 'installationId', 'menderId']
    # "id": CIC id. Distinct count: 9625
    # "createdAt": record created date time 
    # "updatedAt": record updated date time
    # "availableWifiNetworks": show all the available Wifi Networks for this CIC id device.
    # "isScanningForWifi": Bool
    # "lastScannedForWifi": last date time for scanning the WIFI
    # "wifiConnectionStatus": A str variable, "connected" or "disconnected"
    # "installationId": continuous 1-8352, then 10041-48326 with many gaps. Distinct count: 9574   
    # "menderId": Most are "None", 19 out of 9625 have menderId. A example, CIC id:CIC-1106aaaa-a7ca-54cb-8da4-16eca3794e68, menderId:4d38b6fb-5663-4eff-982a-ef0472640180, installationId:4049 

    ## energyConsumption Table: 47484777 rows x 10 columns (Update on 16.07.2024)
    # 10 columns: ['id', 'installationId', 'hpElectric', 'hpHeat', 'boilerHeat', 'timestamp', 'roomSetpoint', 'roomTemperature', 'temperatureOutside', 'waterTemperature']
    # 'id': Distinct count: 47484777 
    # 'installationId': Distinct count:7954
    # 'hpElectric':  Distinct count:4304303  
    # 'hpHeat':
    # 'boilerHeat':
    # 'timestamp': datetime format: year-month-day hour:minutes:second
    # 'roomSetpoint':
    # 'roomTemperature':
    # 'temperatureOutside':
    # 'waterTemperature':

    cursor.execute("SHOW TABLES")
    print("SHOW TABLES:")
    for x in cursor:
        print(x)
    print("\n")


