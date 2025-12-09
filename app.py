from flask import Flask, render_template, request, session, redirect, url_for
from itertools import combinations
from pairfect_ocr import get_active_ingredient
import os

app = Flask(__name__)
app.secret_key = "pairfectkey"   

compatibility = {
    "Hyaluronic Acid": {
        "Salicylic Acid": "Y", "Glycolic Acid": "Y", "Lactic Acid": "Y",
        "Azelaic Acid": "Y", "Kojic Acid": "Y", "Ascorbic Acid": "Y",
        "Retinol": "Y", "Niacinamide": "Y", "Ceramides": "Y", "SPF": "Y"
    },

    "Salicylic Acid": {
        "Hyaluronic Acid": "Y", "Glycolic Acid": "N", "Lactic Acid": "N",
        "Azelaic Acid": "N", "Kojic Acid": "N", "Ascorbic Acid": "N",
        "Retinol": "N", "Niacinamide": "Y", "Ceramides": "Y", "SPF": "Y"
    },

    "Glycolic Acid": {
        "Hyaluronic Acid": "Y", "Salicylic Acid": "N", "Lactic Acid": "N",
        "Azelaic Acid": "N", "Kojic Acid": "Y", "Ascorbic Acid": "N",
        "Retinol": "N", "Niacinamide": "Y", "Ceramides": "Y", "SPF": "Y"
    },

    "Lactic Acid": {
        "Hyaluronic Acid": "Y", "Salicylic Acid": "N", "Glycolic Acid": "N",
        "Azelaic Acid": "N", "Kojic Acid": "N", "Ascorbic Acid": "N",
        "Retinol": "N", "Niacinamide": "Y", "Ceramides": "Y", "SPF": "Y"
    },

    "Azelaic Acid": {
        "Hyaluronic Acid": "Y", "Salicylic Acid": "N", "Glycolic Acid": "N",
        "Lactic Acid": "N", "Kojic Acid": "Y", "Ascorbic Acid": "Y",
        "Retinol": "Y", "Niacinamide": "Y", "Ceramides": "Y", "SPF": "Y"
    },

    "Kojic Acid": {
        "Hyaluronic Acid": "Y", "Salicylic Acid": "N", "Glycolic Acid": "Y",
        "Lactic Acid": "N", "Azelaic Acid": "Y", "Ascorbic Acid": "Y",
        "Retinol": "Y", "Niacinamide": "Y", "Ceramides": "Y", "SPF": "Y"
    },

    "Ascorbic Acid": {
        "Hyaluronic Acid": "Y", "Salicylic Acid": "N", "Glycolic Acid": "N",
        "Lactic Acid": "N", "Azelaic Acid": "Y", "Kojic Acid": "Y",
        "Retinol": "N", "Niacinamide": "N", "Ceramides": "Y", "SPF": "Y"
    },

    "Retinol": {
        "Hyaluronic Acid": "Y", "Salicylic Acid": "N", "Glycolic Acid": "N",
        "Lactic Acid": "N", "Azelaic Acid": "Y", "Kojic Acid": "Y",
        "Ascorbic Acid": "N", "Niacinamide": "Y", "Ceramides": "Y", "SPF": "Y"
    },

    "Niacinamide": {
        "Hyaluronic Acid": "Y", "Salicylic Acid": "Y", "Glycolic Acid": "Y",
        "Lactic Acid": "Y", "Azelaic Acid": "Y", "Kojic Acid": "Y",
        "Ascorbic Acid": "N", "Retinol": "Y", "Ceramides": "Y", "SPF": "Y"
    },

    "Ceramides": {
        "Hyaluronic Acid": "Y", "Salicylic Acid": "Y", "Glycolic Acid": "Y",
        "Lactic Acid": "Y", "Azelaic Acid": "Y", "Kojic Acid": "Y",
        "Ascorbic Acid": "Y", "Retinol": "Y", "Niacinamide": "Y", "SPF": "Y"
    },

    "SPF": {
        "Hyaluronic Acid": "Y", "Salicylic Acid": "Y", "Glycolic Acid": "Y",
        "Lactic Acid": "Y", "Azelaic Acid": "Y", "Kojic Acid": "Y",
        "Ascorbic Acid": "Y", "Retinol": "Y", "Niacinamide": "Y", "Ceramides": "Y"
    }
}

def calculate_synergy(ingredients):
    """ingredients = list of active ingredients the user selected"""
    ingredients = [normalize(i) for i in ingredients if i and i != "None"]

    if len(ingredients) < 2:
        return {
            "score": 100,
            "good_pairs": [],
            "bad_pairs": [],
            "rating": "Not enough data"
        }

    total_pairs = list(combinations(ingredients, 2))
    good_pairs = []
    bad_pairs = []
    score = 100 

    for a, b in total_pairs:
        result = compatibility.get(a, {}).get(b, "Y")

        if result == "Y":
            good_pairs.append((a, b))
        else:
            bad_pairs.append((a, b))
            score -= 10  
    score = max(0, min(100, score))

    if score >= 76:
        rating = "Good Synergy"
    elif score >= 51:
        rating = "Medium Synergy"
    elif score >= 26:
        rating = "Low Synergy"
    else:
        rating = "Poor Synergy"

    return {
        "score": score,
        "good_pairs": good_pairs,
        "bad_pairs": bad_pairs,
        "rating": rating
    }

