from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    regenerate = False

    if request.method == "POST":
        if request.form.get("action") == "next":
            regenerate = True
        else:
            pipette = request.form.get("pipette")
            d1 = int(request.form.get("d1"))
            d2 = int(request.form.get("d2"))
            d3 = int(request.form.get("d3"))
            user_input = request.form.get("volume")

            if pipette in ["P-10", "P-20"]:
                volume_ul = d1 * 10 + d2 + d3 / 10
            else:
                volume_ul = d1 * 100 + d2 * 10 + d3

            correct_volume = volume_ul 

            try:
                user_volume = float(user_input)
                if abs(user_volume - correct_volume) < 0.0001:
                    result = "✅ Correct!"
                else:
                    result = f"❌ Incorrect. Correct: {correct_volume:.4f} µL"
            except:
                result = "⚠️ Invalid input."

            digits = [d1, d2, d3]
    else:
        regenerate = True

    if regenerate:
        pipette = random.choice(["P-1000", "P-200", "P-20", "P-10"])
        d1 = random.randint(0, 9)
        d2 = random.randint(0, 9)
        d3 = random.randint(0, 9)
        digits = [d1, d2, d3]

    return render_template("index.html", pipette=pipette, digits=digits, result=result)

if __name__ == "__main__":
    import os
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
