import psycopg2
import streamlit as st

connection = psycopg2.connect(
    host = st.secrets["db"]["host"],
    database = st.secrets["db"]["database"],
    user = st.secrets["db"]["user"],
    password = st.secrets["db"]["password"],
    port = st.secrets["db"]["port"]
)
cursor = connection.cursor()
connection.autocommit = True

tab = st.tabs(["Автентицікая", "Реєстрація", "Відновлення паролю", "Зміна паролю"])

with tab[0]:
    st.header("Вхід")
    auth_login = st.text_input("Логін").replace(" ", "")
    auth_password = st.text_input("Пароль", type="password").replace(" ", "")
    if st.button("Увійти"):
        cursor.execute("select * from auth where login = %s and password = %s", (auth_login, auth_password))
        result = cursor.fetchone()
        if result:
            st.success("Вхід успішний")
            cursor.execute("select * from user_info join auth on user_info.id = auth.id where auth_login = %s and auth_password = %s;", (auth_login,))
            info_result = cursor.fetchone()
            st.header("Дані користувача: ")
            st.text(f"Ім'я: {info_result[1]}")
            st.text(f"Прізвище: {info_result[2]}")
            st.text(f"Номер телефону: {info_result[3]}")
            st.text(f"Електронна пошта: {info_result[4]}")

        else:
            st.error("Неправильний логін або пароль!")

with tab[1]:
    st.header("Реєстрація")
    reg_login = st.text_input("Логін ").replace(" ", "")
    reg_password = st.text_input("Пароль ", type="password").replace(" ", "")
    reg_first_name = st.text_input("Ім'я ").replace(" ", "")
    reg_last_name = st.text_input("Прізвище ").replace(" ", "")
    reg_phone_number = st.text_input("Номер телефону ").replace(" ", "")
    reg_email = st.text_input("Електронна пошта ").replace(" ", "")
    if st.button("Зареєструватися"):
        cursor.execute("select login from auth where login = %s", (reg_login,))
        login_result = cursor.fetchone()
        if result:
            st.error("Користувач з таким логіном вже існує!")
        else:
            cursor.execute("select email from user_info where email = %s", (reg_email,))
            email_result = cursor.fetchone()
            if email_result:
                cursor.execute("insert into auth(login, password) values (%s, %s) returning id;", (reg_login, reg_password))
                reg_id = cursor.fetchone()
                cursor.execute("insert into user_info(id, first_name, last_name, phone_number, email) values (%s, %s, %s, %s, %s);", (reg_id, reg_first_name, reg_last_name, reg_phone_number, reg_email))
                st.success("Реєстрація успішна!")

with tab[2]:
    st.header("Відновлення паролю")
    reset_login = st.text_input("Логін   ").replace(" ", "")
    reset_email = st.text_input("Електронна пошта   ").replace(" ", "")
    if st.button("Відновити пароль"):
        cursor.execute("select * from auth where login = %s and email = %s", (reset_login, reset_email))
        result = cursor.fetchone()
        if result:
            new_password = st.text_input("Новий пароль", type="password").replace(" ", "")
            cursor.execute("update auth set password = %s where login = %s", (new_password, reset_login))
            st.success("Пароль успішно змінено!")
        else:
            st.error("Користувача з таким логіном та електронною поштою не існує!")

with tab[3]:
    st.header("Зміна паролю")
    change_login = st.text_input("Логін    ").replace(" ", "")
    change_email = st.text_input("Електронна пошта    ").replace(" ", "")
    if st.button("Змінити пароль"):
        cursor.execute("select * from auth where login = %s and email = %s", (change_login, change_email))
        result = cursor.fetchone()
        if result:
            new_password = st.text_input("Новий пароль", type="password").replace(" ", "")
            cursor.execute("update auth set password = %s where login = %s", (new_password, change_login))
            st.success("Пароль успішно змінено!")
        else:
            st.error("Користувача з таким логіном та електронною поштою не існує!")
