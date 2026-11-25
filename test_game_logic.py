from models import Asteroide, Nave
from game_logic import actualizar_asteroides, detectar_colisiones_nave
import unittest
from game_logic import detectar_colision


class TestGameLogic(unittest.TestCase):

    def test_colision_detectada(self):
        self.assertTrue(
            detectar_colision((0, 0), 5, (3, 0), 2)
        )

    def test_sin_colision(self):
        self.assertFalse(
            detectar_colision((0, 0), 2, (10, 10), 2)
        )

    def test_colision_exacta(self):
        self.assertTrue(
            detectar_colision((0, 0), 5, (7, 0), 2)
        )

    def test_asteroides_en_misma_posicion(self):
        self.assertTrue(
            detectar_colision((0, 0), 2, (0, 0), 3)
        )

    def test_asteroides_lejanos(self):
        self.assertFalse(
            detectar_colision((0, 0), 1, (100, 100), 1)
        )

    def test_colision_con_distancias_negativas(self):
        self.assertTrue(
            detectar_colision((0, 0), 5, (-3, 0), 2)
        )
    def test_movimiento_asteroide(self):
        asteroide = Asteroide(1, 10, 20, 5, 10, 3)

        resultado = actualizar_asteroides(
            (asteroide,), 2, 100, 100
        )

        self.assertEqual(resultado[0].x, 20)
        self.assertEqual(resultado[0].y, 40)

    def test_asteroide_sale_por_limite(self):
        asteroide = Asteroide(1, 95, 95, 10, 10, 3)

        resultado = actualizar_asteroides(
            (asteroide,), 1, 100, 100
        )

        self.assertEqual(resultado[0].x, 5)
        self.assertEqual(resultado[0].y, 5)

    def test_colision_con_nave(self):
        nave = Nave(10, 10, 5, 4)
        asteroide = Asteroide(1, 13, 10, 0, 0, 2)

        resultado = detectar_colisiones_nave(
            nave, (asteroide,)
        )

        self.assertEqual(resultado, (1,))

    def test_sin_colision_con_nave(self):
        nave = Nave(10, 10, 2, 4)
        asteroide = Asteroide(1, 50, 50, 0, 0, 3)

        resultado = detectar_colisiones_nave(
            nave, (asteroide,)
        )

        self.assertEqual(resultado, ())

if __name__ == "__main__":
    unittest.main()