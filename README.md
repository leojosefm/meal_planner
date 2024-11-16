# Meal Planning Graph Project

## Overview

This project is designed to help with meal planning based on the ingredients you have available. By leveraging a graph database (Neo4j), the goal is to suggest meal recipes using available ingredients and their relationships in a flexible and efficient way. The project serves as both a personal tool for meal planning and a learning experience in graph data modeling and Cypher query language.

### Project Structure
The project is based on Neo4j, a graph database, which models:

- Meals: Recipes or dishes that can be created.
- Ingredients: Components that make up meals.

#### Relations:

- HAS_INGREDIENT: Connects meals to their ingredients.
- BELONGS_TO_CATEGORY: Connects meals to their categories (e.g., vegetarian, non-vegetarian).
- BELONGS_TO_AREA: Connects meals to their geographic origin (e.g., Italian, Mexican).
- HAS_INGREDIENT: Connects meals to their ingredients.

#### Cypher Queries
Cypher, Neo4j's query language, allows you to search for meals based on available ingredients. Here's an example query:

`MATCH (m:Meal)-[:HAS_INGREDIENT]->(i:Ingredient)
WHERE lower(i.name) IN ["beef"]
WITH m
MATCH (m)-[:HAS_INGREDIENT]->(i2:Ingredient)
WHERE lower(i2.name) IN ['potatoes', 'lemon', 'lime', 'parsley', 'aubergine', 'zucchini', 'tomato', 'yogurt']
RETURN m.title AS Meal, COLLECT(i2.name) AS Ingredients`