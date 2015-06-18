from PIL import Image as PILImage


class Image(object):

    def __init__(self, size):
        self.width = size[0] - 1
        self.height = size[1] - 1

        self.color_matrix = [[0 for _ in range(self.width+1)] for _ in range(self.height+1)]

    def set_from_pil_image(self, pil_image):
        print self.width, self.height
        for i in range(self.width+1):
            for j in range(self.height+1):
                self.set_pixel((i, j), pil_image[i, j])

    def set_pixel(self, position, color_tuple):
        self.color_matrix[position[1]][position[0]] = color_tuple

    def get_pixel(self, position):
        return self.color_matrix[position[1]][position[0]]

class Carver(object):
    
    def __init__(self, img_path):
        self.image = PILImage.open(img_path)
        self.matrix = self.image.load()

    def x_grad(self, image, x, y):
        right = x + 1
        left = x - 1

        if x == 0:
            left = image.width
        elif x == image.width:
            right = 0

        r1, g1, b1 = image.get_pixel((right, y))
        r2, g2, b2 = image.get_pixel((left, y))

        rx = r2-r1
        gx = g2-g1
        bx = b2-b1
        return rx**2 + gx**2 + bx**2

    def y_grad(self, image, x, y):
        top = y - 1
        bottom = y + 1

        if y == 0:
            top = image.height
        elif y == image.height:
            bottom = 0

        r1, g1, b1 = image.get_pixel((x, top))
        r2, g2, b2 = image.get_pixel((x, bottom))

        ry = r2-r1
        gy = g2-g1
        by = b2-b1
        return ry ** 2 + gy **2 + by**2

    def get_energy_of_pixel(self, image, x, y):

        x_gradient = self.x_grad(image, x, y)
        y_gradient = self.y_grad(image, x, y)

        x_gradient_squared = x_gradient ** 2
        y_gradient_squared = y_gradient ** 2

        return x_gradient_squared + y_gradient_squared

    def build_graph(self, image):
        return [[self.get_energy_of_pixel(image, x, y) for x in range(image.width+1)] for y in range(image.height+1)]

    def get_shortest_path(self, graph):
        shortest = -1
        position = -1
        for i in range(len(graph[0])):
            sum = 0
            for j in range(len(graph)):
                sum += graph[j][i]

            if position < 0 or sum <= shortest:
                shortest = sum
                position = i

        return position

    def remove_shortest_seams(self, image, seams_to_remove):

        graph = self.build_graph(image)

        for i in range(seams_to_remove):
            col_to_remove = self.get_shortest_path(graph)
            graph = self._remove_column_from_graph(image.color_matrix, graph, col_to_remove)
            image.width -= 1
        return graph

    def _remove_column_from_graph(self, matrix, graph, column):
        for i in range(len(graph)):
            graph[i].pop(column)
            matrix[i].pop(column)

        return graph

    def resize_image(self, image, width=100):
        self.remove_shortest_seams(image, width)

        im = PILImage.new("RGB", (image.width, image.height))
        pixels = im.load()
        print image.width
        for i in range(image.width):
            for j in range(image.height):
                pixels[i, j] = image.get_pixel((i, j))

        im.save("test123.png", "png")
        print im


if __name__ == '__main__':
    carver = Carver("test.jpeg")
    original_image = Image((carver.image.size[0], carver.image.size[1]))

    original_image.set_from_pil_image(carver.image.load())

    carver.resize_image(original_image, width=100)



