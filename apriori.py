import itertools

def count(item_set, transactions):
    return sum([1 for transaction in transactions if item_set.issubset(transaction)])

def apriori(transactions, min_support):
    # 최소 지지도
    min_support_count = int(min_support * len(transactions) / 100)
    
    # 1차 후보 아이템 집합 생성
    item_set = sorted(list(set(itertools.chain.from_iterable(transactions))))
    freq_item_set = [frozenset([item]) for item in item_set if count({item}, transactions) >= min_support_count]
    freq_item_set.sort()
    freq_item_set = set(freq_item_set)
    all_freq_item_sets = []
    
    # 후보 아이템 집합 생성
    k = 2
    while freq_item_set:
        all_freq_item_sets.append(freq_item_set)
        candidate_item_set = set([i.union(j) for i in freq_item_set for j in freq_item_set if len(i.union(j)) == k])
        freq_item_set = set([item_set for item_set in candidate_item_set if count(item_set, transactions) >= min_support_count])
        k += 1
    
    return all_freq_item_sets

# 임의로 생성한 데이터
transactions = [
    ['apple', 'banana', 'orange'],
    ['banana', 'melon', 'orange'],
    ['apple', 'banana', 'melon'],
    ['apple', 'melon'],
    ['apple', 'banana', 'melon', 'orange'],
    ['apple', 'melon', 'orange'],
    ['banana'],
    ['apple', 'banana', 'orange']
]

all_freq_item_sets = apriori(transactions, min_support=0.3)

for freq_item_set in all_freq_item_sets:
    print(freq_item_set)
