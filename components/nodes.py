import bpy, inspect, mathutils, math

from . import sockets


CATEGORY_INPUT_NAME = 'Input'
CATEGORY_OUTPUT_NAME = 'Output'
CATEGORY_MATH_NAME = 'Math'
CATEGORY_DEBUG_NAME = 'Debug'
CATEGORY_CONVERT_NAME = 'Convert'
CATEGORY_ANALYZERS_NAME = 'Analyzers'
CATEGORY_STRUCTURES_NAME = 'Structures'
CATEGORY_TRANSFORMS_NAME = 'Transforms'


class BaseNode(bpy.types.Node):
    @classmethod
    def poll(cls, node_tree):
        return node_tree.bl_idname == 'components_node_tree'

    def execute(self):
        pass


class ComponentsBooleanNode(BaseNode):
    bl_idname = 'components_boolean_node'
    bl_label = 'Boolean'

    category = CATEGORY_INPUT_NAME

    def init(self, context):
        boolean_output = self.outputs.new(
            'components_boolean_socket',
            'Boolean'
        )
        boolean_output.text = ''


class ComponentsIntegerNode(BaseNode):
    bl_idname = 'components_integer_node'
    bl_label = 'Integer'

    category = CATEGORY_INPUT_NAME

    def init(self, context):
        integer_output = self.outputs.new(
            'components_integer_socket',
            'Integer'
        )
        integer_output.text = ''


class ComponentsFloatNode(BaseNode):
    bl_idname = 'components_float_node'
    bl_label = 'Float'

    category = CATEGORY_INPUT_NAME

    def init(self, context):
        float_output = self.outputs.new(
            'components_float_socket',
            'Float'
        )
        float_output.text = ''


class ComponentsIntegerVectorNode(BaseNode):
    bl_idname = 'components_integer_vector_node'
    bl_label = 'Integer Vector'

    category = CATEGORY_INPUT_NAME

    def init(self, context):
        integer_vector_output = self.outputs.new(
            'components_integer_vector_socket',
            'Integer Vector'
        )
        integer_vector_output.text = ''


class ComponentsFloatVectorNode(BaseNode):
    bl_idname = 'components_float_vector_node'
    bl_label = 'Float Vector'

    category = CATEGORY_INPUT_NAME

    def init(self, context):
        float_vector_output = self.outputs.new(
            'components_float_vector_socket',
            'Float Vector'
        )
        float_vector_output.text = ''


class ComponentsColorNode(BaseNode):
    bl_idname = 'components_color_node'
    bl_label = 'Color'

    category = CATEGORY_INPUT_NAME

    def init(self, context):
        color_output = self.outputs.new(
            'components_color_socket',
            'Color'
        )
        color_output.text = ''


class ComponentsMeshNode(BaseNode):
    bl_idname = 'components_mesh_node'
    bl_label = 'Mesh'

    category = CATEGORY_INPUT_NAME
    bpy_mesh_name: bpy.props.StringProperty()

    def init(self, context):
        vertices_output = self.outputs.new(
            'components_float_vector_socket',
            'Vertices'
        )
        vertices_output.text = 'Vertices'
        vertices_output.is_show = False

        polygons_output = self.outputs.new(
            'components_integer_vector_socket',
            'Polygons'
        )
        polygons_output.text = 'Polygons'
        polygons_output.is_show = False

    def draw_buttons(self, context, layout):
        layout.prop_search(self, 'bpy_mesh_name', bpy.data, 'meshes', text='')

    def execute(self):
        bpy_mesh = bpy.data.meshes.get(self.bpy_mesh_name)
        vertices_socket = self.outputs['Vertices']
        polygons_socket = self.outputs['Polygons']
        if bpy_mesh:
            vertices = []
            polygons = []
            for vertex in bpy_mesh.vertices:
                vertices.append(vertex.co)
            for polygon in bpy_mesh.polygons:
                polygons.append(polygon.vertices)
            sockets.set_socket_data(vertices_socket, vertices)
            sockets.set_socket_data(polygons_socket, polygons)


