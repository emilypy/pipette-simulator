from flask import Flask, render_template, request
import random
import os

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

            # Calculate correct volume in µL
            if pipette == "P-10":
                volume_ul = (d1 * 10 + d2) / 10  # e.g. 15 → 1.5 µL
            elif pipette == "P-20":
                volume_ul = d1 * 10 + d2 + d3 / 10
            elif pipette == "P-200":
                volume_ul = d1 * 100 + d2 * 10 + d3
            elif pipette == "P-1000":
                volume_ul = d1 * 1000 + d2 * 100 + d3 * 10

            correct_volume = volume_ul

            try:
                user_volume = float(user_input)
                if round(user_volume, 2) == round(correct_volume, 2):
                    result = "Correct!"
                else:
                    result = f"Incorrect. Correct: {correct_volume:.1f} µL"
            except:
                result = "⚠️ Invalid input."

            digits = [d1, d2, d3]

    else:
        regenerate = True

    if regenerate:
        pipette = random.choice(["P-1000", "P-200", "P-20", "P-10"])

        if pipette == "P-10":
            volume_ul = round(random.uniform(0.0,10.0),1)
            volume_as_int = int(volume_ul * 10)
            d1 = volume_as_int // 10
            d2 = (volume_as_int % 10)
            d3 = 0
            correct_volume = (d1 *10 +d2) / 10
        elif pipette == "P-20":
            volume_ul = round(random.uniform(0.0, 20.0),1)
            volume_as_int = int(volume_ul * 10)

            d1 = volume_as_int // 100
            d2 = (volume_as_int % 100) // 10
            d3 = volume_as_int % 10

            correct_volume = volume_ul
        elif pipette == "P-200":
            value = random.randint(0, 200)
            d1 = value // 100
            d2 = (value % 100) // 10
            d3 = value % 10
            correct_volume = value
        elif pipette == "P-1000":
            value = random.randint(0, 1000)
            d1 = value // 1000
            d2 = (value % 1000) // 100
            d3 = (value % 100) // 10
            correct_volume = d1 * 1000 + d2 * 100 + d3 * 10
            
        digits = [d1, d2, d3]

    return render_template("index.html", pipette=pipette, digits=digits, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
