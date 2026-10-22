
m flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = 'katalog.db'

def init_db():
        conn = sqlite3.connect(DB_NAME)
            conn.execute('''
                    CREATE TABLE IF NOT EXISTS programs (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            name TEXT NOT NULL,
                                                        version TEXT,
                                                                    description TEXT,
                                                                                category TEXT,
                                                                                            available INTEGER DEFAULT 1
                                                                                                    )
                                                                                                        ''')
                conn.commit()
                    conn.close()

                    init_db()

                    @app.route('/programs', methods=['GET'])
                    def get_programs():
                            search = request.args.get('search', '')
                                conn = sqlite3.connect(DB_NAME)
                                    conn.row_factory = sqlite3.Row
                                        cursor = conn.cursor()
                                            if search:
                                                        cursor.execute("SELECT * FROM programs WHERE name LIKE ?", ('%' + search + '%',))
                                                            else:
                                                                        cursor.execute("SELECT * FROM programs")
                                                                            rows = cursor.fetchall()
                                                                                conn.close()
                                                                                    return jsonify([dict(row) for row in rows])

                                                                                @app.route('/programs', methods=['POST'])
                                                                                def add_program():
                                                                                        data = request.json
                                                                                            conn = sqlite3.connect(DB_NAME)
                                                                                                cursor = conn.cursor()
                                                                                                    cursor.execute(
                                                                                                                    "INSERT INTO programs (name, version, description, category, available) VALUES (?, ?, ?, ?, ?)",
                                                                                                                            (data['name'], data.get('version'), data.get('description'), data.get('category'), data.get('available', 1))
                                                                                                                                )
                                                                                                        conn.commit()
                                                                                                            new_id = cursor.lastrowid
                                                                                                                conn.close()
                                                                                                                    return jsonify({"id": new_id, "message": "Dodano program"}), 201

                                                                                                                @app.route('/programs/<int:id>', methods=['PATCH'])
                                                                                                                def toggle_availability(id):
                                                                                                                        data = request.json
                                                                                                                            new_status = data.get('available')
                                                                                                                                conn = sqlite3.connect(DB_NAME)
                                                                                                                                    conn.execute("UPDATE programs SET available = ? WHERE id = ?", (new_status, id))
                                                                                                                                        conn.commit()
                                                                                                                                            conn.close()
                                                                                                                                                return jsonify({"message": "Zaktualizowano status"})

                                                                                                                                            if __name__ == '__main__':
                                                                                                                                                app.run(host='0.0.0.0', port=10149)
