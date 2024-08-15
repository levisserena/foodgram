#!/bin/bash
echo "Create image..."
mkdir ../media/users
mkdir ../media/recipes
mkdir ../media/recipes/images
for i in `seq 1 30`; do cp scripts_sh/test_u.jpg ../media/users/test_u${i}.jpg; done
for i in `seq 1 150`; do cp scripts_sh/test_r.jpg ../media/recipes/images/test_r${i}.jpg; done
echo "...image created."