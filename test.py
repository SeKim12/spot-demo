import os

GCS_URL = 'https://storage.googleapis.com/download/storage/v1/b/mdl-ckpts/o/checkpoint.tar?alt=media'
TF_REL_PATH = './aws'

S3_BUCKET = 'mdl-ckpts'
S3_OBJ_KEY = 'checkpoint.tar'
CKPT_FILE_PATH = 'checkpoint.tar'

def run():
    os.system(f'curl -k -L -s {GCS_URL}')

    os.system(f'terraform -chdir={TF_REL_PATH} init')
    os.system(f'terraform -chdir={TF_REL_PATH} apply -var resume=true -auto-approve')

    import json

    with open('./aws/terraform.tfstate') as f:
        ec2_state = json.load(f)
    
    public_dns = ''
    for resource in ec2_state['resources']:
        if resource['name'] == 'ec2_spot':
            public_dns = resource['instances'][0]['attributes']['public_dns']
            break
    
    os.system(f'scp -i ~/.ssh/id_rsa ./checkpoint.tar ec2-user@{public_dns}:/home/ec2-user/checkpoint.tar')


if __name__ == "__main__":
    run()