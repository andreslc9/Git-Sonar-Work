import unittest

from faker import Faker

from src.logica.coleccion import Coleccion
from src.modelo.album import Album
from src.modelo.declarative_base import Session


class AlbumTestCase(unittest.TestCase):

    def setUp(self):
        self.session = Session()
        self.coleccion = Coleccion()
        # Generación de datos con libreria Faker
        self.data_factory = Faker()

    def test_agregar_album(self):
        # Nombre aleatorio
        titulo_album1 = self.data_factory.name()
        # Año aleatorio
        anio_album1 = self.data_factory.year()
        # Frase aleatoria
        descripcion_album1 = self.data_factory.sentence()
        self.coleccion.agregar_album(titulo_album1, anio_album1, descripcion_album1, "CD")
        descripcion_album2 = self.data_factory.sentence()
        self.coleccion.agregar_album("Live Killers", 2013, descripcion_album2, "CASETE")
        anio_album3 = self.data_factory.year()
        descripcion_album3 = self.data_factory.sentence()
        self.coleccion.agregar_album("Clara luna", anio_album3, descripcion_album3, "CASETE")
        consulta1 = self.session.query(Album).filter(Album.titulo == titulo_album1).first()
        consulta2 = self.session.query(Album).filter(Album.id == 2).first()
        self.assertEqual(consulta1.titulo, titulo_album1)
        self.assertIsNotNone(consulta2)

    def test_editar_album(self):
        nueva_descripcion_album = self.data_factory.sentence()
        self.coleccion.editar_album(2, "Clara luna-Mix", 2013, nueva_descripcion_album, "DISCO")
        consulta = self.session.query(Album).filter(Album.id == 2).first()
        self.assertIsNot(consulta.titulo, "Live Killers")

    def test_eliminar_album(self):
        self.coleccion.eliminar_album(1)
        consulta = self.session.query(Album).filter(Album.id == 1).first()
        self.assertIsNone(consulta)

    def test_dar_albumes(self):
        consulta1 = self.coleccion.dar_albumes()
        titulo_album = self.data_factory.name()
        anio_album = self.data_factory.year()
        descripcion_album = self.data_factory.sentence()
        self.coleccion.agregar_album(titulo_album, anio_album, descripcion_album, "CD")
        consulta2 = self.coleccion.dar_albumes()
        self.assertGreaterEqual(len(consulta2), len(consulta1))

    def test_dar_album_por_id(self):
        titulo_album = self.data_factory.name()
        anio_album = self.data_factory.year()
        descripcion_album = self.data_factory.sentence()
        self.coleccion.agregar_album(titulo_album, anio_album, descripcion_album, "CASETE")
        album_id = self.session.query(Album).filter(Album.titulo == titulo_album).first().id
        consulta = self.coleccion.dar_album_por_id(album_id)["titulo"]
        self.assertEqual(consulta, titulo_album)

    def test_buscar_albumes_por_titulo(self):
        consulta1 = self.coleccion.buscar_albumes_por_titulo("clara luna")
        anio_album = self.data_factory.year()
        descripcion_album = self.data_factory.sentence()
        self.coleccion.agregar_album("Clara luna-Instrumental", anio_album, descripcion_album, "CD")
        consulta2 = self.coleccion.buscar_albumes_por_titulo("clara luna")
        self.assertLessEqual(len(consulta1), len(consulta2))
    
    def test_dar_medios(self):
        medios_esperados = ['DISCO', 'CASETE', 'CD']
        medios = self.coleccion.dar_medios()
        self.assertEqual(medios, medios_esperados, "Los medios devueltos no coinciden con los esperados")

    # Prueba unitaria para la función buscar_albumes_por_titulo
    def test_buscar_albumes_por_titulo(self):
        # Agregar álbumes de prueba
        titulo_album1 = "Álbum Prueba"
        anio_album1 = 2021
        descripcion_album1 = "Descripción de prueba"
        self.coleccion.agregar_album(titulo_album1, anio_album1, descripcion_album1, "CD")

        titulo_album2 = "Álbum Experimental"
        anio_album2 = 2020
        descripcion_album2 = "Otro álbum de prueba"
        self.coleccion.agregar_album(titulo_album2, anio_album2, descripcion_album2, "DISCO")

        # Buscar álbum por un título parcial
        resultados = self.coleccion.buscar_albumes_por_titulo("Prueba")
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0]['titulo'], titulo_album1, "El título del álbum no coincide con el esperado")

        # Buscar álbum por un título exacto
        resultados = self.coleccion.buscar_albumes_por_titulo("Álbum Experimental")
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0]['titulo'], titulo_album2, "El título del álbum no coincide con el esperado")
    