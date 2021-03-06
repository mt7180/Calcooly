from flask import Flask, flash, redirect, render_template, request, session
import sqlite3
import myFunctionSet as my_fs

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

database = "./data/CalcoolyHistory.db"

@app.route('/', methods = ["GET", "POST"])
# @app.route('/index/<fid>', defaults={'fid': ""}, methods = ["GET", "POST"])
@app.route('/index/<fid>', methods = ["GET", "POST"])
def main(fid = ""):
    message = {}
    if request.method == "POST":
        input_str = ""
        if "action" in request.form:
            # Save
            try:
                inp = request.form.get("cinput")
                if inp:
                    try:
                        db = sqlite3.connect(database)
                        cursor = db.cursor()
                        sql = 'INSERT INTO history(name) VALUES(?)'
                        cursor.execute(sql, (inp,))
                        db.commit()
                        db.close()
                        flash("Saved!")
                    except Exception as e:
                        print(e)
                        flash('SQL error #1!')
                    input_str = inp
                else:
                    flash("No function specified to save!")
            except:
                print("nothing in here!")
        elif "calc" in request.form:
            # Calc
            if not request.form.get("input"):
                flash("Please type function.")
                return redirect("/")
            input_str = request.form.get("input")

        # in every POST mode process Input string or copied input
        # ------------------Process Input -------------------------
        fs = rawInput2functionSet(input_str)
        # ---------------------------------------------------------
        if fs.err == "":        # nur wenn kein err vorgefallen ist
            output = fs.functions2diagram()
            # in case of Exception
            if output[2] == True:
                # print("Except")
                flash(output[0])
                message = {"out":"", "in": input_str, "chart":""}
            # when parsing was successfull
            else:
                message={"out": output[0], "in": input_str, "chart": output[1]}
        else:
            flash(fs.err)
            message = {"out": "", "in": input_str, "chart": ""}
        return render_template("index.html", message = message)

    # else: request.method == "get"
    else:
        # idh = request.args.get('id')
        inp = ""
        if fid:
            db = sqlite3.connect(database)
            cursor = db.cursor()
            cursor.execute("SELECT name FROM history WHERE id=?", (fid,))
            entries = cursor.fetchall()
            db.commit()
            db.close()
            inp = entries[0][0]
        message={"out": "", "in": inp, "chart": ""}
        return render_template("index.html", message = message)

@app.route("/history")
def history():
    """Show history"""
    try:
        db = sqlite3.connect(database)
        db.row_factory = sqlite3.Row  #wichtig, da sonst nur eine liste von tuples generiert wird, jetzt ist es ein dict
        cursor = db.cursor()
        cursor.execute("SELECT * FROM history ORDER BY id DESC")
        entries = cursor.fetchall()
        db.commit()
        db.close()
        return render_template("history.html", entries = entries)

    except Exception as e:
        print(e)
        flash("SQL Error!")
        return redirect("/")

@app.route("/notation")
def notation():
    return render_template("notation.html")

def rawInput2functionSet(input_str):
    """ parse raw input """
    fs = my_fs.FunctionSet()
    input = fs.extrafunc(input_str)  # searches for keywords as ODE or Integral
    if fs.tag == "ODE":
        fs.ode2functionset(input)
    else:
        fs.input2functionset(input)
    return fs

if __name__ == "__main__":
    app.run()