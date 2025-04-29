from db_functions import create_resume

# Передается с фронта
user_id = 1
title = "Я крутой специалист, честно-честно"
job_title = "IT-трубочист"
country = "Россия"
city = "Москва"
district = "хз"
min_salary = "200000"
max_salary = "2000000"
work_schedule_working_days = "пн вт ср чт пт"
work_schedule_time_intervals = "8:00 17:00"
experience = "Очень я опытный"
remote_work = False
education = "MIPT"
skills = "C++ python SQL HTML5"

create_resume(user_id, title, job_title, country, city, district, min_salary, max_salary,
              work_schedule_working_days, work_schedule_time_intervals,
              experience, remote_work, education, skills)
# В будущем хорошо бы реализовать загрузку этого резюме на hhru
