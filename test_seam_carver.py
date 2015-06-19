import unittest
from copy import deepcopy
from seam_carving import Carver, Image, Pixel

test_matrix = [
    [(255, 101, 51), (255, 101, 153), (255, 101, 255)],
    [(255, 153, 51), (255, 153, 153), (255, 153, 255)],
    [(255, 203, 51), (255, 204, 153), (255, 205, 255)],
    [(255, 255, 51), (255, 255, 153), (255, 255, 255)]
]

graph = [
    [
        ((153 - 255)**2)**2 + ((255 - 153)**2)**2,  # row 1
        ((255 - 51)**2)**2 + ((255 - 153)**2)**2,   # row 1
        ((153 - 51)**2)**2 + ((255 - 153)**2)**2],  # row 1
    [
        ((255 - 153)**2)**2 + ((203 - 101)**2)**2,  # row 2
        ((255 - 51)**2)**2 + ((204 - 101)**2)**2,   # row 2
        ((153 - 51)**2)**2 + ((205 - 101)**2)**2],  # row 2
    [
        ((205 - 204)**2 + (255 - 153)**2)**2 + ((255 - 153)**2)**2,  # row 3
        ((205 - 203)**2 + (255 - 51)**2)**2 + ((255 - 153)**2)**2,  # row 3
        ((204 - 203)**2 + (153 - 51)**2)**2 + ((255 - 153)**2)**2   # row 3
    ],
    [
        ((255 - 153)**2)**2 + ((203 - 101)**2)**2,  # row 4
        ((255 - 51)**2)**2 + ((204 - 101)**2)**2,  # row 4
        ((153 - 51)**2)**2 + ((205 - 101)**2)**2   # row 4
    ]
]


def get_shortest_seam_index():
    sums = []
    for i in range(3):
        sums.append(reduce(lambda x, y: x + y, graph[i]))
    pos = sums.index(min(sums))
    return pos


def create_test_image():
    image = Image((3, 4))

    for i in range(4):
        for j in range(3):
            image.set_pixel((j, i), Pixel(i, j, test_matrix[i][j]))

    return image


carver = Carver("test.jpeg")


class TestImage(unittest.TestCase):
    def test_x_grad_middle(self):
        image = create_test_image()

        x_grad_1_2 = image.x_grad(image, 1, 2)  # row 3 in test matrix
        expected = (205 - 203)**2 + (255 - 51) ** 2
        self.assertEqual(x_grad_1_2, expected)

    def test_x_grad_top_left_corner(self):
        image = create_test_image()
        x_grad_0_0 = image.x_grad(image, 0, 0)
        expected = (153 - 255) ** 2

        self.assertEqual(expected, x_grad_0_0)

    def test_x_grad_bottom_right_corner(self):
        image = create_test_image()
        x_grad_2_3 = image.x_grad(image, 2, 3)
        expected = (153 - 51) ** 2

        self.assertEqual(expected, x_grad_2_3)

    def test_y_grad_middle(self):
        image = create_test_image()

        y_grad_1_2 = image.y_grad(image, 1, 2)

        expected = (255 - 153) ** 2

        self.assertEqual(expected, y_grad_1_2)

    def test_y_grad_top_left(self):
        image = create_test_image()

        y_grad_0_0 = image.y_grad(image, 0, 0)
        expected = (255 - 153) ** 2

        self.assertEqual(expected, y_grad_0_0)

    def test_y_grad_bottom_right(self):
        image = create_test_image()

        y_grad_2_3 = image.y_grad(image, 2, 3)
        expected = (205 - 101) ** 2
        self.assertEqual(expected, y_grad_2_3)

    def test_get_energy(self):
        image = create_test_image()

        expected = ((153 - 255) ** 2)**2 + ((255 - 153) ** 2)**2

        self.assertEqual(expected, image.get_energy_of_pixel(image, 0, 0))


class TestCarver(unittest.TestCase):

    def test_create_image(self):
        image = create_test_image()
        for i in range(len(test_matrix[0])):
            for j in range(len(test_matrix)):
                self.assertEqual(test_matrix[j][i], image.get_pixel((i, j)))

    def test_build_graph(self):
        image = create_test_image()
        self.assertEqual(graph, carver.build_graph(image))

    def test_get_shortest_vertical_path(self):
        self.assertEqual(carver.get_shortest_vertical_path(graph), get_shortest_seam_index())

    def test_remove_first_column(self):
        matrix = deepcopy(test_matrix)
        copy = deepcopy(graph[:])
        original = deepcopy(graph[:])

        for i in range(4):
            copy[i].pop(0)

        self.assertEqual(copy, carver._remove_column_from_graph(matrix, original, 0))

    def test_remove_last_column(self):
        matrix = deepcopy(test_matrix)

        copy = deepcopy(graph[:])
        original = deepcopy(graph[:])

        for i in range(4):
            copy[i].pop(2)

        self.assertEqual(copy, carver._remove_column_from_graph(matrix, original, 2))

    def test_remove_one_seam(self):
        image = create_test_image()
        graph_copy = deepcopy(graph)
        matrix_copy = deepcopy(test_matrix)

        self.assertEqual(carver._remove_column_from_graph(matrix_copy, graph_copy, 0),
                         carver.remove_shortest_seams(image, 1))
