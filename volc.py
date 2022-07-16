import sqlite3

class VolcanDB:
    def __init__(self):
        self.__conn = sqlite3.connect('volcans.db')
        self.__curseur = self.__conn.cursor()
    
    def get_name(self, lati, longi):
        self.__curseur.execute("SELECT name FROM volcans WHERE lat = '{}' AND lon = '{}'".format(lati,longi))
        list = self.__curseur.fetchall()        
        return list
    
    def liste_names(self):
        self.__curseur.execute("SELECT name FROM volcans")
        list = self.__curseur.fetchall()        
        return list
    
    def __del__(self):
        self.__conn.close()
    
    def get_abstract(self):
        self.__curseur.execute("SELECT abstract FROM volcans")
        list = self.__curseur.fetchall()        
        return list

    def get_all_volcans_position(self):                     # Selectioner un film à partir d'un ID
        try:
            self.__curseur.execute("SELECT name,lat,lon FROM volcans")
            return self.__curseur.fetchall()
        except sqlite3.OperationalError as err:                                # interception d'une exception
            print('err:', str(err))
            print('type exception:', type(err).__name__)
            return None 

        
    def get_photo(self, nom) :
        try:
            self.__curseur.execute("SELECT photo FROM volcans WHERE name = '{}'".format(nom))
            return(self.__curseur.fetchall())
        except sqlite3.OperationalError as err:                                # interception d'une exception
            print('err:', str(err))
            print('type exception:', type(err).__name__)
            return None 
    
    # def get_all(self) :
    #     try:    
    #         self.__curseur.execute("SELECT * FROM volcans")
    #         return(self.__curseur.fetchall())
    #     except sqlite3.OperationalError as err:                                # interception d'une exception
    #         print('err:', str(err))
    #         print('type exception:', type(err).__name__)
    #         return None 
            
    def get_all(self,site) :
        try:    
            self.__curseur.execute("SELECT * FROM volcans WHERE name = '{}'".format(site))
            return(self.__curseur.fetchall())
        except sqlite3.OperationalError as err:                                # interception d'une exception
            print('err:', str(err))
            print('type exception:', type(err).__name__)
            return None 
        
        
    """"PARTIE COMMENTAIRES """
    
    def nouveau_utilisateur(self, pseudo, email, pwd):
        try:
            self.__curseur.execute("SELECT * FROM utilisateurs WHERE email = '{}'".format(email))
            if len(self.__curseur.fetchall()) != 0:
                print("E-mail deja existant")
            else:
                self.__curseur.execute("INSERT INTO utilisateurs(pseudo,email,pwd) VALUES ('{}','{}','{}')".format(pseudo, email, pwd))
                self.__conn.commit()
                print ("Utilisateur ajouté")
               
        except sqlite3.OperationalError as err:                                # interception d'une exception quelconque
            print('err:', str(err))
            print('type exception:', type(err).__name__)
                    
    def nouveau_commentaire(self, pseudo, site, timestamp, message, date):
        try:
            self.__curseur.execute("SELECT * FROM commentaires WHERE message = '{}' AND pseudo='{}' AND site = '{}'".format(message,pseudo,site))
            if len(self.__curseur.fetchall()) == 0:
                self.__curseur.execute("INSERT INTO commentaires(pseudo, site, timestamp, message, date) VALUES ('{}','{}','{}','{}','{}')".format(pseudo, site, timestamp, message, date))
                self.__conn.commit()
                print ("Commentaire enregistrée")
            else:
                print("Commentaire doublé")
                print(self.__curseur.fetchall())
            
        except sqlite3.OperationalError as err:                                # interception d'une exception quelconque
            print('err:', str(err))
            print('type exception:', type(err).__name__)
    
    def get_commentaires(self, site):
        try:
            self.__curseur.execute("SELECT * FROM commentaires WHERE site = '{}'".format(site))
            data = self.__curseur.fetchall()
            return(data)
               
        except sqlite3.OperationalError as err:                                # interception d'une exception quelconque
            print('err:', str(err))
            print('type exception:', type(err).__name__)
            
    """PARTIE FLUX DE PAGES"""
    
    def getVolcanNomPhotoByContinent(self, continentName):
        if continentName == "Afrique":
            continentName = "Africa"
        elif continentName == "AmeNordCentral":
            continentName = "North America"
        elif continentName == "AmeSud":
            continentName = "South America"
        elif continentName == "Antarctique":
            continentName = "Antarctica"
        elif continentName == "Asie":
            continentName = "Asia"
        elif continentName == "Europe":
            continentName = "Europe"
        elif continentName == "Oceanie":
            continentName = "Oceania"
            
            
        self.__curseur.execute("SELECT name, photo FROM volcans WHERE continent = '{}'".format(continentName))
        list = self.__curseur.fetchall()        
        return list

    def verify_login(self, pseudo, pwd):
        try:
            self.__curseur.execute("SELECT * FROM utilisateurs WHERE pseudo = '{}'".format(pseudo))
            data = self.__curseur.fetchone()
            return pwd == data[2]
               
        except sqlite3.OperationalError as err:                                # interception d'une exception quelconque
            print('err:', str(err))
            print('type exception:', type(err).__name__)
            
    def del_commentaire(self, id_com):
        try:
            self.__curseur.execute("DELETE from commentaires where id = '{}'".format(id_com))
            self.__conn.commit()
            
        except sqlite3.OperationalError as err:                                # interception d'une exception quelconque
            print('err:', str(err))
            print('type exception:', type(err).__name__)

if __name__ == '__main__':
    test = VolcanDB()
    #liste = test.liste()
    #print(liste)
    
    #print(test.verify_login('Giovanni','abcdef'))
    
    #print(test.get_all('Vulcano'))

    data = ["Arthur","The Black Tusk","1655230721","Cool","Juin 2021"]
    
    #test.nouveau_commentaire("Arthur","The Black Tusk","1655230721","Cool","Juin 2021")

    #print(test.get_commentaires("The Black Tusk"))
    
    print(test.verify_login('Arthur', 'password'))