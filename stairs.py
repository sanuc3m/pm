import bpy, bmesh, random, math
from mathutils import Vector

def rect(origin, stepWidth, stepLength, stepHeight, count, direction):

    mesh = bpy.data.meshes.new("mesh")  # add a new mesh
    object = bpy.data.objects.new("Rect", mesh)  # add a new object using the mesh
    scene = bpy.context.scene
    scene.objects.link(object)  # put the object into the scene (link)
    scene.objects.active = object  # set as the active object in the scene
    object.select = True  # select object
    mesh = bpy.context.object.data
    bm = bmesh.new()




    direction = direction.normalized()
    up = Vector((0,0,1))
    right = direction.cross(up).normalized()


    rfw = bm.verts.new(origin+right*stepLength/2)
    lfw = bm.verts.new(origin-right*stepLength/2)

    rightcorner = bm.verts.new(rfw.co + direction*count*stepWidth)
    leftcorner = bm.verts.new(lfw.co + direction*count*stepWidth)

    for i in range(0,count):
        verts = []

        rtop = bm.verts.new(rfw.co+up*stepHeight)
        ltop = bm.verts.new(lfw.co+up*stepHeight)
        verts.append(rfw)
        verts.append(rtop)
        verts.append(ltop)
        verts.append(lfw)
        bm.faces.new(verts)

        #fill

        verts = []
        verts.append(rightcorner)
        verts.append(rtop)
        verts.append(rfw)
        bm.faces.new(verts)
        verts = []
        verts.append(leftcorner)
        verts.append(lfw)
        verts.append(ltop)
        bm.faces.new(verts)



        verts = []

        rfw = bm.verts.new(rtop.co+direction*stepWidth)
        lfw = bm.verts.new(ltop.co+direction*stepWidth)
        verts.append(ltop)
        verts.append(rtop)
        verts.append(rfw)
        verts.append(lfw)
        bm.faces.new(verts)

        #fill

        verts = []
        verts.append(rightcorner)
        verts.append(rfw)
        verts.append(rtop)
        bm.faces.new(verts)
        verts = []
        verts.append(leftcorner)
        verts.append(ltop)
        verts.append(lfw)
        bm.faces.new(verts)






    bm.to_mesh(mesh) # make the bmesh the object's mesh
    bm.free()  # always do this when finished
def rectFromHeightAndLength(origin, height, length, width, direction):
    v = 0.1625 #16.25 cm
    h = 0.2925 #29.25 cm
    a = length/h
    b = height/v
    count = int(round((a+b)/2))
    stepHeight = height/count
    stepWidth = length/count
    stepLength = width
    rect(origin, stepWidth, stepLength, stepHeight, count, direction)




def spiral(origin, radius, stepAngle, stepLength, stepHeight, stepThickness, count, cylinderVertsNumber):
    mesh = bpy.data.meshes.new("mesh")  # add a new mesh
    object = bpy.data.objects.new("Rect", mesh)  # add a new object using the mesh
    scene = bpy.context.scene
    scene.objects.link(object)  # put the object into the scene (link)
    scene.objects.active = object  # set as the active object in the scene
    object.select = True  # select object
    mesh = bpy.context.object.data
    bm = bmesh.new()





    up = Vector((0,0,1))

    curAngle = 0
    curHeight = 0

    curvector = Vector((math.cos(curAngle), math.sin(curAngle), 0))

    lfw = bm.verts.new(origin + curvector*radius)
    rfw = bm.verts.new(lfw.co + curvector*stepLength)


    lth = bm.verts.new(lfw.co - up*stepThickness)
    rth = bm.verts.new(rfw.co - up*stepThickness)


    for i in range(0,count):
        #step front face
        verts = []
        rtop = bm.verts.new(rfw.co+up*stepHeight)
        ltop = bm.verts.new(lfw.co+up*stepHeight)
        verts.append(rfw)
        verts.append(rtop)
        verts.append(ltop)
        verts.append(lfw)
        bm.faces.new(verts)

        curAngle += stepAngle
        curvector = Vector((math.cos(curAngle), math.sin(curAngle), 0))
        curHeight += stepHeight

        #step top face
        verts = []
        lfw = bm.verts.new(origin + curvector*radius + Vector((0,0,curHeight)))
        rfw = bm.verts.new(lfw.co + curvector*stepLength)
        verts.append(ltop)
        verts.append(rtop)
        verts.append(rfw)
        verts.append(lfw)
        bm.faces.new(verts)


        nlth = bm.verts.new(lfw.co - up*stepThickness)
        nrth = bm.verts.new(rfw.co - up*stepThickness)

        #bottom face
        verts = []
        verts.append(lth)
        verts.append(nlth)
        verts.append(nrth)
        verts.append(rth)
        bm.faces.new(verts)

        #external faces
        verts = []
        verts.append(rth)
        verts.append(rfw)
        verts.append(rtop)
        bm.faces.new(verts)
        verts = []
        verts.append(rth)
        verts.append(nrth)
        verts.append(rfw)
        bm.faces.new(verts)

        #internal faces
        verts = []
        verts.append(lfw)
        verts.append(lth)
        verts.append(ltop)
        bm.faces.new(verts)
        verts = []
        verts.append(nlth)
        verts.append(lth)
        verts.append(lfw)
        bm.faces.new(verts)

        lth = nlth
        rth = nrth


    #central cylinder
    if cylinderVertsNumber > 2:
        angleAdd = 2*math.pi/cylinderVertsNumber
        curAngle = 0

        top = []

        a = bm.verts.new(origin + Vector((math.cos(curAngle), math.sin(curAngle), 0))*radius)
        d = bm.verts.new(a.co + up * (stepHeight*count))

        finalb = a
        finalc = d

        top.append(d)

        for i in range(0,cylinderVertsNumber-1):

            curAngle += angleAdd
            b = bm.verts.new(origin + Vector((math.cos(curAngle), math.sin(curAngle), 0))*radius)
            c = bm.verts.new(b.co + up * (stepHeight*count))

            verts = []
            verts.append(a)
            verts.append(b)
            verts.append(c)
            verts.append(d)
            bm.faces.new(verts)

            a = b
            d = c

            top.append(d)

        #last face
        verts = []
        verts.append(a)
        verts.append(finalb)
        verts.append(finalc)
        verts.append(d)
        bm.faces.new(verts)

        #top face
        bm.faces.new(top)


    bm.to_mesh(mesh) # make the bmesh the object's mesh
    bm.free()  # always do this when finished

