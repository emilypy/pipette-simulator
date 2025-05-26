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
            else:
                volume_ul = d1 * 100 + d2 * 10 + d3  # P-200 and P-1000

            correct_volume = volume_ul

            try:
                user_volume = float(user_input)
                if abs(user_volume - correct_volume) < 0.01:
                    result = "✅ Correct!"
                else:
                    result = f"❌ Incorrect. Correct: {correct_volume:.1f} µL"
            except:
                result = "⚠️ Invalid input."

            digits = [d1, d2, d3]

    else:
        regenerate = True

    if regenerate:
        pipette = random.choice(["P-1000", "P-200", "P-20", "P-10"])

        if pipette == "P-10":
            value = random.randint(0, 100)  # 0.0–10.0 µL as 0–100
            d1 = value // 10
            d2 = value % 10
            d3 = 0
        elif pipette == "P-20":
            value = random.randint(0, 200)
            d1 = value // 10
            d2 = value % 10
            d3 = random.randint(0, 9)
        else:
            max_val = 1000 if pipette == "P-1000" else 200
            value = random.randint(0, max_val)
            d1 = value // 100
            d2 = (value % 100) // 10
            d3 = value % 10

        digits = [d1, d2, d3]

    return render_template("index.html", pipette=pipette, digits=digits, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
