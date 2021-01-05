import json
import sys
import time

from decouple import config

from bothub_api import get_all_examples, create_example, delete_example, get_examples_count, create_evaluate_examples

repository = config('REPOSITORY_UUID')
repository_version = config('REPOSITORY_VERSION_ID')
base_url = config('BOTHUB_API_URL')
params = {'repository_uuid': repository}
headers = {
    'Authorization': f'Token {config("ACCOUNT_API_TOKEN")}',
    'Content-Type': 'application/json'
}


def delete_by_intent(intent, *args):
    count = get_examples_count(repository)
    index = 0
    results = get_all_examples(
        headers=headers,
        next_call=f'{base_url}/repository/examples/',
        params=params
    )

    for result in results:
        for item in result:
            if item.get('intent') == intent:
                time.sleep(1)
                delete_example(item.get('id'))
                index += 1
                print(f"%.2f%%" % ((index*100)/count))

    print(F'All sentences with "{intent}" intent are deleted!')


def export_to_json(filename, *args):
    # Getting all sentences from bothub repository
    results = get_all_examples(
        headers=headers,
        next_call=f'{base_url}/repository/examples/',
        params=params
    )
    examples = []
    for result in results:
        for sentence in result:
            examples.append(sentence)
    # Save results in a JSON file
    with open(f'{filename}.json', 'w') as outfile:
        json.dump(examples, outfile)

def export_evaluate_to_json(filename, *args):
    # Getting all evaluate sentences from a bothub repository
    results = get_all_examples(
        headers=headers,
        next_call=f'{base_url}/repository/evaluate/',
        params=params
    )
    examples = []
    for result in results:
        for sentence in result:
            examples.append(sentence)
    # Save results in a JSON file
    with open(f'{filename}.json', 'w') as outfile:
        json.dump(examples, outfile)


def train_json_sentences(filename, *args):
    # Read the examples in JSON file and save in a List
    with open(f'{filename}.json') as json_file:
        examples = json.load(json_file)

    # Function to build the body request and send it to bothub using create_example funtion
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
            "language": example['language'],
            "intent": example['intent'],
            "entities": entities
        }
        time.sleep(1)
        create_example(result)
        index += 1
        print(f"%.2f%%" % ((index*100)/count))


def train_chatito(filename, *args):
    with open(f'{filename}.json', encoding="utf-8") as json_file:
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
                "language": "pt_br",
                "intent": example['intent'],
                "entities": entities
            }
            created_example = create_example(result)
            print(F'HTTP Response {created_example}')
            index += 1
            print(f"%.2f%%" % ((index*100)/count))


def main():
    print('welcome to Chatito-Bothub-Extension!')


if __name__ == '__main__':
    args = sys.argv
    if len(args) > 1:
        try:
            func = eval(f'{args[1]}')
        except Exception:
            print("function doesn't exists!")
        else:
            func(*args[2:])
    else:
        main()
