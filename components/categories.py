import bpy, nodeitems_utils

from . import nodes


class ComponentsNodeCategory(nodeitems_utils.NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'components_node_tree'


def register():
    node_categories_data = {}
    node_classes = nodes.get_nodes()
    for node in node_classes:
        if not node_categories_data.get(node.category, None):
            node_categories_data[node.category] = []
        node_categories_data[node.category].append(node.bl_idname)

    node_categories = []
    for category_name, nodes_ids in node_categories_data.items():
        category_items = []
        for node_id in nodes_ids:
            category_items.append(nodeitems_utils.NodeItem(node_id))
        category = ComponentsNodeCategory(
            category_name.lower().replace(' ', '_'),
            category_name,
            items=category_items
        )
        node_categories.append(category)

    nodeitems_utils.register_node_categories(
        'components_node_tree', node_categories
    )


def unregister():
    nodeitems_utils.unregister_node_categories('components_node_tree')
