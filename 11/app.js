const express = require('express');
const db = require('./db');
const morgan = require('morgan');

const app = express();

// Логирование HTTP-запросов
app.use(morgan(':method :url :status :res[content-length] - :response-time ms'));

// Парсинг JSON
app.use(express.json());

// Логирование тела запроса
app.use((req, res, next) => {
  console.log('Request body:', JSON.stringify(req.body));
  next();
});

// Инициализация БД
db.initializeDatabase().then(() => {
  // Обработчик сообщений
  app.post('/message', async (req, res) => {
    try {
      console.log(`Processing message from ${req.body.userId}`);
      await db.logMessage(req.body.userId, req.body.text);
      res.json({ status: 'success' });
    } catch (err) {
      console.error('Error processing message:', err);
      res.status(500).json({ error: err.message });
    }
  });

  // Запуск сервера
  const PORT = 3000;
  app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
  });
}).catch(err => {
  console.error('Failed to initialize database:', err);
  process.exit(1);
});