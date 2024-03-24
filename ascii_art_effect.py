#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gimpfu import *
import random

def apply_blur(image, drawable, blur_radius):
    pdb.plug_in_gauss(image, drawable, blur_radius, blur_radius, TRUE)

def ascii_art_effect(image, drawable, ascii_chars, font_size, use_random_chars, scale_factor, horizontal_spacing, vertical_spacing, blur_radius):
    if len(image.layers) > 1:
        gimp.message("Nie można zastosować efektu na zmodyfikowanym obrazie. Proszę wgrać nowy obraz lub cofnąć modyfikację.")
        return

    font_name = "MonospaceBold"
    font_size = int(font_size)
    use_random = (use_random_chars == 1)
    scale_factor = float(scale_factor)
    horizontal_spacing = int(horizontal_spacing)
    vertical_spacing = int(vertical_spacing)

    ascii_chars_list = list(ascii_chars)

    pdb.gimp_image_undo_group_start(image)
    pdb.gimp_context_push()
    pdb.gimp_image_undo_disable(image)

    blur_layer = pdb.gimp_layer_new_from_drawable(drawable, image)
    pdb.gimp_image_insert_layer(image, blur_layer, None, 0)
    apply_blur(image, blur_layer, blur_radius)

    if scale_factor != 1.0:
        scaled_width = int(image.width * scale_factor)
        scaled_height = int(image.height * scale_factor)
        pdb.gimp_image_scale(image, scaled_width, scaled_height)

    ascii_layer = pdb.gimp_layer_new_from_drawable(drawable, image)
    pdb.gimp_image_insert_layer(image, ascii_layer, None, 0)
    pdb.gimp_edit_fill(ascii_layer, BACKGROUND_FILL)

    for y in range(0, image.height, font_size + vertical_spacing):
        for x in range(0, image.width, font_size + horizontal_spacing):
            pixel = pdb.gimp_image_pick_color(image, blur_layer, x, y, False, False, 0)
            if pixel is not None:

                char_to_draw = random.choice(ascii_chars_list) if use_random else ascii_chars_list[0]
                pdb.gimp_context_set_foreground(pixel)
                pdb.gimp_text_fontname(image, ascii_layer, x, y - font_size // 2, char_to_draw, 0, True, font_size, PIXELS, font_name)

    image.remove_layer(blur_layer)

    pdb.gimp_context_pop()
    pdb.gimp_image_undo_enable(image)
    pdb.gimp_image_undo_group_end(image)
    gimp.displays_flush()

def plugin_registration():
    plugin_menu = "<Image>/Filters/WSTKT"

register(
    "python_ascii_art_effect",
    "ASCII Art Effect",
    "Applies an ASCII art effect to the image.",
    "PiotrM_WSTKT",
    "PiotrM_WSTKT",
    "2024",
    "ASCII Art",
    "*",
    [
        (PF_IMAGE, "image", "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None),
        (PF_STRING, "ascii_chars", "ASCII Characters", "#@#Default ASCII Characters", ""),
        (PF_INT, "font_size", "Font Size", 20),
        (PF_TOGGLE, "use_random_chars", "Use Random Characters", False),
        (PF_FLOAT, "scale_factor", "Scale Factor", 1.0),
        (PF_INT, "horizontal_spacing", "Horizontal Spacing", 0),
        (PF_INT, "vertical_spacing", "Vertical Spacing", 0),
        (PF_SLIDER, "blur_radius", "Blur Radius", 5.0, (0.1, 100.0, 0.1)),
    ],
    [],
    ascii_art_effect,
    menu="<Image>/Filters/WSTKT"
)

main()