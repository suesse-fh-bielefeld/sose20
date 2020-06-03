#!/usr/bin/env python
# coding: utf-8

"""
Modul zur Erzeugung zufälligen Inhaltes
Schnittstellen:
n - Anzahl der einzufügenden Elemente
fillCustomerTable(n,my_db)
fillConfigAndOrderTable(n,my_db)
"""

# ### Imports
from db_communication import db_communication
import pandas as pd
import numpy as np
import time 
import datetime

# ### Funktionen zur Ermittlung zufälliger Attribute

import random
def randomElementInList(values):
    """
    Auswahl eines zufälligen Elements aus dem Wertebereich values
    Bsp.: ['Basic','Holland','BMX','Klassisch','Einrad'] ->  return = 'BMX'
    """
    return random.choice(values)

def randomNumber(start,stop=None,step=1):
    """
    Generierung einer zufälligen Zahl nach random.randrange():
    Choose a random item from range(start, stop[, step])
    """
    if start != stop:
        return random.randrange(start=start,stop=stop,step=step)
    else:
        return start

def randomDate(start, end=datetime.datetime.now().strftime("%d.%m.%Y"), format="%d.%m.%Y", prop=random.random()):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))

def randomName():
    preNames = ["Tana","Francoise","Emmie","Stuart","Cedrick","Tiffani","Kym","Woodrow","Jolene","Autumn","Moriah","Claud","Antoinette",
                "Gisele","Chrissy","Ellena","Hilton","Susanne","Lindy","Nakesha","Rebecca","Lavenia","Donya","Claudia","Dreama","Alla",
                "Freeman","Weston","Jacki","Helene"]
    lastName = ["Allinder","Longley","Dobyns","Coldiron","Justin","Munroe","Boll","Clingerman","Pries","Santangelo","Miller","Bohman","Meachum",
                "Kamer","Waits","Polin","Suitt","Saulter","Pelt","Dapolito","Guild","Beeks","Hollingshead","Schissler","Cardamone","Sypher",
                "Fannin","Belizaire","Burleigh","Eslinger"]
    return randomElementInList(preNames), randomElementInList(lastName)

def randomMail(preName,lastName):
    providers = ['gmail.com','web.de','telekom.de','apple.com','fh-bielefeld.de']
    mail = "{0}.{1}@{2}".format(preName.lower(),lastName.lower(),randomElementInList(providers).lower())
    return mail

def randomBike(my_db,featureTableName='Merkmale',featureClusterTableName='Merkmalcluster'):
    """
    Generierung eines zufälligen Fahrrad auf Basis der Inhalte aus den Tabellen:
    - featureCluster (Bestandteile eines Fahrrads: Rahmen, Gabel, etc.)
    - feature        (Wie diese Bestandteile umgesetzt werden: Trofeo 5, Carbon Öldruckstoßdämpfer, etc.)
    Und Bestimmung des Gesamtpreises anhand gewählter Merkmale
    """
    # get information about the parts to build a bike from DB
    df_features = my_db.get_table(featureTableName)
    df_featureCluster = my_db.get_table(featureClusterTableName)
    df_featureCluster.set_index('ClusterNr',inplace=True)
    
    # merge both dfs
    arrays = [df_features['Merkmalcluster'].replace(df_featureCluster.to_dict()['Merkmalsbezeichnung']).values, 
              df_features['MerkmalNr'].values]
    tuples = list(zip(*arrays))
    index = pd.MultiIndex.from_tuples(tuples, names=['Merkmalcluster', 'MerkmalNr'])
    df = df_features.set_index(index)
    
    # build bike
    bike = []
    bikePrice = 0
    for cluster in df['Merkmalcluster'].unique():
        # get set of Merkmale
        setMerkmale = df.query("Merkmalcluster == " + str(cluster))['MerkmalNr'].values    
        # select random bike part
        bikePart = randomElementInList(setMerkmale)
        # get price of this part
        pricePart = df.swaplevel().fillna(0).loc[int(bikePart)]['Preis'].astype(float).iloc[0]
        # sum it up to get the total bike price
        bikePrice += pricePart
        bike.append(bikePart)
    return bike, bikePrice