class ComponentsCreateMeshNode(BaseNode):
    bl_idname = 'components_create_mesh_node'
    bl_label = 'Create Mesh'

    category = CATEGORY_OUTPUT_NAME
    bpy_mesh_name: bpy.props.StringProperty(name='Mesh Name')
    is_output: bpy.props.BoolProperty(default=True)

    def init(self, context):
        vertices_input = self.inputs.new(
            'components_float_vector_socket',
            'Vertices'
        )
        vertices_input.text = 'Vertices'
        vertices_input.is_show = False

        polygons_input = self.inputs.new(
            'components_integer_vector_socket',
            'Polygons'
        )
        polygons_input.text = 'Polygons'
        polygons_input.is_show = False

    def draw_buttons(self, context, layout):
        layout.prop(self, 'bpy_mesh_name')

    def execute(self):
        vertices = self.inputs['Vertices'].get_value()
        polygons = self.inputs['Polygons'].get_value()
        bpy_mesh = bpy.data.meshes.get(self.bpy_mesh_name)
        if not bpy_mesh:
            bpy_mesh = bpy.data.meshes.new(self.bpy_mesh_name)
        bpy_mesh.clear_geometry()
        bpy_object = bpy.data.objects.get(self.bpy_mesh_name)
        if not bpy_object:
            bpy_object = bpy.data.objects.new(self.bpy_mesh_name, bpy_mesh)
            bpy.context.scene.collection.objects.link(bpy_object)
        if len(polygons) == 1:
            if polygons[0][0] == 0 and polygons[0][1] == 0 and polygons[0][2] == 0:
                polygons = []
        bpy_mesh.from_pydata(vertices, (), polygons)


def add_vector_execute(self):
    inputs_velues_1 = self.inputs['Input 1'].get_value()
    inputs_velues_2 = self.inputs['Input 2'].get_value()
    result_socket = self.outputs['Result']
    result = []
    if len(inputs_velues_1) == len(inputs_velues_2):
        for index, input_1 in enumerate(inputs_velues_1):
            result.append((
                input_1[0] + inputs_velues_2[index][0],
                input_1[1] + inputs_velues_2[index][1],
                input_1[2] + inputs_velues_2[index][2]
            ))
    elif len(inputs_velues_1) == 1 and len(inputs_velues_2) != 1:
        for index, input_2 in enumerate(inputs_velues_2):
            result.append((
                inputs_velues_1[0][0] + input_2[0],
                inputs_velues_1[0][1] + input_2[1],
                inputs_velues_1[0][2] + input_2[2]
            ))
    elif len(inputs_velues_1) != 1 and len(inputs_velues_2) == 1:
        for index, input_1 in enumerate(inputs_velues_1):
            result.append((
                input_1[0] + inputs_velues_2[0][0],
                input_1[1] + inputs_velues_2[0][1],
                input_1[2] + inputs_velues_2[0][2]
            ))
    sockets.set_socket_data(result_socket, result)


def multiply_vector_execute(self):
    inputs_velues_1 = self.inputs['Input 1'].get_value()
    inputs_velues_2 = self.inputs['Input 2'].get_value()
    result_socket = self.outputs['Result']
    result = []
    if len(inputs_velues_1) == len(inputs_velues_2):
        for index, input_1 in enumerate(inputs_velues_1):
            result.append((
                input_1[0] * inputs_velues_2[index][0],
                input_1[1] * inputs_velues_2[index][1],
                input_1[2] * inputs_velues_2[index][2]
            ))
    elif len(inputs_velues_1) == 1 and len(inputs_velues_2) != 1:
        for index, input_2 in enumerate(inputs_velues_2):
            result.append((
                inputs_velues_1[0][0] * input_2[0],
                inputs_velues_1[0][1] * input_2[1],
                inputs_velues_1[0][2] * input_2[2]
            ))
    elif len(inputs_velues_1) != 1 and len(inputs_velues_2) == 1:
        for index, input_1 in enumerate(inputs_velues_1):
            result.append((
                input_1[0] * inputs_velues_2[0][0],
                input_1[1] * inputs_velues_2[0][1],
                input_1[2] * inputs_velues_2[0][2]
            ))
    sockets.set_socket_data(result_socket, result)


