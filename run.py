from flask import Flask, render_template_string, request
from googletrans import Translator

app = Flask(__name__)

# Configuration
SUPPORTED_LANGUAGES = ['en', 'fr', 'de', 'es', 'ja']
DEFAULT_LANGUAGE = 'fr'
translator = Translator()

# Texte original en anglais
content_dict = {
    "home": {"title": "Bienvenue dans le Portfolio", "content": "Ceci est la page d'accueil."},
    "about": {"title": "À propos de moi", "content": "Ceci est la page à propos."},
    "diplomas": {"title": "Diplômes", "content": "Détails sur les diplômes."},
    "experience": {"title": "Expériences", "content": "Détails sur les expériences."},
    "project": {"title": "Projets", "content": "Détails sur les projets."},
    "skills": {"title": "Compétences", "content": "Détails sur les compétences."},
    "awards": {"title": "Récompenses", "content": "Détails sur les récompenses."},
    "contact": {"title": "Contact", "content": "Coordonnées de contact."},
}

# Fonction de traduction automatique
def translate_content(page, lang):
    if page not in content_dict:
        return {"title": "Page non trouvée", "content": "Le contenu pour cette page est manquant."}

    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE

    translated = {}
    for key, value in content_dict[page].items():
        try:
            result = translator.translate(value, src=DEFAULT_LANGUAGE, dest=lang)
            translated[key] = result.text if result.text else value
        except Exception as e:
            translated[key] = value  # Fallback to original text
    return translated

