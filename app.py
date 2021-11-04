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
    if request.method == "POST":
        if not request.form.get("input"):
            flash("Please type function.")
            return redirect("/")
        input_str = request.form.get("input")
        fs=my_fs.FunctionSet()
        fs.input2functionset(input_str)
        output = fs.functions2diagram()
        
        #in case of Exception
        if output[2]==True:
            flash(output[0])
            message = {"out":"", "in": input_str, "chart":""}
        #when parsing was successfull
        else:
            message={"out":output[0], "in": input_str, "chart":output[1]}
            #flash("Done.")
        return render_template("index.html",message=message) 
    else:
        message={"out":"", "in": ""}
        return render_template("index.html",message=message)

if __name__ == "__main__":
    app.run()

