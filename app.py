from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = "https://api.capasjornaishoje.pt/categorias/nacional?page=1"
IMG_BASE_URL = "https://api.capasjornaishoje.pt/uploads/"

def get_filenames():
    response = requests.get(API_URL)
    data = response.json()

    filenames = []

    def buscar_filenames(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == "filename" and isinstance(v, str) and v.endswith(".jpg"):
                    filenames.append(v)
                else:
                    buscar_filenames(v)
        elif isinstance(obj, list):
            for item in obj:
                buscar_filenames(item)

    buscar_filenames(data)
    return filenames

@app.route("/")
def index():
    imagens = get_filenames()
    page = int(request.args.get('page', 1))
    per_page = 4
    start = (page - 1) * per_page
    end = start + per_page
    pag_imagens = imagens[start:end]

    total_pages = (len(imagens) + per_page - 1) // per_page

    return render_template(
        "index.html",
        imagens=pag_imagens,
        base_url=IMG_BASE_URL,
        page=page,
        total_pages=total_pages
    )

if __name__ == "__main__":
    app.run(debug=True)

