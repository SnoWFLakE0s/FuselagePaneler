# FuselagePaneler
Python script to generate XML files for [SimplePlanes](http://www.simpleplanes.com) that give you nice paneled tubes.
# Usage Instructions
___
NOTE: INSTRUCTIONS BELOW SUPPORTED FOR MACOS ONLY
1. Ensure that you have your SimplePlanes directory set up in the correct file path. It should be `~/Library/Application Support/unity.Jundroo.SimplePlanes/AircraftDesigns/`. 
2. Run the script. This can be done by downloading the script and running it in Terminal. Read on for more details.
3. Ensure that you have Python 3 installed via checking version `python3 --version` (if you do not, head over to python.org to do so). 
4. Run the script by running this command in Terminal: `python3 /path/to/file/FuselagePaneler_MacOS.py`. Alternatively, type up to `python3 ` (with the space) and simply drag & drop the script file in the Terminal window to get the path automatically.
5. Follow the textual prompts and input your desired settings as inquired.
6. Check your AircraftDesigns directory. A XML file should have been generated with the proper encoding. Now load it up in SimplePlanes.app to view the 3D object.

# Sample Run
___
```
>> MacBook-Pro:~ user$ python3 /Users/myName/Downloads/FuselagePaneler_MacOS.py
>> Enter tube length: 
12
>> Enter tube front side diameter.
3
>> Enter tube rear side diameter.
5
>> Enter tube wall thickness.
0.5
>> Enter part count. This number determines the amount of parts the program will use to construct your tube.
50
>> Enter component corner type (0 - Hard, 1 - Smooth, 2 - Curved, 3 - Circular). If in doubt, try to use the hard corner setting to get the best results.
0
>> Please specify the color id (0~12) that you want on the system: 
0
```
<img height="250" alt="Screen Shot 2021-12-13 at 11 39 44 PM" src="https://user-images.githubusercontent.com/32413097/145934186-727bbf57-f6c2-43a6-807c-41d1267a1565.png"><img height="250" alt="Screen Shot 2021-12-13 at 11 41 14 PM" src="https://user-images.githubusercontent.com/32413097/145934295-636f8f2e-c3eb-477a-91d9-917bf0113931.png">

Generated tube, with 12 length, 3 front side diameter, 5 rear diameter, 0.5 thickness, hard corners and color ID 0. Total 50 rectangular pieces.
