from ortools.linear_solver import pywraplp

# declare given variables
N, M, K = map(int, input().split())
a, b, c, d, e, f = map(int, input().split())
s, g, t = {}, {}, [0 for _ in range(N+1)]
temp_lst = []
CONST = 10000

# input the data
for i in range(N):
    temp_lst = list(map(int, input().split()))
    for j in range(N):
        s[i+1, j+1] = temp_lst[j]

for i in range(N):
    temp_lst = list(map(int, input().split()))
    for j in range(M):
        g[i+1, j+1] = temp_lst[j]

temp_lst = list(map(int, input().split()))
for i in range(1, N+1):
    t[i] = temp_lst[i-1]

# create a solver
solver = pywraplp.Solver.CreateSolver("SCIP")

# declare variable to fit the model
x, y = [0 for _ in range(N+1)], [0 for _ in range(M+1)]
for i in range(1, N+1):
    x[i] = solver.IntVar(1, K, "")

for i in range(1, M+1):
    y[i] = solver.IntVar(1, K, "")

# X[n][k], Y[m][k] to determine whether student n, teacher m is in the jury k or not
X,Y = {}, {}
for i in range(1, N+1):
    for j in range(1, K+1):
        X[i, j] = solver.IntVar(0,1,"")

for i in range(1, M+1):
    for j in range(1, K+1):
        Y[i, j] = solver.IntVar(0,1,"")

# Z[n1][n2][k] is to determine if student n1 and n2 are in the same jury k or not
Z, T = {}, {}
for i in range(1, N+1):
    for j in range(1, N+1):
        for k in range(1, K+1):
            Z[i, j, k] = solver.IntVar(0,1,"")

# T[n][m][k] is to determine if student n and teacher m are in the same jury k or not
for i in range(1, N+1):
    for j in range(1, M+1):
        for k in range(1, K+1):
            T[i, j, k] = solver.IntVar(0,1,"")

# Add constraints. For each jury k, the number of student >= a, <= b; the number of teacher >= c, <= d
for k in range(1, K+1):
    solver.Add(solver.Sum([X[i, k] for i in range(1, N+1)]) >= a)
    solver.Add(solver.Sum([X[i, k] for i in range(1, N+1)]) <= b)

for k in range(1, K+1):
    solver.Add(solver.Sum([Y[i, k] for i in range(1, M+1)]) >= c)
    solver.Add(solver.Sum([Y[i, k] for i in range(1, M+1)]) <= d)

for k in range(1, K+1):
    for i in range(1, N+1):
        for j in range(1, N+1):
            solver.Add(CONST * (1 - Z[i,j,k]) + Z[i,j,k] >= e)

for k in range(1, K+1):
    for n in range(1, N+1):
        for m in range(1, M+1):
            solver.Add(CONST * (1 - T[n, m, k]) + T[n, m, k] >= f)
            
# X[n][k] = 1 <=> x[n] = k. 
for n in range(1, N+1):
    for k in range(1, K+1):
        solver.Add(x[n] + CONST * (1 - X[n, k]) >= k)
        solver.Add(x[n] - CONST * (1 - X[n, k]) <= k)

# Y[m][k] = 1 <=> y[m] = k
for m in range(1, M+1):
    for k in range(1, K+1):
        solver.Add(y[m] + CONST * (1 - Y[m, k]) >= k)
        solver.Add(y[m] - CONST * (1 - Y[m, k]) <= k)

# for each jury k, X[n,k] = 1 => Y[t[n], k] = 0 and vice versa
for n in range(1, N+1):
    for k in range(1, K+1):
        solver.Add(X[n, k] + Y[t[n], k] <= 1)

# T[n, t[n], k] = 0 for all k
# for k in range(1, K+1):
#     solver.Add(T[n, t[n], k] <= 0)

# X[n1,k] = X[n2, k] = 1 => Z[n1,n2, k] = 1
for n1 in range(1, N+1):
    for n2 in range(1, N+1):
        if n2 != n1:
            for k in range(1, K+1):
                solver.Add((X[n1, k] + X[n2, k]) <= Z[n1,n2,k] + 1)
                solver.Add(X[n1, k] + X[n2, k] >= 3 * Z[n1, n2, k] - 1)

# X[n, k] = Y[m, k] = 1 => T[n, m, k] = 1
for n in range(1, N+1):
    for m in range(1, M+1):
        for k in range(1, K+1):
            solver.Add((X[n, k] + Y[m, k]) <= 1 + T[n,m,k])
            solver.Add((X[n, k] + Y[m, k]) >= 3*T[n,m,k] - 1)

# objective function
objective = solver.Objective()
for n1 in range(1, N+1):
    for n2 in range(1, N+1):
        for k in range(1, K+1):
            objective.SetCoefficient(Z[n1,n2,k], s[n1,n2])

for n in range(1, N+1):
    for m in range(1, M+1):
        for k in range(1, K+1):
            objective.SetCoefficient(T[n,m,k], g[n,m]*2)

objective.SetMaximization()

# display the solution
status = solver.Solve()

if status == solver.OPTIMAL or status == solver.FEASIBLE:
    print(f"The optimal value is {objective.Value() / 2}")
    print("\nThe solution:")
    print(N)
    for n in range(1, N+1):
        print(x[n].solution_value(), end=" ")
    print()
    print(M)
    for m in range(1, M+1):
        print(y[m].solution_value(), end=" ")
    print()

    # print("X[n, k], Y[m,k]")

    # for n in range(1, N+1):
    #     for k in range(1, K+1):
    #         print(X[n,k].solution_value(), end=" ")
    #     print()

    # print()

    # for m in range(1, M+1):
    #     for k in range(1, K+1):
    #         print(Y[m,k].solution_value(), end=" ")
    #     print()

    # print("Z[n1, n2, k], T[n, m, k]")
    
    # for k in range(1, K+1):
    #     for n1 in range(1, N+1):
    #         for n2 in range(1, N+1):
    #             print(Z[n1,n2,k].solution_value(), end=" ")
    #         print()
    #     print()

    # print()

    # for k in range(1, K+1):
    #         for n in range(1, N+1):
    #             for m in range(1, M+1):
    #                 print(T[n,m,k].solution_value(), end=" ")
    #             print()
    #         print()

else:
    print("No solution")

''' input:
- Hình như SCIP chạy chậm hơn SAT
- set thời gian chạy tầm 1 phút là đủ mang lại kết quả tốt rồi
'''
