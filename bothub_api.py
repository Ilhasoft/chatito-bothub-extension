import os, sys
import json, requests, time

repository = ''
base_url = ''
params = {'repository_uuid': repository}
headers = {
    "Authorization": "Token ",
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
        print(f'Failed to delete this sentence!\nText: {example.get('text')}')
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
        print(f'Failed to train this sentence!\nText: {example.get('text')}')
        return

def delete_evaluate_example(example_id):
    response = requests.delete(f'{base_url}evaluate/{example_id}/?repository_uuid={repository}', headers=headers)
    if response.status_code == 204:
        print("Example deleted!")
    return response.status_code

def delete_all_examples(*args):
    results = get_all_examples(
        headers=headers,
        next_call='{base_url}evaluate/',
        params=params
    )

    for result in results:
        for item in result:
            time.sleep(1)
            response = delete_evaluate_example(item.get('id'))
            print(response)

def create_evaluate_examples(*args):
    with open('data/nlu_test.json') as json_file:
        examples = json.load(json_file)
        index = 0
        for intent, texts in examples.items():
            for text in texts:
                data = {
                    "repository": repository,
                    "language": "pt_br",
                    "entities": [],
                    "text": text,
                    "intent": intent
                }
                response = requests.post(f'{base_url}evaluate/', headers=headers, data=json.dumps(data))
                print(response.status_code)
                if response.status_code == 201:
                    print("\nEvaluate example created!")

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
        next_call='{base_url}examples/',
        params=params
    )
    index = 0

    for result in results:
        for item in result:
            time.sleep(1)
            delete_example(item.get('id'))
            index += 1
            print(f"%.2f%%" % ((index*100)/count))

def main():
    with open('data/rasa_dataset_training.json') as json_file:
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

# Save results in a JSON file
# with open('format_examples.json', 'w') as outfile:
#     json.dump(results, outfile)

# Send this file to Bothub in a Post request
# response = requests.post(
#     f'{base_url}example/upload_examples/',
#     headers={
#         'Authorization': "Token ab245d24bfb052c7a73e34d17f9843e6346058c9",
#     },
#     data={
#         'repository': repository,
#     },
#     files={'file': open('bothub_format_examples.json', 'rb')}
# )

# print(response.status_code)

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
