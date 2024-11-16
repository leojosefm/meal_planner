import os
import requests
from neo4j import GraphDatabase

# Neo4j connection details from environment variables
neo4j_url = os.getenv("NEO4J_URL", "bolt://localhost:7687")
neo4j_user = os.getenv("NEO4J_USER", "neo4j")
neo4j_password = os.getenv("NEO4J_PASSWORD", "test_password")

# Base URL to fetch meals
base_url = "https://www.themealdb.com/api/json/v1/1/search.php?f="

# Neo4j connection setup
driver = GraphDatabase.driver(neo4j_url, auth=(neo4j_user, neo4j_password))


def create_nodes_from_meals():
    with driver.session() as session:
        for letter in "abcdefghijklmnopqrstuvwxyz":
            # Fetch meals starting with the current letter
            url = f"{base_url}{letter}"
            response = requests.get(url)
            data = response.json()

            if not data.get("meals"):
                continue  # Skip if no meals are found

            meals = data["meals"]

            for meal in meals:
                # Extract meal properties
                title = meal.get("strMeal")
                category = meal.get("strCategory")
                area = meal.get("strArea")
                tags = meal.get("strTags", "")
                youtube = meal.get("strYoutube")
                
                # Ingredients as a list
                ingredients = [
                    meal.get(f"strIngredient{i}")
                    for i in range(1, 21) if meal.get(f"strIngredient{i}")
                ]

                # Process tags into a list
                tags_list = tags.split(",") if tags else []

                # Create Meal node
                session.run("""
                    MERGE (m:Meal {title: $title})
                    SET m.tags = $tags, m.youtube = $youtube, m.ingredients = $ingredients
                """, title=title, tags=tags_list, youtube=youtube, ingredients=ingredients)

                # Create Category node and relationship
                if category:
                    session.run("""
                        MERGE (c:Category {title: $category})
                        MATCH (m:Meal {title: $title})
                        MERGE (m)-[:BELONGS_TO_CATEGORY]->(c)
                    """, title=title, category=category)

                # Create Area node and relationship
                if area:
                    session.run("""
                        MERGE (a:Area {title: $area})
                        MATCH (m:Meal {title: $title})
                        MERGE (m)-[:BELONGS_TO_AREA]->(a)
                    """, title=title, area=area)


# Run the script
create_nodes_from_meals()
driver.close()

print("Meal data loaded into Neo4j successfully.")
