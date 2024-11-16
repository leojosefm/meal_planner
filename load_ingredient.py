import os
import requests
from neo4j import GraphDatabase
import time

# Wait until Neo4j is available
time.sleep(10)

# Neo4j connection details
neo4j_url = os.getenv("NEO4J_URL", "bolt://neo4j:7687")
neo4j_user = os.getenv("NEO4J_USER", "neo4j")
neo4j_password = os.getenv("NEO4J_PASSWORD", "test_password")

# URL to fetch JSON data
api_url = "https://www.themealdb.com/api/json/v1/1/list.php?i=list"

# Neo4j connection setup
driver = GraphDatabase.driver(neo4j_url, auth=(neo4j_user, neo4j_password))

def is_initialized():
    # Check if a "DataLoad" flag node exists
    with driver.session() as session:
        result = session.run("MATCH (n:DataLoad {status: 'completed'}) RETURN n LIMIT 1")
        return result.single() is not None
    
def create_flag_node():
    # Create a "DataLoad" flag node to indicate initialization is done
    with driver.session() as session:
        session.run("MERGE (:DataLoad {status: 'completed'})")


def create_ingredient_nodes(ingredients):
    with driver.session() as session:
        for ingredient in ingredients:
            name = ingredient.get("strIngredient")
            description = ingredient.get("strDescription") or "No description available"

            # Neo4j Cypher query to create Ingredient nodes
            session.run("""
                MERGE (i:Ingredient {name: $name, description: $description})
            """, name=name, description=description)


if not is_initialized():
    # Fetch data from API
    response = requests.get(api_url)
    data = response.json()
    ingredients = data.get("meals", [])

    # Load ingredients data into Neo4j
    create_ingredient_nodes(ingredients)
    create_flag_node()
    print("Ingredients loaded into Neo4j successfully.")
else:
    print("Data already loaded, skipping initialization.")

# Close Neo4j connection
driver.close()