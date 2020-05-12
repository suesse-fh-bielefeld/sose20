import mysql.connector as db
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import numpy as np

class db_communication:
    """
    ____________________________________________________________________________________________
    Benötigte python-Module:
    - mysql
    - mysql-connector
    - pandas
    - numpy
    ____________________________________________________________________________________________
    Bietet eine API zur Kommnunikation mit der Fahrradshop-Datenbank an.
    Auf Basis des mysql-Moduls wird mit eine MariaDB kommuniziert.
    
    Durch print()-Ausgaben wird der Erfolg oder Misserfolg bei einem Funktionsaufruf ausgegeben.
    
    Die Klasse ist die folgt zu nutzen:
    my_db = db_communication()
    -----
    my_db.user_func_xyz(args)
    -----
    my_db.close()
    """
    def __init__(self, config = None):
        """
        Default (config = None) wird die Verbindung zur Standard-Datenbank hergestellt.
        Alternativ kann ein config-dict übergeben werden
        config = {
            'user': '',
            'password': '',
            'host': '',
            'port': '',
            'database': ''
        }
        """
        self.__db = self.connect(config)
        if self.__db:
            self.__cursor = self.__db.cursor(buffered=True)
            print("Successfully connected.")
        else:
            print("... no connection ...")

    def connect(self, config=None) -> db.MySQLConnection:    
        """
        Stellt die Verbindung zur Datenbank her und nutzt die übergeben Parameter config.
        Return: 'db.MySQLConnection'.
        """
        if not config:
            config = {
            'user': 'root',
            'password': 'FDS-apm1',
            'host': 'min-ifm-xdm.ad.fh-bielefeld.de',
            'port': '3306',
            'database': 'FDS-APM'
            }

        try:
            return mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            print("Not connected")
            
    def close(self):
        """ 
        Schließt die Verbindung zur Datenbank.
        """
        if self.__db:
            self.__db.close()
            print("Connection closed")
        else:
            pass
    
    def read_tables(self) -> list:
        """
        Liest die Tabellen der Datenbank aus und gibt diese in Liste-Form zurück.
        """
        if self.__db:
            self.__cursor.execute("SHOW TABLES")

            tables = list()
            for x in self.__cursor:
                tables.append(x)

            return tables
        else:
            pass
        
    def insert_data(self, table_name, data_as_dict):
        """
        Der Tabelle 'table_name' wird eine neue Zeile hinzugefügt. 
        Der Inhalt der Zeile wird aus dem 'data_as_dict' erstellt. 
        Die Spalentennamen sind die 'keys' und die Zellenwerte die 'values' des Dictionaries.
        """
        try:
            sql = "INSERT INTO `" + table_name + "` ("
            values = ""
            for key in data_as_dict:
                sql += "`" + str(key) + "`, "
                if data_as_dict[key]: 
                    values += "'" + str(data_as_dict[key]) + "', "
                else:
                    values += "NULL , "
            sql = sql[:len(sql)-2]
            values = values[:len(values)-2]
            sql += ") VALUES (" + values + ");"
            
            print(sql)
            self.__cursor.execute(sql)
            self.__db.commit()
            return True
        except:
           # Rollback in case there is any error
            self.__db.rollback()
            print("Rollback, something went wrong.")
            return False
    
    def get_table(self, table_name, key = None, column = None) -> pd.DataFrame:
        """
        Die gewünschte Tabelle 'table_name' wird als pd.DataFrame zurückgegeben.
        """
        if key and column:
            pass # was war hier nochmal?
        elif column:
            self.__cursor.execute("SELECT {} FROM `{}`".format(column, table_name))
            rows = []
            for y in self.__cursor:
                rows.append(y)
            return pd.DataFrame(np.array(rows), columns = [column])
        elif key:
            pass # was war hier nochmal?
        else:
            self.__cursor.execute("SHOW COLUMNS FROM `{}`".format(table_name))
            columns = []
            for y in self.__cursor:
                columns.append(y[0])
            self.__cursor.execute("SELECT * FROM `{}`".format(table_name))
            rows = []
            for y in self.__cursor:
                rows.append(y)
            try: 
                df = pd.DataFrame(np.array(rows), columns=columns)
                return df
            except ValueError:
                return None
        
    def drop_table(self, name) -> bool:
        """
        Die Tabelle 'name' wird gelöscht, allerdings nur dann, 
        wenn die Tabelle keine Abhängigkeiten zu anderen Tabellen hat.
        """
        sql = "DROP TABLE %s" %str(name)
        try:
            # Execute the SQL command
            self.__cursor.execute(sql)
            # Commit your changes in the database
            self.__db.commit()
            print("Drop table: ", str(name))
        except:
           # Rollback in case there is any error
            self.__db.rollback()
            print("Rollback, something went wrong.")
            return False
        
        return True

    def show_columns(self, table_name):
        """
        Gibt die Spalten der gewünschten Tabelle aus.
        """
        self.__cursor.execute("SHOW COLUMNS FROM `{}`".format(table_name))
        return [i for i in self.__cursor]
        
    def storno(self, key):
        """
        Datenbank spezifische Funktion.
        Eine existierende Bestellung wird stoniert, identifiziert an dem 'key' == 'Bestellung.id'. 
        Die Spalte "Storniert" wird auf True gesetzt.
        """
        
        sql = "UPDATE `Bestellungen` SET `Storniert`='1' WHERE `Bestellungen.id`= '" + key + "';"

        try:
            # Execute the SQL command
            self.__cursor.execute(sql)
            # Commit your changes in the database
            self.__db.commit()
            print("Update Bestellung:", str(key))
        except:
           # Rollback in case there is any error
            self.__db.rollback()
            print("Rollback, something went wrong.")
            return False
    
    def create_table(self, name, rows) -> bool:
        """
        Erstellt eine Tabelle mit dem Namen 'name' und den Spalten 'rows'.
        'rows'-Elemente müssen im MariaDB-Format die Einstellungen enthalten. 
        Bsp.1: 
        `Bauteil.id` INT NOT NULL AUTO_INCREMENT
        Bsp.2:
        FOREIGN KEY (`Baugruppe`) REFERENCES `Baugruppen`(`Baugruppe`)
        """
        tables = self.read_tables()
        if not any(name in s for s in tables):
            sql = "CREATE TABLE `" + name + "` ("
            for row in rows:     
                if rows.index(row) == (len(rows)-1):
                    sql += " " + row
                else:
                    sql += " " + row + ","
            sql += ")"
            print(sql)
            self.__cursor.execute(sql)
            print("Created table: ", name)
            return True
        else:
            print("Table", name, "already exists.")
            return False
    
    def reset_all_tables(self, are_u_sure = False):
        """
        Funktion um die Tabellen der Datenbank zu löschen und neu und leer wieder zu initialiseren.
        Die Variable 'are_u_sure' muss auf True gesetzt sein, um den Vorgang durchzuführen
        Der Aufbau der Tabellen ist fest niedergeschrieben und hat Abhängigkeiten wie FOREIGN KEY untereinander.
        Es ist auf die richtige Reihenfolge zu achten!
        Deswegen wird das Nutzen dieser Funktion empfohlen.
        """
        config_baugruppen = ["`Baugruppe` VARCHAR(20) NOT NULL",
                             "PRIMARY KEY(`Baugruppe`)"]

        config_bauteile = ["`Bauteile.id` INT NOT NULL AUTO_INCREMENT",
                           "`Baugruppe` VARCHAR(20)",
                           "`Name` VARCHAR(40)",
                           "`Farbe` VARCHAR(20)",
                           "`Preis` FLOAT(20)",
                           "`Lieferzeit` INT",
                           "`Montagezeit` INT",
                           "PRIMARY KEY (`Bauteile.id`)",
                           "FOREIGN KEY (`Baugruppe`) REFERENCES `Baugruppen`(`Baugruppe`)"]

        config_grundmodelle = ["`Grundmodelle.id` INT NOT NULL AUTO_INCREMENT",
                              "`Grundmodell` INT",
                              "`Lenker` INT",
                              "`Rahmen` INT",
                              "`Felgen` INT",
                              "`Sattel` INT",
                              "`Reifen` INT",
                              "`Bremsen` INT",
                              "`Gangschaltung` INT",
                              "`Beleuchtung` INT",
                              "`Preis` float",
                              "`Montagezeit` INT",
                              "`Lieferzeit` INT",
                              "PRIMARY KEY (`Grundmodelle.id`)",
                              "FOREIGN KEY (`Lenker`) REFERENCES `Bauteile`(`Bauteile.id`)",
                              "FOREIGN KEY (`Rahmen`) REFERENCES `Bauteile`(`Bauteile.id`)",
                              "FOREIGN KEY (`Sattel`) REFERENCES `Bauteile`(`Bauteile.id`)",
                              "FOREIGN KEY (`Reifen`) REFERENCES `Bauteile`(`Bauteile.id`)",
                              "FOREIGN KEY (`Bremsen`) REFERENCES `Bauteile`(`Bauteile.id`)",
                              "FOREIGN KEY (`Gangschaltung`) REFERENCES `Bauteile`(`Bauteile.id`)",
                              "FOREIGN KEY (`Beleuchtung`) REFERENCES `Bauteile`(`Bauteile.id`)",
                              "FOREIGN KEY (`Felgen`) REFERENCES `Bauteile`(`Bauteile.id`)"]


        config_bestellungen = ["`Bestellungen.id` int NOT NULL AUTO_INCREMENT",
              "`Lenker` int",
              "`Rahmen` int",
              "`Felgen` int",
              "`Sattel` int",
              "`Reifen` int",
              "`Bremsen` int",
              "`Gangschaltung` int",
              "`Beleuchtung` int",
              "`Name` VARCHAR(40)",
              "`Preis` float",
              "`Montagezeit` INT",
              "`Lieferzeit` INT",
              "`Storniert` BOOLEAN",
              "PRIMARY KEY (`Bestellungen.id`)",
              "FOREIGN KEY (`Lenker`) REFERENCES `Bauteile`(`Bauteile.id`)",
              "FOREIGN KEY (`Rahmen`) REFERENCES `Bauteile`(`Bauteile.id`)",
              "FOREIGN KEY (`Sattel`) REFERENCES `Bauteile`(`Bauteile.id`)",
              "FOREIGN KEY (`Reifen`) REFERENCES `Bauteile`(`Bauteile.id`)",
              "FOREIGN KEY (`Bremsen`) REFERENCES `Bauteile`(`Bauteile.id`)",
              "FOREIGN KEY (`Gangschaltung`) REFERENCES `Bauteile`(`Bauteile.id`)",
              "FOREIGN KEY (`Beleuchtung`) REFERENCES `Bauteile`(`Bauteile.id`)",
              "FOREIGN KEY (`Felgen`) REFERENCES `Bauteile`(`Bauteile.id`)"]
        
        if are_u_sure:
            table_names = ["Bestellungen", "Grundmodelle", "Bauteile", "Baugruppen"]
            for t in table_names:
                self.drop_table(t)

            # Richtige Reihenfolge wichtig durch foreignkey-Abhängigkeiten
            table_names = table_names[::-1]

            self.create_table(table_names[0], config_baugruppen)
            self.create_table(table_names[1], config_bauteile)
            self.create_table(table_names[2], config_grundmodelle)
            self.create_table(table_names[3], config_bestellungen)

