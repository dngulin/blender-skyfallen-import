blender-skyfallen-import
========================

Addon for Blender that imports TheEngine's (Skyfallen Entertainment) 3D models. TheEngine is used in games: Planet Alcatraz (Санитары Подземелий), Planet Alcatraz 2 (Саниатры подземелий 2), Dawn of Magick (Магия крови), Dawn of Magick 2 (Магия крови 2), Elven Legacy, Fantasy Wars, King's Bounty.

This is a early version of an import script. The script is developed for Blender 2.79 and tested at 3D-models from Planet Alcatraz game (mesh format version 4.4 and 4.5).

For the addon installation copy the `skyfallen_import` directory into your blender addons directory and activate it in the user preferences.

The addon is licensed under the GNU GPL v.3.


### What is imported

1. Meshes
2. Materials (just textures and UV coordinates)
3. Armature and weights of vertices (from BMA files)


### TODO

1. Animations import: BSA and BCA(?) files
2. Support for mesh format versions greater then 4.5
3. Import material parameters