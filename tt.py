import bpy, bmesh, random, math
from mathutils import Vector

def connect(point1, point2, radius, steps):

    mesh = bpy.data.meshes.new("mesh")  # add a new mesh
    object = bpy.data.objects.new("Rect", mesh)  # add a new object using the mesh
    scene = bpy.context.scene
    scene.objects.link(object)  # put the object into the scene (link)
    scene.objects.active = object  # set as the active object in the scene
    object.select = True  # select object
    mesh = bpy.context.object.data
    bm = bmesh.new()

    up = Vector((0,0,1))
    direction = (point2 - point1).normalized()
    localRight = direction.cross(up).normalized()
    localUp = localRight.cross(direction).normalized()

    angleAdd = 2*math.pi/steps
    curAngle = 0

    a = bm.verts.new(point2 + math.cos(curAngle) * localRight * radius + math.sin(curAngle) * localUp * radius)
    d = bm.verts.new(point1 + math.cos(curAngle) * localRight * radius + math.sin(curAngle) * localUp * radius)

    finalb = a
    finalc = d

    for i in range(0, steps-1):

        curAngle += angleAdd
        b = bm.verts.new(point2 + math.cos(curAngle) * localRight * radius + math.sin(curAngle) * localUp * radius)
        c = bm.verts.new(point1 + math.cos(curAngle) * localRight * radius + math.sin(curAngle) * localUp * radius)

        verts = []
        verts.append(a)
        verts.append(b)
        verts.append(c)
        verts.append(d)
        bm.faces.new(verts)

        a = b
        d = c

    verts = []
    verts.append(a)
    verts.append(finalb)
    verts.append(finalc)
    verts.append(d)
    bm.faces.new(verts)


    bm.to_mesh(mesh) # make the bmesh the object's mesh
    bm.free()  # always do this when finished


def create(ballCount, ballsSubdivisions, ballsSize, horizontalSpaceSize, verticalSpaceSize, connectionRadius, connectionSteps, connectionRate):

    points = []
    for i in range (0, ballCount):
        tLocation = Vector((random.uniform(-horizontalSpaceSize/2, horizontalSpaceSize/2), random.uniform(-horizontalSpaceSize/2, horizontalSpaceSize/2), random.uniform(0, verticalSpaceSize)))
        points.append(tLocation)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=ballsSubdivisions, size=ballsSize, view_align=False, enter_editmode=False, location=tLocation, layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

    for point in points:
        for pointt in points:
            if random.uniform(0,1) < connectionRate:
                connect(pointt, point, connectionRadius, connectionSteps)

create(20, 3, 1, 30, 70, .1, 12, .04);
