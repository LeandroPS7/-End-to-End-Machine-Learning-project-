import gradio as gr
import pandas as pd
import joblib

# 💾 Modell laden
model = joblib.load("rf_model_no_voteaverage.joblib")

# 🎯 Feature-Liste exakt wie beim Training
features = [
    'budget', 'runtime', 'release_year',
    'top_genre_Drama', 'top_genre_Action', 'top_genre_Comedy',
    'top_genre_Thriller', 'top_genre_Adventure', 'top_genre_Crime',
    'top_genre_Science Fiction', 'top_genre_Romance', 'top_genre_Fantasy',
    'top_genre_Family',
    'top_studio_Warner Bros.', 'top_studio_Paramount Pictures',
    'top_studio_Universal Pictures', 'top_studio_Twentieth Century Fox Film Corporation',
    'top_studio_New Line Cinema', 'top_studio_Columbia Pictures',
    'top_studio_Amblin Entertainment', 'top_studio_Miramax Films',
    'top_studio_Touchstone Pictures', 'top_studio_Columbia Pictures Corporation'
]

# 🔮 Vorhersagefunktion
def predict_rating(budget, runtime, release_year, genre, studio):
    try:
        data = {f: 0 for f in features}

        # Zahlen einsetzen
        data['budget'] = float(budget)
        data['runtime'] = float(runtime)
        data['release_year'] = int(release_year)

        # One-hot für Genre & Studio
        genre_col = f"top_genre_{genre}"
        if genre_col in data:
            data[genre_col] = 1

        studio_col = f"top_studio_{studio}"
        if studio_col in data:
            data[studio_col] = 1

        df = pd.DataFrame([data])
        prediction = model.predict(df)[0]
        return f"🎯 Erwartetes Rating: {round(prediction, 2)} von 5"

    except Exception as e:
        return f"❌ Fehler: {str(e)}"

# 📁 Drop-down-Werte nur aus deinen Features
genres = ['Drama', 'Action', 'Comedy', 'Thriller', 'Adventure', 'Crime',
          'Science Fiction', 'Romance', 'Fantasy', 'Family']

studios = ['Warner Bros.', 'Paramount Pictures', 'Universal Pictures',
           'Twentieth Century Fox Film Corporation', 'New Line Cinema',
           'Columbia Pictures', 'Amblin Entertainment', 'Miramax Films',
           'Touchstone Pictures', 'Columbia Pictures Corporation']

# 🎛️ Gradio Interface
demo = gr.Interface(
    fn=predict_rating,
    inputs=[
        gr.Number(label="🎬 Budget (z. B. 10000000)", precision=0),
        gr.Number(label="⏱ Laufzeit in Minuten", precision=0),
        gr.Number(label="📅 Erscheinungsjahr", precision=0),
        gr.Dropdown(choices=genres, label="📁 Genre"),
        gr.Dropdown(choices=studios, label="🏢 Produktionsstudio")
    ],
    outputs=gr.Text(label="🔮 Vorhergesagtes Rating"),
    title="🎥 Filmrating-Vorhersage (ohne vote_average)",
    description="Gib einfache Filmdaten ein und erhalte eine Vorhersage für das Zuschauer-Rating (1–5 Sterne)."
)

if __name__ == "__main__":
    demo.launch()