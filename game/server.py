import time
from flask import Flask, request, jsonify, render_template
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Инициализация SQLAlchemy
engine = create_engine('sqlite:///game.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Модель кота
class Cat(Base):
    __tablename__ = 'cats'
    id = Column(Integer, primary_key=True)
    player_name = Column(String, unique=True, nullable=False)
    x = Column(Integer, nullable=False, default=0)
    y = Column(Integer, nullable=False, default=0)
    target_x = Column(Integer, nullable=False, default=0)
    target_y = Column(Integer, nullable=False, default=0)
    coins = Column(Integer, default=0)
    join_time = Column(Float, nullable=False, default=time.time)

def get_players():
    playes = session.query(Cat).all()
    return [{'name': player.player_name, 'x': player.x, 'y': player.y} for player in playes]

# Инициализация базы данных
Base.metadata.create_all(engine)

@app.route('/api/players')
def players():
    return jsonify(get_players())

# Маршрут для присоединения к игре
@app.route('/api/join', methods=['POST'])
def join_game():
    player_name = request.json.get('player_name')
    if not player_name:
        print("player name required")
        return jsonify({"error": "Player name is required"}), 400

    # Проверка на наличие игрока с таким именем
    existing_cat = session.query(Cat).filter_by(player_name=player_name).first()
    if existing_cat:
        print("player exist")
        return jsonify({"error": "Player already exists"}), 400

    # Создание нового кота и добавление его в базу данных
    cat = Cat(player_name=player_name, x=0, y=0, target_x=0, target_y=0, coins=0, join_time = time.time())
    session.add(cat)
    session.commit()

    return jsonify({"status": "joined", "player": player_name})

@app.route('/api/score', methods=['POST'])
def add_coin():
    player_name = request.json.get('player_name')
    if not player_name:
        print("player name required")
        return jsonify({"error": "Player name is required"}), 400

    # Проверка на наличие игрока с таким именем
    cat = session.query(Cat).filter_by(player_name=player_name).first()
    cat.coins += 1
    session.commit()

    return jsonify({"status": "added", "player": player_name})

# Маршрут для перемещения кота
@app.route('/api/move', methods=['POST'])
def move_cat():
    player_name = request.json.get('player_name')
    direction = request.json.get('direction')

    if not player_name or not direction:
        return jsonify({"error": "Invalid request"}), 400

    cat = session.query(Cat).filter_by(player_name=player_name).first()
    if not cat:
        return jsonify({"error": "Player not found"}), 404

    # Обработка направления движения
    if direction == 'left':
        cat.x -= 1
    elif direction == 'right':
        cat.x += 1
    elif direction == 'up':
        cat.y -= 1
    elif direction == 'down':
        cat.y += 1

    # Сохранение изменений в базе данных
    session.commit()

    return jsonify({"status": "moved", "new_position": (cat.x, cat.y)})

# Страница с таблицей лидеров
@app.route('/leaderboard')
def leaderboard():
    # Получаем игроков и сортируем их по количеству монет
    players = session.query(Cat).order_by(Cat.coins.desc()).all()

    # Генерируем HTML для таблицы лидеров
    leaderboard_html = '''
    <html>
    <head>
        <title>Leaderboard</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
            }
            h1 {
                text-align: center;
                color: #333;
            }
            table {
                width: 50%;
                margin: 0 auto;
                border-collapse: collapse;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            th, td {
                padding: 10px;
                border: 1px solid #ddd;
                text-align: center;
            }
            th {
                background-color: #4CAF50;
                color: white;
            }
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
            tr:hover {
                background-color: #ddd;
            }
        </style>
    </head>
    <body>
        <h1>Leaderboard</h1>
        <table>
            <tr>
                <th>Rank</th>
                <th>Player Name</th>
                <th>Coins Collected</th>
                <th>Time Played (minutes)</th>
            </tr>
    '''
    # Генерация строк таблицы
    for idx, player in enumerate(players):
        leaderboard_html += f'''
        <tr>
            <td>{idx + 1}</td>
            <td>{player.player_name}</td>
            <td>{player.coins}</td>
            <td>{int((time.time() - player.join_time) / 60)}</td>
        </tr>
        '''

    leaderboard_html += '''
        </table>
    </body>
    </html>
    '''

    return leaderboard_html


# Страница "Обо мне"
@app.route('/about')
def about():
    return "<h1>About My GI Experience</h1><p>//.//</p>"

if __name__ == '__main__':
    app.run(debug=True)
