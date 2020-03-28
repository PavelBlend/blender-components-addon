import bpy


class ComponentsNodeTree(bpy.types.NodeTree):
    bl_idname = 'components_node_tree'
    bl_label = 'Components'
    bl_icon = 'MESH_DATA'

    @classmethod
    def poll(cls, context):
        return True


def register():
    bpy.utils.register_class(ComponentsNodeTree)


def unregister():
    bpy.utils.unregister_class(ComponentsNodeTree)
