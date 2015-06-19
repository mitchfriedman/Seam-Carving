from PIL import Image as PILImage
from image import Image
import argparse

class Carver(object):

    def __init__(self, img_path):
        try:
            self.original_image = PILImage.open(img_path)
        except Exception:
            raise Exception("File Not Found")

        self.image = Image(self.original_image.size)
        self.image.set_from_pil_image(self.original_image.load())

    def build_graph(self, image):
        return [[image.get_energy_of_pixel(image, x, y) for x in range(image.width+1)] for y in range(image.height+1)]

    def get_shortest_vertical_path(self, graph):
        shortest = -1
        position = -1
        for i in range(len(graph[0])):
            column_sum = 0
            for j in range(len(graph)):
                column_sum += graph[j][i]

            if position < 0 or column_sum <= shortest:
                shortest = column_sum
                position = i

        return position

    def remove_shortest_seams(self, image, seams_to_remove):
        graph = self.build_graph(image)

        for i in range(seams_to_remove):
            col_to_remove = self.get_shortest_vertical_path(graph)
            graph = self._remove_column_from_graph(image.color_matrix, graph, col_to_remove)

        image.width -= seams_to_remove
        return graph

    def shrink_image(self, by=None):
        by = by or 0
        self.remove_shortest_seams(self.image, by)

        self.write_new_image('new_image.png', self.image)

    def write_new_image(self, image_name, image):
        im = PILImage.new("RGB", (image.width, image.height))
        pixels = im.load()
        for i in range(image.width):
            for j in range(image.height):
                pixels[i, j] = image.get_pixel((i, j))

        im.save(image_name, "png")

    def _remove_column_from_graph(self, color_matrix, graph, column):
        for i in range(len(graph)):
            graph[i].pop(column)
            color_matrix[i].pop(column)

        return graph


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="The image you wish to parse, relative to this path")
    args = parser.parse_args()

    carver = Carver(args.name)
    carver.shrink_image(by=100)
