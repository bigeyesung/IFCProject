import numpy as np
import trimesh
import os
if __name__ == "__main__":
    

    mesh = trimesh.load('data/Cube_3d_printing_sample.stl')
    scene = mesh.scene()
    for facet in mesh.facets:
        mesh.visual.face_colors[facet] = trimesh.visual.random_color()
    scene.show()
    print(scene.centroid)
    # a 45 degree homogeneous rotation matrix around
    # the Y axis at the scene centroid
    rotate = trimesh.transformations.rotation_matrix(
        angle=np.radians(10.0),
        direction=[0, 1, 0],
        point=scene.centroid)
    offset = np.array(
        [
            [1,0,0,0],
            [0,1,0,0],
            [0,0,1,10],
            [0,0,0,1]
        ]
    )
    # data = scene.scene.save_image()
    # if this doesn't work, try it with a visible window:
    # data = scene.save_image(visible=True)
    # png = scene.save_image(resolution=[1920, 1080], visible=True)
    # with open("file_name.png", 'wb') as f:
    #     f.write(png)
    #     f.close()

    for i in range(8):
        trimesh.constants.log.info('Saving image %d', i)

        # rotate the camera view transform
        # camera_old, _geometry = scene.graph[scene.camera]
        camera = scene.camera
        camera_old = scene.camera_transform
        print(scene.camera_transform)
        camera_new = np.dot(offset,camera_old)
       
        # apply the new transform
        # scene.show()
        scene.camera_transform = camera_new
        scene.show()
        # saving an image requires an opengl context, so if -nw
        # is passed don't save the image
        # try:
        #     # increment the file name
        #     file_name = 'render_' + str(i) + '.png'
        #     # save a render of the object as a png
        #     png = scene.save_image(resolution=[1920, 1080], visible=True)
        #     with open(file_name, 'wb') as f:
        #         f.write(png)
        #         f.close()

        # except BaseException as E:
        #     print("unable to save image", str(E))

    # from PIL import Image
    # rendered = Image.open(trimesh.util.wrap_as_stream(data))

# if __name__ == '__main__':
#     # print logged messages
#     trimesh.util.attach_to_log()

#     # load a mesh
#     mesh = trimesh.load('data/Cube_3d_printing_sample.stl')
#     # get a scene object containing the mesh, this is equivalent to:
#     scene = mesh.scene()
#     # a 45 degree homogeneous rotation matrix around
#     # the Y axis at the scene centroid
#     rotate = trimesh.transformations.rotation_matrix(
#         angle=np.radians(10.0),
#         direction=[0, 1, 0],
#         point=scene.centroid)

#     for i in range(4):
#         trimesh.constants.log.info('Saving image %d', i)

#         # rotate the camera view transform
#         # camera_old, _geometry = scene.graph[scene.camera]
#         camera_old = scene.camera_transform
#         camera_new = np.dot(camera_old, rotate)

#         # apply the new transform
#         # scene.camera = camera_new

#         # saving an image requires an opengl context, so if -nw
#         # is passed don't save the image
#         try:
#             # increment the file name
#             file_name = 'render_' + str(i) + '.png'
#             # save a render of the object as a png
#             png = scene.save_image(resolution=[1920, 1080], visible=True)
#             with open(file_name, 'wb') as f:
#                 f.write(png)
#                 f.close()

#         except BaseException as E:
#             print("unable to save image", str(E))