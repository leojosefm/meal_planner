# Meal Planning Graph Project

## Overview

This project is designed to help with meal planning based on the ingredients you have available. By leveraging a graph database (Neo4j), the goal is to suggest meal recipes using available ingredients and their relationships in a flexible and efficient way. The project serves as both a personal tool for meal planning and a learning experience in graph data modeling and Cypher query language.

### Project Structure
The project is based on Neo4j, a graph database, which models:

- **Meals**: Recipes or dishes that can be created.
- **Ingredients**: Components that make up meals.

#### Relations:

- **HAS_INGREDIENT**: Connects meals to their ingredients.
- **BELONGS_TO_CATEGORY**: Connects meals to their categories (e.g., vegetarian, non-vegetarian).
- **BELONGS_TO_AREA**: Connects meals to their geographic origin (e.g., Italian, Mexican).
- **HAS_INGREDIENT**: Connects meals to their ingredients.

#### Cypher Query
Cypher, Neo4j's query language, allows you to search for meals based on available ingredients. Here's an example query:

``` 
MATCH (m:Meal)-[:HAS_INGREDIENT]->(i:Ingredient)
WHERE lower(i.name) IN ["beef"]
WITH m
MATCH (m)-[:HAS_INGREDIENT]->(i2:Ingredient)
WHERE lower(i2.name) IN ['potatoes', 'lemon', 'lime', 'parsley', 'aubergine', 'zucchini', 'tomato', 'yogurt']
RETURN m.title AS Meal, COLLECT(i2.name) AS Ingredients
```


### Why Graph Databases Are Better for This Use Case
Unlike relational databases, graph databases excel at handling relationships between various entities. In a meal planning context, a graph query can return meals based on a wide range of ingredient combinations, categories, and areas, all with natural relationships built into the database.

---

## How Would This Be Done in an RDBMS?

In an **RDBMS**, we would likely use **three tables**:
1. **Meals**: A table of meals with `meal_id`, `title`, etc.
2. **Ingredients**: A table of ingredients with `ingredient_id`, `name`, etc.
3. **MealIngredients**: A join table that maps meals to ingredients, containing `meal_id` and `ingredient_id`.

#### SQL Query for Meal Suggestion:
```sql
SELECT m.title
FROM Meals m
JOIN MealIngredients mi ON m.meal_id = mi.meal_id
JOIN Ingredients i ON mi.ingredient_id = i.ingredient_id
WHERE i.name = 'beef'
AND EXISTS (
    SELECT 1
    FROM MealIngredients mi2
    JOIN Ingredients i2 ON mi2.ingredient_id = i2.ingredient_id
    WHERE mi2.meal_id = m.meal_id
    AND i2.name IN ('potatoes', 'lemon', 'lime', 'parsley', 'aubergine', 'zucchini', 'tomato', 'yogurt')
)