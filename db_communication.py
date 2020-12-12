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
            self.__cursor = self.__db.cursor()
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
            'database': 'Fahrradshop'
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
        tables = self.read_tables()
        if not any(name in s for s in tables):
            return self.__cursor.execute("SHOW COLUMNS FROM `{}`".format(x))
        else:
            print("Table", name, "already exists.")
            return False
        
    def storno(self, key):
        """
        Datenbank spezifische Funktion für die Vorgängerversion des Projektes.
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
        Aus diesem Grund wird das Nutzen dieser Funktion empfohlen, um die Tabellen der Fahrrad-Shop-Datenbank zu löschen
        """
        config_kunde = [
            
            "`KundenNr` INTEGER NOT NULL AUTO_INCREMENT",
            "`Name` CHAR(30) NOT NULL",
            "`Vorname` CHAR(30) NOT NULL",
            "`Mail` CHAR(60)",
            "PRIMARY KEY (`KundenNr`)"
        ]

        config_auftrag = [ 
            
            "`AuftrNr` INTEGER NOT NULL AUTO_INCREMENT",
            "`Bestelldatum` DATE",
            "`Lieferdatum` DATE",
            "`KundenNr` INTEGER NOT NULL",
            "PRIMARY KEY (`AuftrNr`)",
            "FOREIGN KEY (`KundenNr`) REFERENCES `Kunde`(`KundenNr`)"
        ]

        config_merkmalcluster = [
            
            "`ClusterNr` INTEGER NOT NULL AUTO_INCREMENT",
            "`Merkmalsbezeichnung`CHAR(95)",
            "PRIMARY KEY (`ClusterNr`)"
        ]

        config_merkmale = [
           
        " `MerkmalNr` INT(11) NOT NULL AUTO_INCREMENT",
        " `Merkmalcluster` INT(11) NOT NULL",
        "`Bezeichnung` CHAR(95) NOT NULL",
        "`Preis` DECIMAL(7,2) NULL DEFAULT NULL",
        "PRIMARY KEY (`MerkmalNr`)",
        "FOREIGN KEY (`Merkmalcluster`) REFERENCES `apm2`.`Merkmalcluster` (`ClusterNr`)"

        ]
        
        config_konfiguration = [
            
        "`KonfigNr` INTEGER NOT NULL AUTO_INCREMENT",
        "`AuftragNr` INTEGER NOT NULL",
        "`MerkmalNr` INTEGER NOT NULL",
        "PRIMARY KEY (`KonfigNr`)",
        "FOREIGN KEY (`AuftragNr`) REFERENCES `Auftrag`(`AuftrNr`)",
        "FOREIGN KEY (`MerkmalNr`) REFERENCES `Merkmale`(`MerkmalNr`)"
    ]
        

        
        config_arbeitsschrittgruppe = [
            
        "`ArbeitsschrittgruppeNr` INT(11) NOT NULL AUTO_INCREMENT",
        "`Bezeichnung` CHAR(95) NOT NULL",
        "`Optional` TINYINT(1) NULL DEFAULT NULL",
        "`Merkmalcluster` INT(11) NOT NULL",
        "PRIMARY KEY (`ArbeitsschrittgruppeNr`)",
        " FOREIGN KEY (`Merkmalcluster`) REFERENCES `apm2`.`Merkmalcluster` (`ClusterNr`)"

        ]
        
        
        config_fabrik = [
        
        "`idFabrik` INT(11) NOT NULL",
        "`Ecken` CHAR(200) NULL DEFAULT NULL",
        "`Bezeichnung` CHAR(45) NULL DEFAULT NULL",
        " PRIMARY KEY (`idFabrik`)"
        ]
        
        config_teileart = [
    
          "`idTeileart` INT(11) NOT NULL",
          "PRIMARY KEY (`idTeileart`)"
        ]
        
        config_behälter = [
         " `idBehälter` INT(11) NOT NULL",
         " `Teileart_idTeileart` INT(11) NOT NULL",
         "PRIMARY KEY (`idBehälter`)",
         "FOREIGN KEY (`Teileart_idTeileart`) REFERENCES `apm2`.`Teileart` (`idTeileart`)"
        ]
        
        config_ftf = [ 

        " `idFTF` INT(11) NOT NULL",
        "`Standort` CHAR(45) NULL DEFAULT NULL",
        "`Blickrichtung` CHAR(45) NULL DEFAULT NULL",
        "`Beladen` TINYINT(4) NULL DEFAULT NULL",
        "PRIMARY KEY (`idFTF`)"

        ]
        
        config_karossenFTF = [
          
        "`idKarosseFTF` INT(11) NOT NULL",
        " `FTF_idFTF` INT(11) NOT NULL",
        "`Produkt_idProdukt` INT(11) NOT NULL",
        "PRIMARY KEY (`idKarosseFTF`)",
        "FOREIGN KEY (`FTF_idFTF`) REFERENCES `apm2`.`FTF` (`idFTF`)",
        "FOREIGN KEY (`Produkt_idProdukt`) REFERENCES `apm2`.`Produkt` (`idProdukt`)"

        ]
        
        config_teileFTF = [
            
        "`idTeileFTF` INT(11) NOT NULL",
        "`Behälter_idBehälter` INT(11) NOT NULL",
        "`FTF_idFTF` INT(11) NOT NULL",
        " PRIMARY KEY (`idTeileFTF`)",
        "FOREIGN KEY (`Behälter_idBehälter`) REFERENCES `apm2`.`Behälter` (`idBehälter`)",
        "FOREIGN KEY (`FTF_idFTF`) REFERENCES `apm2`.`FTF` (`idFTF`)"
    
        ]
        
        
        
        config_produkt = [
            
        "`idProdukt` INT(11) NOT NULL",
        "`Auftrag_AuftrNr` INT(11) NOT NULL",
        "PRIMARY KEY (`idProdukt`)",
        "FOREIGN KEY (`Auftrag_AuftrNr`) REFERENCES `apm2`.`Auftrag` (`AuftrNr`)"
        ]
        
        config_koordinate = [     
        
        "`idKoordinate` INT(11) NOT NULL",
        "`Mittelpunkt` CHAR(45) NULL DEFAULT NULL",
        "`Laenge` DECIMAL(4,2) NULL DEFAULT NULL",
        "`Breite` DECIMAL(4,2) NULL DEFAULT NULL",
        "PRIMARY KEY (`idKoordinate`)"

        ]
        
        config_hindernis = [

        "`idHindernis` INT(11) NOT NULL",
        "`Koordinate_idKoordinate` INT(11) NOT NULL",
        "`Fabrik_idFabrik` INT(11) NOT NULL",
        "PRIMARY KEY (`idHindernis`)",
        "FOREIGN KEY (`Fabrik_idFabrik`) REFERENCES `apm2`.`Fabrik` (`idFabrik`)",
        "FOREIGN KEY (`Koordinate_idKoordinate`) REFERENCES `apm2`.`Koordinate` (`idKoordinate`)"  
        ]
    
        config_montagestation = [

        "`idMontagestation` INT(11) NOT NULL",
        "`Koordinate_idKoordinate` INT(11) NOT NULL",
        "`Fabrik_idFabrik` INT(11) NOT NULL",
        "PRIMARY KEY (`idMontagestation`)",
        "FOREIGN KEY (`Fabrik_idFabrik`) REFERENCES `apm2`.`Fabrik` (`idFabrik`)",
        "FOREIGN KEY (`Koordinate_idKoordinate`) REFERENCES `apm2`.`Koordinate` (`idKoordinate`)"

        ]
        
        config_puffer = [
    
        "`idPuffer` INT(11) NOT NULL",
        "`Kapazitaet` INT(11) NULL DEFAULT NULL",
        "`Bestand` INT(11) NULL DEFAULT NULL",
        "`Montagestation_idMontagestation` INT(11) NOT NULL",
        "PRIMARY KEY (`idPuffer`)",
        "FOREIGN KEY (`Montagestation_idMontagestation`) REFERENCES `apm2`.`Montagestation` (`idMontagestation`)"

        ]
  
        config_lager = [
            
        "`LagNr` INT(11) NOT NULL",
        "`Koordinate_idKoordinate` INT(11) NOT NULL",
        "`Fabrik_idFabrik` INT(11) NOT NULL",
        "PRIMARY KEY (`LagNr`)",
        "FOREIGN KEY (`Fabrik_idFabrik`) REFERENCES `apm2`.`Fabrik` (`idFabrik`)",
        "FOREIGN KEY (`Koordinate_idKoordinate`) REFERENCES `apm2`.`Koordinate` (`idKoordinate`)"
    

        ]
        
        config_lagerplatz = [
            
        "`idLagerplatz` INT(11) NOT NULL",
        "`Teileart_idTeileart` INT(11) NOT NULL",
        "`Kapazitaet` INT(11) NULL DEFAULT NULL",
        "`Bestand` INT(11) NULL DEFAULT NULL",
        "`Lager_LagNr` INT(11) NOT NULL",
        "PRIMARY KEY (`idLagerplatz`)",
        "FOREIGN KEY (`Lager_LagNr`) REFERENCES `apm2`.`Lager` (`LagNr`)",
        "FOREIGN KEY (`Teileart_idTeileart`) REFERENCES `apm2`.`Teileart` (`idTeileart`)"
            
        ]
        
        
        config_arbeitsschritt = [
            
        "`SchrittNr` INT(11) NOT NULL AUTO_INCREMENT",
        "`ArbeitsschrittgruppeNr` INT(11) NOT NULL",
        "`MerkmalNr` INT(11) NOT NULL",
        "`EinzelteilNr` INT(11) NOT NULL",
        "`Anzahl Einzelteil` INT(11) NULL DEFAULT NULL",
        "`Montagezeit` INT(11) NULL DEFAULT NULL",
        `"Montagestation_idMontagestation` INT(11) NOT NULL",
        "PRIMARY KEY (`SchrittNr`)",
        "FOREIGN KEY (`ArbeitsschrittgruppeNr`) REFERENCES `apm2`.`Arbeitsschrittgruppe` (`ArbeitsschrittgruppeNr`)",
        "FOREIGN KEY (`EinzelteilNr`) REFERENCES `apm2`.`Einzelteile` (`EinzelteilNr`)",
        "FOREIGN KEY (`Montagestation_idMontagestation`) REFERENCES `apm2`.`Montagestation` (`idMontagestation`)"
            
        ]
        
        config_einzelteile = [ 
            
        "`EinzelteilNr` INT(11) NOT NULL AUTO_INCREMENT",
        "`Bezeichnung` CHAR(95) NOT NULL",
        "`Puffer_idPuffer` INT(11) NULL DEFAULT NULL",
        "`Teileart_idTeileart` INT(11) NULL DEFAULT NULL",
        "`Lagerplatz_idLagerplatz` INT(11) NULL DEFAULT NULL",
        "`Behälter_idBehälter` INT(11) NOT NULL",
        "PRIMARY KEY (`EinzelteilNr`)",
        "FOREIGN KEY (`Behälter_idBehälter`) REFERENCES `apm2`.`Behälter` (`idBehälter`)",
        "FOREIGN KEY (`Lagerplatz_idLagerplatz`) REFERENCES `apm2`.`Lagerplatz` (`idLagerplatz`)",
        "FOREIGN KEY (`Puffer_idPuffer`) REFERENCES `apm2`.`Puffer` (`idPuffer`)",
        "FOREIGN KEY (`Teileart_idTeileart`) REFERENCES `apm2`.`Teileart` (`idTeileart`)"

    ]

    
        config_reihenfolgevorgabe = [
            
        "`AktuelleNr` INT(11) NOT NULL",
        "`NachfolgerNr` INT(11) NOT NULL",
        "PRIMARY KEY (`AktuelleNr`, `NachfolgerNr`)",
        "FOREIGN KEY (`AktuelleNr`) REFERENCES `apm2`.`Arbeitsschrittgruppe` (`ArbeitsschrittgruppeNr`)",
        "FOREIGN KEY (`NachfolgerNr`) REFERENCES `apm2`.`Arbeitsschrittgruppe` (`ArbeitsschrittgruppeNr`)"
            
        ]

        if are_u_sure:
            list_names_tables = ["Kunde","Auftrag","Merkmalcluster","Merkmale","Konfiguration","Arbeitsschrittgruppe", "Fabrik", "Teileart", "Behälter", "FTF", "KarossenFTF", "TeileFTF", "Produkt", "Koordinate", "Hindernis", "Montagestation", "Puffer", "Lager", "Lagerplatz","Arbeitsschritt", "Einzelteile", "Reihenfolgevorgabe"]
            list_config_tables=[config_kunde, config_auftrag, config_merkmalcluster, config_merkmale, config_konfiguration, config_arbeitsschrittgruppe, config_fabrik, config_teileart, config_behälter, config_ftf, config_karossenFTF, config_teileFTF, config_produkt, config_koordinate, config_hindernis, config_montagestation, config_puffer, config_lager,config_lagerplatz, config_arbeitsschritt, config_einzelteile, config_reihenfolgevorgabe]
            table_names = list_names_tables[::-1]
            print(table_names)
            for t in table_names:
                self.drop_table(t)

        for idx in range(len(list_config_tables)):
            self.create_table(list_names_tables[idx],list_config_tables[idx])

            
            
