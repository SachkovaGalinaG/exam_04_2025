const mysql = require('mysql2');
const fs = require('fs');
const { stringify } = require('csv-stringify');

const connection = mysql.createConnection({
  host: 'db',
  user: 'root',
  password: 'password',
  database: 'chatbot'
});

connection.query('SELECT * FROM messages', (err, results) => {
  if (err) throw err;
  
  stringify(results, {
    header: true
  }, (err, output) => {
    fs.writeFileSync('messages.csv', output);
    console.log('Data exported to messages.csv');
    process.exit();
  });
});