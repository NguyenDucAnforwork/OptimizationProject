N, M, K = map(int, input().split())    # do an - giao vien - hoi dong
a, b, c, d, e, f = map(int, input().split())   # e: similarity between 2 thesis; f: simi between a thesis and a teacher

x = [0 for _ in range(N+1)]
y = [0 for _ in range(M+1)]

s = []

for i in range(N):
    s.append(list(map(int, input().split())))

g = []

for i in range(N):
    g.append(list(map(int, input().split())))

t = [0 for _ in range(N)]
t = list(map(int, input().split()))
t.insert(0,0)

x = [0 for _ in range(N+1)]
y = [0 for _ in range(M+1)]

group_of_student = [[] for _ in range(M+1)]

student_per_jury = b
teacher_per_jury = -1
result_x, result_y, solution = [], [], []
lst_of_teacher_in_each_jury = [[] for i in range(K+1)]
visited = [0 for _ in range(K+1)]

# group_of_student[m] (m là giáo viên chạy từ 1 đến M) là danh sách sinh viên mà giáo viên m hướng dẫn. 
# LƯU Ý: Phần tử cuối của mỗi list group_of_student[m] là m - đánh dấu cho giáo viên hướng dẫn
# Ta sẽ cố gắng xếp giáo viên mà hướng dẫn nhiều sinh viên nhất trước
def group_and_sort(t):
    global group_of_student
    for i in range(1, N+1):
        group_of_student[t[i]].append(i)
    # add index of teacher at the end
    for i in range(1, M+1):
        group_of_student[i].append(i)
    group_of_student.sort(key=lambda x:len(x), reverse=True)
    group_of_student = group_of_student[:-1]   # tại số cuối là [] ý; mình cắt nó đi bỏ lên đầu cho nó đúng thứ tự thôi
    group_of_student.insert(0, [])
    return group_of_student

# Hàm này để check ràng buộc về số giáo viên trong 1 hội đồng thôi
def check_for_num_teacher_in_a_jury(y):
    for i in range(1, K+1):
        count = int(sum([1 if num == i else 0 for num in y]))
        if count < c or count > d:
            return False
    return True

# Hàm này check ràng buộc xem giáo viên có ở trong cùng hội đồng có sinh viên mình hướng dẫn hay không thôi
# index_of_thesis_in_each_jury[k] chứa danh sách sinh viên trong hội đồng k; địng nghĩa tương tự với index_of_teacher_in_each_jury
def check(x,y):
    index_of_thesis_in_each_jury = [[] for _ in range(K+1)]
    index_of_teacher_in_each_jury = [[] for _ in range(K+1)]

    for i in range(1, N+1):
        index_of_thesis_in_each_jury[x[i]].append(i)

    for i in range(1, M+1):
        index_of_teacher_in_each_jury[y[i]].append(i)

    for i in range(1, K+1):
        for j in range(1, len(t)):
            if j in index_of_thesis_in_each_jury[i] and (t[j]) in index_of_teacher_in_each_jury[i]:
                return False
    return True

# LƯU Ý: lst_of_teacher_in_each_jury[k] chứa danh sách giáo viên trong hội đồng k; với phần tử cuối của mỗi danh sách là k - đánh dấu hội đồng
# Ở đây ta loại teacher nào vi phạm ràng buộc ra khỏi hội đồng cũ và cho vào hội đồng mới
def remove_and_update(teacher, old_jury, new_jury):
    for lst in lst_of_teacher_in_each_jury:
        if len(lst) > 0:
            if lst[-1] == old_jury:
                lst.remove(teacher)
            if lst[-1] == new_jury:
                lst.insert(0, teacher)

def pick_jury_for_teacher(teacher, their_conducted_student):
    for jury in range(1, K+1):
        for i in range(len(lst_of_teacher_in_each_jury)):
            if len(lst_of_teacher_in_each_jury[i]) > 0:
                if lst_of_teacher_in_each_jury[i][-1] == jury:   # hnhu list này được sort rồi nên mới phải tìm list chứa phần tử jury hsy
                    index_jury = i
        
        # tìm xem có hội đồng nào còn slot để chuyển giáo viên sang, 
        # nhưng phải check var trước bằng cách xem có học sinh nào mà giáo viên đấy hướng dẫn trong hội đồng không
        # list visited nhằm đảm bảo trong trường hợp có nhiều giáo viên vi phạm ràng buộc; mỗi hội đồng ta chuyển 1 giáo viên/ 1 số giáo viên sang thôi  
        if len(lst_of_teacher_in_each_jury[index_jury]) < d+1 and visited[jury] == 0 and jury != y[teacher]:
            old_jury = y[teacher]
            check = True

            for student in their_conducted_student:
                if x[student] == jury:
                    check = False
                    break

            if check:
                remove_and_update(teacher, old_jury, new_jury=jury)
                visited[jury] = 1
                return jury

# đầu tiên ta tìm danh sách những giáo viên thừa ra trong tất cả các hội đồng
# sau đó điều chỉnh giáo viên, cho vào hội đồng khác. Cách điều chỉnh có nói ở trên
def adjust_the_final_result():
    failed_teacher = []
    for list_of_teacher in lst_of_teacher_in_each_jury:
        if len(list_of_teacher[:-1]) > d:
            for teacher in (list_of_teacher[:(len(list_of_teacher) - d-1)]):
                failed_teacher.append(teacher)

    for teacher in failed_teacher:
        their_conducted_student = []
        for students in group_of_student:
            if len(students) > 0:
                if students[-1] == teacher:
                    their_conducted_student = students[:-1]
                    break
        new_jury = pick_jury_for_teacher(teacher, their_conducted_student)
        y[teacher] = new_jury
    return failed_teacher