# HTML avec Matrix Rain et modifications visuelles
html_content = """
<!DOCTYPE html>
<html lang="{{ lang }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ translated_content['title'] }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #264653;
            color: #00D9FF;
            margin: 0;
            padding: 0;
            transition: background-color 0.3s, color 0.3s;
        }
        body.light {
            background-color: rgba(255, 255, 255, 0.9);
            color: #264653; /* Bleu charbon */
        }
        nav {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: rgba(0, 0, 20, 0.7);
            padding: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        nav .nav-center {
            display: flex;
            justify-content: center;
            flex-grow: 1;
        }
        nav a {
            color: #00D9FF;
            text-decoration: none;
            margin: 0 10px;
            font-size: 1.1em;
        }
        nav button, nav select {
            font-size: 1em;
            padding: 5px 10px;
            border-radius: 5px;
            border: 1px solid #00D9FF;
            background-color: #264653;
            color: #00D9FF;
            cursor: pointer;
        }
        nav button:hover, nav select:hover {
            background-color: #00D9FF;
            color: #264653;
        }
        nav select {
            margin-right: 20px;
        }
        .content {
            margin-top: 80px;
            padding: 20px;
            text-align: center;
            background-color: rgba(0, 0, 20, 0.8);
            margin: 100px auto;
            border-radius: 10px;
            max-width: 900px;
        }
        .content h1 {
            font-size: 2.5em;
        }
        .content p {
            font-size: 1.2em;
            line-height: 1.6em;
        }
        canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
        }
        
        body.light nav {
            background-color: rgba(255, 255, 255, 0.8);
        }
        
        body.light nav a {
            color: #264653;
        }
        
        body.light nav button, body.light nav select {
            background-color: rgba(255, 255, 255, 0.9);
            color: #264653;
            border: 1px solid #264653;
        }
        
        body.light nav button:hover, body.light nav select:hover {
            background-color: #264653;
            color: rgba(255, 255, 255, 0.9);
        }
        body.light .content {
            background-color: rgba(255, 255, 255, 0.8); /* Fond blanc légèrement transparent */
            color: #264653; /* Texte bleu charbon */
        }
        
        .cards {
        display: flex;
        gap: 20px;
        justify-content: center;
        margin-top: 20px;
    }
    .card {
        background-color: rgba(0, 0, 20, 0.9);
        padding: 20px;
        border-radius: 10px;
        color: #00D9FF;
        text-align: center;
        width: 200px;
        box-shadow: 0 4px 10px rgba(0, 0, 20, 0.2);
    }
    .card h2 {
        margin: 10px 0;
    }
    form {
        display: flex;
        flex-direction: column;
        gap: 15px;
        margin-top: 20px;
    }
    form label {
        font-weight: bold;
    }
    form input, form textarea, form button {
        padding: 10px;
        border-radius: 5px;
        border: none;
        font-size: 1em;
    }
    form button {
        background-color: #00D9FF;
        color: #264653;
        cursor: pointer;
    }
        
    </style>
</head>
<body>
    <nav>
        <div>
            <button id="theme-toggle">Mode Clair</button>
        </div>
        <div class="nav-center">
            <a href="/home?lang={{ lang }}">Accueil</a>
            <a href="/about?lang={{ lang }}">À propos</a>
            <a href="/diplomas?lang={{ lang }}">Diplômes</a>
            <a href="/experience?lang={{ lang }}">Expériences</a>
            <a href="/project?lang={{ lang }}">Projets</a>
            <a href="/skills?lang={{ lang }}">Compétences</a>
            <a href="/awards?lang={{ lang }}">Récompenses</a>
            <a href="/contact?lang={{ lang }}">Contact</a>
        </div>
        <div>
            <select id="language-select">
                <option value="fr" {% if lang == 'fr' %}selected{% endif %}>Français</option>
                <option value="en" {% if lang == 'en' %}selected{% endif %}>English</option>
                <option value="de" {% if lang == 'de' %}selected{% endif %}>Deutsch</option>
                <option value="es" {% if lang == 'es' %}selected{% endif %}>Español</option>
                <option value="ja" {% if lang == 'ja' %}selected{% endif %}>日本語</option>
            </select>
        </div>
    </nav>

    <canvas id="matrix"></canvas>

    <div class="content">
        <h1>{{ translated_content['title'] }}</h1>
        <p>{{ translated_content['content'] }}</p>
        {% if page == 'project' %}
    <div class="cards">
        <div class="card">
            <h2>Projet 1</h2>
            <p>Description du projet 1.</p>
        </div>
        <div class="card">
            <h2>Projet 2</h2>
            <p>Description du projet 2.</p>
        </div>
        <div class="card">
            <h2>Projet 3</h2>
            <p>Description du projet 3.</p>
        </div>
    </div>
    {% elif page == 'skills' %}
<div class="skills-container" style="text-align: left; margin: 20px auto; max-width: 600px;">
    <label for="skills-category" style="font-weight: bold;">Choisir une catégorie :</label>
    <select id="skills-category" style="width: 100%; padding: 10px; margin: 10px 0; border-radius: 5px;">
        <option value="programming">Programmation</option>
        <option value="design">Design</option>
        <option value="management">Gestion</option>
    </select>
    <ul id="skills-list" style="list-style: none; padding: 0;">
        <li>Python</li>
        <li>JavaScript</li>
        <li>HTML/CSS</li>
    </ul>
</div>
<script>
    document.getElementById('skills-category').addEventListener('change', function() {
        const skillsList = document.getElementById('skills-list');
        const category = this.value;
        let skills = [];
        if (category === 'programming') skills = ['Python', 'JavaScript', 'HTML/CSS'];
        else if (category === 'design') skills = ['Photoshop', 'Figma', 'UI/UX'];
        else if (category === 'management') skills = ['Scrum', 'Kanban', 'Communication'];
        skillsList.innerHTML = skills.map(skill => `<li>${skill}</li>`).join('');
    });
</script>
{% elif page == 'diplomas' %}
<div class="table-container">
    <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
        <thead>
            <tr>
                <th style="border: 1px solid #00D9FF; padding: 10px;">Diplôme</th>
                <th style="border: 1px solid #00D9FF; padding: 10px;">Université</th>
                <th style="border: 1px solid #00D9FF; padding: 10px;">Année</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="border: 1px solid #00D9FF; padding: 10px;">Master en Informatique</td>
                <td style="border: 1px solid #00D9FF; padding: 10px;">Université de Paris</td>
                <td style="border: 1px solid #00D9FF; padding: 10px;">2023</td>
            </tr>
            <tr>
                <td style="border: 1px solid #00D9FF; padding: 10px;">Licence en Mathématiques</td>
                <td style="border: 1px solid #00D9FF; padding: 10px;">Université de Lyon</td>
                <td style="border: 1px solid #00D9FF; padding: 10px;">2020</td>
            </tr>
        </tbody>
    </table>
</div>
{% elif page == 'experience' %}
<div class="gallery" style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-top: 20px;">
    <img src="/static/img/experience1.jpg" alt="Expérience 1" style="width: 200px; border-radius: 10px;">
    <img src="/static/img/experience2.jpg" alt="Expérience 2" style="width: 200px; border-radius: 10px;">
    <img src="/static/img/experience3.jpg" alt="Expérience 3" style="width: 200px; border-radius: 10px;">
</div>
    {% elif page == 'contact' %}
    <form action="/send_message" method="POST">
        <label for="name">Nom:</label>
        <input type="text" id="name" name="name" required>
        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required>
        <label for="message">Message:</label>
        <textarea id="message" name="message" required></textarea>
        <button type="submit">Envoyer</button>
    </form>
    {% endif %}
    </div>

    <script>
        const canvas = document.getElementById('matrix');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        const fontSize = 16;
        const columns = Math.floor(canvas.width / fontSize);
        const drops = Array(columns).fill(0);
        const chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'.split('');

        function drawRain() {
            ctx.fillStyle = 'rgba(0, 0, 20, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#00D9FF';
            ctx.font = `${fontSize}px monospace`;
            drops.forEach((y, i) => {
                const text = chars[Math.floor(Math.random() * chars.length)];
                const x = i * fontSize;
                ctx.fillText(text, x, y * fontSize);
                if (y * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                else drops[i]++;
            });
        }
        setInterval(drawRain, 75);

    const themeToggle = document.getElementById('theme-toggle');

    // Initialiser le thème en fonction de LocalStorage
    document.addEventListener('DOMContentLoaded', () => {
        const theme = localStorage.getItem('theme');
        if (theme === 'light') {
            document.body.classList.add('light');
            themeToggle.textContent = 'Mode Sombre';
        }
    });

    // Ajouter un écouteur d'événements pour le bouton de bascule
    themeToggle.addEventListener('click', () => {
        const isLightMode = document.body.classList.toggle('light');
        themeToggle.textContent = isLightMode ? 'Mode Sombre' : 'Mode Clair';
        localStorage.setItem('theme', isLightMode ? 'light' : 'dark');
    });

    const languageSelect = document.getElementById('language-select');
    languageSelect.addEventListener('change', () => {
        const selectedLang = languageSelect.value;
        window.location.href = `?lang=${selectedLang}`;
    });
    </script>
</body>
</html>
"""