class ComponentsAddFloatVectorNode(BaseNode):
    bl_idname = 'components_add_float_vector_node'
    bl_label = 'Add Float Vector'

    category = CATEGORY_MATH_NAME

    def init(self, context):
        result_output = self.outputs.new(
            'components_float_vector_socket',
            'Result'
        )
        result_output.text = 'Result'
        result_output.is_show = False

        input_1 = self.inputs.new(
            'components_float_vector_socket',
            'Input 1'
        )
        input_1.text = 'Value 1'

        input_2 = self.inputs.new(
            'components_float_vector_socket',
            'Input 2'
        )
        input_2.text = 'Value 2'

    def execute(self):
        add_vector_execute(self)


class ComponentsAddIntegerVectorNode(BaseNode):
    bl_idname = 'components_add_integer_vector_node'
    bl_label = 'Add Integer Vector'

    category = CATEGORY_MATH_NAME

    def init(self, context):
        result_output = self.outputs.new(
            'components_integer_vector_socket',
            'Result'
        )
        result_output.text = 'Result'
        result_output.is_show = False

        input_1 = self.inputs.new(
            'components_integer_vector_socket',
            'Input 1'
        )
        input_1.text = 'Value 1'

        input_2 = self.inputs.new(
            'components_integer_vector_socket',
            'Input 2'
        )
        input_2.text = 'Value 2'

    def execute(self):
        add_vector_execute(self)


def multiply_execute(self):
    inputs_velues_1 = self.inputs['Input 1'].get_value()
    inputs_velues_2 = self.inputs['Input 2'].get_value()
    result_socket = self.outputs['Result']
    result = []
    if len(inputs_velues_1) == len(inputs_velues_2):
        for index, input_1 in enumerate(inputs_velues_1):
            result.append(input_1 * inputs_velues_2[index])
    elif len(inputs_velues_1) == 1 and len(inputs_velues_2) != 1:
        for index, input_2 in enumerate(inputs_velues_2):
            result.append(inputs_velues_1[0] * input_2)
    elif len(inputs_velues_1) != 1 and len(inputs_velues_2) == 1:
        for index, input_1 in enumerate(inputs_velues_1):
            result.append(input_1 * inputs_velues_2[0])
    sockets.set_socket_data(result_socket, result)


class ComponentsMultiplyIntegerNode(BaseNode):
    bl_idname = 'components_multiply_integer_node'
    bl_label = 'Multiply Integer'

    category = CATEGORY_MATH_NAME

    def init(self, context):
        result_output = self.outputs.new(
            'components_integer_socket',
            'Result'
        )
        result_output.text = 'Result'
        result_output.is_show = False

        input_1 = self.inputs.new(
            'components_integer_socket',
            'Input 1'
        )
        input_1.text = 'Value 1'

        input_2 = self.inputs.new(
            'components_integer_socket',
            'Input 2'
        )
        input_2.text = 'Value 2'

    def execute(self):
        multiply_execute(self)


class ComponentsMultiplyIntegerVectorNode(BaseNode):
    bl_idname = 'components_multiply_integer_vector_node'
    bl_label = 'Multiply Integer Vector'

    category = CATEGORY_MATH_NAME

    def init(self, context):
        result_output = self.outputs.new(
            'components_integer_vector_socket',
            'Result'
        )
        result_output.text = 'Result'
        result_output.is_show = False

        input_1 = self.inputs.new(
            'components_integer_vector_socket',
            'Input 1'
        )
        input_1.text = 'Value 1'

        input_2 = self.inputs.new(
            'components_integer_vector_socket',
            'Input 2'
        )
        input_2.text = 'Value 2'

    def execute(self):
        multiply_vector_execute(self)


