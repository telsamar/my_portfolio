const express = require('express');
const cors = require('cors');
const { Pool } = require('pg');

const app = express();
app.use(cors());
app.use(express.json());

app.use(express.static('public'));

const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'db_site_1',
  password: 'postgres',
  port: 5432
});

app.get('/filters', async (req, res) => {
  try {
    const manufacturersResult = await pool.query(
      'SELECT DISTINCT manufacturer FROM uavs ORDER BY manufacturer'
    );
    const typesResult = await pool.query(
      'SELECT DISTINCT aircraft_type FROM uavs ORDER BY aircraft_type'
    );
    const areasResult = await pool.query(`
      SELECT DISTINCT application_areas
      FROM uavs
      ORDER BY application_areas
    `);

    res.json({
      manufacturers: manufacturersResult.rows.map(r => r.manufacturer),
      aircraftTypes: typesResult.rows.map(r => r.aircraft_type),
      applicationAreas: areasResult.rows.map(r => r.application_areas)
    });
  } catch (err) {
    console.error(err);
    res.status(500).send('Ошибка сервера');
  }
});

app.get('/uavs', async (req, res) => {
  try {
    console.log('--- /uavs ---');
    console.log('Request URL:', req.url);
    console.log('Parsed query:', req.query);

    const { manufacturer, aircraft_type, application_area } = req.query;
    const whereClauses = [];
    const values = [];

    if (manufacturer) {
      const arrayOfManuf = manufacturer.split('|').map(s => s.trim());
      whereClauses.push(`manufacturer = ANY($${whereClauses.length + 1})`);
      values.push(arrayOfManuf);
    }

    if (aircraft_type) {
      const arrayOfTypes = aircraft_type.split('|').map(s => s.trim());
      whereClauses.push(`aircraft_type = ANY($${whereClauses.length + 1})`);
      values.push(arrayOfTypes);
    }

    if (application_area) {
      const arrayOfAreas = application_area.split('|').map(s => s.trim());
      whereClauses.push(`application_areas = ANY($${whereClauses.length + 1})`);
      values.push(arrayOfAreas);
    }

    let queryText = 'SELECT * FROM uavs';
    if (whereClauses.length > 0) {
      queryText += ' WHERE ' + whereClauses.join(' AND ');
    }

    console.log('Final query:', queryText);
    console.log('Values array:', values);

    const result = await pool.query(queryText, values);
    res.json(result.rows);

    console.log('Rows returned:', result.rows.length);
    console.log('--------------');
  } catch (err) {
    console.error(err);
    res.status(500).send('Ошибка сервера');
  }
});

app.get('/uavs/:id', async (req, res) => {
  try {
    const { id } = req.params;

    console.log('--- /uavs/:id ---');
    console.log('Request ID:', id);

    if (isNaN(id)) {
      return res.status(400).send('Неверный ID');
    }

    const result = await pool.query('SELECT * FROM uavs WHERE id = $1', [id]);
    if (result.rows.length === 0) {
      return res.status(404).send('Не найдено');
    }
    res.json(result.rows[0]);

    console.log('Found drone:', result.rows[0]);
    console.log('--------------');
  } catch (err) {
    console.error(err);
    res.status(500).send('Ошибка сервера');
  }
});

app.listen(3000, () => {
  console.log('Сервер запущен на http://localhost:3000');
});
