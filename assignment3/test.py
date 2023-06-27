# 1. 이웃 설정: 주어진 데이터 세트에서 각 데이터 포인트 간의 거리를 계산하여 이웃을 설정합니다.
# 2. 핵심 포인트 찾기: 주어진 데이터 포인트의 이웃 개수가 미리 지정한 임계값(min_samples) 이상이면 해당 데이터 포인트는 핵심 포인트(core point)로 간주합니다.
# 3. 클러스터 확장: 핵심 포인트를 중심으로 클러스터를 형성합니다. 핵심 포인트의 이웃들을 확인하면서, 이웃이 또 다른 핵심 포인트라면 해당 이웃도 핵심 포인트로 포함시킵니다. 이렇게 확장되는 과정을 반복하면 하나의 클러스터가 형성됩니다.
# 4. 노이즈 포인트 식별: 핵심 포인트가 아닌 데이터 포인트들은 노이즈 포인트(noise point)로 처리합니다. 즉, 어떤 클러스터에도 속하지 않는 이상치로 간주됩니다.




with open(sys.argv[1], 'r') as inputFile:
  n = int(sys.argv[2])
  eps = int(sys.argv[3])
  minPts = int(sys.argv[4])
  points = []
  
  for line in inputFile:
    data = line.strip().split('\t')
    points.append(Point(int(data[0]), float(data[1]), float(data[2])))