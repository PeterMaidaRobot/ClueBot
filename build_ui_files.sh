#!/bin/bash

# Loop through all of our .ui files and autogenerate the python ui file for them
for file in *; do
	if [[ $file == *".ui" ]]; then
		filename=${file%.ui}
		/usr/local/bin/pyside6-uic $file > ui_$filename.py
	fi
done
