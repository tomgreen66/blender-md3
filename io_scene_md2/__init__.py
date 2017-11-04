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


bl_info = {
        "name": "Quake 2 Model (.md2)",
        "author": "Thomas Green",
        "blender": (2, 74, 0),
        "location": "File > Import-Export",
        "description": "Quake 2 Model format (.md2)",
        "warning": "",
        "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Import-Export/MD3",
        "tracker_url": "https://github.com/neumond/blender-md3/issues",
        "support": 'TESTING',
        "category": "Import-Export",
        }

if "bpy" in locals():
    import importlib
    if "import_md2" in locals():
        importlib.reload(import_md2)
    if "export_md2" in locals():
        importlib.reload(export_md2)


import bpy
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper, ExportHelper


class ImportMD2(bpy.types.Operator, ImportHelper):
    '''Import a Quake 2 Model MD2 file'''
    bl_idname = "import_scene.md2"
    bl_label = 'Import MD2'
    filename_ext = ".md2"
    filter_glob = StringProperty(default="*.md2", options={'HIDDEN'})

    def execute(self, context):
        from .import_md2 import MD2Importer
        MD2Importer(context)(self.properties.filepath)
        return {'FINISHED'}


class ExportMD2(bpy.types.Operator, ExportHelper):
    '''Export a Quake 3 Model MD2 file'''
    bl_idname = "export_scene.md2"
    bl_label = 'Export MD2'
    filename_ext = ".md2"
    filter_glob = StringProperty(default="*.md2", options={'HIDDEN'})

    def execute(self, context):
        from .export_md2 import MD2Exporter
        MD2Exporter(context)(self.properties.filepath)
        return {'FINISHED'}


def menu_func_import(self, context):
    self.layout.operator(ImportMD2.bl_idname, text="Quake 2 Model (.md2)")


def menu_func_export(self, context):
    self.layout.operator(ExportMD2.bl_idname, text="Quake 2 Model (.md2)")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_import.append(menu_func_import)
    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_import.remove(menu_func_import)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()
