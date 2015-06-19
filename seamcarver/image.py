from pixel import Pixel


class Image(object):

    def __init__(self, size):
        self.width = size[0] - 1
        self.height = size[1] - 1
        self.color_matrix = [[0 for _ in range(self.width+1)] for _ in range(self.height+1)]

    def set_from_pil_image(self, pil_image):
        for i in range(self.width+1):
            for j in range(self.height+1):
                self.set_pixel((i, j), Pixel(i, j, pil_image[i, j]))

    def set_pixel(self, position, pixel):
        self.color_matrix[position[1]][position[0]] = pixel

    def get_pixel(self, position):
        return self.color_matrix[position[1]][position[0]].color

    def calculate_x_gradient(self, image, x, y):
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

    def calculate_y_gradient(self, image, x, y):
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
        return ry ** 2 + gy ** 2 + by ** 2

    def get_energy_of_pixel(self, image, x, y):

        x_gradient = self.calculate_x_gradient(image, x, y)
        y_gradient = self.calculate_y_gradient(image, x, y)

        x_gradient_squared = x_gradient ** 2
        y_gradient_squared = y_gradient ** 2

        return x_gradient_squared + y_gradient_squared

