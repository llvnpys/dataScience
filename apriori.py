import sys

def apriori(transactions, minSup):
  
  minSupCount = int(minSup * len(transactions) / 100)
  freqItemSet = []
  #input.txt를 참고해서 allItem은 0~19로 고정
  items = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
  
  # finds the L1 itemset
  for item in items:
    count = 0
    for set in transactions:
      if item in set:
        count += 1
    
    if count >= minSupCount:
      freqItemSet.append({item})
  
  # finds the Lk itemset  
  itemSet = freqItemSet
  while(itemSet):
    
    
    
    
    
    itemSet = freqItemSet
  
  # itemSet
  # asoItemSet
  # sup
  # conf




# main
inputFile = open(sys.argv[2], 'r');
outputFile = open(sys.argv[3], 'w');
transactions = []

for line in inputFile:
    lineSet = set(map(int, line.strip().split('\t')))
    transactions.append(lineSet)

freqItemSets = apriori(transactions, int(sys.argv[1]))