from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = 'events.json'

# Функция, которая читает альбом с наклейками
def load_events():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# Функция, которая сохраняет альбом обратно в коробку
def save_events(events):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    # Читаем все фильтры, которые выбрал пользователь
    date_filter = request.args.get('date')
    topic_filter = request.args.get('topic')
    format_filter = request.args.get('format')

    events = load_events()
    
    # Начинаем фильтрацию (прятать ненужные наклейки)
    filtered_events = []
    for event in events:
        # Проверяем дату
        if date_filter and event['date'] != date_filter:
            continue
        # Проверяем тему
        if topic_filter and event['topic'] != topic_filter:
            continue
        # Проверяем формат
        if format_filter and event['format'] != format_filter:
            continue
        filtered_events.append(event)

    # Собираем список уникальных тем, чтобы заполнить кнопочки в фильтре
    topics = list(set(event['topic'] for event in events))
    formats = list(set(event['format'] for event in events))

    return render_template('index.html', 
                           events=filtered_events, 
                           topics=topics, 
                           formats=formats,
                           selected_date=date_filter,
                           selected_topic=topic_filter,
                           selected_format=format_filter)

@app.route('/add', methods=['POST'])
def add_event():
    # Это магия добавления новой наклейки
    events = load_events()
    new_event = {
        'id': len(events) + 1,
        'title': request.form['title'],
        'date': request.form['date'],
        'topic': request.form['topic'],
        'format': request.form['format'],
        'location': request.form['location']
    }
    events.append(new_event)
    save_events(events)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
