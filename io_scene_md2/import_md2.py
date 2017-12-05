# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import bpy
import mathutils
import os.path

from . import fmt_md2 as fmt


def guess_texture_filepath(modelpath, imagepath):
    fileexts = ('', '.png', '.tga', '.jpg', '.jpeg')
    modelpath = os.path.normpath(os.path.normcase(modelpath))
    modeldir, _ = os.path.split(modelpath)
    imagedir, imagename = os.path.split(os.path.normpath(os.path.normcase(imagepath)))
    imagename = os.path.splitext(imagename)[0]
    previp = None
    ip = imagedir
    while ip != previp:
        if ip in modeldir:
            pos = modeldir.rfind(ip)
            nameguess = os.path.join(modeldir[:pos + len(ip)], imagedir[len(ip):], imagename)
            for ext in fileexts:
                yield nameguess + ext
        previp = ip
        ip, _ = os.path.split(ip)
    nameguess = os.path.join(modeldir, imagename)
    for ext in fileexts:
        yield nameguess + ext

#
#def get_tag_matrix_basis(data):
#    basis = mathutils.Matrix.Identity(4)
#    for j in range(3):
#        basis[j].xyz = data.axis[j::3]
#    basis.translation = mathutils.Vector(data.origin)
#    return basis

class MD2Importer:
    def __init__(self, context):
        self.filename = None
        self.context = context
        self.vertices = []
        self.anorms = [[ -0.525731,  0.000000,  0.850651 ], 
                [ -0.442863,  0.238856,  0.864188 ], 
                [ -0.295242,  0.000000,  0.955423 ], 
                [ -0.309017,  0.500000,  0.809017 ], 
                [ -0.162460,  0.262866,  0.951056 ], 
                [  0.000000,  0.000000,  1.000000 ], 
                [  0.000000,  0.850651,  0.525731 ], 
                [ -0.147621,  0.716567,  0.681718 ], 
                [  0.147621,  0.716567,  0.681718 ], 
                [  0.000000,  0.525731,  0.850651 ], 
                [  0.309017,  0.500000,  0.809017 ], 
                [  0.525731,  0.000000,  0.850651 ], 
                [  0.295242,  0.000000,  0.955423 ], 
                [  0.442863,  0.238856,  0.864188 ], 
                [  0.162460,  0.262866,  0.951056 ], 
                [ -0.681718,  0.147621,  0.716567 ], 
                [ -0.809017,  0.309017,  0.500000 ], 
                [ -0.587785,  0.425325,  0.688191 ], 
                [ -0.850651,  0.525731,  0.000000 ], 
                [ -0.864188,  0.442863,  0.238856 ], 
                [ -0.716567,  0.681718,  0.147621 ], 
                [ -0.688191,  0.587785,  0.425325 ], 
                [ -0.500000,  0.809017,  0.309017 ], 
                [ -0.238856,  0.864188,  0.442863 ], 
                [ -0.425325,  0.688191,  0.587785 ], 
                [ -0.716567,  0.681718, -0.147621 ], 
                [ -0.500000,  0.809017, -0.309017 ], 
                [ -0.525731,  0.850651,  0.000000 ], 
                [  0.000000,  0.850651, -0.525731 ], 
                [ -0.238856,  0.864188, -0.442863 ], 
                [  0.000000,  0.955423, -0.295242 ], 
                [ -0.262866,  0.951056, -0.162460 ], 
                [  0.000000,  1.000000,  0.000000 ], 
                [  0.000000,  0.955423,  0.295242 ], 
                [ -0.262866,  0.951056,  0.162460 ], 
                [  0.238856,  0.864188,  0.442863 ], 
                [  0.262866,  0.951056,  0.162460 ], 
                [  0.500000,  0.809017,  0.309017 ], 
                [  0.238856,  0.864188, -0.442863 ], 
                [  0.262866,  0.951056, -0.162460 ], 
                [  0.500000,  0.809017, -0.309017 ], 
                [  0.850651,  0.525731,  0.000000 ], 
                [  0.716567,  0.681718,  0.147621 ], 
                [  0.716567,  0.681718, -0.147621 ], 
                [  0.525731,  0.850651,  0.000000 ], 
                [  0.425325,  0.688191,  0.587785 ], 
                [  0.864188,  0.442863,  0.238856 ], 
                [  0.688191,  0.587785,  0.425325 ], 
                [  0.809017,  0.309017,  0.500000 ], 
                [  0.681718,  0.147621,  0.716567 ], 
                [  0.587785,  0.425325,  0.688191 ], 
        [  0.955423,  0.295242,  0.000000 ], 
[  1.000000,  0.000000,  0.000000 ], 
[  0.951056,  0.162460,  0.262866 ], 
[  0.850651, -0.525731,  0.000000 ], 
[  0.955423, -0.295242,  0.000000 ], 
[  0.864188, -0.442863,  0.238856 ], 
[  0.951056, -0.162460,  0.262866 ], 
[  0.809017, -0.309017,  0.500000 ], 
[  0.681718, -0.147621,  0.716567 ], 
[  0.850651,  0.000000,  0.525731 ], 
[  0.864188,  0.442863, -0.238856 ], 
[  0.809017,  0.309017, -0.500000 ], 
[  0.951056,  0.162460, -0.262866 ], 
[  0.525731,  0.000000, -0.850651 ], 
[  0.681718,  0.147621, -0.716567 ], 
[  0.681718, -0.147621, -0.716567 ], 
[  0.850651,  0.000000, -0.525731 ], 
[  0.809017, -0.309017, -0.500000 ], 
[  0.864188, -0.442863, -0.238856 ], 
[  0.951056, -0.162460, -0.262866 ], 
[  0.147621,  0.716567, -0.681718 ], 
[  0.309017,  0.500000, -0.809017 ], 
[  0.425325,  0.688191, -0.587785 ], 
[  0.442863,  0.238856, -0.864188 ], 
[  0.587785,  0.425325, -0.688191 ], 
[  0.688191,  0.587785, -0.425325 ], 
[ -0.147621,  0.716567, -0.681718 ], 
[ -0.309017,  0.500000, -0.809017 ], 
[  0.000000,  0.525731, -0.850651 ], 
[ -0.525731,  0.000000, -0.850651 ], 
[ -0.442863,  0.238856, -0.864188 ], 
[ -0.295242,  0.000000, -0.955423 ], 
[ -0.162460,  0.262866, -0.951056 ], 
[  0.000000,  0.000000, -1.000000 ], 
[  0.295242,  0.000000, -0.955423 ], 
[  0.162460,  0.262866, -0.951056 ], 
[ -0.442863, -0.238856, -0.864188 ], 
[ -0.309017, -0.500000, -0.809017 ], 
[ -0.162460, -0.262866, -0.951056 ], 
[  0.000000, -0.850651, -0.525731 ], 
[ -0.147621, -0.716567, -0.681718 ], 
[  0.147621, -0.716567, -0.681718 ], 
[  0.000000, -0.525731, -0.850651 ], 
[  0.309017, -0.500000, -0.809017 ], 
[  0.442863, -0.238856, -0.864188 ], 
[  0.162460, -0.262866, -0.951056 ], 
[  0.238856, -0.864188, -0.442863 ], 
[  0.500000, -0.809017, -0.309017 ], 
[  0.425325, -0.688191, -0.587785 ], 
[  0.716567, -0.681718, -0.147621 ], 
[  0.688191, -0.587785, -0.425325 ], 
[  0.587785, -0.425325, -0.688191 ], 
[  0.000000, -0.955423, -0.295242 ], 
[  0.000000, -1.000000,  0.000000 ], 
[  0.262866, -0.951056, -0.162460 ], 
[  0.000000, -0.850651,  0.525731 ], 
[  0.000000, -0.955423,  0.295242 ], 
[  0.238856, -0.864188,  0.442863 ], 
[  0.262866, -0.951056,  0.162460 ], 
[  0.500000, -0.809017,  0.309017 ], 
[  0.716567, -0.681718,  0.147621 ], 
[  0.525731, -0.850651,  0.000000 ], 
[ -0.238856, -0.864188, -0.442863 ], 
[ -0.500000, -0.809017, -0.309017 ], 
[ -0.262866, -0.951056, -0.162460 ], 
[ -0.850651, -0.525731,  0.000000 ], 
[ -0.716567, -0.681718, -0.147621 ], 
[ -0.716567, -0.681718,  0.147621 ], 
[ -0.525731, -0.850651,  0.000000 ], 
[ -0.500000, -0.809017,  0.309017 ], 
[ -0.238856, -0.864188,  0.442863 ], 
[ -0.262866, -0.951056,  0.162460 ], 
[ -0.864188, -0.442863,  0.238856 ], 
[ -0.809017, -0.309017,  0.500000 ], 
[ -0.688191, -0.587785,  0.425325 ], 
[ -0.681718, -0.147621,  0.716567 ], 
[ -0.442863, -0.238856,  0.864188 ], 
[ -0.587785, -0.425325,  0.688191 ], 
[ -0.309017, -0.500000,  0.809017 ], 
[ -0.147621, -0.716567,  0.681718 ], 
[ -0.425325, -0.688191,  0.587785 ], 
[ -0.162460, -0.262866,  0.951056 ], 
[  0.442863, -0.238856,  0.864188 ], 
[  0.162460, -0.262866,  0.951056 ], 
[  0.309017, -0.500000,  0.809017 ], 
[  0.147621, -0.716567,  0.681718 ], 
[  0.000000, -0.525731,  0.850651 ], 
[  0.425325, -0.688191,  0.587785 ], 
[  0.587785, -0.425325,  0.688191 ], 
[  0.688191, -0.587785,  0.425325 ], 
[ -0.955423,  0.295242,  0.000000 ], 
[ -0.951056,  0.162460,  0.262866 ], 
[ -1.000000,  0.000000,  0.000000 ], 
[ -0.850651,  0.000000,  0.525731 ], 
[ -0.955423, -0.295242,  0.000000 ], 
[ -0.951056, -0.162460,  0.262866 ], 
[ -0.864188,  0.442863, -0.238856 ], 
[ -0.951056,  0.162460, -0.262866 ], 
[ -0.809017,  0.309017, -0.500000 ], 
[ -0.864188, -0.442863, -0.238856 ], 
[ -0.951056, -0.162460, -0.262866 ], 
[ -0.809017, -0.309017, -0.500000 ], 
[ -0.681718,  0.147621, -0.716567 ], 
[ -0.681718, -0.147621, -0.716567 ], 
[ -0.850651,  0.000000, -0.525731 ], 
[ -0.688191,  0.587785, -0.425325 ], 
[ -0.587785,  0.425325, -0.688191 ], 
[ -0.425325,  0.688191, -0.587785 ], 
[ -0.425325, -0.688191, -0.587785 ], 
[ -0.587785, -0.425325, -0.688191 ], 
[ -0.688191, -0.587785, -0.425325 ]]

    def read_n_items(self, n, offset, func):
        if offset is not None:
            self.file.seek(offset)
        return [func(i) for i in range(n)]

    def unpack(self, rtype):
        return rtype.funpack(self.file)

    def read_frame(self, i):
        frame = self.unpack(fmt.Frame)
        verts = self.read_n_items(self.header.nVerts, None, self.read_vertex)
        return (frame, verts)
     
    def read_vertex(self, i):
        return self.unpack(fmt.Vert)

    def read_skin(self, i):
        return self.unpack(fmt.Skin)

    def read_texcoord(self, i):
        return self.unpack(fmt.TexCoord)

    def read_surface_ST(self, i):
        data = self.read_texcoord(i)
        return (data.s/self.header.skinwidth, 1.-(data.t/self.header.skinheight))

    def read_tri(self, i):
        return self.unpack(fmt.Tri)

    def read_glcmd(self, i):
        return self.unpack(fmt.GlCmd)
  
    def read_glcmdtype(self, i):
        return self.unpack(fmt.GlCmdType)


    def render_frame(self):
        #start_pos = self.file.tell()
        start_pos = 0
        
        self.mesh = bpy.data.meshes.new('MD2 Mesh')
        self.mesh.vertices.add(count=self.header.nVerts)
        self.mesh.polygons.add(count=self.header.nTris)
        self.mesh.loops.add(count=self.header.nTris * 3)
        
        self.read_n_items(self.header.nTris, start_pos + self.header.offTris, self.render_frame_tri)
        
        self.verts = self.mesh.vertices
        self.read_n_items(1, start_pos + self.header.offFrames, self.render_frame_vert)
         
        self.mesh.update(calc_edges=True)
        self.mesh.validate()
        
        self.read_n_items(self.header.nFrames, start_pos + self.header.offFrames, self.render_frame_normals)
        
        self.material = bpy.data.materials.new('Main')
        self.mesh.materials.append(self.material)
        self.mesh.uv_textures.new('UVMap')
        self.make_surface_UV_map(
            self.read_n_items(self.header.nTexCoords, start_pos + self.header.offTexCoords, self.read_surface_ST),
            self.read_n_items(self.header.nTris, start_pos + self.header.offTris, self.read_tri),
            self.mesh.uv_layers['UVMap'].data)

        self.read_n_items(self.header.nSkins, start_pos + self.header.offSkins, self.read_surface_skin)