# ## Fill data

# ### Kundendaten
# Im ersten Schritt ist es erforderliche einen Kundendatenstamm anzulegen, welcher unabhängig befüllt werden kann und auf den weitere Bestellungen bzw. Konfigurationen zugreifen können.

def fillCustomerTable(n,my_db,columnNamesDB=['Name','Vorname','Mail'],includeID=False):
    """
    Hinzufügen von zufällig generierten Einträgen in der DB-Tabelle 'Kunde'
    
    n - Anzahl der Einträge die hinzugefügt werden sollen
    my_db - Instanz der Klasse db_communication mit aktiver Verbindung
    columnNamesDB - Spaltennamen der Kunden-Tabelle in der DB (mit Ausnahme der KundenNr; Reihenfolge beachten!) 
    includeID - Ob KundenNr seperat mit angelegt werden soll
    
    Es werden die Inhalte nach den defaults in den Parametern erzeugt!
    Das Ändern der Reihenfolge der Spalten und die Hinzunahme weiterer Spalten muss im Quellcode angepasst werden!
    """
    if type(my_db) != db_communication: raise ValueError("my_db ist nicht vom Typ db_communication")
    # Kundentabelle füllen
    table_name = 'Kunde'
    customerId = 'KundenNr'
    if includeID:
        customer_keys = np.concatenate(([customerId],columnNamesDB)) 
    else:
        customer_keys = columnNamesDB
    for i in range(n):
        customer_name = randomName()
        customer_values = i+1, customer_name[0], customer_name[1], randomMail(*customer_name)
        if includeID:
            customer_dict = dict(zip(customer_keys,customer_values))
        else:
            customer_dict = dict(zip(customer_keys,customer_values[1:]))
        my_db.insert_data(table_name,customer_dict)

# ### Konfiguraton
# Im zweiten Schritt werden zufällige Konfigurationen von Fahrrädern erstellt, die einer Auftragsnummer hinzugefügt werden und dessen Gesamtpreis berechnet wird. Erst werden die Daten aufgrund der gegenseitigen Abhängigkeit bestimmt und anschließend wird die DB hiermit befüllt.

def generateConfigurationData(n,my_db,columnNamesDB=['AuftragNr','MerkmalNr'],
                              tableName_Order='Auftrag',tableName_Config='Konfiguration',
                              configId_name = 'KonfigNr',includeID=True):
    """
    Aufgrund der Abhängigkeiten der Tabellen 'Auftrag' und 'Konfiguration' mit den Spalten 'Gesamtpreis' <-> 'AuftragNr', 
    wird in dieser Funktion der Output für die Konfiguration inkl. Informationen für den Auftragfür ein späteres Einfügen 
    in die DB erzeugt.
    
    n - Anzahl der Einträge die hinzugefügt werden sollen
    columnNamesDB - Spaltennamen der Kunden-Tabelle in der DB (mit Ausnahme der KundenNr; Reihenfolge beachten!) 
    tableName_Order - Name der Tabelle für die Aufträge
    tableName_Config - Name der Tabelle für die Konfiguration
    configId_name - Name des PrimaryKeys der Konfiguration-Tabelle
    includeID - Ob KonfigNr seperat mit angelegt werden soll
    """
    # create keys
    if includeID:
        config_keys = np.concatenate(([configId_name],columnNamesDB)) 
    else:
        config_keys = columnNamesDB

    # get old entries in order to appending new ones
    df_before = my_db.get_table(tableName_Order)
    if df_before is None:
        start = 1
    else:
        start = df_before.iloc[:,0].max() + 1 #max orderId + 1
    n += start

    order = []
    config_dict = []
    # iterate through all orders that should be created
    for orderId in range(start,n):
        # build random bike
        bike,bikePrice = randomBike(my_db)
        # keep orderId and bikePrice for later order fillings
        order.append(dict(zip(('orderId','bikePrice'),(orderId,bikePrice))))
        # iterate through each bike part
        for partId, featureId in enumerate(bike):
            # generate values
            config_values = orderId*100+partId, orderId, featureId
            # keep the config_dict for later inserts 
            if includeID:
                config_dict.append(dict(zip(config_keys,config_values)))
            else:
                config_dict.append(dict(zip(config_keys,config_values[1:])))
    # to data frame          
    df_order = pd.DataFrame(order)
    return config_dict, df_order 

