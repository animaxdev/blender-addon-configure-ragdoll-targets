
import bpy

bone_guide_format = 'RD_Target_{}'
copy_transform_name = 'RD guide'

bl_info = {
    'name': 'Configure RagDoll Targets',
    'author': 'gabriel montagné, gabriel@tibas.london',
    'version': (0, 0, 1),
    'blender': (2, 77, 0),
    'description': 'Add empties at each of the selected bones position and rotation  and add a bone "copy transforms" pointing to the empty.',
    'tracker_url': 'https://github.com/gabrielmontagne/blender-addon-configure-ragdoll-targets',
    'category': 'Object'
}

class ConfigureRDTargets(bpy.types.Operator):

    bl_idname = "pose.configure_rd_targets"
    bl_label = "Configure RagDoll Targets"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        active = bpy.context.active_object
        return active and active.pose and active.pose.bones

    def execute(self, context):
        scene = context.scene
        for bone, pose_bone, obj in [ (pose_bone.bone, pose_bone, pose_bone.id_data) for pose_bone in bpy.context.active_object.pose.bones if pose_bone.bone.select  ]:

            name = bone.name
            guide_name = bone_guide_format.format(name)

            guide_empty = bpy.data.objects.get(guide_name)

            if not guide_empty:
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.empty_add(type='PLAIN_AXES', radius=0.15)

                guide_empty = bpy.context.active_object
                guide_empty.name = guide_name

                transforms = pose_bone.constraints.new('COPY_TRANSFORMS')
                transforms.name = copy_transform_name
                transforms.target = guide_empty

            matrix_final = obj.matrix_world * pose_bone.matrix
            guide_empty.matrix_world = matrix_final



        return {'FINISHED'}

def register():
    bpy.utils.register_class(ConfigureRDTargets)

def unregister():
    bpy.utils.unregister_class(ConfigureRDTargets)

if __name__ == '__main__':
    register()
