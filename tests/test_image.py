import unittest
from tests import create_test_image


class TestImage(unittest.TestCase):
    def test_x_grad_middle(self):
        image = create_test_image()

        x_grad_1_2 = image.calculate_x_gradient(image, 1, 2)  # row 3 in test matrix
        expected = (205 - 203)**2 + (255 - 51) ** 2
        self.assertEqual(x_grad_1_2, expected)

    def test_x_grad_top_left_corner(self):
        image = create_test_image()
        x_grad_0_0 = image.calculate_x_gradient(image, 0, 0)
        expected = (153 - 255) ** 2

        self.assertEqual(expected, x_grad_0_0)

    def test_x_grad_bottom_right_corner(self):
        image = create_test_image()
        x_grad_2_3 = image.calculate_x_gradient(image, 2, 3)
        expected = (153 - 51) ** 2

        self.assertEqual(expected, x_grad_2_3)

    def test_y_grad_middle(self):
        image = create_test_image()

        y_grad_1_2 = image.calculate_y_gradient(image, 1, 2)

        expected = (255 - 153) ** 2

        self.assertEqual(expected, y_grad_1_2)

    def test_y_grad_top_left(self):
        image = create_test_image()

        y_grad_0_0 = image.calculate_y_gradient(image, 0, 0)
        expected = (255 - 153) ** 2

        self.assertEqual(expected, y_grad_0_0)

    def test_y_grad_bottom_right(self):
        image = create_test_image()

        y_grad_2_3 = image.calculate_y_gradient(image, 2, 3)
        expected = (205 - 101) ** 2
        self.assertEqual(expected, y_grad_2_3)

    def test_get_energy(self):
        image = create_test_image()

        expected = ((153 - 255) ** 2)**2 + ((255 - 153) ** 2)**2

        self.assertEqual(expected, image.get_energy_of_pixel(image, 0, 0))
