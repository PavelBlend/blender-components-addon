import bpy


socket_colors = {
    'BOOLEAN':  (0.0, 0.6, 0.0, 1.0),
    'INTEGER': (0.3, 0.3, 0.3, 1.0),
    'FLOAT': (0.6, 0.6, 0.6, 1.0),
    'INTEGER_VECTOR': (0.3, 0.3, 0.6, 1.0),
    'FLOAT_VECTOR': (0.6, 0.6, 1.0, 1.0),
    'COLOR': (1.0, 1.0, 0.0, 1.0),
    'MATRIX': (0.0, 0.3, 0.3, 1.0)
}
sockets_data = {}


def set_socket_data(socket, data):
    global sockets_data
    socket_data = sockets_data.get(socket.node.name)
    if not socket_data:
        sockets_data[socket.node.name] = {}
    sockets_data[socket.node.name][socket.name] = data


def get_socket_data(socket):
    global sockets_data
    node_data = sockets_data.get(socket.node.name, {})
    socket_data = node_data.get(socket.name, None)
    has_elements = not socket_data is None
    return socket_data, has_elements


class ComponentsBaseSocket(bpy.types.NodeSocket):
    bl_idname = 'components_base_socket'

    split_factor = 0.6

    def get_value(self):
        if len(self.links) and not self.is_output:
            from_socket = self.links[0].from_socket
            if hasattr(from_socket, 'get_value'):
                from_socket.node.execute()
                return from_socket.get_value()
            else:
                from_socket.node.execute()
                elements, has_elements = get_socket_data(self)
                if has_elements:
                    return elements
                else:
                    return [self.value, ]
        else:
            elements, has_elements = get_socket_data(self)
            if has_elements:
                return elements
            else:
                return [self.value, ]

    def draw(self, context, layout, node, text):
        if (not len(self.links) or self.is_output) and self.is_show:
            if self.text:
                row = layout.split(factor=self.split_factor)
                row.label(text=self.text)
                row.prop(self, 'value', text='')
            else:
                row = layout.split(factor=1.0)
                row.prop(self, 'value', text='')
        else:
            layout.label(text=self.text)


class ComponentsBooleanSocket(ComponentsBaseSocket):
    bl_idname = 'components_boolean_socket'

    value: bpy.props.BoolProperty(default=True)
    text: bpy.props.StringProperty(default='Boolean')

    def draw_color(self, context, node):
        return socket_colors['BOOLEAN']


class ComponentsIntegerSocket(ComponentsBaseSocket):
    bl_idname = 'components_integer_socket'

    value: bpy.props.IntProperty(default=0)
    text: bpy.props.StringProperty(default='Integer')

    def draw_color(self, context, node):
        return socket_colors['INTEGER']


class ComponentsFloatSocket(ComponentsBaseSocket):
    bl_idname = 'components_float_socket'

    value: bpy.props.FloatProperty(default=0.0, precision=6)
    text: bpy.props.StringProperty(default='Float')

    def draw_color(self, context, node):
        return socket_colors['FLOAT']


class ComponentsIntegerVectorSocket(ComponentsBaseSocket):
    bl_idname = 'components_integer_vector_socket'

    value: bpy.props.IntVectorProperty(default=(0, 0, 0), size=3)
    text: bpy.props.StringProperty(default='Integer Vector')

    def draw_color(self, context, node):
        return socket_colors['INTEGER_VECTOR']


class ComponentsFloatVectorSocket(ComponentsBaseSocket):
    bl_idname = 'components_float_vector_socket'

    value: bpy.props.FloatVectorProperty(
        default=(0.0, 0.0, 0.0), size=3, precision=6
    )
    text: bpy.props.StringProperty(default='Float Vector')

    def draw_color(self, context, node):
        return socket_colors['FLOAT_VECTOR']


class ComponentsColorSocket(ComponentsBaseSocket):
    bl_idname = 'components_color_socket'

    value: bpy.props.FloatVectorProperty(
        default=(1.0, 1.0, 1.0, 1.0), size=4, subtype='COLOR'
    )
    text: bpy.props.StringProperty(default='Color')

    def draw_color(self, context, node):
        return socket_colors['COLOR']


socket_classes = [
    ComponentsBooleanSocket,
    ComponentsIntegerSocket,
    ComponentsFloatSocket,
    ComponentsIntegerVectorSocket,
    ComponentsFloatVectorSocket,
    ComponentsColorSocket
]


def register():
    for socket_class in socket_classes:
        socket_class.__annotations__['is_show'] = bpy.props.BoolProperty(default=True)
        bpy.utils.register_class(socket_class)


def unregister():
    for socket_class in reversed(socket_classes):
        bpy.utils.unregister_class(socket_class)
