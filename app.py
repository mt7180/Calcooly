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
@app.route('/index/<function_id>', methods = ["GET", "POST"])
def main(function_id = ""):
    html_input = {}
    if request.method == "POST":
        input_str = ""
        if "action" in request.form:
            safe_function(input_str := request.form.get("input_function"))
        elif "calc" in request.form:
            if not request.form.get("input"):
                flash("Please type function.")
                return redirect("/")
            input_str = request.form.get("input")

        # in every POST mode PROCESS input string or copied input
        fs = Calcooly()
        fs.parse_raw_input(input_str)
        
        if not fs._err:
            latex_legend = fs.get_latex_functions()
            diagram = fs.get_diagram()
            if not diagram._err:
                html_input={"out": latex_legend, "in": input_str, "chart": diagram.figure}
            else:
                flash(diagram._err)
                html_input = {"out":"", "in": input_str, "chart":""}
        else:
            flash(fs._err)
            html_input = {"out": "", "in": input_str, "chart": ""}
        return render_template("index.html", message = html_input)

    elif request.method == "GET":
        html_input = {"out": "", "in": get_DBfunction(function_id), "chart": ""}
        return render_template("index.html", message = html_input)

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

def safe_function(inp):
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
    else:
        flash("No function specified to save!")

def get_DBfunction(id):
    inp = ""
    if id:
        db = sqlite3.connect(database)
        cursor = db.cursor()
        cursor.execute("SELECT name FROM history WHERE id=?", (id,))
        entries = cursor.fetchall()
        db.commit()
        db.close()
        inp = entries[0][0]
    return inp


if __name__ == "__main__":
    app.run()