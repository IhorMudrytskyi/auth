import psycopg2
import streamlit as st

connection = psycopg2.connect(
    host = st.secrets["psql"]["host"],
    user = st.secrets["psql"]["user"],
    database = st.secrets["psql"]["database"],
    port = st.secrets["psql"]["port"],
    password = st.secrets["psql"]["password"]
)

cursor = connection.cursor()

connection.autocommit = True

tab = st.tabs(["Авторизація", "Реєстрація", "Забули логін/пароль"])

with tab[0]:
    auth_login = st.text_input("Логін").replace(" ", "")
    auth_password = st.text_input("Пароль").replace(" ", "")
    if st.button("Увійти"):
        cursor.execute("select login, password from auth where login = %s and password = %s;",(auth_login, auth_password))
        auth_result = cursor.fetchone()
        if auth_result:
            st.success("Ви успішно авторизувались!")
            st.header("Дані користувача:")
            cursor.execute("select id, first_name, last_name, phone_number, email from user_info join(select id, login, password from auth where login = %s and password = %s) on user_info.id = auth.id;",(auth_login, auth_password))
            info_result = cursor.fetchone()
            st.text(f"Ваше ім'я: {info_result[1]}")
            st.text(f"Ваше прізвище: {info_result[2]}")
            st.text(f"Ваш номер телефону: {info_result[3]}")
            st.text(f"Ваша електронна пошта: {info_result[4]}")
        else:
            st.warning("Логін чи пароль невірний!")

with tab[1]:
    reg_first_name = st.text_input("Ім'я ").replace(" ", "")
    reg_last_name = st.text_input("Прізвище ").replace(" ", "")
    reg_phone_number = st.text_input("Номер телефону ").replace(" ", "")
    reg_email = st.text_input("Електронна пошта ").replace(" ", "")
    reg_login = st.text_input("Логін ").replace(" ", "")
    reg_password = st.text_input("Пароль ").replace(" ", "")
    if st.button("Зареєструватися"):
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
                st.success("Акаунт створено!")

with tab[2]:
    zab_first_name = st.text_input("Ім'я  ").replace(" ", "")
    zab_last_name = st.text_input("Прізвище  ").replace(" ", "")
    zab_phone_number = st.text_input("Номер телефону  ").replace(" ", "")
    zab_email = st.text_input("Електронна пошта  ").replace(" ", "")
    if st.button("Нагадати"):
        cursor.execute("select login, password from auth join(select first_name, last_name, phone_number, email from user_info where first_name = %s and last_name = %s and phone_number = %s and email = %s) on auth.id = user_info.id;",(zab_first_name, zab_last_name, zab_phone_number, zab_email))
        zab_result = cursor.fetchone()
        if zab_result:
            st.header("Дані для авторизації:")
            st.text(f"Логін: {zab_result[0]}")
            st.text(f"Пароль: {zab_result[1]}")
        else:
            st.warning("Користувача з такими даними не знайдено!")
cursor.close()
connection.close()
