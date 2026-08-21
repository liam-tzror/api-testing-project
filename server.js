const express = require('express');
const Database = require('better-sqlite3');

const app = express();
app.use(express.json());

const db = new Database('tasks.db');

db.exec(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
  )
`);

db.exec(`
  CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )
`);

// הרשמה
app.post('/register', (req, res) => {
  const { username, password } = req.body;
  if (!username || !password) {
    return res.status(400).json({ error: 'username and password are required' });
  }
  try {
    db.prepare('INSERT INTO users (username, password) VALUES (?, ?)').run(username, password);
    res.status(201).json({ message: 'User created successfully' });
  } catch (e) {
    res.status(400).json({ error: 'Username already exists' });
  }
});

// התחברות
app.post('/login', (req, res) => {
  const { username, password } = req.body;
  const user = db.prepare('SELECT * FROM users WHERE username = ? AND password = ?').get(username, password);
  if (!user) {
    return res.status(401).json({ error: 'Invalid username or password' });
  }
  res.json({ token: `token-${user.id}-${username}` });
});

// middleware לבדיקת token
function auth(req, res, next) {
  const token = req.headers['authorization'];
  if (!token) {
    return res.status(401).json({ error: 'Token required' });
  }
  next();
}

// GET - קבל את כל המשימות
app.get('/tasks', auth, (req, res) => {
  const tasks = db.prepare('SELECT * FROM tasks').all();
  res.json(tasks);
});

// GET - קבל משימה ספציפית לפי id
app.get('/tasks/:id', auth, (req, res) => {
  const { id } = req.params;
  const task = db.prepare('SELECT * FROM tasks WHERE id = ?').get(id);
  if (!task) {
    return res.status(404).json({ error: 'Task id not found' });
  }
  res.json(task);
});

// POST - צור משימה חדשה
app.post('/tasks', auth, (req, res) => {
  const { title } = req.body;
  if (!title || !title.trim()) {
    return res.status(400).json({ error: 'Title is required' });
  }
  const result = db.prepare('INSERT INTO tasks (title) VALUES (?)').run(title);
  res.status(201).json({ id: result.lastInsertRowid, title, status: 'pending' });
});

// PUT - עדכן משימה
app.put('/tasks/:id', auth, (req, res) => {
  const { id } = req.params;
  const { title, status } = req.body;
  const task = db.prepare('SELECT * FROM tasks WHERE id = ?').get(id);
  if (!task) {
    return res.status(404).json({ error: 'Task not found' });
  }
  db.prepare('UPDATE tasks SET title = ?, status = ? WHERE id = ?')
    .run(title || task.title, status || task.status, id);
  res.json({ id, title: title || task.title, status: status || task.status });
});

// DELETE - מחק משימה
app.delete('/tasks/:id', auth, (req, res) => {
  const { id } = req.params;
  const task = db.prepare('SELECT * FROM tasks WHERE id = ?').get(id);
  if (!task) {
    return res.status(404).json({ error: 'Task not found' });
  }
  db.prepare('DELETE FROM tasks WHERE id = ?').run(id);
  res.json({ message: 'Task deleted successfully' });
});

app.listen(3000, () => {
  console.log('Server is running on http://localhost:3000');
});