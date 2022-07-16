import http.server
import socketserver
from urllib.parse import urlparse, parse_qs, unquote
import json
import datetime

from volc import VolcanDB

# définition du handler
class RequestHandler(http.server.SimpleHTTPRequestHandler):
    # sous-répertoire racine des documents statiques
    static_dir = '/client'
    # version du serveur
    server_version = 'serveur1.py/0.1'

    # on surcharge la méthode qui traite les requêtes GET
    def do_GET(self):
        self.init_params()
      
        # le chemin d'accès commence par commentaires, suivi du point d'interêt
        if self.path_info[0] == "commentaires":
            self.send_commentaires()

        elif self.path_info[0] == "volcans":
            self.send_volcans()
            
        elif self.path_info[0] == "infos":
            self.send_infos()

        elif self.path_info[0] == "liste_continent":
            self.get_volcans_continent()

        # document statique ?
        else:
            self.send_static()
    
    # méthode pour traiter les requêtes HEAD
    def do_HEAD(self):
        self.send_static()


    # méthode pour traiter les requêtes POST
    def do_POST(self):
        self.init_params()
        if len(self.path_info) > 0 and self.path_info[0] == "commentaire":
            self.post_commentaire()
        elif len(self.path_info) > 0 and self.path_info[0] == "add_user":
            self.post_user()
        elif len(self.path_info) > 0 and self.path_info[0] == "login":
            print(self.params)
            self.post_login()
            
        # Method not supported
        else:
            self.send_error(405)

    def do_DELETE(self):
        self.init_params()
        if len(self.path_info) > 0 and self.path_info[0] == "commentaire":
            self.supression_commentaire()
        
        # Method not supported
        else:
            self.send_error(405)


    # on envoie le document statique demandé
    def send_static(self):
        # on modifie le chemin d'accès en insérant le répertoire préfixe
        self.path = self.static_dir + self.path
        # on appelle la méthode parent (do_GET ou do_HEAD)
        # à partir du verbe HTTP (GET ou HEAD)
        if (self.command=='HEAD'):
            http.server.SimpleHTTPRequestHandler.do_HEAD(self)
        else:
            http.server.SimpleHTTPRequestHandler.do_GET(self)


    # on envoie la réponse
    def send(self,body,headers=[]):
        encoded = bytes(body, 'UTF-8')
     
        self.send_response(200)
     
        [self.send_header(*t) for t in headers]
        self.send_header('Content-Length',int(len(encoded)))
        self.end_headers()
     
        self.wfile.write(encoded)

    
    def send_volcans(self):
        db = VolcanDB()
        data = db.get_all_volcans_position()
        
        # on construit la réponse en json
        body = json.dumps([list(d) for d in data])
        
        # on envoie la réponse au client
        headers = [('Content-Type','application/json')]
        self.send(body,headers)
        
    def send_infos(self) :
        site = self.path_info[1]
        
        db = VolcanDB()
        data = db.get_all(site)
        #data = db.get_all()
        
        # on construit la réponse en json
        #body = json.dumps([{d[1]:d} for d in data])
        body = json.dumps(data)
        
        # on envoie la réponse au client
        headers = [('Content-Type','application/json')]
        self.send(body,headers)
        

    def send_commentaires(self):
        site = self.path_info[1]

        db = VolcanDB()
        data = db.get_commentaires(site)
        
        # construction de la réponse json
        body = json.dumps([list(d) for d in data])
        
        headers = [('Content-Type','application/json')]
        self.send(body,headers)
        
    # def post_login(self):        
    #     data = self.params
        
    #     email = data['email']
    #     pwd = data['password']
        
    #     db = VolcanDB()
    #     var = db.verify_login(email, pwd)
    #     del db
        
    #     print(var)
        
    #     headers = [('Content-Type','application/json')]
        
    #     if var:
    #         self.send('True',headers)
    #     elif var == False:
    #         self.send('False',headers)
    #     elif var == None:
    #         self.send('None',headers)
    
    def post_user(self):
        data = self.params
        
        pseudo = data['user_pseudo']
        email =  data['email']
        pwd = data['user_password']
        
        db = VolcanDB()
        db.nouveau_utilisateur(pseudo, email, pwd)
        del db
        
        self.send(json.dumps({'Status':'Done'}),[('Content-Type','application/json')])

    def post_commentaire(self):
        time = timestamp()
        
        data = self.params
        site = data["site"]
        pseudo = data['pseudo']
        pwd = data['password']
        message =  data['message']
        date = data['date']
        
        print(pseudo, site, time, message, date)
        
        db = VolcanDB()
        if db.verify_login(pseudo, pwd):
            db.nouveau_commentaire(pseudo, site, time, message, date)
            
            self.send(json.dumps({'Status':'Done'}),[('Content-Type','application/json')])
        del db
    
    def supression_commentaire(self):
        data = self.params
        
        pseudo = data['pseudo']
        pwd = data['password']
        id_com =  self.path_info[1]
        
        
        print(pseudo,pwd,id_com)
        
        db = VolcanDB()
        if db.verify_login(pseudo, pwd):
            db.del_commentaire(id_com)
            
            self.send(json.dumps({'Status':'Done'}),[('Content-Type','application/json')])
        del db


    def get_volcans_continent(self):
        continent = self.path_info[1]
        print("aaa = "+continent)
        
        
        db = VolcanDB()
        data = db.getVolcanNomPhotoByContinent(continent)
        del db 
        
        body = json.dumps([list(d) for d in data])
        headers = [('Content-Type','application/json')]
        self.send(body,headers)
        
    # analyse d'une chaîne de requête pour récupérer les paramètres
    def parse_qs(self,query_string):
        self.params = parse_qs(query_string)
        for k in self.params:
            if len(self.params[k]) == 1:
                self.params[k] = self.params[k][0]


    # on analyse la requête pour initialiser nos paramètres
    def init_params(self):
        # analyse de l'adresse
        info = urlparse(self.path)
        self.path_info = [unquote(v) for v in info.path.split('/')[1:]]  # info.path.split('/')[1:]
        self.query_string = info.query
        self.parse_qs(info.query)
      
        # récupération du corps
        length = self.headers.get('Content-Length')
        ctype = self.headers.get('Content-Type')
        if length:
            self.body = str(self.rfile.read(int(length)),'utf-8')
            if ctype == 'application/x-www-form-urlencoded' : 
                self.parse_qs(self.body)
            elif ctype == 'application/json' : 
                self.params = json.loads(self.body)
        else:
            self.body = ''
       
        # traces
        print('path_info =',self.path_info)
        print('body =',length,ctype,self.body)
        print('params =', self.params)
        print('query =',self.query_string)
    
def timestamp():
    return int(datetime.datetime.timestamp(datetime.datetime.now()))


if __name__ == "__main__":
    # instanciation et lancement du serveur
    httpd = socketserver.TCPServer(("", 8080), RequestHandler)
    httpd.serve_forever()