def ushaped(origin, stepWidth, stepLength, stepHeight, stepThickness, stepsPerSegment, segmentCount, restDepth, direction):
    mesh = bpy.data.meshes.new("mesh")  # add a new mesh
    object = bpy.data.objects.new("Rect", mesh)  # add a new object using the mesh
    scene = bpy.context.scene
    scene.objects.link(object)  # put the object into the scene (link)
    scene.objects.active = object  # set as the active object in the scene
    object.select = True  # select object
    mesh = bpy.context.object.data
    bm = bmesh.new()




    direction = direction.normalized()
    up = Vector((0,0,1))
    right = direction.cross(up).normalized()
    curPosition = origin

    for i in range(0, segmentCount):
        if i%2==0:
            if i==0:
                lfw = bm.verts.new(curPosition)
                rfw = bm.verts.new(lfw.co + right*stepLength)

            #lth = bm.verts.new(lfw.co - up*stepThickness)
            #rth = bm.verts.new(rfw.co - up*stepThickness)
            for j in range(0, stepsPerSegment):
                ltop = bm.verts.new(lfw.co + up*stepHeight)
                rtop = bm.verts.new(rfw.co + up*stepHeight)

                verts = []
                verts.append(lfw)
                verts.append(rfw)
                verts.append(rtop)
                verts.append(ltop)
                bm.faces.new(verts)

                lfw = bm.verts.new(ltop.co + direction*stepWidth)
                rfw = bm.verts.new(rtop.co + direction*stepWidth)

                verts = []
                verts.append(rtop)
                verts.append(rfw)
                verts.append(lfw)
                verts.append(ltop)
                bm.faces.new(verts)

            ltop = bm.verts.new(lfw.co + up*stepHeight)
            rtop = bm.verts.new(rfw.co + up*stepHeight)

            verts = []
            verts.append(lfw)
            verts.append(rfw)
            verts.append(rtop)
            verts.append(ltop)
            bm.faces.new(verts)

            lfw = ltop
            rfw = bm.verts.new(ltop.co - right*stepLength)

            #rest
            rrc = bm.verts.new(rtop.co + direction*restDepth)
            rlc = bm.verts.new(rfw.co + direction*restDepth)
            verts = []
            verts.append(rfw)
            verts.append(rtop)
            verts.append(rrc)
            verts.append(rlc)
            bm.faces.new(verts)


        else:
            #lfw = bm.verts.new(curPosition + right*2*stepLength + direction*stepWidth*stepsPerSegment)
            #rfw = bm.verts.new(lfw.co - right*stepLength)

            for j in range(0, stepsPerSegment):
                ltop = bm.verts.new(lfw.co + up*stepHeight)
                rtop = bm.verts.new(rfw.co + up*stepHeight)

                verts = []
                verts.append(lfw)
                verts.append(rfw)
                verts.append(rtop)
                verts.append(ltop)
                bm.faces.new(verts)

                lfw = bm.verts.new(ltop.co - direction*stepWidth)
                rfw = bm.verts.new(rtop.co - direction*stepWidth)

                verts = []
                verts.append(rtop)
                verts.append(rfw)
                verts.append(lfw)
                verts.append(ltop)
                bm.faces.new(verts)

            ltop = bm.verts.new(lfw.co + up*stepHeight)
            rtop = bm.verts.new(rfw.co + up*stepHeight)

            verts = []
            verts.append(lfw)
            verts.append(rfw)
            verts.append(rtop)
            verts.append(ltop)
            bm.faces.new(verts)

            lfw = ltop
            rfw = bm.verts.new(ltop.co + right*stepLength)

            #rest
            rrc = bm.verts.new(rtop.co - direction*restDepth)
            rlc = bm.verts.new(rfw.co - direction*restDepth)
            verts = []
            verts.append(rfw)
            verts.append(rtop)
            verts.append(rrc)
            verts.append(rlc)
            bm.faces.new(verts)

        curPosition = Vector((curPosition.x, curPosition.y, curPosition.z + (stepsPerSegment+1)*stepHeight))






    bm.to_mesh(mesh) # make the bmesh the object's mesh
    bm.free()  # always do this when finished




#ushaped(Vector((0,0,0)), .6, 1, .2, 1, 7, 5, 1, Vector((0,1,0)))
rect(Vector((0,0,0)), .3, 2, .1, 20, Vector((0,1,0)))
spiral(Vector((5,0,0)), .1, .2, 2, .1, .5, 30, 10)
ushaped(Vector((-5,0,0)), .2, 2, .1, 1, 20, 3, 3, Vector((0,1,0)))
