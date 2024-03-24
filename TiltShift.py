#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gimpfu import *

def apply_tilt_shift(image, drawable, blur_radius, focus_x, focus_y, focus_radius, sharpness):
    if len(image.layers) > 1:
        gimp.message("Nie można zastosować efektu na zmodyfikowanym obrazie. Proszę wgrać nowy obraz lub cofnąć modyfikację.")

        return

    layer = pdb.gimp_image_get_active_layer(image)

    layer_copy = pdb.gimp_layer_copy(layer, True)
    pdb.gimp_image_insert_layer(image, layer_copy, None, 0)
    pdb.plug_in_gauss_rle(image, layer_copy, blur_radius, blur_radius, True)

    if layer_copy.mask:
        pdb.gimp_item_delete(layer_copy.mask)

    layer_mask = pdb.gimp_layer_create_mask(layer_copy, ADD_BLACK_MASK)
    pdb.gimp_layer_add_mask(layer_copy, layer_mask)

    pdb.gimp_palette_set_foreground((255, 255, 255))
    pdb.gimp_context_push()
    pdb.gimp_context_set_opacity(100)
    pdb.gimp_edit_blend(layer_mask, CUSTOM_MODE, NORMAL_MODE, GRADIENT_RADIAL, 100, 0, REPEAT_NONE, False, False, 0, 0,
                        True, focus_x, focus_y, focus_x - focus_radius, focus_y)
    pdb.gimp_context_pop()

    if sharpness > 0:
        pdb.plug_in_unsharp_mask(image, layer_copy, sharpness, 1.5, 0)

    pdb.gimp_image_select_item(image, CHANNEL_OP_REPLACE, layer_mask)
    pdb.gimp_selection_none(image)

    layer_copy.update(0, 0, image.width, image.height)
    gimp.displays_flush()


register(
    "python_tilt_shift",
    "Tilt shift",
    "Tilt shift effect",
    "PiotrM_WSTKT",
    "PiotrM_WSTKT",
    "2024",
    "Tilt_Shift",
    "*",
    [
        (PF_IMAGE, "image", "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None),
        (PF_SLIDER, "blur_radius", "Blur Radius", 5.0, (0.1, 100.0, 0.1)),
        (PF_INT, "focus_x", "Focus X (0-Image Width)", 0),
        (PF_INT, "focus_y", "Focus Y (0-Image Height)", 0),
        (PF_SLIDER, "focus_radius", "Focus Radius", 100.0, (0.1, 400.0, 0.1)),
        (PF_SLIDER, "sharpness", "Sharpness", 0.0, (0.0, 2.0, 0.1)),
    ],
    [],
    apply_tilt_shift,
    menu="<Image>/Filters/WSTKT"
)

main()