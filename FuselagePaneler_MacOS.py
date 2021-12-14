#Variable Input
tubelength = float(input("Enter tube length:\n"))

#new inputs for front/back size
frontdiameter = float(input("Enter tube front side diameter.\n"))
backdiameter = float(input("Enter tube rear side diameter.\n"))
tubediameter = (frontdiameter + backdiameter) / 2

radius_outer = tubediameter / 2
#new variables analagous to radius_outer (front/back)
outerradius_front = frontdiameter / 2
outerradius_back = backdiameter / 2

thickness = float(input("Enter tube wall thickness.\n"))
fillratio = int(input("Enter part count. This number determines the amount of parts the program will use to construct your tube.\n"))
cornertype = int(input("Enter component corner type (0 - Hard, 1 - Smooth, 2 - Curved, 3 - Circular). If in doubt, try to use the hard corner setting to get the best results.\n"))
color = input("Please specify the color id (0~12) that you want on the system: \n")

#file output setup
import os.path
fileDirectory = str(os.environ['HOME'] + "/Library/Application Support/unity.Jundroo.SimplePlanes/AircraftDesigns/")
completeName = os.path.join(fileDirectory, "GeneratedGear.xml")

import math
#Approximating the tube as a inscribed polygon. The "triangles"  that composes the inscribed polygon are isosceles triangles with two equal legs of length r. Then, the remaining side of the triangle (the perimeter section) is defined by 2*r*sin(theta/2), where theta is the triangle interior angle (center of the polygon).
#Thus, theta would be defined by 360 (or 2pi) divded by the fill ratio.

#theta in degrees
theta = 360 / fillratio
#workflow stage 2, independent calculations
#below is the initial width calculation algorithm
outerside = 2 * radius_outer * math.sin(math.radians(theta / 2))
#this needs be applied to the front and rear diameter values, respectively
frontwidth = 2 * outerradius_front * math.sin(math.radians(theta / 2))
backwidth = 2 * outerradius_back * math.sin(math.radians(theta / 2))

#new process: calculate rise for pieces
#(back diameter - front)/2 = rise
rise = (backdiameter - frontdiameter) / 2

#set stdout to file
import sys
sys.stdout = open(completeName, 'w')

#Results
finaltext1 = '''<?xml version="1.0" encoding="utf-8"?>
<Aircraft name="GeneratedObject" url="" theme="Default" xmlVersion="6">
  <Assembly>
    <Parts>
      <Part id="0" partType="Cockpit-1" position="0,0,0" rotation="0,0,0" drag="0,0,0,0,0,0" materials="{0}" scale="1,1,1" massScale="0" calculateDrag="false" dragScale="0" partCollisionResponse="Default">
        <Cockpit.State primaryCockpit="True" lookBackTranslation="0,0" />
      </Part>'''.format(color)
print(finaltext1)

partcount = 1
offsetangle = 0

while partcount < fillratio + 1:
  xpos = ((radius_outer / 2) - (thickness / 4)) * math.sin(math.radians(offsetangle))
  ypos = ((radius_outer / 2) - (thickness / 4)) * math.cos(math.radians(offsetangle))
  finaltext2 = '''\t\t<Part id="{0}" partType="Fuselage-Body-1" position="{1},{2},0" rotation="0,0,{9}" drag="0,0,0,0,0,0" materials="{3}" disableAircraftCollisions="true" scale="1,1,1" massScale="0" calculateDrag="false" dragScale="0" partCollisionResponse="Default">
          <FuelTank.State fuel="0" capacity="0" />
          <Fuselage.State version="2" frontScale="{4},{6}" rearScale="{5},{6}" offset="0,{10},{7}" deadWeight="0" buoyancy="0" fuelPercentage="0" autoSizeOnConnected="false" cornerTypes="{8},{8},{8},{8},{8},{8},{8},{8}" />
        </Part>'''.format(partcount, xpos, ypos, color, frontwidth, backwidth, thickness, tubelength, cornertype, -offsetangle, rise)
  print(finaltext2)
  partcount += 1
  offsetangle += theta

finaltext3 = '''\t\t</Parts>
      <Connections>'''
print(finaltext3)

partcountsv = partcount - 1
partcount -= 1
while partcount > 0:
    finaltext4 = '''\t\t\t<Connection partA="{0}" partB="{1}" attachPointsA="2" attachPointsB="2" />'''.format(partcount - 1, partcount)
    print(finaltext4)
    partcount -= 1

finaltext5 = '''\t</Connections>
      <Bodies>'''
print(finaltext5)

while partcountsv > -1:
    finaltext6 = '''\t\t\t<Body partIds="{0}" position="0,0,0" rotation="0,0,0" velocity="0,0,0" angularVelocity="0,0,0" />'''.format(partcountsv)
    print(finaltext6)
    partcountsv -= 1

finaltext7 = '''\t</Bodies>
  </Assembly>
</Aircraft>'''
print(finaltext7)

#close file
sys.stdout.close()