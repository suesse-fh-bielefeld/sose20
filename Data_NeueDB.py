config_kunde = ["`KundenNr` INTEGER NOT NULL AUTO_INCREMENT",
                "`Name` CHAR(30) NOT NULL",
                "`Vorname` CHAR(30) NOT NULL",
                "`Mail` CHAR(60)",
                "PRIMARY KEY (`KundenNr`)"]
my_db = db_communication()
my_db.create_table("Kunde", config_kunde)
my_db.close()

config_auftrag = [ "`AuftrNr` INTEGER NOT NULL AUTO_INCREMENT",
                   "`Datum` DATE",
                   "`KundenNr` INTEGER NOT NULL",
                   "PRIMARY KEY (`AuftrNr`)",
                   "FOREIGN KEY (`KundenNr`) REFERENCES `Kunde`(`KundenNr`)"]
my_db = db_communication()
my_db.create_table("Auftrag", config_auftrag)
my_db.close()

config_artikel = [ "`ArtNr` INTEGER NOT NULL AUTO_INCREMENT",
                   " Bezeichnung CHAR(35) NOT NULL",
                   "`Preis` NUMERIC(7,2)",
                   "`Montagezeit` INTEGER",
                   "`Ausstattung` CHAR(35)",
                   "PRIMARY KEY (`ArtNr`)"]
my_db = db_communication()
my_db.create_table("Artikel", config_artikel)
my_db.close()

config_einzelteile = [ "`EinzelteilNr` INTEGER NOT NULL AUTO_INCREMENT",
                   " Bezeichnung CHAR(35) NOT NULL",
                   "`Preis` NUMERIC(7,2)",
                   "PRIMARY KEY (`EinzelteilNr`)"]
my_db = db_communication()
my_db.create_table("Einzelteile", config_einzelteile)
my_db.close()

config_auftragposten = ["`PosNr` INTEGER NOT NULL AUTO_INCREMENT",
                        "`AuftragNr` INTEGER NOT NULL",
                        "`ArtikelNr` INTEGER NOT NULL",
                        "`Anzahl` INTEGER",
                        "`Gesamtpreis` NUMERIC(7,2)",
                        "PRIMARY KEY (`PosNr`)",
                        "FOREIGN KEY (`AuftragNr`) REFERENCES `Auftrag`(`AuftrNr`)",
                        "FOREIGN KEY (`ArtikelNr`) REFERENCES `Artikel`(`ArtNr`)"]
my_db = db_communication()
my_db.create_table("Auftragsposten", config_auftragposten)
my_db.close()

config_stueckliste = [ "`ArtNr` INTEGER",
                       " `EinzelteilNr` INTEGER",
                       "`Anzahl` INTEGER",
                       "FOREIGN KEY (`ArtNr`) REFERENCES `Artikel`(`ArtNr`)",
                       "FOREIGN KEY (`EinzelteilNr`) REFERENCES `Einzelteile`(`EinzelteilNr`)",
                       "PRIMARY KEY (`ArtNr`,`EinzelteilNr`)"]
my_db = db_communication()
my_db.create_table("Stueckliste", config_stueckliste)
my_db.close()

#Examples
kunde = [{'KundenNr' : '1','Name' : 'Kraus','Vorname':'Maria','Mail' : 'MaKrau@radelwelt.com'},
         {'KundenNr' : '2','Name' : 'Müller','Vorname':'Lischen','Mail' : 'keinklische@web.de'},
         {'KundenNr' : '3','Name' : 'Rolle','Vorname':'Heinz','Mail' : 'Rolle@gmail.com'}]
my_db = db_communication()
for i in range(len(kunde)):
    my_db.insert_data("Kunde", kunde[i])
my_db.close()

auftrag = [{'AuftrNr':'1','Datum':'2020-04-20','KundenNr':'2'},
           {'AuftrNr':'2','Datum':'2020-05-01','KundenNr':'3'},
           {'AuftrNr':'3','Datum':'2020-05-08','KundenNr':'1'},
           {'AuftrNr':'4','Datum':'2020-05-19','KundenNr':'3'}]

my_db = db_communication()
for i in range(len(auftrag)):
    my_db.insert_data("Auftrag", auftrag[i])
my_db.close()