def normalize(name):
    aliases = {
        "Vitamin C": "Ascorbic Acid",
        "Vit C": "Ascorbic Acid",
        "Hyalurronic Acid": "Hyaluronic Acid"  
    }
    return aliases.get(name, name)

UPLOAD_FOLDER = "/tmp/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#Landing page
@app.route('/')
def landing():
    return render_template('landing.html', no_nav=True)

#Options page
@app.route('/options')
def options():
    return render_template('options.html')


#Identifying skintype page
@app.route('/skin-types')
def skin_types():
    return render_template('skintypes.html')


#Ingredient literacy page
@app.route('/ingredients')
def ingredients():
    return render_template('ingredients.html')


#Ingredient combination page
@app.route("/combos")
def combos():
    ingredients = [
        {"name": "Niacinamide", "img": "niacinamide.jpg"},
        {"name": "Salicylic Acid", "img": "salicylic.jpg"},
        {"name": "Hyaluronic Acid", "img": "hyaluronic.jpg"},
        {"name": "Kojic Acid", "img": "kojic.jpg"},
        {"name": "Ascorbic Acid", "img": "vitc.jpg"},
        {"name": "Retinol", "img": "retinol.jpg"},
        {"name": "SPF", "img": "spf.jpg"},
        {"name": "Ceramides", "img": "ceramides.jpg"},
        {"name": "Glycolic Acid", "img": "glycolic.jpg"},
        {"name": "Lactic Acid", "img": "lactic.jpg"},
        {"name": "Azelaic Acid", "img": "azelaic.jpg"}
    ]

    return render_template("combos.html", ingredients=ingredients)


#Preferred method page
@app.route('/method')
def method():
    return render_template('method_select.html')


#Manual entry page
@app.route('/manual', methods=['GET', 'POST'])
def manual_entry():

    # List of available ingredients
    available_ingredients = [
        "Niacinamide", "Hyaluronic Acid", "Salicylic Acid", "Glycolic Acid",
        "Lactic Acid", "Azelaic Acid", "Retinol", "Vitamin C", "Ceramides", "SPF"
    ]

    # Restore saved data if exists
    saved = session.get("manual_data", [{}]*10)

    auto_ingredients = {}

    product_num = request.args.get("product")
    ingredient = request.args.get("ingredient")

    if product_num and ingredient:
        product_num = int(product_num)
        auto_ingredients[product_num] = ingredient
        saved[product_num-1]["ingredient"] = ingredient
        session["manual_data"] = saved

    if request.method == "POST":
        manual_data = []
        for i in range(1, 11):
            ptype = request.form.get(f"product_type_{i}")
            ing = request.form.get(f"ingredient_{i}")

            manual_data.append({
                "product": i,
                "type": ptype,
                "ingredient": ing
            })

        session["manual_data"] = manual_data
        return redirect("/results")

    return render_template(
        "manual_entry.html",
        ingredients=available_ingredients,
        auto_ingredients=auto_ingredients,
        saved=saved
    )

#Upload image page
@app.route('/upload_image', methods=['GET','POST'])
def upload_image():
    ingredient = None

    if request.method == 'POST':
        file = request.files.get('image')

        if file:
            save_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(save_path)

            # Run OCR
            ingredient = get_active_ingredient(save_path)

            product_num = request.args.get("product")
            return redirect(f"/manual?product={product_num}&ingredient={ingredient}")

    return render_template('upload_image.html', ingredient=ingredient)

#Results page
@app.route('/results')
def results():

    data = session.get("manual_data", [])
    selected = [item["ingredient"] for item in data if item["ingredient"]]
    selected = [normalize(i) for i in selected]
    selected = [i for i in selected if i in compatibility]
    if len(selected) < 2:
        return render_template(
            "results.html",
            score=100,
            good=[],
            bad=[],
            explanation="Not enough ingredients to calculate synergy."
        )

    good_pairs = []
    bad_pairs = []
    total_pairs = 0
    positive = 0
    negative = 0

    from itertools import combinations
    for a, b in combinations(selected, 2):
        total_pairs += 1
        
        relation = compatibility.get(a, {}).get(b)
        if relation == "Y":
            good_pairs.append((a, b))
            positive += 1
        elif relation == "N":
            bad_pairs.append((a, b))
            negative += 1

    if total_pairs > 0:
        score = round((positive / total_pairs) * 100)
    else:
        score = 100

    if score >= 76:
        explanation = "Great synergy! Your routine has strong ingredient compatibility."
    elif score >= 51:
        explanation = "Moderate synergy. Some pairs may conflict."
    elif score >= 26:
        explanation = "Low synergy. Several ingredients may not work well together."
    else:
        explanation = "Poor synergy. Many ingredients conflict and may irritate skin."

    return render_template(
        "results.html",
        score=score,
        good=good_pairs,
        bad=bad_pairs,
        explanation=explanation
    )

#About us page
@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
