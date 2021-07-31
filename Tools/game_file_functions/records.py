def push_records(name: str, score: int, time: str) -> list:
    old_records = load_records()

    with open('data/records.trec', encoding="utf-8", mode='w') as file:
        players = create_players_list(name, score, time, old_records)
        file.write('\n'.join([str(i + 1) + ' ' + ' '.join(map(str, players[i])) for i in range(len(players))][:10]))

    return players


def load_records():
    with open('data/records.trec', encoding="utf-8", mode='r') as file:
        return [i.strip() for i in file.readlines()]


def create_players_list(name: str, score: int, time: str, old_records: list) -> list:
    players = [i.split()[1:] for i in old_records]
    players.append([name, score, time])
    players = sorted(players, key=sort_key, reverse=True)

    return players


def sort_key(value):
    return int(value[1]), list(map(lambda x: -int(x), value[2].split(':')))
