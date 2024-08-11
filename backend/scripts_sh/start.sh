#!/bin/bash
echo "_________________________________"
echo "‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾"
echo "Start of filling the database..."
echo "---------------------------------"
sh scripts_sh/migrate.sh
echo "---------------------------------"
sh scripts_sh/user.sh
echo "---------------------------------"
sh scripts_sh/token.sh
echo "---------------------------------"
sh scripts_sh/follow.sh
echo "---------------------------------"
sh scripts_sh/tag.sh
echo "---------------------------------"
sh scripts_sh/ingredient.sh
echo "---------------------------------"
sh scripts_sh/recipe.sh
echo "---------------------------------"
sh scripts_sh/favorit.sh
echo "---------------------------------"
sh scripts_sh/shoping.sh
echo "---------------------------------"
echo "...finihs filling the database."
echo "_________________________________"
echo "‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾"