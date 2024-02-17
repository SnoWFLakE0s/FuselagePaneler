import tkinter, math, os.path, sys
from tkinter import ttk
from ctypes import windll
#GUI DPI Scaling
windll.shcore.SetProcessDpiAwareness(1)

def xPos(alphaFront, alphaRear, thickness, offsetAngle):
  return ((0.5 * (alphaFront - 0.5 * thickness) * math.sin(offsetAngle)) + (0.5 * (alphaRear - 0.5 * thickness) * math.sin(offsetAngle))) / 2
  
def yPos(alphaFront, alphaRear, thickness, offsetAngle):
  return ((0.5 * (alphaFront - 0.5 * thickness) * math.cos(offsetAngle)) + (0.5 * (alphaRear - 0.5 * thickness) * math.cos(offsetAngle))) / 2

def enter_data():
  #Basic dimension parameters
  frontDiameter = float(front_diameter_entry.get())
  rearDiameter = float(rear_diameter_entry.get())
  thickness = float(thickness_entry.get())
  diameterType = int(diameter_status_var.get())
  #Diameter Type Check & Update
  #Check if inner diameter is checked
  if diameterType == 1:
    #Update outer diameters to match
    frontDiameter += 2 * thickness
    rearDiameter += 2 * thickness
  detailLevel = int(detail_level_spinbox.get())
  theta = (2 * math.pi) / detailLevel
  alphaFront = 0.5 * frontDiameter * math.cos(math.pi / detailLevel)
  alphaRear = 0.5 * rearDiameter * math.cos(math.pi / detailLevel)

  #Extra Parameters
  collisionState = collisions_status_var.get()
  calculateDrag = drag_status_var.get()
  cornerType = corner_type_combo.get()
  if cornerType == "Hard":
    cornerType = 0
  elif cornerType == "Smooth":
    cornerType = 1
  elif cornerType == "Curved":
    cornerType = 2
  elif cornerType == "Circular":
    cornerType = 3
  colorId = int(color_spinbox.get())
  craftName = name_entry.get() + ".xml"

  frontWidth = frontDiameter * math.sin(theta / 2)
  rearWidth = rearDiameter * math.sin(theta / 2)
  rise = (rearDiameter - frontDiameter) / 2
  length = float(length_entry.get())

  #File output setup
  fileDirectory = str(os.environ['USERPROFILE'] + "\AppData\LocalLow\Jundroo\SimplePlanes\AircraftDesigns")
  completeName = os.path.join(fileDirectory, craftName)
  sys.stdout = open(completeName, 'w')

  #File Header
  output = '''<?xml version="1.0" encoding="utf-8"?>
  <Aircraft name="{0}" url="" theme="Default" xmlVersion="6">
    <Assembly>
      <Parts>
      <Part id="{1}" partType="Cockpit-1" position="0,0,0" rotation="0,0,0" drag="0,0,0,0,0,0" materials="0" scale="0,0,0" massScale="0" calculateDrag="false" dragScale="0" partCollisionResponse="None">
        <Cockpit.State primaryCockpit="True" lookBackTranslation="0,0" />
      </Part>'''.format(craftName, detailLevel)
  print(output)

  partCount = 0
  offsetAngle = 0.0

  while partCount < detailLevel:
    x = xPos(alphaFront, alphaRear, thickness, offsetAngle)
    y = yPos(alphaFront, alphaRear, thickness, offsetAngle)
    output = '''\t\t<Part id="{0}" partType="Fuselage-Body-1" position="{1},{2},0" rotation="0,0,{3}" drag="0,0,0,0,0,0" materials="{4}" disableAircraftCollisions="{5}" scale="1,1,1" massScale="1" calculateDrag="{6}" partCollisionResponse="None">
            <FuelTank.State fuel="0" capacity="0" />
            <Fuselage.State version="2" frontScale="{7},{8}" rearScale="{9},{8}" offset="0,{10},{11}" deadWeight="0" buoyancy="0" fuelPercentage="0" autoSizeOnConnected="false" cornerTypes="{12},{12},{12},{12},{12},{12},{12},{12}" />
          </Part>'''.format(partCount, x, y, math.degrees(-offsetAngle), colorId, collisionState, calculateDrag, frontWidth, thickness, rearWidth, rise, length, cornerType)
    print(output)
    partCount += 1
    offsetAngle += theta

  output = '''\t\t</Parts>
        <Connections>'''
  print(output)

  partCount = 0
  while partCount < detailLevel - 1:
      output = '''\t\t\t<Connection partA="{0}" partB="{1}" attachPointsA="2" attachPointsB="2" />'''.format(partCount, partCount + 1)
      print(output)
      partCount += 1

  output = '''\t</Connections>
        <Bodies>
        </Bodies>
    </Assembly>
  </Aircraft>'''
  print(output)
  #Close file
  sys.stdout.close()

