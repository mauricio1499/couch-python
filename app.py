from datetime import datetime
import logging, os
import couchdb
from dotenv import load_dotenv

class DocumentoCouch(object):

    load_dotenv()       ### Carga archivo .env                    
    def __init__(self, nombre_base ):
        __usuario = os.environ.get('USER_COUCH')
        __contra  = os.environ.get('PASS_COUCH')
        __host    = os.environ.get('HOST_COUCH')
        __puerto  = os.environ.get('PORT_COUCH')
        try:
            self.couchserver  = couchdb.Server("http://%s:%s@%s:%s/" % (__usuario, __contra, __host , __puerto))
            self.bd           = self.couchserver[nombre_base] ##Base de datos debe estar creada ## ir a --> your_host:port/_utils
        except Exception as e:
            self.__guardar_log_couch__('init','error en conexion',str(e))
    
    def __guardar_log_couch__( self, origen , datos , error  ):### Guarda Logs que presente couch al conectarse.
        logging.basicConfig( 
            level    = logging.DEBUG, 
            format   = '%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
            filename = 'logs/info-log.log',datefmt='%d/%m/%Y %H:%M:%S'
        )
        logging.info('\nOrigen: '+str(origen)+'\nDatos: '+str(datos)+'\nError: '+str(error)+'\n'+'#'*100)

    def guardar(self , datos ):
        try:    self.bd.save({'fecha':datetime.now().strftime("%d/%m/%Y, %H:%M:%S") ,'datos':datos })
        except Exception as e:  self.__guardar_log_couch__('guardar ', datos , str(e) )             


##### PRUEBA ######
datos = {'nombre':'Python','apellido':'Couch'}
doc   = DocumentoCouch('nombre_de_mi_base')   ##Crear base de datos en couch, ir a --> your_host:port/_utils
doc.guardar()