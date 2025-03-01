import google.generativeai as genai
import os

# Load your API key from environment variables
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# Configure the Generative AI client
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-2.0-flash-exp')  # Specify Gemini 2.0 Flash

def search_recipes(ingredients, dietary_restrictions):
    """
    Simulates searching a recipe database based on ingredients and dietary restrictions.
    In a real-world scenario, this would call an actual API.
    """
    #Hardcoded example
    recipes = [
        {"name": "Vegetarian Pasta Primavera", "ingredients": ["pasta", "vegetables"], "dietary_restrictions": ["vegetarian"]},
        {"name": "Chicken Stir-Fry", "ingredients": ["chicken", "vegetables", "soy sauce"], "dietary_restrictions": ["gluten-free", "dairy-free"]},
        {"name": "Beef Stew", "ingredients": ["beef", "vegetables", "potatoes"], "dietary_restrictions": []}
    ]
    filtered_recipes = [
        recipe for recipe in recipes
        if all(ing in recipe["ingredients"] for ing in ingredients) and all(res in recipe["dietary_restrictions"] for res in dietary_restrictions)
    ]

    if not filtered_recipes:
        return "No recipes found matching your criteria."
    else:
        return filtered_recipes

# Define the function specification for Gemini
function_descriptions = [
    {
        "name": "search_recipes",
        "description": "Searches for recipes based on available ingredients and dietary restrictions.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "ingredients": {
                    "type": "ARRAY",
                    "items": {"type": "STRING"},
                    "description": "A list of ingredients the user has available.",
                },
                "dietary_restrictions": {
                    "type": "ARRAY",
                    "items": {"type": "STRING"},
                    "description": "A list of dietary restrictions (e.g., vegetarian, gluten-free).",
                },
            },
            "required": ["ingredients", "dietary_restrictions"],
        },
    }
]

def generate_prompt(user_input):
  prompt = f"""
  You are a smart recipe recommendation agent.  A user will provide their available ingredients and any dietary restrictions they have. Use the search_recipes function to find a recipe that meets their needs.
  The user's input is: {user_input}
  """
  return prompt

def get_recipe_recommendation(user_input):
    prompt = generate_prompt(user_input)
    response = model.generate_content(
        prompt,
        tools=function_descriptions
    )

    response_message = response.candidates[0].content.parts[0].function_call

    if response_message:
        tool_name = response_message.name
        arguments = response_message.args

        if tool_name == "search_recipes":
            recipe = search_recipes(ingredients=arguments["ingredients"], dietary_restrictions=arguments["dietary_restrictions"])

            if recipe:
              return recipe

        else:
          return "Error: Could not find tool."

    return "I couldn't find a suitable recipe based on your input."


if __name__ == "__main__":
    # Example Usage
    user_input = "I have pasta and vegetables.  I am a vegetarian."
    recommendation = get_recipe_recommendation(user_input)
    print(f"Recommended Recipe: {recommendation}")
