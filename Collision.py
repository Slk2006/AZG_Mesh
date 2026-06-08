import bpy

def create_collision_meshes():
    obj = bpy.context.object
    if not obj or obj.type != 'MESH':
        bpy.ops.message.report('INVOKE_DEFAULT', message="Select a valid mesh object")
        return

    mesh = obj.data
    original_name = obj.name
    total_faces = len(mesh.polygons)

    # Create or get collision collection
    collision_collection_name = f"{original_name}_collision_mesh"
    collision_collection = bpy.data.collections.get(collision_collection_name)
    if not collision_collection:
        collision_collection = bpy.data.collections.new(collision_collection_name)
        bpy.context.scene.collection.children.link(collision_collection)

    # Using mesh data directly without redundant operations
    verts = [v.co.copy() for v in mesh.vertices]

    # Generate collision mesh for each face
    for i, poly in enumerate(mesh.polygons, 1):
        face_verts = [verts[v] for v in poly.vertices]

        # Create mesh and object
        mesh_name = f"UCX_{original_name}_{str(i).zfill(2)}"
        new_mesh = bpy.data.meshes.new(mesh_name)
        new_mesh.from_pydata(face_verts, [], [list(range(len(face_verts)))])
        new_mesh.update()

        new_obj = bpy.data.objects.new(mesh_name, new_mesh)
        collision_collection.objects.link(new_obj)

    bpy.ops.message.report('INVOKE_DEFAULT', message=f"Created {total_faces} collision meshes in '{collision_collection_name}'")

# To make this a Blender operator with UI integration, register accordingly
class OBJECT_OT_CreateCollisionMeshes(bpy.types.Operator):
    bl_idname = "object.create_collision_meshes"
    bl_label = "Create Collision Meshes"
    bl_description = "Generate per-face collision meshes in a dedicated collection"

    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == 'MESH'

    def execute(self, context):
        create_collision_meshes()
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_CreateCollisionMeshes.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_CreateCollisionMeshes)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_CreateCollisionMeshes)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()

