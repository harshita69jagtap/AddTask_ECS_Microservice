from flask import Flask, render_template, request, redirect,jsonify
import requests
import sys, traceback

##### directory structure - 
##/root/project/addtask.py
##/root/project/templates/base.html
##/root/project/templates/addtask.html

###dependencies installed
### yum install -y tree python3 python3-pip
### pip3 install flask requests


app = Flask(__name__)

@app.route('/', methods=['GET'])   #### ONLY APPLICABLE FOR PUB-ALB HEALTHCHECK PATH
def index():  #### ONLY APPLICABLE FOR PUB-ALB HEALTHCHECK PATH
    print(" HTTP GET REQUEST FROM pub-alb for health check ON addtask PRIVATE IP - {0}".format(request.method))  #### ONLY APPLICABLE FOR PUB-ALB HEALTHCHECK PATH
    return(jsonify({'status':'HEALTH CHECK FROM PUB-ALB'}))   #### ONLY APPLICABLE FOR PUB-ALB HEALTHCHECK PATH

@app.route('/addtask', methods=['POST', 'GET'])

def addtask():

    if request.method == 'POST':

        # text below is a string

        text = request.form.get('content')   ### IF USER DID NOT FILL IN THE TASK TEXT AREA IN FORM THEN RETURN empty string

        print("Retrieved task value and it's DATA TYPE from submitted FORM POST REQUEST- {0},{1}".format(text,type(text)))

        if text != "" :   # user pressed add task button after entering the text in input box of form
            #MAKING A POST REQUEST WITH JSON OBJECT IN DATA PAYLOAD FIELD OF HTTP POST REQUEST TO DBTASK SERVICE, "JSON =" CONSTRUCTS A JSON OBJECT FROM PASSED ARGUMENT PYTHON DICT()
            #REMEMBER making request to a server from inside the code like above always hits the private ip of server as DEST and uses private IP of client as SRC in case of AWS 
            r = requests.post('http://dns-name-of-priv-alb:80/dbtask', json = {'text':text,'service':'addtask'})
            try:
      
                resp = r.json()   # this command is suuupppperrrr important to parse server json response into a python dict() # resp = {'id':q.id}
                print("RECEIVED JSON RESPONSE FROM DBTASK - {0} ".format(resp))

                if resp['id'] != 0:  # task either already exists in TODO table or is newly inserted
                    print("YOUR TASK {0} EITHER ADDED SUCCESSFULLY OR IT ALREADY EXISTS".format(resp['id']))
                    return redirect('http://dns-name-of-pub-alb:80/viewtask')    #### ALWAYS USE PUBLIC IP WITH REDIRECT('') AND <a>href = ''</a> HTML TAG 
                elif resp['id'] == 0: # task not added or does not already exists in TODO table and exception occured in retrieving/adding this task in table
                    print("YOUR TASK NOT ADDED SUCCESSFULLY AND EXCEPTION OCCURED IN INSERT OF DBTASK")
                    return render_template('addtask.html')

            except Exception:
                print("EXCEPTION OCCURED IN /ADDTASK SERVICE")
                print("-"*60)
                traceback.print_exc(file=sys.stdout)
                print("-"*60)
                return render_template('addtask.html') # REDIRECT ALWAYS HITS THE PUBLIC IP OF SERVER IT IS == HITTING THE URL OF SERVER FROM BROWSER

        elif text == "" :  # user pressed add task button without entering the text in input box of form
            print("YOU CANNOT PRESS SUBMIT WITHOUT ENTERING A TASK DO SO FIRST")
            return render_template('addtask.html')
            


    elif request.method == 'GET':
        return render_template('addtask.html') ######## USER HAS HIT /ADDTASK URL FROM BROWSER  OR REDIRECTED FROM /VIEWTASK SERVICE VIA HTTP GET
        
if __name__ == "__main__":
    app.run(host = '0.0.0.0', port='5000', debug=True)

