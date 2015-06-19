import unittest
from copy import deepcopy
from seamcarver.seam_carving import Carver
from tests import (
    create_test_image,
    test_matrix,
    test_graph,
    get_shortest_seam_index
)


class TestCarver(unittest.TestCase):

    carver = Carver("../test.jpeg")

    def test_create_image(self):
        image = create_test_image()
        for i in range(len(test_matrix[0])):
            for j in range(len(test_matrix)):
                self.assertEqual(test_matrix[j][i], image.get_pixel((i, j)))

    def test_build_graph(self):
        image = create_test_image()
        self.assertEqual(test_graph, self.carver.build_graph(image))

    def test_get_shortest_vertical_path(self):
        self.assertEqual(self.carver.get_shortest_vertical_path(test_graph), get_shortest_seam_index())

    def test_remove_first_column(self):
        matrix = deepcopy(test_matrix)
        copy = deepcopy(test_graph[:])
        original = deepcopy(test_graph[:])

        for i in range(4):
            copy[i].pop(0)

        self.assertEqual(copy, self.carver._remove_column_from_graph(matrix, original, 0))

    def test_remove_last_column(self):
        matrix = deepcopy(test_matrix)

        copy = deepcopy(test_graph[:])
        original = deepcopy(test_graph[:])

        for i in range(4):
            copy[i].pop(2)

        self.assertEqual(copy, self.carver._remove_column_from_graph(matrix, original, 2))

    def test_remove_one_seam(self):
        image = create_test_image()
        graph_copy = deepcopy(test_graph)
        matrix_copy = deepcopy(test_matrix)

        self.assertEqual(self.carver._remove_column_from_graph(matrix_copy, graph_copy, 0),
                         self.carver.remove_shortest_seams(image, 1))