artikel = [{ 'ArtNr':'100001','Bezeichnung': 'FH100','Preis':'499.00','Montagezeit': '2','Ausstattung':'City'},
           { 'ArtNr':'100002','Bezeichnung': 'S100','Preis':'649.99','Montagezeit': '2','Ausstattung':'Sport'},
           { 'ArtNr':'100003','Bezeichnung': 'Trofeo 5','Preis':'599.00','Montagezeit': '2','Ausstattung':'Rennen'},
           { 'ArtNr':'200001','Bezeichnung': '3 Gang Nexus RT','Preis':'100.00','Montagezeit': '1','Ausstattung':'NULL'},
           { 'ArtNr':'200002','Bezeichnung': '7 Gang Nexus RT','Preis':'110.00','Montagezeit': '1','Ausstattung':'NULL'},
           { 'ArtNr':'200003','Bezeichnung': '9 Gang Nexus RT','Preis':'150.00','Montagezeit': '1','Ausstattung':'NULL'},
           { 'ArtNr':'300001','Bezeichnung': 'Asvert Cityradsattel','Preis':'10.00','Montagezeit': '1','Ausstattung':'NULL'},
           { 'ArtNr':'300002','Bezeichnung': 'Asvert Comfortsattel','Preis':'39.00','Montagezeit': '1','Ausstattung':'NULL'},
           { 'ArtNr':'300003','Bezeichnung': 'Avert Rennradsattel','Preis':'59.00','Montagezeit': '1','Ausstattung':'Rennen'},
           { 'ArtNr':'400001','Bezeichnung': 'Retro Lenker','Preis':'89.99','Montagezeit': '1','Ausstattung':'Sport'},
           { 'ArtNr':'400002','Bezeichnung': 'Classic Lenker','Preis':'59.49','Montagezeit': '1','Ausstattung':'NULL'},
           { 'ArtNr':'400003','Bezeichnung': 'Rennradlenker','Preis':'99.99','Montagezeit': '1','Ausstattung':'Rennen'},
           { 'ArtNr':'500001','Bezeichnung': 'Shimano V-Brake','Preis':'10.00','Montagezeit': '1','Ausstattung':'NULL'},
           { 'ArtNr':'500002','Bezeichnung': 'Shimano GRB Scheibenbremse','Preis':'99.99','Montagezeit': '2','Ausstattung':'NULL'},
           { 'ArtNr':'500003','Bezeichnung': 'Fagura Felgenbremse','Preis':'39.99','Montagezeit': '1','Ausstattung':'NULL'},
           { 'ArtNr':'500004','Bezeichnung': 'Clarks Scheibenbremse','Preis':'69.99','Montagezeit': '2','Ausstattung':'Sport'},
           { 'ArtNr':'600001','Bezeichnung': 'Beleuchtung Dynamo','Preis':'5.00','Montagezeit': '1','Ausstattung':'City'},
           { 'ArtNr':'600002','Bezeichnung': 'Beleuchtung LED','Preis':'29.00','Montagezeit': '1','Ausstattung':'NULL'},
           { 'ArtNr':'600003','Bezeichnung': 'Leuchtstreifen','Preis':'15.00','Montagezeit': '0','Ausstattung':'City'},
           { 'ArtNr':'700001','Bezeichnung': 'Aluminium Felgen','Preis':'10.00','Montagezeit': '3','Ausstattung':'NULL'},
           { 'ArtNr':'700002','Bezeichnung': 'Redondo Rennradfelgen','Preis':'99.99','Montagezeit': '4','Ausstattung':'Rennen'},
           { 'ArtNr':'700003','Bezeichnung': 'Spengle Carbonfelgen','Preis':'79.99','Montagezeit': '2','Ausstattung':'NULL'},
           { 'ArtNr':'700004','Bezeichnung': 'Taylor Sportfelgen','Preis':'39.99','Montagezeit': '5','Ausstattung':'Sport'},
           { 'ArtNr':'700005','Bezeichnung': 'Taylor Cityfelgen','Preis':'69.99','Montagezeit': '5','Ausstattung':'City'},
           { 'ArtNr':'800001','Bezeichnung': 'Bereifung Schwalbe City','Preis':'15.00','Montagezeit': '2','Ausstattung':'City'},
           { 'ArtNr':'800002','Bezeichnung': 'Bereifung Schwalbe Sport','Preis':'20.00','Montagezeit': '1','Ausstattung':'Sport'},
           { 'ArtNr':'800003','Bezeichnung': 'Bereifung Schwalbe Marathon','Preis':'35.00','Montagezeit': '4','Ausstattung':'Rennen'}]
           
