# -*- coding: utf-8 -*-
"""Интерактивный дашборд по результатам олимпиады.

Запуск:  streamlit run src/app.py
Дашборд читает очищенный датасет data/olympiad_results_clean.csv.
"""
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

# Пути относительно корня проекта (src/app.py -> ..)
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / 'data'

st.set_page_config(page_title='Дашборд: олимпиада', layout='wide')

# Единая цветовая палитра (как в ноутбуке/презентации)
COLORS = px.colors.qualitative.Set2


@st.cache_data
def load_data():
    path = DATA_DIR / 'olympiad_results_clean.csv'
    if not path.exists():
        st.error(f'Файл не найден: {path}. Сначала выполните ноутбук '
                 f'(notebooks/analysis.ipynb), он создаёт очищенный датасет.')
        st.stop()
    return pd.read_csv(path)


df = load_data()

st.title('📊 Результаты онлайн-олимпиады')
st.caption(f'Источник: {DATA_DIR / "olympiad_results_clean.csv"} '
           f'· {df.shape[0]} прохождений · {df["region"].nunique()} регионов')

# ---- Саидбар: фильтры ----
st.sidebar.header('Фильтры')

regions = sorted(df['region'].unique())
sel_regions = st.sidebar.multiselect('Регионы', regions, default=regions)

grades = sorted(df['grade'].unique())
sel_grades = st.sidebar.multiselect('Классы', grades, default=grades)

devices = sorted(df['device_type'].dropna().unique())
sel_devices = st.sidebar.multiselect('Устройства', devices, default=devices)

# Фильтрация
mask = (
    df['region'].isin(sel_regions) &
    df['grade'].isin(sel_grades) &
    df['device_type'].isin(sel_devices)
)
sub = df[mask]

if sub.empty:
    st.warning('По выбранным фильтрам нет данных. Расширьте фильтры.')
    st.stop()

# ---- KPI ----
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric('Участников', f'{len(sub):,}')
c2.metric('Средний балл', f"{sub['total_score_calc'].mean():.2f}")
c3.metric('Доля правильных', f"{sub['correct_rate'].mean()*100:.1f}%")
c4.metric('Среднее время на задачу', f"{sub['avg_task_time'].mean():.0f} сек")
c5.metric('Средняя длительность', f"{sub['duration_sec'].mean()/60:.0f} мин")

# ---- Графики (plotly) ----
left, right = st.columns(2)

with left:
    st.subheader('Распределение итогового балла')
    score_counts = sub['total_score_calc'].value_counts().sort_index()
    fig = px.bar(x=score_counts.index, y=score_counts.values,
                 labels={'x': 'Итоговый балл', 'y': 'Число участников'},
                 color_discrete_sequence=[COLORS[0]])
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, width='stretch')

with right:
    st.subheader('Средний балл по классам')
    grade_order = sorted(sub['grade'].unique())
    by_grade = sub.groupby('grade')['total_score_calc'].mean().reindex(grade_order)
    fig = px.line(x=by_grade.index, y=by_grade.values, markers=True,
                  labels={'x': 'Класс', 'y': 'Средний балл (0–12)'},
                  color_discrete_sequence=[COLORS[1]])
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, width='stretch')

left2, right2 = st.columns(2)

# Сложность заданий (доля правильных среди отвечавших)
with left2:
    st.subheader('Сложность заданий')
    task_deets = []
    for i in range(1, 13):
        answered = sub[f'Task_{i}_answer'].notna().sum()
        if answered == 0:
            continue
        task_deets.append({
            'Задание': f'Задание {i}',
            'Доля правильных, %': sub[f'Task_{i}_correct'].sum() / answered * 100,
        })
    task_df = pd.DataFrame(task_deets).sort_values('Доля правильных, %', ascending=False)
    fig = px.bar(task_df, x='Доля правильных, %', y='Задание', orientation='h',
                 color_discrete_sequence=[COLORS[2]])
    fig.update_layout(showlegend=False, yaxis=dict(autorange='reversed'))
    st.plotly_chart(fig, width='stretch')

# Средний балл по регионам
with right2:
    st.subheader('Средний балл по регионам')
    region_mean = sub.groupby('region')['total_score_calc'].mean().sort_values(ascending=False)
    fig = px.bar(x=region_mean.index, y=region_mean.values,
                 labels={'x': 'Регион', 'y': 'Средний балл (0–12)'},
                 color_discrete_sequence=px.colors.qualitative.Vivid)
    fig.add_hline(y=sub['total_score_calc'].mean(), line_dash='dash',
                  line_color='red',
                  annotation_text=f"Среднее: {sub['total_score_calc'].mean():.2f}")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, width='stretch')

# ---- Таблица топ-школ ----
st.subheader('Топ-10 школ по среднему баллу (≥ 5 участников)')
schools = (
    sub.groupby(['region', 'school_number'])
    .agg(Участников=('student_id', 'count'),
         Средний_балл=('total_score_calc', 'mean'))
    .query('Участников >= 5')
    .sort_values('Средний_балл', ascending=False)
    .head(10)
    .round(2)
)
st.dataframe(schools)

# ---- Гистограмма длительности ----
st.subheader('Длительность прохождения')
duration_min = sub['duration_sec'] / 60
fig = px.histogram(x=duration_min, nbins=30,
                   labels={'x': 'Длительность, мин', 'y': 'Число участников'},
                   color_discrete_sequence=[COLORS[0]])
fig.update_layout(showlegend=False)
st.plotly_chart(fig, width='stretch')

st.caption('Дашборд построен на очищенных данных олимпиады. '
           'Фильтры в боковой панели пересчитывают все метрики и графики.')