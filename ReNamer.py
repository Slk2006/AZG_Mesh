bl_info = {
    "name": "Collection Objects Renamer",
    "author": "YourName",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "Scene Properties",
    "description": "Rename mesh objects in a collection with collection name prefix",
    "category": "Object",
}

import bpy

class CollectionRenamerPanel(bpy.types.Panel):
    bl_label = "Collection Renamer"
    bl_idname = "SCENE_PT_collection_renamer"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "cr_collection_name")
        layout.operator("object.rename_collection_objects", text="Rename Objects")

class RenameCollectionObjectsOperator(bpy.types.Operator):
    bl_idname = "object.rename_collection_objects"
    bl_label = "Rename Objects in Collection"

    def execute(self, context):
        scene = context.scene
        collection_name = scene.cr_collection_name.strip()

        if not collection_name:
            self.report({'ERROR'}, "Please enter a collection name")
            return {'CANCELLED'}

        collection = bpy.data.collections.get(collection_name)
        if not collection:
            self.report({'ERROR'}, f"Collection '{collection_name}' not found")
            return {'CANCELLED'}

        count = 1
        for obj in collection.objects:
            if obj.type == 'MESH':
                obj.name = f"{collection_name}{count:02d}"
                count += 1

        self.report({'INFO'}, f"Renamed {count-1} mesh objects in collection '{collection_name}'")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(CollectionRenamerPanel)
    bpy.utils.register_class(RenameCollectionObjectsOperator)
    bpy.types.Scene.cr_collection_name = bpy.props.StringProperty(
        name="Collection Name",
        description="Name of the collection to rename",
        default=""
    )

def unregister():
    bpy.utils.unregister_class(CollectionRenamerPanel)
    bpy.utils.unregister_class(RenameCollectionObjectsOperator)
    del bpy.types.Scene.cr_collection_name

if __name__ == "__main__":
    register()
