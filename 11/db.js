const mysql = require('mysql2/promise');
const util = require('util');

const pool = mysql.createPool({
  host: process.env.MYSQL_HOST,
  user: process.env.MYSQL_USER,
  password: process.env.MYSQL_PASSWORD,
  database: process.env.MYSQL_DB
});

// Функция для логирования SQL-запросов
async function queryWithLogging(sql, params) {
  console.log(`Executing SQL: ${sql}`);
  console.log(`With parameters: ${util.inspect(params)}`);
  
  const start = Date.now();
  try {
    const [rows] = await pool.query(sql, params);
    const duration = Date.now() - start;
    console.log(`Query succeeded in ${duration}ms`);
    return rows;
  } catch (err) {
    console.error(`Query failed: ${err.message}`);
    throw err;
  }
}

async function initializeDatabase() {
  console.log('Initializing database tables...');
  try {
    await queryWithLogging(`
      CREATE TABLE IF NOT EXISTS messages (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id VARCHAR(255) NOT NULL,
        text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )`, []);
    
    await queryWithLogging(`
      CREATE TABLE IF NOT EXISTS user_stats (
        user_id VARCHAR(255) PRIMARY KEY,
        message_count INT DEFAULT 1,
        first_message TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_message TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
      )`, []);
    
    console.log('Database tables initialized successfully');
  } catch (err) {
    console.error('Database initialization failed:', err);
    throw err;
  }
}

async function logMessage(userId, text) {
  const conn = await pool.getConnection();
  try {
    console.log(`Starting transaction for user ${userId}`);
    await conn.beginTransaction();
    
    // Логируем сообщение
    const messageResult = await queryWithLogging(
      'INSERT INTO messages (user_id, text) VALUES (?, ?)',
      [userId, text]
    );
    console.log(`Message logged with ID: ${messageResult.insertId}`);
    
    // Обновляем статистику
    const statsResult = await queryWithLogging(`
      INSERT INTO user_stats (user_id) VALUES (?)
      ON DUPLICATE KEY UPDATE
        message_count = message_count + 1,
        last_message = CURRENT_TIMESTAMP`,
      [userId]
    );
    console.log(`Stats updated: ${JSON.stringify(statsResult)}`);
    
    await conn.commit();
    console.log('Transaction committed successfully');
  } catch (err) {
    console.error('Transaction failed, rolling back:', err);
    await conn.rollback();
    throw err;
  } finally {
    conn.release();
  }
}

module.exports = {
  initializeDatabase,
  logMessage,
  queryWithLogging
};