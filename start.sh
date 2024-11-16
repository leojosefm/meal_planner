#!/bin/bash

echo "Starting load_ingredient.py..."
python load_ingredient.py
if [ $? -ne 0 ]; then
  echo "load_ingredient.py failed. Exiting."
  exit 1
fi

echo "load_ingredient.py completed successfully. Starting load_meal_category.py..."
python load_meal_category.py
if [ $? -ne 0 ]; then
  echo "load_meal_category.py failed. Exiting."
  exit 1
fi

echo "load_meal_category.py completed successfully. Starting create_has_ingredient_relations.py..."
python create_has_ingredient_relations.py
if [ $? -ne 0 ]; then
  echo "create_has_ingredient_relations.py failed. Exiting."
  exit 1
fi


echo "All scripts completed successfully."
