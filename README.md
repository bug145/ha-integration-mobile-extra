# HA Integration Mobile Extra

Интеграция для Home Assistant, которая добавляет новые сенсоры в интеграцию мобильного приложения.

## Описание

Эта интеграция расширяет функциональность стандартной интеграции мобильного приложения Home Assistant, добавляя дополнительные сенсоры и возможности.

## Установка

### Через HACS (рекомендуется)

1. Убедитесь, что у вас установлен [HACS](https://hacs.xyz/)
2. Добавьте этот репозиторий как кастомный репозиторий в HACS
3. Найдите "HA Integration Mobile Extra" в HACS и установите
4. Перезапустите Home Assistant
5. Добавьте интеграцию через UI

### Ручная установка

1. Скопируйте папку `custom_components/ha_integration_mobile_extra` в папку `config/custom_components/` вашего Home Assistant
2. Перезапустите Home Assistant
3. Добавьте интеграцию через UI

## Конфигурация

Интеграция не требует дополнительной конфигурации и автоматически создает сенсор после установки.

## Поддерживаемые платформы

- Sensor

## Требования

- Home Assistant 2023.8.0 или новее
- Интеграция mobile_app должна быть установлена

## Структура проекта

```
ha-integration-mobile-extra/
├── custom_components/
│   └── ha_integration_mobile_extra/
│       ├── __init__.py
│       ├── manifest.json
│       ├── sensor.py
│       ├── const.py
│       └── translations/
│           ├── en.json
│           └── ru.json
└── README.md
```

## Лицензия

MIT License
