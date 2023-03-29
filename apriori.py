import sys
import itertools

def apriori(transactions, minSup):
  minSupCount = int(minSup * len(transactions) / 100)
  allFreqItemSet = []
  # finds the Lk itemset
  k = 1
  while(True):
    if k > 1:  
      candItemSet = []
      for i in range(len(freqItemSet)):
        for j in range(i, len(freqItemSet)):
          temp = freqItemSet[i] | freqItemSet[j]
          if len(temp) == k:
            candItemSet.append(temp)

    else:
      candItemSet = [{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18},{19}]
    
    if len(candItemSet) == 0:
      break;
    
    freqItemSet = []      
    for item in candItemSet:
      count = 0
      for set in transactions:
        if item.issubset(set):
          count += 1   
      if count >= minSupCount and item not in freqItemSet:
        freqItemSet.append(item)
    
    allFreqItemSet.append(freqItemSet)  
    k += 1
    
  return allFreqItemSet

# main
inputFile = open(sys.argv[2], 'r');
outputFile = open(sys.argv[3], 'w');
transactions = []


for line in inputFile:
  transactions.append(set(map(int, line.strip().split('\t'))))

tranLength = len(transactions)

allFreqItemSet = apriori(transactions, int(sys.argv[1]))


for i in range(len(allFreqItemSet)):
  for j in range(i+1,len(allFreqItemSet)):
    for k in range(len(allFreqItemSet[i])):
      for l in range(len(allFreqItemSet[j])):
        superSet = allFreqItemSet[j][l]
        subSet = allFreqItemSet[i][k]
        itemSet = superSet - subSet
        asoItemSet = superSet - itemSet
        if (len(asoItemSet) != 0):
          supCount = 0
          confCount = 0
          confAll = 0
          for set in transactions:
            if superSet.issubset(set):
              supCount += 1
            if itemSet.issubset(set):
              confAll += 1
              if asoItemSet.issubset(set):
                confCount += 1
                
          sup = format(supCount / tranLength * 100, '.2f')
          if confAll ==0:
            conf = 0
          else:
            conf = format(confCount / confAll * 100, '.2f')
          outputFile.writelines('\t'.join([str(itemSet), str(asoItemSet), str(sup), str(conf), '\n']))

