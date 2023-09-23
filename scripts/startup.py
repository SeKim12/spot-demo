import argparse
import os

TF_VARS = [
    'image',
    'machine_type',
    'project',
    'region',
    'zone',
    'gcs_path'
]

TF_PATH = './terraform'

parser = argparse.ArgumentParser()

for var in TF_VARS:
    parser.add_argument(f'--{var}', default=None)

args = parser.parse_args()

os.system(f'terraform -chdir={TF_PATH} init')
os.system(f'terraform -chdir={TF_PATH} plan')

set_args = []
for arg in vars(args):
    if getattr(args, arg) is not None:
        set_args.append(f'{arg}={getattr(args, arg)}')

var_cli = ' -var '.join(set_args)

os.system(f'terraform -chdir={TF_PATH} apply -var {var_cli}')