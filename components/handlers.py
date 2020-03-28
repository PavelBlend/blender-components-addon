import bpy


@bpy.app.handlers.persistent
def execute_node_tree(scene):
    for node_group in bpy.data.node_groups:
        if node_group.bl_idname == 'components_node_tree':
            for node in node_group.nodes:
                if hasattr(node, 'is_output'):
                    node.execute()


def register():
    bpy.app.handlers.frame_change_post.append(execute_node_tree)


def unregister():
    bpy.app.handlers.frame_change_post.remove(execute_node_tree)
