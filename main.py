import os
import bpy
import molecularnodes as mn
from xdatbus.fbld01_pos2bpdb import pos2bpdb
from xdatbus.fbld02_rm_bond import rm_bond
from xdatbus.utils_bpy import clear_scene, apply_modifiers_to_mesh, apply_yaml, yaml_gen

current_dir = os.getcwd()
poscar_path = os.path.join(current_dir, 'LLTO-U2-N0-OV1-07-013-POSCAR.poscar')
pdb_path = os.path.join(current_dir, 'LLTO-U2-N0-OV1-07-013-POSCAR.pdb')
pos2bpdb(poscar_path, pdb_path)

rm_bond(pdb_path, "LI", "TI", pdb_path)
rm_bond(pdb_path, "LA", "TI", pdb_path)
rm_bond(pdb_path, "LA", "O", pdb_path)
rm_bond(pdb_path, "LA", "LA", pdb_path)
rm_bond(pdb_path, "LA", "LI", pdb_path)

# Generate YAML file
yaml_gen(pdb_path)

# Load the molecule and apply the style
clear_scene()
mol = mn.load.molecule_local(pdb_path, default_style='ball_and_stick')
yaml_path = pdb_path[:-4] + '_style.yaml'
apply_yaml(mol, yaml_path)

# Export the scene to a blender file
output_blend_path = os.path.join(current_dir, 'output.blend')
bpy.ops.wm.save_as_mainfile(filepath=output_blend_path)

# Apply modifiers if the object is a mesh
apply_modifiers_to_mesh(mol)

# Export the scene to an FBX file
output_fbx_path = os.path.join(current_dir, 'output.fbx')
bpy.ops.export_scene.fbx(filepath=output_fbx_path,
                         use_selection=True,
                         path_mode='COPY')

