"""Cloud Foundry test"""
from flask import Flask,jsonify
import os

# New imports
import json
import ibm_db
import logging
import watson_developer_cloud

# Emit Bluemix deployment event
#cf_deployment_tracker.track()

app = Flask(__name__)

# New code for VCAP
# Parse VCAP_SERVICES Variable
vcap_services = json.loads(os.environ['VCAP_SERVICES'])
print(vcap_services)
service = vcap_services['discovery'][0]
credentials = service["credentials"]

@app.route('/')
def hello_world():
    result = discovery_v1()
    return result

# Update port #
port = os.getenv('PORT', '5000')

def discovery_v1():
    #print only print output into logs , so have to define a string to record output to be shown in UI
    return_str = ""
    #below codes are copy from discovery_v1.py
    
    ## Note: username,password have to get from credentials
    discovery = watson_developer_cloud.DiscoveryV1('2017-02-01',username=credentials["username"],password=credentials["password"])

    environments = discovery.get_environments()
    print(environments)
    return_str = return_str + str(environments)
    
    news_environments = [x for x in environments['environments'] if
                     x['name'] == 'Watson News Environment']
    news_environment_id = news_environments[0]['environment_id']
    print(news_environment_id)
    return_str = return_str + "<br>\n"+str(news_environment_id)

    collections = discovery.list_collections(news_environment_id)
    news_collections = [x for x in collections['collections']]
    print(collections)
    return_str = return_str + "<br>\n"+str(collections)
    
    configs = discovery.list_configurations(environment_id=news_environment_id)
    print(configs)
    return_str = return_str + "<br>\n"+str(configs)
    default_config_id = discovery.get_default_configuration_id(environment_id=news_environment_id)
    print(default_config_id)
    return_str = return_str + "<br>\n"+str(default_config_id)
    

    default_config = discovery.get_configuration(environment_id=news_environment_id, configuration_id=default_config_id)
    print(default_config)
    return_str = return_str + "<br>\n"+str(default_config)
    
    return return_str
    
    
if __name__ == "__main__":

    app.run(host='0.0.0.0', port=int(port))

# On Bluemix, get the port number from the environment variable VCAP_APP_PORT
# When running this app on the local machine, default the port to 8080
#port = int(os.getenv('VCAP_APP_PORT', 8080))
#@app.route('/')
#def hello_world():
#    return 'Hello World! I am running on port ' + str(port)
#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=port)
