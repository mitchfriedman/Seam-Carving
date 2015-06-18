import unittest
from copy import deepcopy
from seam_carving import Carver, Image


carver = Carver("test.jpeg")

class TestCarver(unittest.TestCase):

    test_matrix = [
        [(255,101,51), (255,101,153), (255,101,255)],
        [(255,153,51), (255,153,153), (255,153,255)],
        [(255,203,51), (255,204,153), (255,205,255)],
        [(255,255,51), (255,255,153), (255,255,255)]
    ]

    graph = [
        [
            ((153 - 255)**2)**2 + ((255 - 153)**2)**2,  # row 1
            ((255 -  51)**2)**2 + ((255 - 153)**2)**2,  # row 1
            ((153 -  51)**2)**2 + ((255 - 153)**2)**2], # row 1
        [
            ((255 - 153)**2)**2 + ((203 - 101)**2)**2, # row 2
            ((255 -  51)**2)**2 + ((204 - 101)**2)**2, # row 2
            ((153 -  51)**2)**2 + ((205 - 101)**2)**2],# row 2
        [
            ((205 - 204)**2 + (255 - 153)**2)**2 + ((255 - 153)**2)**2, # row 3
            ((205 - 203)**2 + (255 -  51)**2)**2 + ((255 - 153)**2)**2, # row 3
            ((204 - 203)**2 + (153 -  51)**2)**2 + ((255 - 153)**2)**2  # row 3
        ],
        [
            ((255 - 153)**2)**2 + ((203 - 101)**2)**2, # row 4
            ((255 -  51)**2)**2 + ((204 - 101)**2)**2, # row 4
            ((153 -  51)**2)**2 + ((205 - 101)**2)**2  # row 4
        ]
    ]

    def _get_shortest_seam_index(self):
        sums = []
        for i in range(3):
            sums.append(reduce(lambda x, y: x + y, self.graph[i]))
        pos = sums.index(min(sums))
        return pos


    def _create_test_image(self):
        image = Image((3, 4))

        for i in range(4):
            for j in range(3):
                image.set_pixel((j, i), self.test_matrix[i][j])

        return image

    def test_create_image(self):
        image = self._create_test_image()
        self.assertEqual(self.test_matrix, image.color_matrix)

    def test_x_grad_middle(self):
        image = self._create_test_image()

        x_grad_1_2 = carver.x_grad(image, 1, 2)

        # row 3 in test matrix
        expected = (205 - 203)**2 + (255 - 51) ** 2

        self.assertEqual(x_grad_1_2, expected)

    def test_x_grad_top_left_corner(self):
        image = self._create_test_image()

        x_grad_0_0 = carver.x_grad(image, 0, 0)

        expected = (153 - 255) ** 2

        self.assertEqual(expected, x_grad_0_0)

    def test_x_grad_bottom_right_corner(self):
        image = self._create_test_image()

        x_grad_2_3 = carver.x_grad(image, 2, 3)

        expected = (153 - 51) ** 2

        self.assertEqual(expected, x_grad_2_3)

    def test_y_grad_middle(self):
        image = self._create_test_image()

        y_grad_1_2 = carver.y_grad(image, 1, 2)

        expected = (255 - 153) ** 2

        self.assertEqual(expected, y_grad_1_2)

    def test_y_grad_top_left(self):
        image = self._create_test_image()

        y_grad_0_0 = carver.y_grad(image, 0, 0)
        expected = (255 - 153) ** 2

        self.assertEqual(expected, y_grad_0_0)

    def test_y_grad_bottom_right(self):
        image = self._create_test_image()

        y_grad_2_3 = carver.y_grad(image, 2, 3)
        expected = (205 - 101) ** 2
        self.assertEqual(expected, y_grad_2_3)

    def test_get_energy(self):
        image = self._create_test_image()

        expected = ((153 - 255) ** 2)**2 + ((255 - 153) ** 2)**2

        self.assertEqual(expected, carver.get_energy_of_pixel(image, 0, 0))

    def test_build_graph(self):
        image = self._create_test_image()

        test_against = carver.build_graph(image)
        self.assertEqual(self.graph, carver.build_graph(image))

    def test_get_shortest_path(self):
        image = self._create_test_image()

        self.assertEqual(carver.get_shortest_path(self.graph), self._get_shortest_seam_index())

    def test_remove_first_column(self):
        matrix = deepcopy(self.test_matrix)
        copy = deepcopy(self.graph[:])
        original = deepcopy(self.graph[:])

        copy[0].pop(0)
        copy[1].pop(0)
        copy[2].pop(0)
        copy[3].pop(0)

        self.assertEqual(copy, carver._remove_column_from_graph(matrix, original, 0))

    def test_remove_last_column(self):
        matrix = deepcopy(self.test_matrix)

        copy = deepcopy(self.graph[:])
        original = deepcopy(self.graph[:])

        copy[0].pop(2)
        copy[1].pop(2)
        copy[2].pop(2)
        copy[3].pop(2)


        self.assertEqual(copy, carver._remove_column_from_graph(matrix, original, 2))

    def test_remove_one_seam(self):
        image = self._create_test_image()
        graph_copy = deepcopy(self.graph)
        matrix_copy = deepcopy(self.test_matrix)

        self.assertEqual(carver._remove_column_from_graph(matrix_copy, graph_copy, 0),
                         carver.remove_shortest_seams(image, 1))


