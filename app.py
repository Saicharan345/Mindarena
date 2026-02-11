from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------- DATABASE MODEL ---------------- #

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, default=0)

# ---------------- TRIE ---------------- #

class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.end = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.end

trie = Trie()

# ---------------- LOAD DICTIONARY ---------------- #

try:
    with open("words.txt", "r") as f:
        for word in f:
            trie.insert(word.strip().lower())
except:
    print("words.txt not found!")

# ---------------- ROUTES ---------------- #

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/validate", methods=["POST"])
def validate():
    word = request.json.get("word", "").lower()
    return jsonify({"valid": trie.search(word)})

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if User.query.filter_by(username=username).first():
        return jsonify({"status": "user_exists"})

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"status": "registered"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify({"status": "success"})
    return jsonify({"status": "invalid"})

@app.route("/update_score", methods=["POST"])
def update_score():
    data = request.json
    username = data.get("username")
    points = data.get("points", 0)

    user = User.query.filter_by(username=username).first()
    if user:
        user.score += points
        db.session.commit()
        return jsonify({"status": "updated"})

    return jsonify({"status": "user_not_found"})

@app.route("/leaderboard")
def leaderboard():
    users = User.query.order_by(User.score.desc()).limit(10).all()
    return jsonify([
        {"username": u.username, "score": u.score}
        for u in users
    ])

# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
