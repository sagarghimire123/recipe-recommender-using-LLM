import streamlit as st
from langchain import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI API with the API key
llm = OpenAI(api_key=openai_api_key)

# Function to get recipe recommendations
def get_recipes(input_recipe):
    prompt = f"You are a recipe recommender. Please suggest at least 10 recipes for {input_recipe}."
    response = llm(prompt)
    
    if isinstance(response, str):
        recipes = response.strip().split('\n')
        formatted_recipes = [f"{i + 1}. {recipe.strip()}" for i, recipe in enumerate(recipes) if recipe.strip()]
        return formatted_recipes[:10]  # Ensure only 10 recipes are returned
    else:
        st.error("Error: Received an unexpected response format.")
        return []

# Function to get details of a selected recipe
def get_recipe_details(selected_recipe):
    prompt = f"Provide complete details of the recipe: {selected_recipe}."
    response = llm(prompt)
    
    if isinstance(response, str):
        return f"**Details for {selected_recipe}:**\n{response}"
    else:
        st.error("Error: Received an unexpected response format.")
        return "No details available."

# Streamlit UI
st.title("Recipe Recommender")

# Initialize session state for recipes and selected recipe
if 'recipes' not in st.session_state:
    st.session_state.recipes = []
if 'selected_recipe' not in st.session_state:
    st.session_state.selected_recipe = None
if 'show_details' not in st.session_state:
    st.session_state.show_details = False
if 'recipe_names' not in st.session_state:
    st.session_state.recipe_names = []

# User input for recipe
input_recipe = st.text_input("Enter a recipe or cuisine you want recommendations for:")

# Button to get recommendations
if st.button("Get Recommendations"):
    if input_recipe:
        st.session_state.recipes = get_recipes(input_recipe)  # Update recipes in session state
        st.session_state.selected_recipe = None  # Reset selected recipe
        st.session_state.show_details = False  # Reset details display flag
        
        if st.session_state.recipes:
            # Create a list of recipe names for dropdown
            st.session_state.recipe_names = [recipe.split('. ', 1)[1] for recipe in st.session_state.recipes]
            st.session_state.recipe_names.insert(0, "")  # Add an empty string for the default option
        else:
            st.error("No recipes found. Please try again.")
    else:
        st.error("Please enter a recipe or cuisine.")

# Dropdown for recipe selection
if st.session_state.recipe_names:
    selected_recipe_name = st.selectbox("Select a recipe to view details:", options=st.session_state.recipe_names)
    
    if selected_recipe_name and selected_recipe_name != "":
        if selected_recipe_name != st.session_state.selected_recipe:
            st.session_state.selected_recipe = selected_recipe_name
            st.session_state.show_details = True

    # Display recipe details if the user has selected a recipe
    if st.session_state.show_details and st.session_state.selected_recipe:
        details = get_recipe_details(st.session_state.selected_recipe)
        st.write(details)
