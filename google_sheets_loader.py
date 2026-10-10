import gspread
from oauth2client.service_account import ServiceAccountCredentials


def load_google_sheets(credentials_path, spreadsheet_id):
    """
    Загружает данные из трёх листов Google Sheets.

    credentials_path — путь к файлу учётных данных
    spreadsheet_id — идентификатор Google-таблицы

    Возвращает три списка словарей.
    """

    # Права доступа: только чтение Google Sheets
    scope = [
        'https://www.googleapis.com/auth/spreadsheets.readonly'
    ]

    # Загружаем учётные данные сервисного аккаунта
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_path,
        scope
    )

    # Авторизуемся в Google Sheets API
    client = gspread.authorize(creds)

    # Открываем таблицу по идентификатору
    spreadsheet = client.open_by_key(spreadsheet_id)

    # Получаем данные из трёх листов
    sheet1 = spreadsheet.worksheet('Лист1').get_all_records()
    sheet2 = spreadsheet.worksheet('Лист2').get_all_records()
    sheet3 = spreadsheet.worksheet('Лист3').get_all_records()

    return sheet1, sheet2, sheet3
