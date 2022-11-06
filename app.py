from flask import Flask, flash, redirect, render_template, request, session
import sqlite3

from calcooly import Calcooly

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
        fs = Calcooly()
        fs.parse_raw_input(input_str)
        # ---------------------------------------------------------
        if fs._err == "":        # nur wenn kein err vorgefallen ist
            #output = fs.functions2diagram()
            latex_legend = fs.get_latex_functions()
            try:
                diagram = fs.get_diagram()
            except Exception as e:
                print("Error #1: ", e)
            print(latex_legend)
            # in case of Exception
            if diagram._err:
                flash(diagram._err)
                message = {"out":"", "in": input_str, "chart":""}
            # when parsing was successfull
            else:
                message={"out": latex_legend, "in": input_str, "chart": diagram.figure}
        else:
            flash(fs._err)
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
        db.row_factory = sqlite3.Row  #wichtig, da sonst nur eine liste von tuples generiert wird, so ist es ein dict
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


if __name__ == "__main__":
    app.run()