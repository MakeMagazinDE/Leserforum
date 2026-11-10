import cadquery as cq
from pathlib import Path
P=Path('/mnt/data/meatloaf_case')
# Units mm. X width, Y depth (front negative), Z height.
W,D,H=150,110,40
# bottom tray: 2.4mm floor, 2.5mm walls, height 31
base=cq.Workplane('XY').box(W,D,31,centered=(True,True,False)).cut(cq.Workplane('XY').box(W-5,D-5,35,centered=(True,True,False)).translate((0,0,2.4)))
# front aperture, leaving side mounting rails
base=base.cut(cq.Workplane('XY').box(129,8,21,centered=(True,True,False)).translate((0,-54,5)))
# front mounting pilot holes through face, horizontal along y
for x in (-68,68):
 base=base.cut(cq.Solid.makeCylinder(1.25,8,cq.Vector(x,-57,17),cq.Vector(0,1,0)))
# rear IEC round aperture + USB C + reset
base=base.cut(cq.Solid.makeCylinder(9,8,cq.Vector(49,57,17),cq.Vector(0,-1,0)))
base=base.cut(cq.Workplane('XY').box(10,8,4,centered=(True,True,False)).translate((-49,54,15)))
base=base.cut(cq.Solid.makeCylinder(2,8,cq.Vector(-18,57,17),cq.Vector(0,-1,0)))
# bosses for lid screws; internal locations, blind pilot holes
for x in (-68,68):
 for y in (-48,48):
  boss=cq.Workplane('XY').center(x,y).circle(4.2).extrude(28.6).translate((0,0,2.4))
  base=base.union(boss)
  base=base.cut(cq.Workplane('XY').center(x,y).circle(1.25).extrude(12).translate((0,0,21)))
# bottom universal electronics mounts (un-drilled to allow matching to board)
for x in (-25,25):
 for y in (-21,21):
  base=base.union(cq.Workplane('XY').center(x,y).circle(3.4).extrude(4).translate((0,0,2.4)))
# lid cap: 2.5mm roof and shallow skirt, sits at z31
lid=cq.Workplane('XY').box(W,D,9,centered=(True,True,False)).translate((0,0,31))
lid=lid.cut(cq.Workplane('XY').box(W-5,D-5,7,centered=(True,True,False)).translate((0,0,31)))
# screw clearance through roof
for x in (-68,68):
 for y in (-48,48):
  lid=lid.cut(cq.Workplane('XY').center(x,y).circle(1.65).extrude(12).translate((0,0,30)))
  lid=lid.cut(cq.Workplane('XY').center(x,y).circle(3.2).extrude(1.4).translate((0,0,38.6)))
# roof vents, slots towards rear, avoid bosses
for x in range(-54,55,6):
 lid=lid.cut(cq.Workplane('XY').box(2.4,27,5,centered=(True,True,False)).translate((x,24,37)))
# front plate: flat rectangular part, thickness 2mm, facing -Y, 138x26, center Z17
plate=cq.Workplane('XY').box(138,2,26).translate((0,-56.25,17))
# plate holes OLED x=-41, center z=17, width 42 height 16
plate=plate.cut(cq.Workplane('XY').box(42,5,16).translate((-41,-56.25,17)))
# LEDs x positions, center z 17
for x in (0,13,26,39):
 plate=plate.cut(cq.Solid.makeCylinder(2.55,5,cq.Vector(x,-59,17),cq.Vector(0,1,0)))
# microSD slot on right
plate=plate.cut(cq.Workplane('XY').box(17,5,3.2).translate((57,-56.25,17)))
for x in (-68,68):
 plate=plate.cut(cq.Solid.makeCylinder(1.55,5,cq.Vector(x,-59,17),cq.Vector(0,1,0)))
for name,shape in [('Meatloaf_Boden_v0.1',base),('Meatloaf_Deckel_v0.1',lid),('Meatloaf_Frontplatte_v0.1',plate)]:
 cq.exporters.export(shape,str(P/(name+'.stl')),tolerance=0.12,angularTolerance=0.15)
 print(name, shape.val().Volume())
