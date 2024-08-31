#!/bin/bash
echo "_________________________________"
echo "‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾"
echo "Start of filling the database..."
echo "---------------------------------"
sh scripts_sh/migrate.sh
echo "---------------------------------"
sh scripts_sh/tag.sh
echo "---------------------------------"
sh scripts_sh/ingredient.sh
echo "---------------------------------"
sh scripts_sh/static.sh
echo "---------------------------------"
sh scripts_sh/docs.sh
echo "---------------------------------"
echo "...finihs filling the database."
echo "_________________________________"
echo "‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾"