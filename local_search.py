import random
import copy

N, M, K = map(int, input().split())   
a, b, c, d, e, f = map(int, input().split())  

s = []
for i in range(N):
    s.append(list(map(int, input().split())))

g = []
for i in range(N):
    g.append(list(map(int, input().split())))

t = list(map(int, input().split()))
t.insert(0,0)

# Khởi tạo mỗi giá trị x,y là ngẫu nhiên, miễn sao số giáo viên, đồ án trong mỗi hội đồng ~ giá trị trung bình là được
# đoạn này nếu với test case số lẻ; kiểu N = 51; K = 5 thì cần điều chỉnh số đồ án mỗi hội đồng một chút, kiểu <= [N/K] + 1
def initialSolution():
    global N, M, K
    count = [0 for i in range(K+1)]
    initialX = [0 for _ in range(N+1)]
    initialY = [0 for _ in range(M+1)]

    for i in range(1, N+1):
        check = True
        while check:
            num = random.randint(1, K)
            if count[num] + 1 <= N/K:
                initialX[i] = num
                count[num] += 1
                check = False
            if sum(count) == N:
                break

    count = [0 for i in range(K+1)]

    for i in range(1, M+1):
        check = True
        while check:
            num = random.randint(1, K)
            if count[num] + 1 <= M/K:
                initialY[i] = num
                check = False
            if sum(count) == M:
                break
    return initialX, initialY

# nhóm xem mỗi hội đồng chứa giáo viên nào, sinh viên nào
def groupStudentAndTeacherIntoEachJury(solutionX, solutionY):
    global N, M, K
    juryX, juryY = [[] for _ in range(K+1)], [[] for _ in range(K+1)]

    for i in range(1, N+1):
        juryX[solutionX[i]].append(i)
    
    for i in range(1, M+1):
        juryY[solutionY[i]].append(i)

    return juryX, juryY

# hàm tính số ràng buộc bị vi phạm 
# công thức = số giáo viên vi phạm + số học sinh vi phạm + mức độ tương đồng vi phạm + cặp giáo viên/sinh viên vi phạm
def violatedConstraint(solutionX, solutionY):
    global K, M, N, e, f, a, b, c, d, s, g, t
    res = 0
    juryX, juryY = groupStudentAndTeacherIntoEachJury(solutionX, solutionY)
    
    for k in range(1, K+1):
        for n1 in range(len(juryX[k])):
            for n2 in range(n1, len(juryX[k])):
                res += e - s[juryX[k][n1]-1][juryX[k][n2]-1] if e > s[n1-1][n2-1] else 0

    for k in range(1, K+1):
        for n1 in range(len(juryX[k])):
            for n2 in range(len(juryY[k])):
                res += f - s[juryX[k][n1]-1][juryY[k][n2]-1] if f > s[n1-1][n2-1] else 0
    
    for k in range(1, K+1):
        res += a - len(juryX[k]) if a > len(juryX[k]) else 0
        res += len(juryX[k]) - b if b < len(juryX[k]) else 0
        res += c - len(juryY[k]) if c > len(juryY[k]) else 0
        res += len(juryY[k]) - d if d < len(juryY[k]) else 0

    for n in range(1, N+1):
        res += 1 if solutionX[n] == solutionY[t[n]] else 0

    return res

# giáo viên ở hội đồng k bị vi phạm => chuyển sang k + STEP; STEP cho thay đổi từ 1 đến K-1, mục đích là tạo ra nhiều neighbor để dễ chọn ra giải pháp tốt hơn
def neighbour(solutionX, solutionY):
    global t
    step = 1
    initialLoss = violatedConstraint(solutionX, solutionY)

    currentLoss = float('inf')

    while step < K and currentLoss >= initialLoss:
        neighbourX = (solutionX).copy()         
        neighbourY = (solutionY).copy()          # đcm ngu vl bug đbrr new year same bug :)
        for i in range(1, N+1):
            if solutionY[t[i]] == solutionX[i]:
                neighbourY[t[i]] = (solutionY[t[i]] + step) % K if (solutionY[t[i]] + step) % K != 0 else K
        currentLoss = violatedConstraint(neighbourX, neighbourY)
        step += 1
        
    # print(f"loss after: {violatedConstraint(neighbourX, neighbourY)}")
    return neighbourX, neighbourY

def calculateScore(solutionX, solutionY):
    global K, g, s
    score = 0
    juryX, juryY = groupStudentAndTeacherIntoEachJury(solutionX, solutionY)

    for j in range(1, K+1):
        for i in range(len(juryX[j])):
            if i == 0:
                continue
            for k in range(i-1):
                score = score + s[juryX[j][i]-1][juryX[j][k]-1]    # we dont count it 2 times
        for thesis in juryX[j]:
            for teacher in juryY[j]:
                score += g[thesis-1][teacher-1]

    return score

def hillClimbingVariant():
    global N, M
    resX, resY = randomRestart()
    print(N)
    for i in range(1, len(resX)):
        print(resX[i], end=" ")
    print()
    print(M)
    for i in range(1, len(resY)):
        print(resY[i], end=" ")
    print()

# mỗi lần khởi tạo ngẫu nhiên một lời giải, sau đó cho nó dịch chuyển sang hàng xóm bên cạnh 10 lần (chưa thử số khác) xem có tìm được cháu nào tốt hơn không
# tìm được thì cho vào lời giải khả thi rồi cuối cùng cho mấy cháu đấm nhau xem cháu nào khỏe nhất
def randomRestart():
    feasibleSolution = []
    curRes = 0
    resX, resY = [], []

    for _ in range(10000):
        Try = 0
        initialX, initialY = initialSolution()
        currentX, currentY = initialX, initialY
        while violatedConstraint(currentX, currentY) > 0:
            neighbourX, neighbourY = neighbour(currentX, currentY)
            currentX, currentY = neighbourX, neighbourY
            Try += 1
            if Try > 10:
                break
        if violatedConstraint(currentX, currentY) == 0 and (currentX, currentY) not in feasibleSolution:
            feasibleSolution.append((currentX, currentY))
            if len(feasibleSolution) == 2:
                break

    for solutionX, solutionY in feasibleSolution:
        if calculateScore(solutionX, solutionY) > curRes:
            resX = solutionX
            resY = solutionY
    
    return resX, resY

if __name__=="__main__":
    hillClimbingVariant()

'''
6 4 2
2 4 1 3 1 1
0 2 4 1 2 5 
2 0 5 5 3 5 
4 5 0 4 3 5 
1 5 4 0 3 2 
2 3 3 3 0 3 
5 5 5 2 3 0 
3 5 1 5 
5 2 5 3 
3 1 3 3 
5 5 1 3 
4 5 4 1 
5 3 4 5 
1 3 4 2 2 3 
'''