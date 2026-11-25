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


if __name__ == "__main__":
    unittest.main()