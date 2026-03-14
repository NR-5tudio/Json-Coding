@echo off

python ../../json_runner.py does_MyFile_exist.json
pause

python ../../json_runner.py make_MyFile.json
pause

python ../../json_runner.py does_MyFile_exist.json
pause

python ../../json_runner.py read_MyFile.json
pause