#GUI APP
window = tkinter.Tk()
window.title("Fuselage Paneler v0.2a")

frame = tkinter.Frame(window)
frame.pack()

#Size Parameter Frame
size_parameter_frame = tkinter.LabelFrame(frame, text="Size Parameters")
size_parameter_frame.grid(row=0, column=0, padx=20, pady=10)

#Detail Parameter Frame
detail_parameter_frame = tkinter.LabelFrame(frame, text="Detail Parameters")
detail_parameter_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

#Cosmetic Parameter Frame
cosmetic_parameter_frame = tkinter.LabelFrame(frame, text="Cosmetic Parameters")
cosmetic_parameter_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)

#Size Parameter Fields
length_label = tkinter.Label(size_parameter_frame, text="Length")
length_label.grid(row=0, column=0)
length_entry = tkinter.Entry(size_parameter_frame)
length_entry.grid(row=1, column=0)

front_diameter_label = tkinter.Label(size_parameter_frame, text="Front Diameter")
front_diameter_label.grid(row=0, column=1)
front_diameter_entry = tkinter.Entry(size_parameter_frame)
front_diameter_entry.grid(row=1, column=1)

rear_diameter_label = tkinter.Label(size_parameter_frame, text="Rear Diameter")
rear_diameter_label.grid(row=0, column=2)
rear_diameter_entry = tkinter.Entry(size_parameter_frame)
rear_diameter_entry.grid(row=1, column=2)

diameter_status_var = tkinter.StringVar(value=0)
diameter_type_check = tkinter.Checkbutton(size_parameter_frame, text="If checked, use specfied diameters as internal diameters.", variable=diameter_status_var, onvalue=1, offvalue=0)
diameter_type_check.grid(row=2, column=0, columnspan=3)

for widget in size_parameter_frame.winfo_children():
  widget.grid_configure(padx=10, pady=5, sticky="w")

#Detail Parameter Fields
thickness_label = tkinter.Label(detail_parameter_frame, text="Tube Wall Thickness")
thickness_label.grid(row=0, column=0)
thickness_entry = tkinter.Entry(detail_parameter_frame)
thickness_entry.grid(row=1, column=0)

detail_level_label = tkinter.Label(detail_parameter_frame, text="Detail Level")
detail_level_label.grid(row=0, column=1)
detail_level_spinbox = tkinter.Spinbox(detail_parameter_frame, from_=12, to='infinity')
detail_level_spinbox.grid(row=1, column=1)

collisions_status_var = tkinter.StringVar(value="false")
collisions_check = tkinter.Checkbutton(detail_parameter_frame, text="Disable collisions? Will disable collisions on entire object.", variable=collisions_status_var, onvalue="true", offvalue="false")
collisions_check.grid(row=2, column=0, columnspan=2)
drag_status_var = tkinter.StringVar(value="false")
drag_check = tkinter.Checkbutton(detail_parameter_frame, text="Calculate drag? Calculating drag increases performance impact.", variable=drag_status_var, onvalue="true", offvalue="false")
drag_check.grid(row=3, column=0, columnspan=2)

for widget in detail_parameter_frame.winfo_children():
  widget.grid_configure(padx=10, pady=5, sticky="w")

#Cosmetic Parameter Fields
corner_type_label = tkinter.Label(cosmetic_parameter_frame, text="Panel Corner Type")
corner_type_label.grid(row=0, column=0)
corner_type_combo = ttk.Combobox(cosmetic_parameter_frame, state="readonly", values=["Hard", "Smooth", "Curved", "Circular"])
corner_type_combo.current(0)
corner_type_combo.grid(row=1, column=0)

color_label = tkinter.Label(cosmetic_parameter_frame, text="Tube Color ID")
color_label.grid(row=0, column=1)
color_spinbox = tkinter.Spinbox(cosmetic_parameter_frame, from_=0, to=12)
color_spinbox.grid(row=1, column=1)

name_label = tkinter.Label(cosmetic_parameter_frame, text="File Name")
name_label.grid(row=2, column=0)
name_entry = tkinter.Entry(cosmetic_parameter_frame)
name_entry.insert(0, "GeneratedObject")
name_entry.grid(row=3, column=0)

for widget in cosmetic_parameter_frame.winfo_children():
  widget.grid_configure(padx=10, pady=5, sticky="w")

#Button
button = tkinter.Button(frame, text="Generate Paneled Object", command=enter_data)
button.grid(row=3, column=0, sticky="news", padx=20, pady=10)

window.mainloop()