my_db = db_communication()
for i in range(len(artikel)):
    my_db.insert_data("Artikel", artikel[i])
my_db.close()

einzelteile = [{ 'EinzelteilNr':'1001','Bezeichnung': 'Rohr 25CrMo4 9mm','Preis':'7.50'},
               { 'EinzelteilNr':'1002','Bezeichnung': 'Rohr 34CrMo4 2.1mm','Preis':'4.00'},
               { 'EinzelteilNr':'1003','Bezeichnung': 'Rohr 34CrMo3 2.4mm','Preis':'4.50'},
               { 'EinzelteilNr':'2001','Bezeichnung': 'Kette','Preis':'7.50'},
               { 'EinzelteilNr':'2002','Bezeichnung': 'Zahnräder','Preis':'75.00'},
               { 'EinzelteilNr':'2003','Bezeichnung': 'Tretlager','Preis':'30.00'},
               { 'EinzelteilNr':'2004','Bezeichnung': 'Pedalsatz','Preis':'40.00'},
               { 'EinzelteilNr':'3001','Bezeichnung': 'Schlauch','Preis':'8.00'},
               { 'EinzelteilNr':'4001','Bezeichnung': 'Gummigriffe','Preis':'3.99'},
               { 'EinzelteilNr':'5001','Bezeichnung': 'Schrauben','Preis':'0.25'},
               { 'EinzelteilNr':'5002','Bezeichnung': 'Mutter','Preis':'0.50'},
               { 'EinzelteilNr':'6001','Bezeichnung': 'Lackierung','Preis':'25.50'}]
my_db = db_communication()
for i in range(len(einzelteile)):
    my_db.insert_data("Einzelteile", einzelteile[i])
my_db.close()

auftragposten =[{'PosNr':'101','AuftragNr':'1','ArtikelNr':'100001','Anzahl':'1','Gesamtpreis':'499.00'},
                {'PosNr':'102','AuftragNr':'1','ArtikelNr':'200002','Anzahl':'1','Gesamtpreis':'110.00'},
                {'PosNr':'103','AuftragNr':'1','ArtikelNr':'300002','Anzahl':'1','Gesamtpreis':'39.00'},
                {'PosNr':'104','AuftragNr':'1','ArtikelNr':'400002','Anzahl':'1','Gesamtpreis':'59.49'},
                {'PosNr':'105','AuftragNr':'1','ArtikelNr':'500002','Anzahl':'1','Gesamtpreis':'99.99'},
                {'PosNr':'106','AuftragNr':'1','ArtikelNr':'600001','Anzahl':'1','Gesamtpreis':'5.00'},
                {'PosNr':'107','AuftragNr':'1','ArtikelNr':'700001','Anzahl':'2','Gesamtpreis':'20.00'},
                {'PosNr':'108','AuftragNr':'1','ArtikelNr':'800001','Anzahl':'2','Gesamtpreis':'30.00'},
                {'PosNr':'201','AuftragNr':'2','ArtikelNr':'100003','Anzahl':'1','Gesamtpreis':'599.00'},
                {'PosNr':'202','AuftragNr':'2','ArtikelNr':'200003','Anzahl':'1','Gesamtpreis':'150.00'},
                {'PosNr':'203','AuftragNr':'2','ArtikelNr':'300002','Anzahl':'1','Gesamtpreis':'59.00'},
                {'PosNr':'204','AuftragNr':'2','ArtikelNr':'400003','Anzahl':'1','Gesamtpreis':'99.99'},
                {'PosNr':'205','AuftragNr':'2','ArtikelNr':'500002','Anzahl':'1','Gesamtpreis':'99.99'},
                {'PosNr':'206','AuftragNr':'2','ArtikelNr':'600002','Anzahl':'1','Gesamtpreis':'29.00'},
                {'PosNr':'207','AuftragNr':'2','ArtikelNr':'700002','Anzahl':'2','Gesamtpreis':'199.98'},
                {'PosNr':'208','AuftragNr':'2','ArtikelNr':'800003','Anzahl':'2','Gesamtpreis':'70.00'},
                {'PosNr':'301','AuftragNr':'3','ArtikelNr':'100002','Anzahl':'1','Gesamtpreis':'649.99'},
                {'PosNr':'302','AuftragNr':'3','ArtikelNr':'200002','Anzahl':'1','Gesamtpreis':'110.00'},
                {'PosNr':'303','AuftragNr':'3','ArtikelNr':'300002','Anzahl':'1','Gesamtpreis':'39.00'},
                {'PosNr':'304','AuftragNr':'3','ArtikelNr':'400001','Anzahl':'1','Gesamtpreis':'89.99'},
                {'PosNr':'305','AuftragNr':'3','ArtikelNr':'500002','Anzahl':'1','Gesamtpreis':'99.99'},
                {'PosNr':'306','AuftragNr':'3','ArtikelNr':'600002','Anzahl':'1','Gesamtpreis':'29.00'},
                {'PosNr':'307','AuftragNr':'3','ArtikelNr':'700004','Anzahl':'2','Gesamtpreis':'79.98'},
                {'PosNr':'308','AuftragNr':'3','ArtikelNr':'800002','Anzahl':'2','Gesamtpreis':'40.00'},
                {'PosNr':'401','AuftragNr':'4','ArtikelNr':'100001','Anzahl':'1','Gesamtpreis':'499.00'},
                {'PosNr':'402','AuftragNr':'4','ArtikelNr':'200001','Anzahl':'1','Gesamtpreis':'100.00'},
                {'PosNr':'403','AuftragNr':'4','ArtikelNr':'300001','Anzahl':'1','Gesamtpreis':'10.00'},
                {'PosNr':'404','AuftragNr':'4','ArtikelNr':'400002','Anzahl':'1','Gesamtpreis':'59.49'},
                {'PosNr':'405','AuftragNr':'4','ArtikelNr':'500001','Anzahl':'1','Gesamtpreis':'10.00'},
                {'PosNr':'406','AuftragNr':'4','ArtikelNr':'600001','Anzahl':'1','Gesamtpreis':'5.00'},
                {'PosNr':'407','AuftragNr':'4','ArtikelNr':'700001','Anzahl':'2','Gesamtpreis':'20.00'},
                {'PosNr':'408','AuftragNr':'4','ArtikelNr':'800001','Anzahl':'2','Gesamtpreis':'30.00'}]
                
