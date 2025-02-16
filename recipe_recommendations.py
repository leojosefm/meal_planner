from typing import List, Dict, Optional
import os
from neo4j import GraphDatabase
from langchain.agents import Tool, initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.tools import tool
from pydantic import BaseModel

class RecipeAISystem:
    def __init__(self):
        # Neo4j connection
        self.neo4j_url = os.getenv("NEO4J_URL", "bolt://localhost:7687")
        self.neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        self.neo4j_password = os.getenv("NEO4J_PASSWORD", "test_password")
        self.driver = GraphDatabase.driver(
            self.neo4j_url, 
            auth=(self.neo4j_user, self.neo4j_password)
        )

        # Initialize LLM
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0
        )

        # Initialize query generator chain
        self.query_generator = self._setup_query_generator()
        
        # Initialize agents
        self.tools = self._setup_tools()
        self.agent = self._setup_agent()

    def _setup_query_generator(self) -> LLMChain:
        template = """
        Generate a Cypher query for Neo4j based on the following natural language request.
        The database has the following schema:
        - (Meal) nodes with properties: title, tags, youtube, ingredients
        - (Ingredient) nodes with properties: name, description
        - (Category) nodes with property: title
        - (Area) nodes with property: title
        - Relationships: [:HAS_INGREDIENT], [:BELONGS_TO_CATEGORY], [:BELONGS_TO_AREA]

        User request: {user_input}

        Return only the Cypher query without any explanations.
        """
        
        prompt = PromptTemplate(
            input_variables=["user_input"],
            template=template
        )
        
        return LLMChain(llm=self.llm, prompt=prompt)

    @tool
    def search_recipes(self, ingredients: str) -> List[Dict]:
        """Search for recipes based on available ingredients"""
        query = self.query_generator.run(
            f"Find recipes I can make with these ingredients: {ingredients}"
        )
        
        with self.driver.session() as session:
            result = session.run(query)
            return [dict(record) for record in result]

    @tool
    def get_recipe_details(self, recipe_name: str) -> Dict:
        """Get detailed information about a specific recipe"""
        query = self.query_generator.run(
            f"Get detailed information about the recipe: {recipe_name}"
        )
        
        with self.driver.session() as session:
            result = session.run(query)
            return dict(result.single())

    @tool
    def suggest_substitutes(self, ingredient: str) -> List[str]:
        """Suggest possible ingredient substitutions"""
        # This would use the LLM to suggest substitutes based on
        # culinary knowledge and database contents
        pass

    def _setup_tools(self) -> List[Tool]:
        return [
            Tool(
                name="Recipe Search",
                func=self.search_recipes,
                description="Search for recipes based on available ingredients"
            ),
            Tool(
                name="Recipe Details",
                func=self.get_recipe_details,
                description="Get detailed information about a specific recipe"
            ),
            Tool(
                name="Ingredient Substitution",
                func=self.suggest_substitutes,
                description="Suggest possible ingredient substitutions"
            )
        ]

    def _setup_agent(self):
        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )

    def process_user_request(self, user_input: str) -> Dict:
        """Process natural language user request"""
        return self.agent.run(user_input)

# Example usage
if __name__ == "__main__":
    recipe_system = RecipeAISystem()
    
    # Example natural language queries
    queries = [
        "What can I make with chicken and potatoes?",
        "I have tomatoes, basil, and mozzarella. Any Italian recipes?",
        "Show me some vegetarian recipes using mushrooms",
        "What's a good substitute for eggs in baking?"
    ]
    
    for query in queries:
        result = recipe_system.process_user_request(query)
        print(f"\nQuery: {query}")
        print(f"Result: {result}")