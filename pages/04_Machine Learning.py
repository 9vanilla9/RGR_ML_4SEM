import streamlit as st
import pandas as pd
import pickle
import os
#import lightgbm

# Установка заголовка страницы
st.set_page_config(page_title="Quality of Wine", layout="centered")
st.title("Прогнозирование оценки качества вина")

st.markdown("Загрузите CSV-файл или введите данные вручную для получения прогноза.")

# Путь к папке с моделями
models_dir = "models"

# Проверка наличия папки models
if not os.path.exists(models_dir):
    st.error(f"Папка с моделями не найдена: {models_dir}")
else:
    # Получаем список всех .pkl файлов
    model_files = [f for f in os.listdir(models_dir) if f.endswith('.pkl')]

    if not model_files:
        st.warning("В папке models нет моделей (.pkl файлов)")
    else:
        # Выбор модели пользователем
        selected_model = st.selectbox("Выберите модель", model_files)

        # Загрузка модели
        model_path = os.path.join(models_dir, selected_model)
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        st.success(f"Модель '{selected_model}' загружена")

        # Разделение на две колонки: загрузка файла и ручной ввод
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Загрузите CSV-файл")
            uploaded_file = st.file_uploader("Выберите CSV-файл", type=["csv"])
            if uploaded_file:
                try:
                    df_uploaded = pd.read_csv(uploaded_file)
                    st.success("Файл успешно загружен!")
                    st.write("Предпросмотр данных:")
                    st.dataframe(df_uploaded.head())

                    # Предсказание по файлу
                    if 'quality' in df_uploaded.columns:
                        X = df_uploaded.drop(columns=['quality'])
                    else:
                        X = df_uploaded

                    predictions = model.predict(X)
                    df_uploaded['predicted_quality'] = predictions
                    st.download_button(
                        label="Скачать с предсказаниями",
                        data=df_uploaded.to_csv(index=False),
                        file_name="predictions.csv",
                        mime="text/csv"
                    )
                except Exception as e:
                    st.error(f"Ошибка при обработке файла: {e}")

        with col2:
            st.subheader("Введите данные вручную")

            fixed_acidity_count = st.number_input("Концентрация нелетучих кислот", min_value=4.8, max_value=9.6, value=7.9)
            volatile_acidity_count = st.number_input("Концентрация уксусной кислоты", min_value=0.1, max_value=0.65, value=0.6)
            citric_acid_count = st.number_input("Содержание лимонной кислоты", min_value=0.06, max_value=0.57, value=0.06)
            residual_sugar_count = st.number_input("Количество сахара, г/л", min_value=1.0, max_value=17.2, value=1.6)
            chlorides_count = st.number_input("Содержание соли", min_value=0.01, max_value=0.8, value=0.7)
            free_sulfur_dioxide_count = st.number_input("Свободный SO₂, мг/л", min_value=2.0, max_value=77.0, value=15.0)
            total_sulfur_dioxide_count = st.number_input("Общий SO₂, мг/л", min_value=6.0, max_value=251.0, value=59.0)
            density_count = st.number_input("Плотность", min_value=0.98, max_value=1.0, value=0.99)
            pH_count = st.number_input("Количество pH", min_value=2.8, max_value=3.6, value=3.3)
            sulphates_count = st.number_input("Концентрация солей серной кислоты", min_value=0.22, max_value=0.82, value=0.46)
            alcohol_count = st.number_input("Количество алкоголя", min_value=8.4, max_value=14.0, value=9.4)

            if st.button("🔮 Получить предсказание"):
                input_data = pd.DataFrame({
                    'fixed acidity': [fixed_acidity_count],
                    'volatile acidity': [volatile_acidity_count],
                    'citric acid': [citric_acid_count],
                    'residual sugar': [residual_sugar_count],
                    'chlorides': [chlorides_count],
                    'free_sulfur_dioxide': [free_sulfur_dioxide_count],
                    'total_sulfur_dioxide': [total_sulfur_dioxide_count],
                    'density': [density_count],
                    'pH': [pH_count],
                    'sulphates': [sulphates_count],
                    'alcohol': [alcohol_count]
                })

                prediction = model.predict(input_data)[0]
                st.success(f"⏳ Прогнозируемое качество вина: **{prediction} баллов.**")

st.markdown("---")
st.markdown("© 2025 — ML Trip Predictor App")