my_db = db_communication()
for i in range(len(auftragposten)):
    my_db.insert_data("Auftragsposten", auftragposten[i])
my_db.close()

stueckliste = [{'ArtNr': '100001','EinzelteilNr':'5001','Anzahl':'20'},
               {'ArtNr': '100001','EinzelteilNr':'5002','Anzahl':'15'},
               {'ArtNr': '100001','EinzelteilNr':'6001','Anzahl':'1'},
               {'ArtNr': '100002','EinzelteilNr':'5001','Anzahl':'24'},
               {'ArtNr': '100002','EinzelteilNr':'5002','Anzahl':'19'},
               {'ArtNr': '100002','EinzelteilNr':'6001','Anzahl':'1'},
               {'ArtNr': '100003','EinzelteilNr':'5001','Anzahl':'27'},
               {'ArtNr': '100003','EinzelteilNr':'5002','Anzahl':'25'},
               {'ArtNr': '100003','EinzelteilNr':'6001','Anzahl':'1'},
               {'ArtNr': '200001','EinzelteilNr':'5001','Anzahl':'4'},
               {'ArtNr': '200001','EinzelteilNr':'5002','Anzahl':'4'},
               {'ArtNr': '200001','EinzelteilNr':'2001','Anzahl':'1'},
               {'ArtNr': '200001','EinzelteilNr':'2002','Anzahl':'3'},
               {'ArtNr': '200001','EinzelteilNr':'2003','Anzahl':'1'},
               {'ArtNr': '200002','EinzelteilNr':'5001','Anzahl':'7'},
               {'ArtNr': '200002','EinzelteilNr':'5002','Anzahl':'7'},
               {'ArtNr': '200002','EinzelteilNr':'2001','Anzahl':'1'},
               {'ArtNr': '200002','EinzelteilNr':'2002','Anzahl':'7'},
               {'ArtNr': '200002','EinzelteilNr':'2003','Anzahl':'1'},
               {'ArtNr': '200003','EinzelteilNr':'5001','Anzahl':'11'},
               {'ArtNr': '200003','EinzelteilNr':'5002','Anzahl':'11'},
               {'ArtNr': '200003','EinzelteilNr':'2001','Anzahl':'1'},
               {'ArtNr': '200003','EinzelteilNr':'2002','Anzahl':'9'},
               {'ArtNr': '200003','EinzelteilNr':'2003','Anzahl':'1'},
               {'ArtNr': '300001','EinzelteilNr':'5001','Anzahl':'1'},
               {'ArtNr': '300001','EinzelteilNr':'5002','Anzahl':'1'},
               {'ArtNr': '300001','EinzelteilNr':'1002','Anzahl':'1'},
               {'ArtNr': '300002','EinzelteilNr':'5001','Anzahl':'1'},
               {'ArtNr': '300002','EinzelteilNr':'5002','Anzahl':'1'},
               {'ArtNr': '300002','EinzelteilNr':'1002','Anzahl':'1'},
               {'ArtNr': '300003','EinzelteilNr':'5001','Anzahl':'2'},
               {'ArtNr': '300003','EinzelteilNr':'5002','Anzahl':'2'},
               {'ArtNr': '300003','EinzelteilNr':'1003','Anzahl':'1'},
               {'ArtNr': '400001','EinzelteilNr':'1001','Anzahl':'1'},
               {'ArtNr': '400001','EinzelteilNr':'4001','Anzahl':'2'},
               {'ArtNr': '400001','EinzelteilNr':'5001','Anzahl':'4'},
               {'ArtNr': '400001','EinzelteilNr':'5002','Anzahl':'4'},
               {'ArtNr': '400002','EinzelteilNr':'1001','Anzahl':'1'},
               {'ArtNr': '400002','EinzelteilNr':'4001','Anzahl':'2'},
               {'ArtNr': '400002','EinzelteilNr':'5001','Anzahl':'4'},
               {'ArtNr': '400002','EinzelteilNr':'5002','Anzahl':'4'},
               {'ArtNr': '400003','EinzelteilNr':'1001','Anzahl':'1'},
               {'ArtNr': '400003','EinzelteilNr':'4001','Anzahl':'2'},
               {'ArtNr': '400003','EinzelteilNr':'5001','Anzahl':'4'},
               {'ArtNr': '400003','EinzelteilNr':'5002','Anzahl':'4'},
               {'ArtNr': '500001','EinzelteilNr':'5001','Anzahl':'8'},
               {'ArtNr': '500001','EinzelteilNr':'5002','Anzahl':'8'},
               {'ArtNr': '500002','EinzelteilNr':'5001','Anzahl':'5'},
               {'ArtNr': '500002','EinzelteilNr':'5002','Anzahl':'5'},
               {'ArtNr': '500003','EinzelteilNr':'5001','Anzahl':'11'},
               {'ArtNr': '500003','EinzelteilNr':'5002','Anzahl':'11'},
               {'ArtNr': '500004','EinzelteilNr':'5001','Anzahl':'6'},
               {'ArtNr': '500004','EinzelteilNr':'5002','Anzahl':'6'},
               {'ArtNr': '600001','EinzelteilNr':'5002','Anzahl':'2'},
               {'ArtNr': '600001','EinzelteilNr':'1001','Anzahl':'2'},
               {'ArtNr': '600002','EinzelteilNr':'4001','Anzahl':'3'},
               {'ArtNr': '600002','EinzelteilNr':'5001','Anzahl':'3'},
               {'ArtNr': '700001','EinzelteilNr':'5001','Anzahl':'2'},
               {'ArtNr': '700001','EinzelteilNr':'5002','Anzahl':'2'},
               {'ArtNr': '700002','EinzelteilNr':'5001','Anzahl':'2'},
               {'ArtNr': '700002','EinzelteilNr':'5002','Anzahl':'2'},
               {'ArtNr': '700003','EinzelteilNr':'5001','Anzahl':'2'},
               {'ArtNr': '700003','EinzelteilNr':'5002','Anzahl':'2'},
               {'ArtNr': '700004','EinzelteilNr':'5001','Anzahl':'2'},
               {'ArtNr': '700004','EinzelteilNr':'5002','Anzahl':'2'},
               {'ArtNr': '700005','EinzelteilNr':'5001','Anzahl':'2'},
               {'ArtNr': '700005','EinzelteilNr':'5002','Anzahl':'2'},
               {'ArtNr': '800001','EinzelteilNr':'3001','Anzahl':'2'},
               {'ArtNr': '800002','EinzelteilNr':'3001','Anzahl':'2'},
               {'ArtNr': '800003','EinzelteilNr':'3001','Anzahl':'2'}]
               

my_db = db_communication()
for i in range(len(stueckliste)):
     my_db.insert_data("Stueckliste", stueckliste[i])
my_db.close()
