#!/bin/bash
echo "Start of filling the database..."
sh scripts_sh/migrate.sh
sh scripts_sh/user.sh
sh scripts_sh/token.sh
sh scripts_sh/follow.sh
sh scripts_sh/tag.sh
sh scripts_sh/ingredient.sh
echo "...finihs filling the database."