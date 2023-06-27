import sys
import itertools

def apriori(transactions, minSup):
  minSupCount = int(minSup * len(transactions) / 100)
  allFreqItemSet = []
  
  # find candidate sets
  k = 1
  while(True):
    if k > 1:  
      candItemSet = []
      for i in range(len(freqItemSet)):
        for j in range(i, len(freqItemSet)):
          temp = freqItemSet[i] | freqItemSet[j]
          
          # self-joining
          if len(temp) == k:
            isFreq = True
            for subset in itertools.combinations(temp, k-1):
                if set(subset) not in freqItemSet:
                    isFreq = False
                    break
            if isFreq:
                candItemSet.append(temp)
                
    # transactions의 모든 item을 candItemSet에 담음
    else:
      candItemSet = set.union(*transactions)
      candItemSet = [set([i]) for i in candItemSet]
    
    # no candidate set can be generated
    if len(candItemSet) == 0:
      break;
    
    # find frequent sets
    freqItemSet = []
    for item in candItemSet:
      count = 0
      for itemSet in transactions:
        if item.issubset(itemSet):
          count += 1
      # minSupCount를 만족하고 중복되지 않으면 freqItemSet에 추가
      if count >= minSupCount and item not in freqItemSet:
        freqItemSet.append(item)
        
    # no frequent set can be generated
    if len(freqItemSet) == 0:
      break;
    
    # freqItemSet 저장
    allFreqItemSet.append(freqItemSet)  
    k += 1
    
  return allFreqItemSet

# main
with open(sys.argv[2], 'r') as inputFile, open(sys.argv[3], 'w') as outputFile:
  transactions = [set(map(int, line.strip().split('\t'))) for line in inputFile]
  allFreqItemSet = apriori(transactions, int(sys.argv[1]))
  tranLength = len(transactions)

  for i in range(len(allFreqItemSet)):
    for j in range(i+1,len(allFreqItemSet)):
      for subSet in allFreqItemSet[i]:
        for superSet in allFreqItemSet[j]:
          # item_set, associative_item_set
          itemSet = superSet - subSet
          asoItemSet = superSet - itemSet
          # support, confidence를 찾기 위한 코드
          if (len(asoItemSet) != 0 and i + j + 2 - len(asoItemSet) == len(itemSet) + len(asoItemSet)):
            supCount = 0
            confCount = 0
            confAll = 0
            for set in transactions:
              # support
              if superSet.issubset(set):
                supCount += 1
              #confidence
              if itemSet.issubset(set):
                confAll += 1
                if asoItemSet.issubset(set):
                  confCount += 1
                  
            sup = format(supCount / tranLength * 100, '.2f')
            if confAll ==0:
              conf = 0
            else:
              conf = format(confCount / confAll * 100, '.2f')
              
            outputFile.writelines('\t'.join([str(itemSet).replace(" ", ""), str(asoItemSet).replace(" ", ""), str(sup), str(conf), '\n']))

