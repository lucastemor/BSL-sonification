#!/bin/bash
pdoc --html *.py  -o docs/ --force
pdoc --html ./lib/*.py  -o docs/ --force

#doesnt work .. figure out the proper way to do this .....
for folder in ./lib/*/; do
	pdoc --html $folder/*.py  -o docs/ --force ;
done