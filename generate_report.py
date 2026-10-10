from datetime import datetime, timedelta


def generate_report(sheet1, sheet2, sheet3):
    """
    Формирует отчёт о задолженности студентов
    на 1 марта 2023 года.

    sheet1 — сведения о студентах
    sheet2 — даты платежей
    sheet3 — финансовые данные
    """

    report_date = datetime.strptime('01.03.2023', '%d.%m.%Y')
    payment_period = timedelta(days=183)

    # Создаём справочники по идентификатору студента
    dates = {row['student_id']: row for row in sheet2}
    payments = {row['student_id']: row for row in sheet3}

    debtors = []

    for student in sheet1:
        # Учитываем только студентов с рассрочкой
        if student['installment'] != 'Y':
            continue

        student_id = student['student_id']

        # Пропускаем записи без необходимых данных
        if student_id not in dates or student_id not in payments:
            continue

        expected_date = datetime.strptime(
            dates[student_id]['expected_payment_date'],
            '%d.%m.%Y'
        )

        payment_info = payments[student_id]

        one_time_payment = int(payment_info['one-time_payment'])
        left_to_pay = int(payment_info['left_to_pay'])

        # Подсчитываем количество пропущенных платежей
        missed_payments = 0

        while expected_date <= report_date:
            missed_payments += 1
            expected_date += payment_period

        # Задолженность не может превышать остаток рассрочки
        debt = min(
            missed_payments * one_time_payment,
            left_to_pay
        )

        if debt > 0:
            debtors.append(
                f"Студент {student['student_name']} - долг {debt} рублей"
            )

    # Записываем отчёт в текстовый файл
    with open('student_debt_report.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(debtors))
