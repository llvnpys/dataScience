import sys
import math

# cluster Id, cluster 배열 전역변수로 지정
global nextClusterId
nextClusterId = 1
clusters = []

# point class
class Point:
  def __init__(self, id, x, y):
    self.id = id
    self.x_coordination = x
    self.y_coordination = y
    self.label = 0 # 0: undefined / -1: noise / > 0: cluster_id 
  
  # 중복되는 point를 제거할 때 label은 고려하지 않아야 함.
  def __eq__(self, other):
    if isinstance(other, Point):
        return (
            self.id == other.id and
            self.x_coordination == other.x_coordination and
            self.y_coordination == other.y_coordination
        )
    return False
  
  def __hash__(self):
        return hash((self.id, self.x_coordination, self.y_coordination))

# Neighbor class
class Group:
  def __init__(self):
    self.points = set();
    self.size = 0
  
  # 
  def merge(self, otherGroup):
    self.points.update(otherGroup.points)
    self.size = len(self.points)

# 
def DBSCAN(points, n, eps, minPts):
  global nextClusterId
  global clusters
  
  # dataset 순회
  for point in points:
    # 방문한 적이 있는 point면 pass
    if point.label != 0: 
      continue
    
    # point의 이웃을 설정해주는 함수 적용
    N = rangeQuery(points, point, eps)

    # 만약 epsilon 범위 내의 point개수가 minpts보다 작으면
    if N.size < minPts:
      # point는 noise로 처리 (border point or outlier)
      point.label = -1
      continue
    
    # 여기에 도달했으면 P는 core point
    # cluster Id 할당
    point.label = nextClusterId;
    nextClusterId += 1
    
    # expands cluster
    flag = 1
    # N에 undefined point가 없을 때까지 반복
    while(flag):
      flag = 0
      for p in N.points:
        # undefined point인 경우
          if p.label == 0:
            N = expandCluster(points, N, eps, minPts, point.label)
            flag = 1
            break;
    
    # cluster 개수 조절
    if len(clusters) < n:
      clusters.append(N)
      
    # cluster 개수가 n보다 클 경우, point가 가장 적은 cluster 제거
    else:
      minIdx = -1
      minLen = len(N.points)
      for idx in range(len(clusters)):
        if minLen > len(clusters[idx].points):
          minIdx = idx
          minLen = len(clusters[idx].points)

      if minIdx != -1:
        clusters[idx] = N

# distance와 eps를 비교해 neighbor를 생성하는 함수
def rangeQuery(points, point, eps):
  global nextClusterId
  global clusters
  
  neighbor = Group()
  for p in points:
    # point와 p 사이의 거리를 계산
    distance = math.sqrt((point.x_coordination - p.x_coordination) ** 2 + (point.y_coordination - p.y_coordination) ** 2)
    
    # 거리가 eps보다 작으면 neighbor에 추가
    if distance <= eps:
      neighbor.points.add(p)
      neighbor.size = len(neighbor.points)
  
  return neighbor

# core point의 neighbor point로 cluster를 확장하는 함수
def expandCluster(points, cluster, eps, minPts, lebal):
  for p in list(cluster.points):
    # noise로 분류돼있는 경우, cluster에 추가
    if p.label == -1:
      p.label = lebal
      
    if p.label != 0:
      continue
    
    # p가 undefined인 경우
    p.label = lebal
    N = rangeQuery(points, p, eps)
    if N.size >= minPts:
      N.merge(cluster)
      cluster = N
      
  return cluster

# Main
with open(sys.argv[1], 'r') as inputFile:
  # step 1
  n = int(sys.argv[2])
  eps = int(sys.argv[3])
  minPts = int(sys.argv[4])
  points = []
  # dataset 생성
  for line in inputFile:
    data = line.strip().split('\t')
    points.append(Point(int(data[0]), float(data[1]), float(data[2])))
  
  DBSCAN(points, n, eps, minPts)
  
  # outputFile
  index = 0
  for cluster in clusters:
    with open(sys.argv[1].rstrip(".txt")+"_cluster_"+str(index)+".txt", "w") as file:
      for object in cluster.points:
        file.write(str(object.id) + "\n")
      index += 1