def generateOrderData(df_order,my_db,columnNamesDB=['Bestelldatum','Lieferdatum','KundenNr'],
                      table_name='Auftrag',orderId_name='AuftrNr', includeID=True, 
                      customerTableName='Kunde',customerId='KundenNr',startDate='2020-01-01'):
    """
    Erstellen von zufälligen Auftragsinhalten in Abhängigkeit zuvor erstellter Konfigurationen
    
    df_order - DataFrames welches von dem Konfigurator zur Anlegung eines Auftrags und zur Bestimmung des Gesamtpreises verwendet wird
    columnNamesDB - Spaltennamen der Auftrag-Tabelle in der DB (mit Ausnahme der AuftrNr; Reihenfolge beachten!) 
    table_name - Name der Tabelle für die Aufträge
    configId_name - Name des PrimaryKeys der Auftrag-Tabelle
    includeID - Ob AuftrNr seperat mit angelegt werden soll
    customerTableName - Name der DB-Tabelle 'Kunde'
    customerId - Name der Identifikationsnummer in customerTable
    startDate - Startdatum zur zufälligen Erzeugung
    
    Es werden die Inhalte nach den defaults in den Parametern erzeugt!
    Das Ändern der Reihenfolge der Spalten und die Hinzunahme weiterer Spalten muss im Quellcode angepasst werden!
    """
    # Read relevant range of values for existing customers
    df_customers = my_db.get_table(customerTableName)
    
    # create keys
    if includeID:
        order_keys = np.concatenate(([orderId_name],columnNamesDB)) 
    else:
        order_keys = columnNamesDB
        
    # create values and fill order_dict_lst
    order_dict = []
    for _,order in df_order.iterrows():
        orderId = order[0].astype(int)
        #orderPrice = order[1].astype(float)
        
        rand_orderDate = randomDate(start=startDate,
                                    end=datetime.datetime.now().strftime("%Y-%m-%d"),
                                    format="%Y-%m-%d",
                                    prop=random.random())
        rand_delivDate = datetime.datetime.strftime(datetime.datetime.strptime(rand_orderDate,"%Y-%m-%d") 
                                                    + datetime.timedelta(days=14),"%Y-%m-%d")
        rand_customerId = randomNumber(start=df_customers[customerId].astype(int).min(),
                                        stop=df_customers[customerId].astype(int).max())
        order_values = orderId, rand_orderDate, rand_delivDate, rand_customerId
        #order_values = orderId, rand_orderDate, rand_delivDate, rand_customerId, orderPrice
        if includeID:
            order_dict.append(dict(zip(order_keys,order_values)))
        else:
            order_dict.append(dict(zip(order_keys,order_values[1:])))
    return order_dict

def fillConfigAndOrderTable(n,my_db,tableName_Order='Auftrag',tableName_Config='Konfiguration'):
    """
    Tatsächliches Befüllen der beiden Tabellen 'Auftrag' und 'Konfiguration'
    Entspricht der Simulation eines (oder mehreren) Kunden, die sich ein Fahrrad in einem Online-Konfigurator zusammenstellen 
    lassen und bestellen, wodurch ein Auftrag angelegt wird 
    
    n - Anzahl der zu erstellenden Aufträge inkl. Konfigurationen
    my_db - Instanz der Klasse db_communication mit aktiver Verbindung
    """
    if type(my_db) != db_communication: raise ValueError("my_db ist nicht vom Typ db_communication")
    config_dict, df_order = generateConfigurationData(n,my_db)
    order_dict = generateOrderData(df_order,my_db)
    for order_dict_part in order_dict:
        my_db.insert_data(tableName_Order,order_dict_part)
    for config_dict_part in config_dict:
        my_db.insert_data(tableName_Config,config_dict_part)