def add_execute(self):
    inputs_velues_1 = self.inputs['Input 1'].get_value()
    inputs_velues_2 = self.inputs['Input 2'].get_value()
    result_socket = self.outputs['Result']
    result = []
    if len(inputs_velues_1) == len(inputs_velues_2):
        for index, input_1 in enumerate(inputs_velues_1):
            result.append(input_1 + inputs_velues_2[index])
    elif len(inputs_velues_1) == 1 and len(inputs_velues_2) != 1:
        for index, input_2 in enumerate(inputs_velues_2):
            result.append(inputs_velues_1[0] + input_2)
    elif len(inputs_velues_1) != 1 and len(inputs_velues_2) == 1:
        for index, input_1 in enumerate(inputs_velues_1):
            result.append(input_1 + inputs_velues_2[0])
    sockets.set_socket_data(result_socket, result)


class ComponentsAddFloatNode(BaseNode):
    bl_idname = 'components_add_float_node'
    bl_label = 'Add Float'

    category = CATEGORY_MATH_NAME

    def init(self, context):
        result_output = self.outputs.new(
            'components_float_socket',
            'Result'
        )
        result_output.text = 'Result'
        result_output.is_show = False

        input_1 = self.inputs.new(
            'components_float_socket',
            'Input 1'
        )
        input_1.text = 'Value 1'

        input_2 = self.inputs.new(
            'components_float_socket',
            'Input 2'
        )
        input_2.text = 'Value 2'

    def execute(self):
        add_execute(self)


class ComponentsAddIntegerNode(BaseNode):
    bl_idname = 'components_add_integer_node'
    bl_label = 'Add Integer'

    category = CATEGORY_MATH_NAME

    def init(self, context):
        result_output = self.outputs.new(
            'components_integer_socket',
            'Result'
        )
        result_output.text = 'Result'
        result_output.is_show = False

        input_1 = self.inputs.new(
            'components_integer_socket',
            'Input 1'
        )
        input_1.text = 'Value 1'

        input_2 = self.inputs.new(
            'components_integer_socket',
            'Input 2'
        )
        input_2.text = 'Value 2'

    def execute(self):
        add_vector_execute(self)


class ComponentsSeparateFloatVectorNode(BaseNode):
    bl_idname = 'components_separate_float_vector_node'
    bl_label = 'Separate Float Vector'

    category = CATEGORY_CONVERT_NAME

    def init(self, context):
        result_x_output = self.outputs.new(
            'components_float_socket',
            'X'
        )
        result_x_output.text = 'X'
        result_x_output.is_show = False

        result_y_output = self.outputs.new(
            'components_float_socket',
            'Y'
        )
        result_y_output.text = 'Y'
        result_y_output.is_show = False

        result_z_output = self.outputs.new(
            'components_float_socket',
            'Z'
        )
        result_z_output.text = 'Z'
        result_z_output.is_show = False

        input_vector = self.inputs.new(
            'components_float_vector_socket',
            'Input'
        )
        input_vector.text = 'Input'

    def execute(self):
        input_vectors = self.inputs['Input'].get_value()
        result_x = []
        result_y = []
        result_z = []

        for vector in input_vectors:
            result_x.append(vector[0])
            result_y.append(vector[1])
            result_z.append(vector[2])

        result_x_socket = self.outputs['X']
        sockets.set_socket_data(result_x_socket, result_x)

        result_y_socket = self.outputs['Y']
        sockets.set_socket_data(result_y_socket, result_y)

        result_z_socket = self.outputs['Z']
        sockets.set_socket_data(result_z_socket, result_z)


