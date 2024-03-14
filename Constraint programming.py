from ortools.sat.python import cp_model

def main():
    model = cp_model.CpModel()
    
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

    # declare variable to fit the model
    x, y = [0 for _ in range(N+1)], [0 for _ in range(M+1)]
    for i in range(1, N+1):
        x[i] = model.NewIntVar(1, K, "")

    for i in range(1, M+1):
        y[i] = model.NewIntVar(1, K, "")

    # X[n][k], Y[m][k] to determine whether student n, teacher m is in the jury k or not
    X,Y = {}, {}
    for i in range(1, N+1):
        for j in range(1, K+1):
            X[i, j] = model.NewIntVar(0,1,"")

    for i in range(1, M+1):
        for j in range(1, K+1):
            Y[i, j] = model.NewIntVar(0,1,"")

    # Z[n1][n2][k] is to determine if student n1 and n2 are in the same jury k or not
    Z, T = {}, {}
    for i in range(1, N+1):
        for j in range(1, N+1):
            for k in range(1, K+1):
                Z[i, j, k] = model.NewIntVar(0,1,"")

    # T[n][m][k] is to determine if student n and teacher m are in the same jury k or not
    for i in range(1, N+1):
        for j in range(1, M+1):
            for k in range(1, K+1):
                T[i, j, k] = model.NewIntVar(0,1,"")

    # Add constraints. For each jury k, the number of student >= a, <= b; the number of teacher >= c, <= d
    for k in range(1, K+1):
        model.Add(sum([X[i, k] for i in range(1, N+1)]) >= a)
        model.Add(sum([X[i, k] for i in range(1, N+1)]) <= b)

    for k in range(1, K+1):
        model.Add(sum([Y[i, k] for i in range(1, M+1)]) >= c)
        model.Add(sum([Y[i, k] for i in range(1, M+1)]) <= d)

    # X[n][k] = 1 <=> x[n] = k. 
    for n in range(1, N+1):
        for k in range(1, K+1):
            model.Add(x[n] + CONST * (1 - X[n, k]) >= k)
            model.Add(x[n] - CONST * (1 - X[n, k]) <= k)

    # Y[m][k] = 1 <=> y[m] = k
    for m in range(1, M+1):
        for k in range(1, K+1):
            model.Add(y[m] + CONST * (1 - Y[m, k]) >= k)
            model.Add(y[m] - CONST * (1 - Y[m, k]) <= k)

    for k in range(1, K+1):
        for i in range(1, N+1):
            for j in range(1, N+1):
                model.Add(CONST * (1 - Z[i,j,k]) + Z[i,j,k] >= e)

    for k in range(1, K+1):
        for n in range(1, N+1):
            for m in range(1, M+1):
                model.Add(CONST * (1 - T[n, m, k]) + T[n, m, k] >= f)

    # for each jury k, X[n,k] = 1 => Y[t[n], k] = 0 and vice versa
    for n in range(1, N+1):
        for k in range(1, K+1):
            model.Add(X[n, k] + Y[t[n], k] <= 1)

    # X[n1,k] = X[n2, k] = 1 => Z[n1,n2, k] = 1
    for n1 in range(1, N+1):
        for n2 in range(1, N+1):
            if n2 != n1:
                for k in range(1, K+1):
                    model.Add((X[n1, k] + X[n2, k]) <= Z[n1,n2,k] + 1)
                    model.Add(X[n1, k] + X[n2, k] >= 3 * Z[n1, n2, k] - 1)

    # X[n, k] = Y[m, k] = 1 => T[n, m, k] = 1
    for n in range(1, N+1):
        for m in range(1, M+1):
            for k in range(1, K+1):
                model.Add((X[n, k] + Y[m, k]) <= 1 + T[n,m,k])
                model.Add((X[n, k] + Y[m, k]) >= 3*T[n,m,k] - 1)

    # objective function
    objective = model.NewIntVar(0, 100000, "")
    for n1 in range(1, N+1):
        for n2 in range(1, N+1):
            for k in range(1, K+1):
                objective += s[n1, n2] / 2 * Z[n1, n2, k]

    for n in range(1, N+1):
        for m in range(1, M+1):
            for k in range(1, K+1):
                objective += g[n, m] * T[n, m, k]


    model.Maximize(objective)

    # solves the model
    solver = cp_model.CpSolver()
    # Sets a time limit of 10 seconds.
    solver.parameters.max_time_in_seconds = 60.0

    status = solver.Solve(model)

    # print the solution
    # print the solution
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f"The feasible value is {solver.ObjectiveValue() - 100000}")
        print("\nThe solution:")
        print(N)
        for n in range(1, N+1):
            print(solver.Value(x[n]), end=" ")
        print()
        print(M)
        for m in range(1, M+1):
            print(solver.Value(y[m]), end=" ")
        print()

if __name__ == "__main__":
    main()