from flask import Flask
import os
import argparse

app = Flask(__name__)

GCS_URL = 'https://storage.googleapis.com/download/storage/v1/b/mdl-ckpts/o/checkpoint.tar?alt=media'

AWS_TF_PATH = '/home/ec2-user/aws'
GCP_TF_PATH = '/home/ec2-user/gcp'

S3_BUCKET = 'mdl-ckpts'
S3_OBJ_KEY = 'checkpoint.tar'
CKPT_FILE_PATH = 'checkpoint.tar'

@app.route('/preempted')
def context_switch():
    os.system(f'curl -k -L -s {GCS_URL} -o /home/ec2-user/checkpoint.tar')

    os.system(f'terraform -chdir={AWS_TF_PATH} init')
    os.system(f'terraform -chdir={AWS_TF_PATH} apply -var resume=true -auto-approve')

    import json

    with open('/home/ec2-user/aws/terraform.tfstate') as f:
        ec2_state = json.load(f)
    
    public_dns = ''
    for resource in ec2_state['resources']:
        if resource['name'] == 'ec2_spot':
            public_dns = resource['instances'][0]['attributes']['public_dns']
            break
    
    # once copied,
    # this will trigger the resume() function
    os.system('sudo aws s3 cp /home/ec2-user/checkpoint.tar s3://mdl-ckpts/checkpoint.tar --profile demo-user')

    return ''

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--ipaddr')

    args = parser.parse_args()

    # when created, the spotvisor starts training on one cloud platform
    # NOTE: for the purposes of the demo, the order of GCP -> AWS is fixed
    os.system(f'sudo terraform -chdir={GCP_TF_PATH} init')
    os.system(f'sudo terraform -chdir={GCP_TF_PATH} apply -var \"api_host={args.ipaddr}\" -auto-approve')

    app.run(host='0.0.0.0', port=5000)

    