import os
import json
import argparse

from google_sheets_loader import load_google_sheets
from generate_report import generate_report


def load_demo_data():
    """
    Загружает демонстрационные данные из JSON-файла.
    Не требует подключения к Google Sheets API.
    """

    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'sample_data',
        'students_sample.json'
    )

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data['sheet1'], data['sheet2'], data['sheet3']


def main():
    # Настраиваем аргументы командной строки
    parser = argparse.ArgumentParser(
        description='Автоматический расчёт задолженности студентов'
    )

    parser.add_argument(
        '--demo',
        action='store_true',
        help='Запуск на демонстрационных данных без Google API'
    )

    args = parser.parse_args()

    if args.demo:
        print('Режим: демонстрационные данные')

        sheet1, sheet2, sheet3 = load_demo_data()

    else:
        print('Режим: Google Sheets API')

        spreadsheet_id = (
            '1hRnw-PEftF0J-6KY7InlILVwWdkJu4vJiGwRjuE_P4U'
        )

        credentials_path = os.getenv(
            'GOOGLE_CREDENTIALS_PATH',
            'creds.json'
        )

        sheet1, sheet2, sheet3 = load_google_sheets(
            credentials_path,
            spreadsheet_id
        )

    # Показываем количество загруженных записей
    print(f'Студентов: {len(sheet1)}')
    print(f'Записей о датах платежей: {len(sheet2)}')
    print(f'Финансовых записей: {len(sheet3)}')

    # Рассчитываем задолженность
    print('Рассчитываем задолженность...')

    generate_report(sheet1, sheet2, sheet3)

    print('Отчёт создан: student_debt_report.txt')


if __name__ == '__main__':
    main()
