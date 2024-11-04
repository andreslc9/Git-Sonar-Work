import sys

import src.vista.interfaz_coleccion as ic
from src.logica.coleccion import Coleccion
from src.modelo.declarative_base import session, Base, engine

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    session.close()
    
    coleccion = Coleccion()

    app = ic.App(sys.argv, coleccion)
    app.config['JWT_SECRET_KEY'] = 'secreto'
    sys.exit(app.exec_())