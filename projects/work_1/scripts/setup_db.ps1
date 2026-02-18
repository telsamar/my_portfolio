$DB_NAME = "university_db"
$DB_USER = "postgres"
$DB_PASSWORD = $env:DB_PASSWORD
$HOST = "localhost"
$PORT = "5432"

$env:PGPASSWORD = $DB_PASSWORD

function Execute-Command {
    param (
        [string]$Command,
        [string]$Description
    )
    
    Write-Host $Description -ForegroundColor Cyan
    Invoke-Expression $Command
    if ($LASTEXITCODE -eq 0) {
        Write-Host "$Description успешно выполнено." -ForegroundColor Green
    }
    else {
        Write-Host "Не удалось выполнить: $Description" -ForegroundColor Red
        exit $LASTEXITCODE
    }
}

$createDbCommand = "createdb -h $HOST -p $PORT -U $DB_USER $DB_NAME"
try {
    Execute-Command -Command $createDbCommand -Description "Создание базы данных '$DB_NAME'"
}
catch {
    Write-Host "База данных '$DB_NAME' возможно уже существует или произошла другая ошибка." -ForegroundColor Yellow
}

$SQL_SCRIPT = @"
CREATE TABLE IF NOT EXISTS Студенты (
    id SERIAL PRIMARY KEY,
    имя VARCHAR(100) NOT NULL,
    фамилия VARCHAR(100) NOT NULL,
    дата_рождения DATE,
    email VARCHAR(100) UNIQUE
);

CREATE TABLE IF NOT EXISTS Предметы (
    id SERIAL PRIMARY KEY,
    название VARCHAR(100) NOT NULL UNIQUE,
    описание TEXT
);

CREATE TABLE IF NOT EXISTS Преподаватели (
    id SERIAL PRIMARY KEY,
    имя VARCHAR(100) NOT NULL,
    фамилия VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    должность VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Экзамены (
    id SERIAL PRIMARY KEY,
    студент_id INTEGER NOT NULL REFERENCES Студенты(id) ON DELETE CASCADE,
    предмет_id INTEGER NOT NULL REFERENCES Предметы(id) ON DELETE CASCADE,
    преподаватель_id INTEGER NOT NULL REFERENCES Преподаватели(id) ON DELETE CASCADE,
    оценка INTEGER CHECK (оценка >= 0 AND оценка <= 100),
    дата_экзамена DATE NOT NULL
);
"@

$tempSqlFile = "$env:TEMP\setup_db.sql"
$SQL_SCRIPT | Out-File -FilePath $tempSqlFile -Encoding UTF8

$executeSqlCommand = "psql -h $HOST -p $PORT -U $DB_USER -d $DB_NAME -f `"$tempSqlFile`""
try {
    Execute-Command -Command $executeSqlCommand -Description "Создание таблиц в базе данных '$DB_NAME'"
}
catch {
    Write-Host "Произошла ошибка при создании таблиц." -ForegroundColor Red
    exit $LASTEXITCODE
}

Remove-Item -Path $tempSqlFile -Force

Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue

Write-Host "Настройка базы данных завершена." -ForegroundColor Green
