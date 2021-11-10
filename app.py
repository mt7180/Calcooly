from flask import Flask, flash, redirect, render_template, request, session
#from extraFunctions import *
import myFunctionSet as my_fs

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route("/", methods=["GET", "POST"])
def main(): 
    message={} 
    if request.method == "POST":
        if not request.form.get("input"):
            flash("Please type function.")
            return redirect("/")
        input_str = request.form.get("input")
        #print(input_str)
        # ------------------Process Input -------------------------
        fs = rawInput2functionSet(input_str)
        #-----------------------------------------------------------
        #Output todo: Aufräumen
        print("tag: ",fs.tag, "err: ", fs.err)
        if fs.err == "":        #nur wenn kein err vorgefallen ist
            output = fs.functions2diagram()
        
            #in case of Exception
            if output[2]==True:
                flash(output[0])
                message = {"out":"", "in": input_str, "chart":""}
            #when parsing was successfull
            else:
                message={"out":output[0], "in": input_str, "chart":output[1]}
                #flash("Done.")
        else:
            message = {"out":"", "in": input_str, "chart":""}
        return render_template("index.html",message=message) 
    else:
        message={"out":"", "in": ""}
        return render_template("index.html",message=message)

def rawInput2functionSet(input_str):
    fs = my_fs.FunctionSet()
    input_str = fs.extrafunc(input_str)  # searches for keywords as ODE or Integral
    if fs.tag == "ODE":
        fs.ode2functionset(input_str)
    elif fs.tag == "Integral":
        #todo
        pass
    else:
        fs.input2functionset(input_str)
    return fs

if __name__ == "__main__":
    app.run()