class ComponentsSeparateIntegerVectorNode(BaseNode):
    bl_idname = 'components_separate_integer_vector_node'
    bl_label = 'Separate Integer Vector'

    category = CATEGORY_CONVERT_NAME

    def init(self, context):
        result_x_output = self.outputs.new(
            'components_integer_socket',
            'X'
        )
        result_x_output.text = 'X'
        result_x_output.is_show = False

        result_y_output = self.outputs.new(
            'components_integer_socket',
            'Y'
        )
        result_y_output.text = 'Y'
        result_y_output.is_show = False

        result_z_output = self.outputs.new(
            'components_integer_socket',
            'Z'
        )
        result_z_output.text = 'Z'
        result_z_output.is_show = False

        input_vector = self.inputs.new(
            'components_integer_vector_socket',
            'Input'
        )
        input_vector.text = 'Input'

    def execute(self):
        input_vectors = self.inputs['Input'].get_value()
        result_x = []
        result_y = []
        result_z = []

        for vector in input_vectors:
            result_x.append(vector[0])
            result_y.append(vector[1])
            result_z.append(vector[2])

        result_x_socket = self.outputs['X']
        sockets.set_socket_data(result_x_socket, result_x)

        result_y_socket = self.outputs['Y']
        sockets.set_socket_data(result_y_socket, result_y)

        result_z_socket = self.outputs['Z']
        sockets.set_socket_data(result_z_socket, result_z)


class ComponentsCombineFloatVectorNode(BaseNode):
    bl_idname = 'components_combine_float_vector_node'
    bl_label = 'Combine Float Vector'

    category = CATEGORY_CONVERT_NAME

    def init(self, context):
        result_x_input = self.inputs.new(
            'components_float_socket',
            'X'
        )
        result_x_input.text = 'X'

        result_y_input = self.inputs.new(
            'components_float_socket',
            'Y'
        )
        result_y_input.text = 'Y'

        result_z_input = self.inputs.new(
            'components_float_socket',
            'Z'
        )
        result_z_input.text = 'Z'

        output_vector = self.outputs.new(
            'components_float_vector_socket',
            'Vector'
        )
        output_vector.text = 'Vector'
        output_vector.is_show = False

    def execute(self):
        input_x = self.inputs['X'].get_value()
        input_y = self.inputs['Y'].get_value()
        input_z = self.inputs['Z'].get_value()
        result = []
        if len(input_x) == len(input_y) == len(input_z):
            for index, x in enumerate(input_x):
                y = input_y[index]
                z = input_z[index]
                result.append([x, y, z])
        sockets.set_socket_data(self.outputs['Vector'], result)


class ComponentsCombineIntegerVectorNode(BaseNode):
    bl_idname = 'components_combine_integer_vector_node'
    bl_label = 'Combine Integer Vector'

    category = CATEGORY_CONVERT_NAME

    def init(self, context):
        result_x_input = self.inputs.new(
            'components_integer_socket',
            'X'
        )
        result_x_input.text = 'X'

        result_y_input = self.inputs.new(
            'components_integer_socket',
            'Y'
        )
        result_y_input.text = 'Y'

        result_z_input = self.inputs.new(
            'components_integer_socket',
            'Z'
        )
        result_z_input.text = 'Z'

        output_vector = self.outputs.new(
            'components_integer_vector_socket',
            'Vector'
        )
        output_vector.text = 'Vector'
        output_vector.is_show = False

    def execute(self):
        input_x = self.inputs['X'].get_value()
        input_y = self.inputs['Y'].get_value()
        input_z = self.inputs['Z'].get_value()
        result = []
        if len(input_x) == len(input_y) == len(input_z):
            for index, x in enumerate(input_x):
                y = input_y[index]
                z = input_z[index]
                result.append([x, y, z])
        sockets.set_socket_data(self.outputs['Vector'], result)


