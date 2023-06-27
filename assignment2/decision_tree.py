import sys
import math

# entropy를 게산하는 함수
def getEntropy(data):
  # 데이터에서 result만 추출하여 개수 count
  resultCounts = {}
  for row in data:
      result = row[-1]
      if result not in resultCounts:
          resultCounts[result] = 0
      resultCounts[result] += 1
  
  # entropy 계산
  entropy = 0.0
  for count in resultCounts.values():
      prob = float(count) / len(data)
      entropy -= prob * math.log(prob, 2)
  return entropy

# gainRatio를 계산하는 함수
def getGainRatio(data, attributeLength, entropy):
  # gainRatio를 계산하기 위한 변수 list 생성
  attributes = []
  entropies = []
  splitInfo_A = []
  gainRatio = []
  for _ in range(attributeLength):
    attributes.append({})
    entropies.append(0.0)
    splitInfo_A.append(0.0)
  
  # 각각 attribute의 result에 대한 count 계산 nested dictionary로 관리
  for row in data:
    result = row[-1]
    for idx in range(len(row)):
      # dictionary 내부에 attribute key를 가지는 dictionary 추가 
      if row[idx] not in attributes[idx]:
        attributes[idx][row[idx]] = {}
        attributes[idx][row[idx]]["count"] = 0
      if result not in attributes[idx][row[idx]]:
        attributes[idx][row[idx]][result] = 0
      
      # 각 result의 count, 전체 count 관리
      attributes[idx][row[idx]][result] += 1
      attributes[idx][row[idx]]["count"] += 1
      
  
  # Info_A, splitInfo_A
  idx = 0
  for attribute in attributes[:-1]:
    for state in attribute:
      temp = 0.0
      for result in attribute[state]:
        if result != "count":
          # Info(D_j)를 구하는 code
          prob = float(attribute[state][result]) / float(attribute[state]['count'])
          temp -= prob * math.log(prob, 2)
          
      # Info_A를 구하는 code
      temp = temp * (float(attribute[state]['count']) / len(data))
      entropies[idx] += temp
      
      # splitInfo_A를 구하는 code
      prob2 = (float(attribute[state]['count'])) / len(data)
      splitInfo_A[idx] -= prob2 * math.log(prob2, 2)
      
    idx += 1
    
  # gainRatio, 소숫점 4번째 자리까지 반올림
  for i in range(attributeLength - 1):
    if splitInfo_A[i] == 0.0:
      gainRatio_A = 0.0
    else:
      gainRatio_A = round((entropy - entropies[i]) / splitInfo_A[i], 4)
      
    gainRatio.append(gainRatio_A)
  return gainRatio

# Tree를 생성하는 함수
def buildDecisionTree(attributeNames, attributes, attributeLength):
  # entropy, gainRatio 구하기
  entropy = getEntropy(attributes)
  gainRatio = getGainRatio(attributes, attributeLength, entropy)
  
  # overfitting을 방지하기 위해 entropy가 0.1보다 작으면 분류 중단
  if(entropy <= 0.1):
    maxIndex = len(gainRatio)
    rootAttribute = attributeNames[maxIndex]
    rootNode = Node(rootAttribute)
    rootNode.leaf = True
    if(entropy == 0):
      rootNode.result = attributes[0][-1]
      
    # entropy가 0이 아닐 경우 결과값 count해서 더 큰 쪽 선택
    else:
      dic = {}
      for row in attributes:
        if row[-1] not in dic:
          dic[row[-1]] = 0
        dic[row[-1]] += 1
      maxIndex = dic.index(max(dic))
      rootNode.result = dic[maxIndex]
        
  # 아닌 경우, gain ratio가 가장 큰 attribute 선택
  else: 
    maxIndex = gainRatio.index(max(gainRatio))
    rootAttribute = attributeNames[maxIndex]
    rootNode = Node(rootAttribute)
    # createNode 함수를 이용하여 branch마다 node 생성
    createNode(rootNode, attributeNames, attributes, attributeLength)
  
  # decision tree 반환
  return rootNode

# 구분할 attribute를 선택했으면 attribute value로 node 생성
def createNode(parentNode, attributeNames, attributes, attributeLength):
  # parentNode에 속하는 attributes 추출
  parentAttribute = parentNode.attribute
  parentAttributeIndex = attributeNames.index(parentAttribute)
  parentAttributeValues = set([row[parentAttributeIndex] for row in attributes])
  
  # value가 일치하는 row를 모아 list 생성, subtree를 만들기 위함
  for state in parentAttributeValues:
    subAttributes = []
    for row in attributes:
      if state == row[parentAttributeIndex]:
        subAttributes.append(row)
    # subtree 생성
    parentNode.addChild(state, buildDecisionTree(attributeNames, subAttributes, attributeLength))
    
# decision tree 생성에 필요한 class 
class Node:
  def __init__(self, attribute):
    self.attribute = attribute
    self.children = {}
    self.leaf = False
    self.result = None
    
  def addChild(self, value, node):
    self.children[value] = node
  
# Main
with open(sys.argv[1], 'r') as trainFile, open(sys.argv[2], 'r') as testFile, open(sys.argv[3], 'w') as resultFile:
  # trainFile에서 attribute 읽어와서 list에 정리
  attributeNames = trainFile.readline().strip().split('\t')
  attributes = [list(map(str, line.strip().split('\t'))) for line in trainFile]
  attributeLength = len(attributeNames)
  resultFile.write('\t'.join(attributeNames) + '\n')
  # decisionTree 생성
  decisionTree = buildDecisionTree(attributeNames, attributes, attributeLength)
  
  # testFile에서 attribute 읽어와서 list에 정리
  testAttributeNames = testFile.readline().strip().split('\t')
  testAttributes = [list(map(str, line.strip().split('\t'))) for line in testFile]
  
  # 각 test 데이터 예측
  for test in testAttributes:
    currentNode = decisionTree
    while not currentNode.leaf:
      # 현재 노드의 attribute index
      attributeIndex = attributeNames.index(currentNode.attribute)
      # 현재 노드의 attribute 값에 따라 다음 노드 선택
      
      # branch가 있는 경우
      if test[attributeIndex] in currentNode.children:
        currentNode = currentNode.children[test[attributeIndex]]
      # train data의 부족으로 branch가 없는 경우, 이웃 branch로 이동
      else:
        currentNode = currentNode.children[list(currentNode.children.keys())[0]]
        
    # 예측 결과 출력
    resultFile.write('\t'.join(test))
    resultFile.write('\t' + currentNode.result + '\n')