#
        obj = bpy.data.objects.new('MD2 Object', self.mesh)
        self.context.scene.objects.link(obj)
        self.frames = self.read_n_items(self.header.nFrames, start_pos + self.header.offFrames, self.read_frame)
        if self.header.nFrames > 1:
            self.read_mesh_animation(obj, self.header, start_pos)

        self.file.seek(start_pos + self.header.offEnd)
#
    def render_frame_tri(self,i):
        data = self.unpack(fmt.Tri)
        ls = i * 3
        self.mesh.loops[ls].vertex_index = data.vertex[0]
        self.mesh.loops[ls + 1].vertex_index = data.vertex[1]  # swapped
        self.mesh.loops[ls + 2].vertex_index = data.vertex[2]  # swapped
        self.mesh.polygons[i].loop_start = ls
        self.mesh.polygons[i].loop_total = 3
        self.mesh.polygons[i].use_smooth = True

    def render_frame_vert(self,i,data=None):
        # Returns a tuple of (frame, verts)
        if data is None:
            data = self.read_frame(i)
        # List to store real coords
        v = [None, None, None]
        # Loop across all verts in frame.
        for j in range(len(data[1])):
            for k in range(3):
                v[k] = data[0].translate[k] + data[0].scale[k]*data[1][j].v[k]
            self.verts[j].co = mathutils.Vector(v)

    def render_frame_normals(self, i):
        data = self.read_frame(i)
        for j in range(len(data[1])): 
            normalIndex = data[1][j].normalIndex
            self.verts[j].normal = mathutils.Vector(self.anorms[normalIndex])

    def read_surface_skin(self, i):
        data = self.unpack(fmt.Skin)

        texture = bpy.data.textures.new(data.name, 'IMAGE')
        texture_slot = self.material.texture_slots.create(i)
        texture_slot.uv_layer = 'UVMap'
        texture_slot.use = True
        texture_slot.texture_coords = 'UV'
        texture_slot.texture = texture
        for fname in guess_texture_filepath(self.filename, data.name):
            if '\0' in fname:  # preventing ValuError: embedded null byte
                continue
            if os.path.isfile(fname):
                print(fname)
                image = bpy.data.images.load(fname)
                texture.image = image
                break

    def make_surface_UV_map(self, uv, tri, uvdata):
        for poly in self.mesh.polygons:
            stindex = tri[poly.loop_start//3].st
            for i in range(poly.loop_start, poly.loop_start + poly.loop_total):
                #vidx = self.mesh.loops[i].vertex_index
                uvdata[i].uv = uv[stindex[i-poly.loop_start]]

    def read_mesh_animation(self, obj, header, start_pos):
        obj.shape_key_add(name=self.frames[0][0].name)  # adding first frame, which is already loaded
        self.mesh.shape_keys.use_relative = False
        # TODO: ensure MD3 has linear frame interpolation
        for frame in range(1, header.nFrames):  # first frame skipped
            shape_key = obj.shape_key_add(name=self.frames[frame][0].name)
            self.verts = shape_key.data
            self.render_frame_vert(frame, self.frames[frame])
        bpy.context.scene.objects.active = obj
        bpy.context.object.active_shape_key_index = 0
        bpy.ops.object.shape_key_retime()
        for frame in range(header.nFrames):
            self.mesh.shape_keys.eval_time = 10.0 * (frame + 1)
            self.mesh.shape_keys.keyframe_insert('eval_time', frame=frame)

#
#    def create_tag(self, i):
#        data = self.unpack(fmt.Tag)
#        bpy.ops.object.add(type='EMPTY')
#        tag = bpy.context.object
#        tag.name = data.name
#        tag.empty_draw_type = 'ARROWS'
#        tag.rotation_mode = 'QUATERNION'
#        tag.matrix_basis = get_tag_matrix_basis(data)
#        return tag
#
#    def read_tag_frame(self, i):
#        tag = self.tags[i % self.header.nTags]
#        data = self.unpack(fmt.Tag)
#        tag.matrix_basis = get_tag_matrix_basis(data)
#        frame = i // self.header.nTags
#        tag.keyframe_insert('location', frame=frame, group='LocRot')
#        tag.keyframe_insert('rotation_quaternion', frame=frame, group='LocRot')
#
#    def read_surface_triangle(self, i):
#        data = self.unpack(fmt.Triangle)
#        ls = i * 3
#        self.mesh.loops[ls].vertex_index = data.a
#        self.mesh.loops[ls + 1].vertex_index = data.c  # swapped
#        self.mesh.loops[ls + 2].vertex_index = data.b  # swapped
#        self.mesh.polygons[i].loop_start = ls
#        self.mesh.polygons[i].loop_total = 3
#        self.mesh.polygons[i].use_smooth = True
#
#    def read_surface_vert(self, i):
#        data = self.unpack(fmt.Vertex)
#        self.verts[i].co = mathutils.Vector((data.x, data.y, data.z))
#        # ignoring data.normal here
#        # read_surface_normals reads them as a separate step
#
#    def read_surface_normals(self, i):
#        data = self.unpack(fmt.Vertex)
#        self.mesh.vertices[i].normal = mathutils.Vector(data.normal)
#
#    def read_mesh_animation(self, obj, data, start_pos):
#        obj.shape_key_add(name=self.frames[0].name)  # adding first frame, which is already loaded
#        self.mesh.shape_keys.use_relative = False
#        # TODO: ensure MD3 has linear frame interpolation
#        for frame in range(1, data.nFrames):  # first frame skipped
#            shape_key = obj.shape_key_add(name=self.frames[frame].name)
#            self.verts = shape_key.data
#            self.read_n_items(
#                data.nVerts,
#                start_pos + data.offVerts + frame * fmt.Vertex.size * data.nVerts,
#                self.read_surface_vert)
#        bpy.context.scene.objects.active = obj
#        bpy.context.object.active_shape_key_index = 0
#        bpy.ops.object.shape_key_retime()
#        for frame in range(data.nFrames):
#            self.mesh.shape_keys.eval_time = 10.0 * (frame + 1)
#            self.mesh.shape_keys.keyframe_insert('eval_time', frame=frame)
#
#    def read_surface_ST(self, i):
#        data = self.unpack(fmt.TexCoord)
#        return (data.s, data.t)
#
#    def make_surface_UV_map(self, uv, uvdata):
#        for poly in self.mesh.polygons:
#            for i in range(poly.loop_start, poly.loop_start + poly.loop_total):
#                vidx = self.mesh.loops[i].vertex_index
#                uvdata[i].uv = uv[vidx]
#
#    def read_surface_shader(self, i):
#        data = self.unpack(fmt.Shader)
#
#        texture = bpy.data.textures.new(data.name, 'IMAGE')
#        texture_slot = self.material.texture_slots.create(i)
#        texture_slot.uv_layer = 'UVMap'
#        texture_slot.use = True
#        texture_slot.texture_coords = 'UV'
#        texture_slot.texture = texture
#
#        for fname in guess_texture_filepath(self.filename, data.name):
#            if '\0' in fname:  # preventing ValuError: embedded null byte
#                continue
#            if os.path.isfile(fname):
#                image = bpy.data.images.load(fname)
#                texture.image = image
#                break
#
#    def read_surface(self, i):
#        start_pos = self.file.tell()
#
#        data = self.unpack(fmt.Surface)
#        assert data.magic == b'IDP3'
#        assert data.nFrames == self.header.nFrames
#        assert data.nShaders <= 256
#        if data.nVerts > 4096:
#            print('Warning: md3 surface contains too many vertices')
#        if data.nTris > 8192:
#            print('Warning: md3 surface contains too many triangles')
#
#        self.mesh = bpy.data.meshes.new(data.name)
#        self.mesh.vertices.add(count=data.nVerts)
#        self.mesh.polygons.add(count=data.nTris)
#        self.mesh.loops.add(count=data.nTris * 3)
#
#        self.read_n_items(data.nTris, start_pos + data.offTris, self.read_surface_triangle)
#        self.verts = self.mesh.vertices
#        self.read_n_items(data.nVerts, start_pos + data.offVerts, self.read_surface_vert)
#
#        self.mesh.update(calc_edges=True)
#        self.mesh.validate()
#
#        # separate step for normals. update() causes recalculation
#        self.read_n_items(data.nVerts, start_pos + data.offVerts, self.read_surface_normals)
#
#        self.material = bpy.data.materials.new('Main')
#        self.mesh.materials.append(self.material)
#
#        self.mesh.uv_textures.new('UVMap')
#        self.make_surface_UV_map(
#            self.read_n_items(data.nVerts, start_pos + data.offST, self.read_surface_ST),
#            self.mesh.uv_layers['UVMap'].data)
#
#        self.read_n_items(data.nShaders, start_pos + data.offShaders, self.read_surface_shader)
#
#        obj = bpy.data.objects.new(data.name, self.mesh)
#        self.context.scene.objects.link(obj)
#
#        if data.nFrames > 1:
#            self.read_mesh_animation(obj, data, start_pos)
#
#        self.file.seek(start_pos + data.offEnd)
#
    def post_settings(self):
        self.context.scene.frame_set(0)
        self.context.scene.game_settings.material_mode = 'GLSL'
        bpy.ops.object.lamp_add(type='SUN')
#
#    def __call__(self, filename):
#        self.filename = filename
#        with open(filename, 'rb') as file:
#            self.file = file
#
#            self.header = self.unpack(fmt.Header)
#            assert self.header.magic == fmt.MAGIC
#            assert self.header.version == fmt.VERSION
#
#            bpy.ops.scene.new()
#            self.context.scene.name = self.header.modelname
#            self.context.scene.frame_start = 0
#            self.context.scene.frame_end = self.header.nFrames - 1
#
#            self.frames = self.read_n_items(self.header.nFrames, self.header.offFrames, self.read_frame)
#            self.tags = self.read_n_items(self.header.nTags, self.header.offTags, self.create_tag)
#            if self.header.nFrames > 1:
#                self.read_n_items(self.header.nTags * self.header.nFrames, self.header.offTags, self.read_tag_frame)
#            self.read_n_items(self.header.nSurfaces, self.header.offSurfaces, self.read_surface)
#
#        self.post_settings()
    def __call__(self, filename):
        self.filename = filename
        with open(filename, 'rb') as file:
            self.file = file

            self.header = self.unpack(fmt.Header)
            assert self.header.magic == fmt.MAGIC
            assert self.header.version == fmt.VERSION
            print(self.header)
            bpy.ops.scene.new()
            self.context.scene.name = 'Quake 2 model'
            self.context.scene.frame_start = 0
            self.context.scene.frame_end = self.header.nFrames - 1
            
            #print(self.header.nGlCmds)
            #size = self.read_n_items(1, self.header.offGlCmds, self.read_glcmdtype)
            #print(size[0].n)
            #while (size[0].n != 0):
            #    data = self.read_n_items(abs(size[0].n), None, self.read_glcmd)
            #    print(data)
            #    size = self.read_n_items(1, None, self.read_glcmdtype)
            #    print(size[0].n)
            
            #data = self.read_n_items(self.header.nGlCmds//3, self.header.offGlCmds, self.read_glcmd)
            #print(data)

            self.render_frame()
        self.post_settings()

