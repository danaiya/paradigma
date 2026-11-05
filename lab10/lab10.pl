% ==========================================
% Лабораторная работа 10. Логическое программирование в SWI Prolog
% ==========================================

% --- База знаний: студенты, курсы, завершенные курсы и пререквизиты ---

student(aida).
student(miras).
student(dana).
student(timur).
% Задание 1: добавлено имя нового студента
student(aliya).

course(programming_1).
course(programming_2).
course(data_structures).
course(databases).
course(artificial_intelligence).
course(machine_learning).

completed(aida, programming_1).
completed(aida, programming_2).
completed(aida, data_structures).
completed(aida, databases).

completed(miras, programming_1).
completed(miras, databases).

completed(dana, programming_1).
completed(dana, programming_2).
completed(dana, data_structures).

completed(timur, programming_1).

% Задание 1: факты об освоенных дисциплинах для aliya
completed(aliya, programming_1).
completed(aliya, programming_2).

requires(programming_2, programming_1).
requires(data_structures, programming_2).
requires(artificial_intelligence, data_structures).
requires(artificial_intelligence, databases).
requires(machine_learning, artificial_intelligence).


% --- Задание 2: Правила и составные цели ---

ai_candidate(Student) :-
    completed(Student, data_structures),
    completed(Student, databases).

% Правило strong_student/1: студент считается подготовленным, если освоил programming_2 и data_structures
strong_student(Student) :-
    completed(Student, programming_2),
    completed(Student, data_structures).


% --- Задание 4: Проверка непосредственного допуска ---

missing_direct(Student, Course, Prerequisite) :-
    student(Student),
    requires(Course, Prerequisite),
    \+ completed(Student, Prerequisite).

immediate_eligible(Student, Course) :-
    student(Student),
    course(Course),
    \+ missing_direct(Student, Course, _).


% --- Задание 5: Транзитивные пререквизиты ---

prerequisite(Course, Prerequisite) :-
    requires(Course, Prerequisite).
prerequisite(Course, Prerequisite) :-
    requires(Course, Intermediate),
    prerequisite(Intermediate, Prerequisite).


% --- Задание 6: Полный допуск и список недостающих курсов ---

missing_all(Student, Course, Missing) :-
    setof(P,
          (prerequisite(Course, P), \+ completed(Student, P)),
          Missing), !.
missing_all(_, _, []).

eligible(Student, Course) :-
    student(Student),
    course(Course),
    missing_all(Student, Course, []).


% --- Задание 7: Безопасность рекурсии (защита от циклов) ---

safe_prerequisite(Course, Prerequisite) :-
    safe_prerequisite(Course, Prerequisite, [Course]).

safe_prerequisite(Course, Prerequisite, _) :-
    requires(Course, Prerequisite).
safe_prerequisite(Course, Prerequisite, Visited) :-
    requires(Course, Next),
    \+ memberchk(Next, Visited),
    safe_prerequisite(Next, Prerequisite, [Next | Visited]).


% --- Задание 8: Интегрированный отчёт ---

recommendation(Student, Course, eligible, []) :-
    eligible(Student, Course).
recommendation(Student, Course, missing, Missing) :-
    missing_all(Student, Course, Missing),
    Missing \= [].