class ComponentsConsoleOutputNode(BaseNode):
    bl_idname = 'components_console_output_node'
    bl_label = 'Console Output'
    is_output: bpy.props.BoolProperty(default=True)

    category = CATEGORY_DEBUG_NAME
    strings = []

    def init(self, context):
        input_socket = self.inputs.new(
            'components_boolean_socket',
            'Input'
        )
        input_socket.text = 'Input'
        input_socket.is_show = False

    def execute(self):
        self.strings.clear()
        input_socket = self.inputs['Input']
        input_data = input_socket.get_value()
        if len(input_socket.links):
            if len(input_data) <= 100:
                for value in input_data:
                    try:
                        iter(value)
                        iterable = True
                    except:
                        iterable = False
                    if iterable:
                        debug_string = ' '.join(map(str, value))
                    else:
                        debug_string = str(value)
                    self.strings.append(debug_string)
            else:
                for value_index in (0, 1, 2, -3, -2, -1):
                    value = input_data[value_index]
                    if value_index == -3:
                        self.strings.append('...')
                    try:
                        iter(value)
                        iterable = True
                    except:
                        iterable = False
                    if iterable:
                        debug_string = ' '.join(map(str, value))
                    else:
                        debug_string = str(value)
                    self.strings.append(debug_string)
        print(self.name)
        for string in self.strings:
            print(string)
        print(79 * '#')


class ComponentsGetLengthNode(BaseNode):
    bl_idname = 'components_get_length_node'
    bl_label = 'Get Length'

    category = CATEGORY_ANALYZERS_NAME
    strings = []

    def init(self, context):
        input_socket = self.inputs.new(
            'components_boolean_socket',
            'Input'
        )
        input_socket.text = 'Input'
        input_socket.is_show = False

        output_socket = self.outputs.new(
            'components_integer_socket',
            'Length'
        )
        output_socket.text = 'Length'
        output_socket.is_show = False

    def execute(self):
        result = [len(self.inputs['Input'].get_value()), ]
        sockets.set_socket_data(self.outputs['Length'], result)


class ComponentsMergeFloatNode(BaseNode):
    bl_idname = 'components_merge_float_node'
    bl_label = 'Merge Float'

    category = CATEGORY_STRUCTURES_NAME

    def init(self, context):
        result_output = self.outputs.new(
            'components_float_socket',
            'Result'
        )
        result_output.text = 'Result'
        result_output.is_show = False

        input_1 = self.inputs.new(
            'components_float_socket',
            'Input 1'
        )
        input_1.text = 'Value 1'

        input_2 = self.inputs.new(
            'components_float_socket',
            'Input 2'
        )
        input_2.text = 'Value 2'

    def execute(self):
        result_socket = self.outputs['Result']
        result = []
        input_1 = self.inputs['Input 1'].get_value()
        input_2 = self.inputs['Input 2'].get_value()
        result.extend(input_1)
        result.extend(input_2)
        sockets.set_socket_data(result_socket, result)


class ComponentsMergeInegerNode(BaseNode):
    bl_idname = 'components_merge_integer_node'
    bl_label = 'Merge Integer'

    category = CATEGORY_STRUCTURES_NAME

    def init(self, context):
        result_output = self.outputs.new(
            'components_integer_socket',
            'Result'
        )
        result_output.text = 'Result'
        result_output.is_show = False

        input_1 = self.inputs.new(
            'components_integer_socket',
            'Input 1'
        )
        input_1.text = 'Value 1'

        input_2 = self.inputs.new(
            'components_integer_socket',
            'Input 2'
        )
        input_2.text = 'Value 2'

    def execute(self):
        result_socket = self.outputs['Result']
        result = []
        input_1 = self.inputs['Input 1'].get_value()
        input_2 = self.inputs['Input 2'].get_value()
        result.extend(input_1)
        result.extend(input_2)
        sockets.set_socket_data(result_socket, result)


