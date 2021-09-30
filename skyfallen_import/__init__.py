import bpy
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator

bl_info = {
    'name': 'Skyfallen TheEngine 3D Data Importer',
    'author': 'Danil Gulin',
    'version': (2, 0, 0),
    'blender': (2, 93, 0),
    'location': 'File > Import > Skyfallen Geometry',
    'description': 'Imports BMS and BMA files',
    'warning': '',
    'category': 'Import-Export'
}


class ImportGeometry(Operator, ImportHelper):
    bl_idname = 'import_geometry.skyfallen_geometry'
    bl_label = 'Skyfallen Geometry (*.bms, *.bma)'

    filter_glob = StringProperty(default='*.bms;*.bma', options={'HIDDEN'})

    def execute(self, context):
        print('Importing file', self.filepath)
        from . import import_geometry
        with open(self.filepath, 'rb') as file:
            import_geometry.read(file, self)
        return {'FINISHED'}


def menu_import_geometry(self, context):
    self.layout.operator(ImportGeometry.bl_idname, text=ImportGeometry.bl_label)


def register():
    bpy.utils.register_class(ImportGeometry)
    bpy.types.TOPBAR_MT_file_import.append(menu_import_geometry)


def unregister():
    bpy.utils.unregister_class(ImportGeometry)
    bpy.types.TOPBAR_MT_file_import.remove(menu_import_geometry)


if __name__ == "__main__":
    register()
