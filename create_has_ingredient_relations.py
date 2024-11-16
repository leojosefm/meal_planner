import os
import requests
from neo4j import GraphDatabase
import time

# Wait until Neo4j is available
time.sleep(10)


# Neo4j connection details from environment variables
neo4j_url = os.getenv("NEO4J_URL", "bolt://localhost:7687")
neo4j_user = os.getenv("NEO4J_USER", "neo4j")
neo4j_password = os.getenv("NEO4J_PASSWORD", "test_password")

# Base URL to fetch meals
base_url = "https://www.themealdb.com/api/json/v1/1/search.php?f="

# Neo4j connection setup
driver = GraphDatabase.driver(neo4j_url, auth=(neo4j_user, neo4j_password))


def is_initialized():
    # Check if a "DataLoad" flag node exists
    with driver.session() as session:
        result = session.run("MATCH (n:DataLoad_ing_relation {status: 'completed'}) RETURN n LIMIT 1")
        return result.single() is not None
    
def create_flag_node():
    # Create a "DataLoad" flag node to indicate initialization is done
    with driver.session() as session:
        session.run("MERGE (:DataLoad_ing_relation {status: 'completed'})")

def create_has_ingredient_relations():
    with driver.session() as session:
        query = """
        MATCH (m:Meal)
        UNWIND m.ingredients AS ingredient_name
        MATCH (i:Ingredient)
        WHERE lower(i.name) = lower(ingredient_name)
        MERGE (m)-[:HAS_INGREDIENT]->(i)
        """
        session.run(query)

if not is_initialized():
    create_has_ingredient_relations()
    create_flag_node()
    print("Ingredient - Meal relation created in  Neo4j successfully.")
else:
    print("Data already loaded, skipping initialization.")

driver.close()

