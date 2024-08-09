#!/bin/bash
echo "Start of filling the database..."
sh migrate.sh
sh user.sh
sh token.sh
sh follow.sh
sh tag.sh
sh ingredient.sh
echo "...finihs filling the database."