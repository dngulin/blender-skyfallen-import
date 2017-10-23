import os.path
import re
import bpy
import bmesh
from .skyfallen import SFGeometry


def get_texture_name(path, mat_texname):
    texnames = []
    texnames.append(mat_texname)

    if mat_texname[-4:] == '.dds':
        texnames.append(mat_texname[:-4] + '_hi.dds')

    basename = os.path.basename(path)[:-4]
    texnames.append(basename + '.dds')
    texnames.append(basename + '_hi.dds')

    cmntexname = re.sub(r'_\d+$', '', basename)
    if cmntexname != basename:
        texnames.append(cmntexname + '.dds')
        texnames.append(cmntexname + '_hi.dds')

    # Validate list
    dirname = os.path.dirname(path)
    for texname in texnames:
        if os.path.isfile(os.path.join(dirname, texname)):
            return texname

    return ''


def load_texture(material, texname, dirname):
    tex = bpy.data.textures.new(name=texname, type='IMAGE')
    path = os.path.join(dirname, texname)
    try:
        tex.image = bpy.data.images.load(path)
    except:
        warning = 'Cannot load the texture {}'
        print(warning.format(path))
    else:
        info = 'The texture {} has been loaded'
        print(info.format(texname))
    mtex = material.texture_slots.add()
    mtex.texture = tex
    mtex.texture_coords = 'UV'


def read(file, context, operation):
    del context
    amt = bpy.data.armatures.new('Skeleton')
    root_name = os.path.basename(operation.filepath)
    root = bpy.data.objects.new(root_name, amt)
    bpy.context.scene.objects.link(root)

    sf_geom = SFGeometry(file)

    materials = []
    for sf_mat in sf_geom.materials:
        material = bpy.data.materials.new(sf_mat.name)
        texname = get_texture_name(operation.filepath, sf_mat.texture)
        if texname:
            dirname = os.path.dirname(operation.filepath)
            load_texture(material, texname, dirname)
        materials.append(material)

    if sf_geom.bones:
        bpy.context.scene.objects.active = root
        bpy.ops.object.mode_set(mode='EDIT')

        for sf_bone in sf_geom.bones:
            bone = amt.edit_bones.new(sf_bone.name)
            bone.head = sf_bone.pos_start
            bone.head_radius = sf_bone.bs_range
            bone.tail = sf_bone.pos_end

            if sf_bone.parent_id >= 0:
                bone.parent = amt.edit_bones[sf_bone.parent_id]

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.scene.objects.active = None

    for frag in sf_geom.fragments:
        name = sf_geom.materials[frag.mat_id].name
        mesh = bpy.data.meshes.new(name)
        obj = bpy.data.objects.new(name, mesh)
        obj.parent = root
        bpy.context.scene.objects.link(obj)

        # Push material
        material = materials[frag.mat_id]
        obj.data.materials.append(material)

        # Push vertices and faces to mesh
        offset = frag.facees_offset
        length = frag.facees_length
        indices = sf_geom.get_indices(offset, length)

        b_mesh = bmesh.new()
        b_mesh.from_mesh(mesh)

        # Vertices
        tex_coords = []
        for i in indices:
            sf_vertex = sf_geom.vertices[i]
            vertex = b_mesh.verts.new()
            vertex.co = sf_vertex.pos
            vertex.normal = sf_vertex.normal
            tex_coords.append(sf_vertex.tex_uv)
        b_mesh.verts.ensure_lookup_table()
        b_mesh.verts.index_update()

        # Faces
        for i in range(offset, offset+length):
            ids = sf_geom.faces[i].get_mapped_indices(indices)
            idx_1 = b_mesh.verts[ids[0]]
            idx_2 = b_mesh.verts[ids[1]]
            idx_3 = b_mesh.verts[ids[2]]
            try:
                b_mesh.faces.new((idx_1, idx_2, idx_3))
            except:
                msg = 'Warning: Skipped face for \'{}\' ({})'
                print(msg.format(name, frag.mat_id))

        # Texture coordinates
        uv_layer = b_mesh.loops.layers.uv.new()
        for face in b_mesh.faces:
            for loop in face.loops:
                loop[uv_layer].uv = tex_coords[loop.vert.index]

        b_mesh.to_mesh(mesh)
        b_mesh.free()