@app.route('/<page>')
def render_page(page):
    if page not in content_dict:
        return render_template_string(
            html_content,
            page="404",
            lang=DEFAULT_LANGUAGE,
            translated_content={"title": "404 Non Trouvée", "content": "Désolé, la page n'existe pas."}
        ), 404

    lang = request.args.get('lang', DEFAULT_LANGUAGE)
    translated_content = translate_content(page, lang)
    return render_template_string(
        html_content,
        page=page,  # Ajout de la variable `page`
        lang=lang,
        translated_content=translated_content
    )

@app.route('/')
def index():
    return render_page('home')

@app.errorhandler(404)
def page_not_found(e):
    return render_template_string(
        html_content,
        lang=DEFAULT_LANGUAGE,
        translated_content={"title": "404 Non Trouvée", "content": "Désolé, la page que vous cherchez n'existe pas."}
    ), 404

@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    # Traitement du message (par exemple, envoyer un email ou sauvegarder dans une base de données)
    print(f"Message reçu : {name}, {email}, {message}")
    return render_template_string(
        html_content,
        page="contact",  # Ajout de `page` ici
        lang=DEFAULT_LANGUAGE,
        translated_content={
            "title": "Message Envoyé",
            "content": "Merci de m'avoir contacté. Je vous répondrai bientôt."
        }
    )

if __name__ == '__main__':
    app.run(debug=True)