# tính kết quả cuối cùng, lưu ý là độ tương đồng giữa 2 đồ án i và j CHỈ ĐƯỢC TÍNH 1 LẦN THÔI
def calculate_score(x, y, K):
    score = 0
    index_of_the_in_each_jury = [[] for _ in range(K+1)]
    index_of_teacher_in_each_jury = [[] for _ in range(K+1)]

    for i in range(1, N+1):
        index_of_the_in_each_jury[x[i]].append(i)

    for i in range(1, M+1):
        index_of_teacher_in_each_jury[y[i]].append(i)

    for j in range(1, K+1):
        for i in range(len(index_of_the_in_each_jury[j])):
            if i == 0:
                continue
            for k in range(i-1):
                score = score + s[index_of_the_in_each_jury[j][i]-1][index_of_the_in_each_jury[j][k]-1]    # we dont count it 2 times

        for thesis in index_of_the_in_each_jury[j]:
            for teacher in index_of_teacher_in_each_jury[j]:
                score += g[thesis-1][teacher-1]
    return score

# đại loại là ta xết giáo viên hướng dẫn nhiều sv nhất; nhét sinh viên vào các hội đồng; nhét xong thì đánh dấu hội đồng vừa nhét xong => nhét giáo viên vào hội đồng tiếp theo
# ngoài ra có một trường hợp khá củ chuối, đó là khi giáo viên không hướng dẫn sinh viên vào :) nên phải xử lý riêng bằng list lacked_teacher
# Để tăng xác suất tìm ra lời giải feasbile thì khởi tạo lời giải ở các điểm bắt đầu khác nhau
# khởi tạo một lời giải theo kiểu: 1 1 1 2 2 2 3 3 3 (các học sinh liên tiếp được xếp vào 1 hội đồng cho đến khi đạt tới con số trung bình thì thôi)
def group_by_numerical_constraint(group_of_student):
    global student_per_jury, teacher_per_jury, x, y, K
    for index in range(1, K+1):
        if len(result_x) > 0:
            break
        mark_jury = index
        for teacher in range(1, M+1):
            if student_per_jury == 0:
                mark_jury = (mark_jury + 1) if mark_jury < K else 1
                student_per_jury = int(N/K)

            for student in group_of_student[teacher][:-1]:
                teacher_index = group_of_student[teacher][-1]
                if student_per_jury > 0:
                    x[student] = mark_jury
                    student_per_jury -= 1
                else:
                    mark_jury = (mark_jury + 1) if mark_jury < K else 1
                    x[student] = mark_jury
                    student_per_jury = int(N/K)
                    student_per_jury -= 1

            y[teacher_index] = 1 if mark_jury == K else mark_jury + 1
        
        lacked_teacher = []
        for i in range(1, M+1):
            if y[i] == 0:
                lacked_teacher.append(i)
        temp_teacher = 0

        # find the index of teacher in each jury
        for i in range(1, M+1):
            lst_of_teacher_in_each_jury[y[i]].append(i)

        # add index of jury at the end
        index_of_jury_with_no_teacher = []

        # jury with no teacher
        for i in range(1, K+1):
            if len(lst_of_teacher_in_each_jury[i]) == 0:
                index_of_jury_with_no_teacher.append(i)
            lst_of_teacher_in_each_jury[i].append(i)
        lst_of_teacher_in_each_jury.sort(key=lambda x:len(x))

        # check if there a teacher who doesn't conduct any student. Với những giáo viên này thì cứ nhét đều vào các hội đồng thôi => nhằm tránh vi phạm ràng buộc về số giáo viên trong hội đồng
        if len(lacked_teacher) > 0:
            temp_teacher = 0
            lst_of_jury_with_descending_num_of_teacher = [lst_of_teacher_in_each_jury[i][-1] for i in range(1, len(lst_of_teacher_in_each_jury))]

            while temp_teacher < len(lacked_teacher):
                y[lacked_teacher[temp_teacher]] = lst_of_jury_with_descending_num_of_teacher[temp_teacher]
                temp_teacher += 1

        if len(result_x) == 0:
            if not check_for_num_teacher_in_a_jury(y):
                adjust_the_final_result()
                for jury in index_of_jury_with_no_teacher:
                    Old_jury = lst_of_teacher_in_each_jury[-1][-1]
                    cur_teacher = lst_of_teacher_in_each_jury[-1][0]
                    New_jury = jury
                    remove_and_update(cur_teacher, Old_jury, jury)
                    y[cur_teacher] = New_jury

            if check(x,y):
                result_x.append(x)
                result_y.append(y)
                print(N)
                for i in range(1, N+1):
                    print(x[i], end=" ")
                print()
                print(M)
                for i in range(1, M+1):
                    print(y[i], end=" ")
                print()

if __name__=="__main__":
    group_and_sort(t)
    group_by_numerical_constraint(group_of_student)


'''
COMMENT:
- Ở đây chưa có hàm check điều kiện với e,f (nhưng mà kệ mẹ đi)
- Xử lý ràng buộc về số giáo viên bị vi phạm hơi liều; trong test case 
mà cận trên đúng bằng giá trị trung bình; tức mỗi hội đồng BẮT BUỘC CÓ ĐỦ số 
giáo viên thì rất dễ "đứt" (đề xuất hướng: dịch chuyển random; thêm một mảng đánh dấu xem hội đồng đầy chưa)
- Có những cách khác để khởi tạo lời giải nhưng qua thực nghiệm thì 
cách làm đơn giản đã mang lại hiệu quả cao rồi 
'''
