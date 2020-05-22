import json
# import os
import requests
import sys
import time

repository = ""  # new
repository_version = 0
base_url = 'https://api.bothub.it/v2/repository/'

params = {'repository_uuid': repository}
headers = {
    "Authorization": "Token ...",
    "Content-Type": "application/json"
}


def get_examples_count(repository_uuid, *args):
    return json.loads(requests.get(
        f'{base_url}repository-info/{repository_uuid}',
        headers=headers
    ).content).get('examples__count')


def delete_repository(repository_uuid):
    return requests.delete(
        f'{base_url}repository-info/{repository_uuid}/',
        headers=headers
    )


def get_all_examples(headers, next_call, params, *args):
    while next_call is not None:
        response = requests.get(next_call, headers=headers, params=params)
        response_json = response.json()
        next_call = response_json.get('next')
        yield response_json.get('results', None)


def delete_example(example_id, *args):
    try:
        response = requests.delete(f'{base_url}example/{example_id}/', headers=headers)
        if response.status_code == 204:
            print("Example deleted!")
        return response.status_code
    except err:
        print(err)
        print(f'Failed to delete this sentence!\nText: {example.get("text")}')
        return


def create_example(example, *args):
    entities = []
    if len(example.get('entities')) > 0:
        for entity in example.get('entities'):
            if entity:
                entities.append({
                    "entity": entity.get('entity'),
                    "start": entity.get('start'),
                    "end": entity.get('end')
                })

    data = {
        "repository": repository,
        "text": example.get('text'),
        "intent": example.get('intent'),
        "entities": entities
    }
    try:
        response = requests.post(f'{base_url}example/', headers=headers, data=json.dumps(data))
        print("Example created!")
        return response.status_code
    except err:
        print(err)
        print(f'Failed to train this sentence!\nText: {example.get("text")}')
        return


def delete_evaluate_example(example_id):
    response = requests.delete(f'{base_url}evaluate/{example_id}/?repository_uuid={repository}', headers=headers)
    if response.status_code == 204:
        print("Example deleted!")
    return response.status_code


def delete_all_examples(*args):
    results = get_all_examples(
        headers=headers,
        next_call=f'{base_url}evaluate/',
        params=params
    )

    for result in results:
        for item in result:
            time.sleep(1)
            response = delete_evaluate_example(item.get('id'))
            print(response)


def create_evaluate_examples(*args):
    with open('rasa-dataset-testing.json') as json_file:
        examples = json.load(json_file)

        count = len(examples)
        index = 0

        for example in examples:
            data = {
                "is_corrected": False,
                "repository": repository,
                "repository_version": int(repository_version),
                "text": example['text'],
                "language": example['language'],
                "intent": example['intent'],
                "entities": []
            }

            response = requests.post(f'{base_url}evaluate/', headers=headers, data=json.dumps(data))

            if response.status_code == 201:
                print("\nEvaluate example created!")
            print(f"%.2f%%" % ((index*100)/count))


def sentences_count(intent=None, *args):
    def count_intent(examples, intent):
        count = 0
        for example in examples:
            if example['intent'] == intent:
                count += 1
        return count

    with open('data/rasa_dataset_training.json') as json_file:
        examples = json.load(json_file)['rasa_nlu_data']['common_examples']
        if intent:
            count = count_intent(examples, intent)
            print(count)
            return

        intents = []
        total = 0
        for example in examples:
            if example['intent'] not in intents:
                count = count_intent(examples, example['intent'])
                print(f'{count} - {example["intent"]}')
                total += count
                intents.append(example['intent'])
        print(f'{total} - total')


def delete_all():
    count = get_examples_count(repository)
    results = get_all_examples(
        headers=headers,
        next_call=f'{base_url}examples/',
        params=params
    )
    index = 0

    for result in results:
        for item in result:
            time.sleep(1)
            delete_example(item.get('id'))
            index += 1
            print(f"%.2f%%" % ((index*100)/count))


def delete_by_intent(intent, *args):
    count = get_examples_count(repository)
    index = 0
    results = get_all_examples(
        headers=headers,
        next_call=f'{base_url}examples/',
        params=params
    )

    for result in results:
        for item in result:
            if item.get('intent') == intent:
                time.sleep(1)
                delete_example(item.get('id'))
                index += 1
                print(f"%.2f%%" % ((index*100)/count))


# Função para treinar as frases a partir de um json gerado pelo Chatito GSL
def main():
    with open('rasa_dataset_training.json') as json_file:
        examples = json.load(json_file)['rasa_nlu_data']['common_examples']
        count = len(examples)
        index = 0

        for example in examples:
            entities = []
            for entity in example['entities']:
                entities.append({
                    "entity": entity['entity'],
                    "start": entity['start'],
                    "end": entity['end']
                })

            result = {
                "text": example['text'],
                "language": "pt-br",
                "intent": example['intent'],
                "entities": entities
            }
            create_example(result)
            index += 1
            print(f"%.2f%%" % ((index*100)/count))

if __name__ == '__main__':
    args = sys.argv
    if len(args) > 1:
        try:
            func = eval(f'{args[1]}')
        except:
            print("function doesn't exists!")
        else:
            func(*args[2:])
    else:
        main()
