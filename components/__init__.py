bl_info = {
    'name': 'Components',
    'blender': (2, 82, 0),
    'category': 'Node'
}


from . import tree, sockets, nodes, categories, handlers


addon_modules = [
    tree,
    sockets,
    nodes,
    categories,
    handlers
]


def register():
    for addon_module in addon_modules:
        addon_module.register()


def unregister():
    for addon_module in reversed(addon_modules):
        addon_module.unregister()
