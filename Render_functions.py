import os
import pygame


def load_image(name, path="Images", alpha_cannel=""):
    try:
        fullname = os.path.join(path, name)  # Указываем путь к папке с картинками
    except:
        return None
    try:
        image = pygame.image.load(fullname)  # Загружаем картинку и сохраняем поверхность (Surface)
    except (pygame.error):  # Если картинки нет на месте
        print("Cannot load image:", name)
        return 0
    if(alpha_cannel):
        image = image.convert_alpha()
    else:
        image = image.convert()

    return image


def load_text(text, color=(255, 255, 255), font=None, pt=20):
    return pygame.font.Font(font, pt).render(text, True, color)


def tiled_background(img, res_x, res_y):
    x = 0
    y = 0
    img = load_image(img, alpha_cannel="True")
    surface = pygame.Surface((res_x, res_y))
    size = img.get_rect()[3]
    while True:
        surface.blit(img, (x, y))
        x += size
        if x >= res_x:
            if y >= res_y:
                return surface
            x = 0
            y += size


def scene_render(map_f, map_w, objects, sur):
    y = 0
    for line in map_f:
        x = 0
        for tile in line:
            if tile:
                objects["Floor"][tile].render(sur, x, y)
            x += 1
        y += 1
    y = 0
    for line in map_w:
        x = 0
        for tile in line:
            z = 0
            for dir in tile:
                if dir == 1:
                    if z == 0:
                        objects["Wall"][dir].set_coords((x, y))
                        objects["Wall"][dir].set_rotate("D")
                        objects["Wall"][dir].render(sur)
                    elif z == 1:
                        objects["Wall"][dir].set_coords((x, y))
                        objects["Wall"][dir].set_rotate("L")
                        objects["Wall"][dir].render(sur)
                    elif z == 2:
                        objects["Wall"][dir].set_coords((x, y))
                        objects["Wall"][dir].set_rotate("U")
                        objects["Wall"][dir].render(sur)
                    elif z == 3:
                        objects["Wall"][dir].set_coords((x, y))
                        objects["Wall"][dir].set_rotate("R")
                        objects["Wall"][dir].render(sur)
                z += 1
            x += 1
        y += 1
    sur = pygame.transform.scale(sur, (100*len(map_f[0]), 100*len(map_f)))
    return sur
