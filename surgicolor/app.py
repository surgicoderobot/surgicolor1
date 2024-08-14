import streamlit as st
import os
import random
from PIL import Image
import numpy as np
from streamlit_drawable_canvas import st_canvas

# Title of the app
st.title("CholecSeg8k Image Coloring Game")

# List of available structures and their corresponding colors
structures = {
    "Gallbladder": "#ff0000",  # Red
    "Cystic Pedicle": "#00ff00",  # Green
    "Omentum": "#0000ff",  # Blue
    "Duodenum": "#ffff00",  # Yellow
    "Abdominal Wall": "#ff00ff",  # Magenta
    "Cystic Duct": "#00ffff",  # Cyan
    "Cystic Artery": "#ff7f00",  # Orange
    "Grasper": "#7f00ff",  # Purple
    "L-hook Electrocautery": "#ff007f",  # Pink
    "Liver": "#7f7f00",  # Olive
    "Blood": "#00007f",  # Dark Blue
    "Connective Tissue": "#7f0000",  # Dark Red
    "Gastrointestinal Tract": "#007f00",  # Dark Green
    "Bipolar": "#007f7f",  # Teal
    "Irrigator": "#7f7f7f",  # Gray
    "Clipper": "#ff00ff",  # Fuchsia
    "Scissors": "#00ff00"   # Lime
}

# Function to find matching images in the archive
def find_image_set(structure_name):
    while True:
        archive_path = random.choice(os.listdir('surgicolor/image_data'))
        full_archive_path = f'surgicolor/image_data/{archive_path}'
        
        # Check if the necessary images exist
        if os.path.exists(f'{full_archive_path}/image.png') and os.path.exists(f'{full_archive_path}/{structure_name}.png'):
            original_image = f'{full_archive_path}/image.png'
            colored_image = f'{full_archive_path}/{structure_name}.png'
            return original_image, colored_image

# Function to save the colored image
def save_colored_image(image, structure_name, image_number):
    filename = f'colored_{structure_name.lower().replace(" ", "_")}_{image_number}.png'
    image.save(filename)
    st.success(f'Image saved as {filename}')

# Initialize session state
if "structure_index" not in st.session_state:
    st.session_state.structure_index = -1
    st.session_state.image_number = 1

# Get a new structure and image set when the button is clicked
if st.button('Go to Next Image') or st.session_state.structure_index == -1:
    # Choose a new structure
    st.session_state.structure_index = (st.session_state.structure_index + 1) % len(structures)
    st.session_state.current_structure = list(structures.keys())[st.session_state.structure_index]
    st.session_state.current_color = structures[st.session_state.current_structure]
    
    # Get a new set of images for the new structure
    st.session_state.image_set = [find_image_set(st.session_state.current_structure) for _ in range(2)]
    st.session_state.current_image_index = 0
    
    # Reset the canvas
    st.session_state.canvas_key = f"canvas_{st.session_state.structure_index}"
    st.session_state.image_number += 1

# Display images in 2 sets
for i, (original, colored) in enumerate(st.session_state.image_set):
    col1, col2 = st.columns(2)
    with col1:
        st.image(original, caption=f'Original Image {i + 1}', use_column_width=True)
    with col2:
        st.image(colored, caption=f'Colored Structure Image {i + 1} ({st.session_state.current_structure})', use_column_width=True)

# Display a third image with the same structure for the player to color
third_image_path = st.session_state.image_set[st.session_state.current_image_index][0]
print(third_image_path)

st.write(f"Now, color the selected structure '{st.session_state.current_structure}' in the image below:")

# Load the third image
third_image = Image.open(third_image_path)

# Convert the image to a format suitable for Streamlit canvas
image_array = np.array(third_image)

# Drawing canvas directly on the third image
canvas_result = st_canvas(
    fill_color=st.session_state.current_color,  # Use the color specific to the selected structure
    stroke_width=20,
    stroke_color=st.session_state.current_color,
    background_image=third_image,  # Set the third image as the background
    height=image_array.shape[0],
    width=image_array.shape[1],
    drawing_mode="freedraw",
    key=st.session_state.canvas_key
)

# Save and show the colored image
if st.button('Save and Next'):
    if canvas_result.image_data is not None:
        # Convert canvas drawing data to a PIL image
        drawing_image = Image.fromarray(canvas_result.image_data)
        
        # Ensure drawing image has the same size as the original image
        drawing_image = drawing_image.resize(third_image.size)
        
        # Convert the drawing image to numpy array
        drawing_array = np.array(drawing_image.convert("RGBA"))
        
        # Combine the original image with the drawing
        combined_image = np.where(
            drawing_array[:, :, 3:] != 0,  # If drawing data is not transparent
            drawing_array[:, :, :3],  # Use the drawing image
            image_array  # Otherwise use the original image
        )
        
        # Convert back to PIL Image
        combined_pil_image = Image.fromarray(combined_image)
        
        # Save the image with the structure name and image number
        save_colored_image(combined_pil_image, st.session_state.current_structure, st.session_state.image_number)
        
        # Display the combined image
        st.image(combined_pil_image, caption=f'Your Colored Image {st.session_state.image_number}', use_column_width=True)
        
        # Reset the canvas and image index for the next structure
        st.session_state.current_image_index = (st.session_state.current_image_index + 1) % len(st.session_state.image_set)
        if st.session_state.current_image_index == 0:
            st.session_state.structure_index = (st.session_state.structure_index + 1) % len(structures)
            st.session_state.current_structure = list(structures.keys())[st.session_state.structure_index]
            st.session_state.current_color = structures[st.session_state.current_structure]
            st.session_state.image_set = [find_image_set(st.session_state.current_structure) for _ in range(2)]
            st.session_state.image_number += 1
            st.session_state.canvas_key = f"canvas_{st.session_state.structure_index}"