class ComponentsMergeIntegerVectorNode(BaseNode):
    bl_idname = 'components_merge_integer_vector_node'
    bl_label = 'Merge Integer Vector'

    category = CATEGORY_STRUCTURES_NAME

    def init(self, context):
        result_output = self.outputs.new(
            'components_integer_vector_socket',
            'Result'
        )
        result_output.text = 'Result'
        result_output.is_show = False

        input_1 = self.inputs.new(
            'components_integer_vector_socket',
            'Input 1'
        )
        input_1.text = 'Value 1'

        input_2 = self.inputs.new(
            'components_integer_vector_socket',
            'Input 2'
        )
        input_2.text = 'Value 2'

    def execute(self):
        result_socket = self.outputs['Result']
        result = []
        input_1 = self.inputs['Input 1'].get_value()
        input_2 = self.inputs['Input 2'].get_value()
        result.extend(input_1)
        result.extend(input_2)
        sockets.set_socket_data(result_socket, result)


class ComponentsMergeFloatVectorNode(BaseNode):
    bl_idname = 'components_merge_float_vector_node'
    bl_label = 'Merge Float Vector'

    category = CATEGORY_STRUCTURES_NAME

    def init(self, context):
        result_output = self.outputs.new(
            'components_float_vector_socket',
            'Result'
        )
        result_output.text = 'Result'
        result_output.is_show = False

        input_1 = self.inputs.new(
            'components_float_vector_socket',
            'Input 1'
        )
        input_1.text = 'Value 1'

        input_2 = self.inputs.new(
            'components_float_vector_socket',
            'Input 2'
        )
        input_2.text = 'Value 2'

    def execute(self):
        result_socket = self.outputs['Result']
        result = []
        input_1 = self.inputs['Input 1'].get_value()
        input_2 = self.inputs['Input 2'].get_value()
        result.extend(input_1)
        result.extend(input_2)
        sockets.set_socket_data(result_socket, result)


class ComponentsFloatToIntegerNode(BaseNode):
    bl_idname = 'components_float_to_integer_node'
    bl_label = 'Float to Integer'

    category = CATEGORY_CONVERT_NAME
    strings = []

    def init(self, context):
        input_socket = self.inputs.new(
            'components_float_socket',
            'Input'
        )
        input_socket.text = 'Input'

        output_socket = self.outputs.new(
            'components_integer_socket',
            'Result'
        )
        output_socket.text = 'Integer'
        output_socket.is_show = False

    def execute(self):
        result = []
        for float_value in self.inputs['Input'].get_value():
            result.append(int(float_value))
        sockets.set_socket_data(self.outputs['Result'], result)


class ComponentsIntegerToFloatNode(BaseNode):
    bl_idname = 'components_integer_to_float_node'
    bl_label = 'Integer to Float'

    category = CATEGORY_CONVERT_NAME
    strings = []

    def init(self, context):
        input_socket = self.inputs.new(
            'components_integer_socket',
            'Input'
        )
        input_socket.text = 'Input'

        output_socket = self.outputs.new(
            'components_float_socket',
            'Result'
        )
        output_socket.text = 'Float'
        output_socket.is_show = False

    def execute(self):
        result = []
        for integer_value in self.inputs['Input'].get_value():
            result.append(float(integer_value))
        sockets.set_socket_data(self.outputs['Result'], result)


