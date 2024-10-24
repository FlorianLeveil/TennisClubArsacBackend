import copy
import json
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict

NEW_TRAINING_TEMPLATE = {
    'model': 'BackendTennis.Training',
    'pk': '',
    'fields': {
        'id': '',
        'name': '',
        'participants': [],
        'unregisteredParticipants': [],
        'cancel': False,
        'start': '',
        'end': '',
        'createAt': '',
        'updateAt': ''
    }
}


def get_datetime_now():
    dt = datetime.now(tz=timezone(timedelta(hours=2)))

    formatted_date = dt.isoformat()
    return formatted_date


def generate_training_until_date(training, until_date, excluded_dates):
    all_trainings_until_date = []
    start_training_date = datetime.fromisoformat(training['fields'].get('start', ''))
    end_training_date = datetime.fromisoformat(training['fields'].get('end', ''))
    while start_training_date < until_date:
        start_training_date += timedelta(days=7)
        end_training_date += timedelta(days=7)
        in_holidays = False

        for excluded_date in excluded_dates:
            if excluded_date['start'] <= start_training_date <= excluded_date['end']:
                in_holidays = True
                break
            if excluded_date['start'] <= end_training_date <= excluded_date['end']:
                in_holidays = True
                break
        if in_holidays:
            continue
        _uuid = str(uuid.uuid4())
        _creation_date = get_datetime_now()
        new_training = copy.deepcopy(training)
        new_training['pk'] = _uuid
        new_training['fields']['id'] = _uuid
        new_training['fields']['start'] = start_training_date.isoformat()
        new_training['fields']['end'] = end_training_date.isoformat()
        new_training['fields']['createAt'] = _creation_date
        new_training['fields']['updateAt'] = _creation_date

        all_trainings_until_date.append(new_training)
    return all_trainings_until_date


def format_new_training(old_training: Dict) -> Dict:
    _uuid = str(uuid.uuid4())
    _creation_date = get_datetime_now()
    new_training = copy.deepcopy(NEW_TRAINING_TEMPLATE)
    new_training['pk'] = _uuid
    new_training['fields']['id'] = _uuid
    new_training['fields']['name'] = old_training.get('name', '')
    new_training['fields']['cancel'] = old_training.get('cancel', '')
    new_training['fields']['start'] = old_training.get('start', '')
    new_training['fields']['end'] = old_training.get('end', '')
    new_training['fields']['createAt'] = _creation_date
    new_training['fields']['updateAt'] = _creation_date

    participants_name = old_training.get('description', '').split('/')
    participants_name = [name.strip() for name in participants_name]
    new_training['fields']['unregisteredParticipants'] = participants_name

    return new_training


def main():
    old_trainings_files_path = 'json_files/all_training_first_date.json'
    new_trainings_files_path = 'json_files/new_trainings.json'
    with open(old_trainings_files_path, 'r+') as _file:
        trainings_old_format = json.loads(_file.read())
    trainings_new_format = []

    holidays = [
        {
            'start': datetime(2024, 10, 19, 23, 59, 59, tzinfo=timezone(timedelta(hours=2))),
            'end': datetime(2024, 11, 4, 0, 0, 0, tzinfo=timezone(timedelta(hours=2)))
        },
        {
            'start': datetime(2024, 12, 21, 23, 59, 59, tzinfo=timezone(timedelta(hours=2))),
            'end': datetime(2025, 1, 6, 0, 0, 0, tzinfo=timezone(timedelta(hours=2)))
        },
        {
            'start': datetime(2025, 2, 22, 23, 59, 59, tzinfo=timezone(timedelta(hours=2))),
            'end': datetime(2025, 3, 10, 0, 0, 0, tzinfo=timezone(timedelta(hours=2)))
        },
        {
            'start': datetime(2025, 4, 19, 23, 59, 59, tzinfo=timezone(timedelta(hours=2))),
            'end': datetime(2025, 5, 5, tzinfo=timezone(timedelta(hours=2)))
        }
    ]
    training_end_date = datetime(2025, 7, 5, 0, 0, 0, tzinfo=timezone(timedelta(hours=2)))

    for training in trainings_old_format:
        new_training = format_new_training(training)
        trainings_new_format.append(new_training)

        all_year_trainings = generate_training_until_date(new_training, training_end_date, holidays)

        trainings_new_format.extend(all_year_trainings)

    with open(new_trainings_files_path, 'w+') as _file:
        _file.write(json.dumps(trainings_new_format, ensure_ascii=False))


if __name__ == '__main__':
    main()
