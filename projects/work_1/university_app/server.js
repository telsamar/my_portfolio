const express = require('express');
const cors = require('cors');
const { Pool } = require('pg');
const multer = require('multer');
const xlsx = require('xlsx');
const path = require('path');

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

const pool = new Pool({
  user: process.env.DB_USER || 'postgres',
  host: process.env.DB_HOST || 'localhost',
  database: process.env.DB_NAME || 'university_db',
  password: process.env.DB_PASSWORD,
  port: parseInt(process.env.DB_PORT || '5432', 10),
});

const upload = multer({
  dest: 'uploads/',
  limits: { fileSize: 5 * 1024 * 1024 },
  fileFilter: (req, file, cb) => {
    const filetypes = /xlsx|xls/;
    const extname = filetypes.test(path.extname(file.originalname).toLowerCase());
    if (extname) {
      return cb(null, true);
    } else {
      cb(new Error('Только файлы Excel (.xlsx, .xls) разрешены.'));
    }
  }
});

app.get('/api/students', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM Студенты');
    res.json(result.rows);
  } catch (err) {
    console.error(err);
    res.status(500).send('Ошибка сервера');
  }
});

app.post('/api/students', async (req, res) => {
  const { имя, фамилия, дата_рождения, email } = req.body;
  if (!имя || !фамилия || !email) {
    return res.status(400).send('Необходимые поля: имя, фамилия, email');
  }
  try {
    const insertQuery = `
      INSERT INTO Студенты (имя, фамилия, дата_рождения, email)
      VALUES ($1, $2, $3, $4) RETURNING *;
    `;
    const values = [имя, фамилия, дата_рождения, email];
    const result = await pool.query(insertQuery, values);
    res.status(201).json(result.rows[0]);
  } catch (err) {
    console.error(err);
    if (err.code === '23505') {
      res.status(400).send('Студент с таким email уже существует.');
    } else {
      res.status(500).send('Ошибка сервера');
    }
  }
});

app.delete('/api/students/:id', async (req, res) => {
  const studentId = req.params.id;
  try {
    const deleteQuery = 'DELETE FROM Студенты WHERE id = $1 RETURNING *;';
    const result = await pool.query(deleteQuery, [studentId]);
    if (result.rowCount === 0) {
      return res.status(404).send('Студент не найден.');
    }
    res.status(200).json({ message: 'Студент удалён успешно.' });
  } catch (err) {
    console.error(err);
    res.status(500).send('Ошибка сервера');
  }
});

app.get('/api/subjects', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM Предметы');
    res.json(result.rows);
  } catch (err) {
    console.error(err);
    res.status(500).send('Ошибка сервера');
  }
});

app.get('/api/teachers', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM Преподаватели');
    res.json(result.rows);
  } catch (err) {
    console.error(err);
    res.status(500).send('Ошибка сервера');
  }
});

app.get('/api/exams', async (req, res) => {
  try {
    const query = `
      SELECT 
        Экзамены.id,
        Студенты.имя AS студент_имя,
        Студенты.фамилия AS студент_фамилия,
        Предметы.название AS предмет,
        Преподаватели.имя AS преподаватель_имя,
        Преподаватели.фамилия AS преподаватель_фамилия,
        Экзамены.оценка,
        Экзамены.дата_экзамена
      FROM Экзамены
      JOIN Студенты ON Экзамены.студент_id = Студенты.id
      JOIN Предметы ON Экзамены.предмет_id = Предметы.id
      JOIN Преподаватели ON Экзамены.преподаватель_id = Преподаватели.id
      ORDER BY Экзамены.id;
    `;
    const result = await pool.query(query);
    res.json(result.rows);
  } catch (err) {
    console.error(err);
    res.status(500).send('Ошибка сервера');
  }
});

app.post('/api/exams', async (req, res) => {
  const { студент_id, предмет_id, преподаватель_id, оценка, дата_экзамена } = req.body;
  if (!студент_id || !предмет_id || !преподаватель_id || оценка === undefined || !дата_экзамена) {
    return res.status(400).send('Необходимые поля: студент_id, предмет_id, преподаватель_id, оценка, дата_экзамена');
  }
  if (оценка < 0 || оценка > 100) {
    return res.status(400).send('Оценка должна быть от 0 до 100.');
  }
  try {
    const insertQuery = `
      INSERT INTO Экзамены (студент_id, предмет_id, преподаватель_id, оценка, дата_экзамена)
      VALUES ($1, $2, $3, $4, $5) RETURNING *;
    `;
    const values = [студент_id, предмет_id, преподаватель_id, оценка, дата_экзамена];
    const result = await pool.query(insertQuery, values);
    res.status(201).json(result.rows[0]);
  } catch (err) {
    console.error(err);
    res.status(500).send('Ошибка сервера');
  }
});

app.post('/api/subjects/upload', upload.single('file'), async (req, res) => {
  if (!req.file) {
    return res.status(400).send('Файл не был загружен.');
  }

  try {
    const workbook = xlsx.readFile(req.file.path);
    const sheetName = workbook.SheetNames[0];
    const worksheet = workbook.Sheets[sheetName];
    const jsonData = xlsx.utils.sheet_to_json(worksheet, { header: 1 });

    if (jsonData.length === 0) {
      return res.status(400).send('Файл пуст.');
    }

    const subjects = jsonData.map(row => ({
      название: row[0],
      описание: row[1] || ''
    })).filter(subj => subj.название);

    if (subjects.length === 0) {
      return res.status(400).send('Нет данных для импорта.');
    }

    const insertQuery = `
        INSERT INTO Предметы (название, описание)
        VALUES ($1, $2)
        ON CONFLICT (название) DO NOTHING
        RETURNING *;
    `;


    const insertedSubjects = [];

    for (const subject of subjects) {
      const values = [subject.название, subject.описание];
      const result = await pool.query(insertQuery, values);
      if (result.rows.length > 0) {
        insertedSubjects.push(result.rows[0]);
      }
    }

    res.status(201).json({
      message: `Импортировано ${insertedSubjects.length} предметов.`,
      subjects: insertedSubjects
    });

  } catch (error) {
    console.error('Ошибка при импорте предметов:', error);
    res.status(500).send('Произошла ошибка при импорте предметов.');
  } finally {
    const fs = require('fs');
    fs.unlink(req.file.path, (err) => {
      if (err) console.error('Ошибка при удалении временного файла:', err);
    });
  }
});

app.listen(port, () => {
  console.log(`Сервер запущен на http://localhost:${port}`);
});
