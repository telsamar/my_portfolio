#!/bin/bash

DB_NAME="db_site_1"
DB_USER="postgres"
DB_PASS="postgres"
DB_HOST="localhost"
DB_PORT="5432"

export PGPASSWORD=$DB_PASS

psql -U $DB_USER -h $DB_HOST -p $DB_PORT -c "CREATE DATABASE $DB_NAME;"

psql -U $DB_USER -h $DB_HOST -p $DB_PORT -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

psql -U $DB_USER -h $DB_HOST -p $DB_PORT -d $DB_NAME <<EOSQL

CREATE TABLE IF NOT EXISTS uavs (
  id SERIAL PRIMARY KEY,
  photo_url TEXT,
  name TEXT NOT NULL,
  description TEXT,
  official_website TEXT,
  manufacturer TEXT,
  aircraft_type TEXT,
  weight_category_kg TEXT,
  payload TEXT,
  communication_range_km INTEGER,
  max_takeoff_mass_kg NUMERIC,
  max_flight_time_min INTEGER,
  max_route_length_km INTEGER,
  max_speed_km_h INTEGER,
  max_payload_kg NUMERIC,
  cruise_speed_km_h INTEGER,
  application_areas TEXT
);

INSERT INTO uavs (
  photo_url,
  name,
  description,
  official_website,
  manufacturer,
  aircraft_type,
  weight_category_kg,
  payload,
  communication_range_km,
  max_takeoff_mass_kg,
  max_flight_time_min,
  max_route_length_km,
  max_speed_km_h,
  max_payload_kg,
  cruise_speed_km_h,
  application_areas
) VALUES (
  '1.jpg',
  'Геоскан 201',
  'Комплекс, созданный для съемки и моделирования обширных территорий и протяженных объектов. На борт можно установить одновременно две полезные нагрузки (например: камеру 45 Мпикс и мультиспектральную камеру).',
  'https://www.geoscan.ru/ru/products/geoscan201/geo?utm_source=aeronet2035&utm_medium=organic&utm_campaign=catalog&utm_content=201geo',
  'ГК Геоскан',
  'Самолет',
  '3-15',
  'Аэро фото-видео-камера / Тепловизионная / Мультиспектральная',
  40,
  8.5,
  180,
  210,
  110,
  1.5,
  80,
  'Сбор данных, мониторинг'
);

INSERT INTO uavs (
  photo_url,
  name,
  description,
  official_website,
  manufacturer,
  aircraft_type,
  weight_category_kg,
  payload,
  communication_range_km,
  max_takeoff_mass_kg,
  max_flight_time_min,
  max_route_length_km,
  max_payload_kg,
  cruise_speed_km_h,
  application_areas
) VALUES (
  '2.jpg',
  'Sigma mini',
  'Производитель: НПП Авакс-Геосервис. Компактный БВС типа VTOL со взлётной массой 16 кг.',
  '-',
  'НПП Авакс-Геосервис',
  'VTOL',
  '15-30',
  'Аэро фото-видео-камера / Тепловизионная камера',
  70,
  16,
  120,
  140,
  2.5,
  72,
  'Сбор данных, мониторинг'
);

INSERT INTO uavs (
  photo_url,
  name,
  description,
  official_website,
  manufacturer,
  aircraft_type,
  weight_category_kg,
  payload,
  communication_range_km,
  max_takeoff_mass_kg,
  max_flight_time_min,
  max_payload_kg,
  application_areas
) VALUES (
  '3.jpg',
  'Supercam X6M2',
  'Производитель: ФИНКО ГК Беспилотные системы. Мультикоптер с большой вариативностью полезной нагрузки (лидар, гамма-спектрометр и т.д.).',
  'https://supercam.aero/catalog/supercaam-x6m2lidar',
  'ФИНКО ГК Беспилотные системы',
  'Мультиротор',
  '3-15',
  'Фото-видео-камера / Тепловизионная / Мультиспектральная / Лидар / и т.д.',
  10,
  8,
  55,
  2.0,
  'Аэрологистика'
);

EOSQL

echo "База данных $DB_NAME создана и заполнена тремя записями."
