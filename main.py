import os

from google_sheets_loader import load_google_sheets
from generate_report import generate_report


def main():
    # Идентификатор учебной Google-таблицы
    spreadsheet_id = '1hRnw-PEftF0J-6KY7InlILVwWdkJu4vJiGwRjuE_P4U'

    # Путь к учётным данным сервисного аккаунта
    credentials_path = os.getenv('GOOGLE_CREDENTIALS_PATH', 'creds.json')

    print('Подключаемся к Google Sheets API...')

    # Получаем данные с трёх листов
    sheet1, sheet2, sheet3 = load_google_sheets(
        credentials_path,
        spreadsheet_id
    )

    print(f'Загружено студентов: {len(sheet1)}')
    print(f'Загружено записей о датах платежей: {len(sheet2)}')
    print(f'Загружено финансовых записей: {len(sheet3)}')

    print('Рассчитываем задолженность...')

    # Формируем итоговый отчёт
    generate_report(sheet1, sheet2, sheet3)

    print('Отчёт успешно создан: student_debt_report.txt')


if __name__ == '__main__':
    main()
