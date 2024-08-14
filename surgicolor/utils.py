import streamlit as st
from PIL import Image, ImageDraw
import numpy as np

def load_image(image_path):
    """
    Load the original and colored version of an image.
    Assumes that the original image and the colored one are stored together.
    """
    image_orig = Image.open(image_path)
    image_colored_path = image_path.replace('orig', 'colored')
    image_colored = Image.open(image_colored_path)
    return image_orig, image_colored

def draw_on_canvas(structure_name):
    """
    Draw on a canvas using Streamlit's drawing canvas widget.
    """
    canvas_width = 400
    canvas_height = 400

    # Create an empty image
    image = Image.new("RGBA", (canvas_width, canvas_height), "white")
    draw = ImageDraw.Draw(image)

    # Add a drawing canvas
    canvas_result = st.canvas(
        stroke_width=3,
        stroke_color='rgba(255, 0, 0, 1.0)',
        background_color="rgba(0, 0, 0, 0)",
        update_streamlit=True,
        height=canvas_height,
        width=canvas_width,
        drawing_mode="freedraw",
        key="canvas"
    )

    if canvas_result.image_data is not None:
        image = Image.fromarray(canvas_result.image_data.astype("uint8"), "RGBA")

    return image