class ComponentsCycleNode(BaseNode):
    bl_idname = 'components_cycle_node'
    bl_label = 'Cycle'

    category = CATEGORY_MATH_NAME
    iteration_node: bpy.props.StringProperty()

    def init(self, context):
        result_output = self.outputs.new(
            'components_boolean_socket',
            'Result'
        )
        result_output.text = 'Result'
        result_output.is_show = False

        iterations_input = self.inputs.new(
            'components_integer_socket',
            'Iterations'
        )
        iterations_input.text = 'Iterations'

        input_value = self.inputs.new(
            'components_boolean_socket',
            'Input'
        )
        input_value.text = 'Input'
        input_value.is_show = False

    def execute(self):
        iterations_count = self.inputs['Iterations'].get_value()
        result = []
        iteration_node = self.id_data.nodes.get(self.iteration_node)
        for iteration_index in range(0, iterations_count[0]):
            if iteration_node:
                iteration_socket = iteration_node.outputs['Iteration']
                sockets.set_socket_data(iteration_socket, [iteration_index, ])
            iteration_result = self.inputs['Input'].get_value()
            result.extend(iteration_result)
        sockets.set_socket_data(self.outputs['Result'], result)

    def draw_buttons(self, context, layout):
        layout.prop_search(self, 'iteration_node', self.id_data, 'nodes', text='Iteration Node')


class ComponentsCycleIterationNode(BaseNode):
    bl_idname = 'components_cycle_iteration_node'
    bl_label = 'Cycle Iteration'

    category = CATEGORY_MATH_NAME

    def init(self, context):
        result_output = self.outputs.new(
            'components_boolean_socket',
            'Iteration'
        )
        result_output.text = 'Iteration'
        result_output.is_show = False


class ComponentsRotateNode(BaseNode):
    bl_idname = 'components_rotate_node'
    bl_label = 'Rotate'

    category = CATEGORY_TRANSFORMS_NAME

    def init(self, context):
        input_socket = self.inputs.new(
            'components_float_vector_socket',
            'Input'
        )
        input_socket.text = 'Input'

        euler_socket = self.inputs.new(
            'components_float_vector_socket',
            'Euler'
        )
        euler_socket.text = 'Euler'

        output_socket = self.outputs.new(
            'components_float_vector_socket',
            'Result'
        )
        output_socket.text = 'Result'
        output_socket.is_show = False

    def execute(self):
        result = []
        euler = self.inputs['Euler'].get_value()
        inputs = self.inputs['Input'].get_value()
        if len(euler) == 1:
            for index, value in enumerate(inputs):
                matrix = mathutils.Euler(
                    map(math.radians, euler[0]),
                    'XYZ'
                ).to_matrix().to_4x4()
                result.append(matrix @ mathutils.Vector(value))
        elif len(euler) == len(inputs):
            for index, value in enumerate(self.inputs['Input'].get_value()):
                matrix = mathutils.Euler(
                    map(math.radians, euler[index]),
                    'XYZ'
                ).to_matrix().to_4x4()
                result.append(matrix @ mathutils.Vector(value))
        sockets.set_socket_data(self.outputs['Result'], result)


class ComponentsHashNode(BaseNode):
    bl_idname = 'components_hash_node'
    bl_label = 'Hash'

    category = CATEGORY_MATH_NAME
    seed: bpy.props.IntProperty()

    def init(self, context):
        result_output = self.outputs.new(
            'components_float_socket',
            'Hash'
        )
        result_output.text = 'Hash'
        result_output.is_show = False

        input_value = self.inputs.new(
            'components_boolean_socket',
            'Input'
        )
        input_value.text = 'Input'
        input_value.is_show = False

    def execute(self):
        input_value = self.inputs['Input'].get_value()
        result = []
        for value in input_value:
            try:
                value = tuple(value)
            except:
                value = value
            result.append([(hash(value) + hash(self.seed)) / 2, ])
        sockets.set_socket_data(self.outputs['Hash'], result)


def get_nodes():
    node_classes = []
    glabal_variables = globals().copy()
    for variable_name, variable_object in glabal_variables.items():
        if hasattr(variable_object, '__mro__'):
            object_mro = inspect.getmro(variable_object)
            if BaseNode in object_mro and variable_object != BaseNode:
                node_classes.append(variable_object)
    return node_classes


def register():
    node_classes = get_nodes()

    for node_class in node_classes:
        bpy.utils.register_class(node_class)


def unregister():
    node_classes = get_nodes()

    for node_class in reversed(node_classes):
        bpy.utils.unregister_class(node_class)
