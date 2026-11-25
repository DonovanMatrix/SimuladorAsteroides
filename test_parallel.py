
import unittest

from models import Nave, Asteroide
from parallel import (
    detectar_colisiones_paralelo,
    procesar_grupo
)


class TestParallel(unittest.TestCase):

    def setUp(self):
        self.nave = Nave(
            x=0,
            y=0,
            radio=5,
            velocidad=2
        )

        self.asteroides = (
            Asteroide(1, 3, 0, 1, 1, 2),
            Asteroide(2, 20, 20, 1, 1, 2),
            Asteroide(3, 0, 0, 1, 1, 3),
            Asteroide(4, 15, 15, 1, 1, 1)
        )

    def test_detecta_colisiones_secuenciales(self):
        resultado = procesar_grupo(
            (self.nave, self.asteroides)
        )

        self.assertEqual(resultado, [1, 3])

    def test_detecta_colisiones_paralelas(self):
        resultado = detectar_colisiones_paralelo(
            self.nave,
            self.asteroides,
            num_procesos=2
        )

        self.assertEqual(resultado, [1, 3])

    def test_lista_vacia(self):
        resultado = detectar_colisiones_paralelo(
            self.nave,
            (),
            num_procesos=2
        )

        self.assertEqual(resultado, [])

    def test_un_solo_proceso(self):
        resultado = detectar_colisiones_paralelo(
            self.nave,
            self.asteroides,
            num_procesos=1
        )

        self.assertEqual(resultado, [1, 3])

    def test_resultados_secuenciales_y_paralelos(self):
        secuencial = procesar_grupo(
            (self.nave, self.asteroides)
        )

        paralelo = detectar_colisiones_paralelo(
            self.nave,
            self.asteroides,
            num_procesos=2
        )

        self.assertEqual(secuencial, paralelo)


if __name__ == "__main__":
    unittest.main()
