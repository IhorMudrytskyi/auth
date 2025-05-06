import psycopg2
import streamlit as st

connection = psycopg2.connect(
    host = st.secrets["psql"]["host"],
    user = st.secrets["psql"]["user"],
    database = st.secrets["psql"]["database"],
    password = st.secrets["psql"]["password"],
    port = st.secrets["psql"]["port"]
)

connection.autocommit = True

cursor = connection.cursor()

tab = st.tabs(["Увійти", "Зареєструватися"])

with tab[0]:
    auth_login = st.text_input("Логін").replace(" ", "")
    auth_password = st.text_input("Пароль", type = "password").replace(" ", "")
    if st.button("Увійти"):
        cursor.execute("select login, password from auth where login = %s and password = %s;",(auth_login, auth_password))
        auth_result = cursor.fetchone()
        if auth_result:
            st.success("Ви успішно авторизувались!")
            st.header("Дані користувача: ")
            cursor.execute("select user_info.* from user_info join auth on user_info.id = auth.id where auth.login = %s and auth.password = %s;",(auth_login, auth_password))
            info_result = cursor.fetchone()
            if info_result:
                st.text(f"Ім'я: {info_result[1]}")
                st.text(f"Прізвище: {info_result[2]}")
                st.text(f"Номер телефону: {info_result[3]}")
                st.text(f"Електронна пошта: {info_result[4]}")
        else:
            st.warning("Невірно введені логін чи пароль!")

with tab[1]:
    reg_first_name = st.text_input("Ім'я ").replace(" ", "")               
    reg_last_name = st.text_input("Прізвище ").replace(" ", "")               
    reg_phone_number = st.text_input("Номер телефону ").replace(" ", "")               
    reg_email = st.text_input("Електронна пошта ").replace(" ", "")               
    reg_login = st.text_input("Логін ").replace(" ", "")               
    reg_password = st.text_input("Пароль ", type="password").replace(" ", "")               
    if st.button("Створити акаунт"):
        cursor.execute("select login from auth where login = %s;",(reg_login,))
        login_result = cursor.fetchone()
        if login_result:
            st.warning("Користувач з таким логіном вже існує!")
        else:
            cursor.execute("select email from user_info where email = %s;",(reg_email,))
            email_result = cursor.fetchone()
            if email_result:
                st.warning("Користувач з такою електронною поштою вже існує!")
            else:
                cursor.execute("insert into auth(login, password) values (%s, %s) returning id;",(reg_login, reg_password))
                reg_id = cursor.fetchone()
                cursor.execute("insert into user_info(id, first_name, last_name, phone_number, email) values (%s, %s, %s, %s, %s);",(reg_id, reg_first_name, reg_last_name, reg_phone_number, reg_email))
                st.success("Акаунт успішно створено!")
