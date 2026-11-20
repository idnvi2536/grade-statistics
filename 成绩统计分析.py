# 项目一：成绩统计分析（成品）
# 用法：把成绩表 students.csv 放在本脚本同一文件夹，Git Bash 里运行：
#      py 成绩统计分析.py
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # 只保存图片、不弹窗
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

base = os.path.dirname(os.path.abspath(__file__))

# ===== 配置：要统计的科目，按你表格里的列名改 =====
SUBJECTS = ['语文', '数学', '英语']

# ---------- 1. 读取 + 清洗 ----------
df = pd.read_csv(os.path.join(base, 'students.csv'))
df = df.dropna(how='all')                      # 删掉整行空白
for col in SUBJECTS:
    df[col] = pd.to_numeric(df[col], errors='coerce')  # 成绩转成数字，转不了的变空

# ---------- 2. 各科统计 ----------
report = []
report.append('===== 成绩统计报告 =====')
report.append(f'班级人数：{len(df)} 人')

for col in SUBJECTS:
    s = df[col].dropna()
    avg = s.mean()
    high, low = s.max(), s.min()
    pass_rate = (s >= 60).mean() * 100       # >=60 算及格
    report.append(
        f'{col}：平均 {avg:.2f}，最高 {high:.0f}，最低 {low:.0f}，及格率 {pass_rate:.1f}%'
    )

# ---------- 3. 总分 + 排名 ----------
df['总分'] = df[SUBJECTS].sum(axis=1)
df = df.sort_values('总分', ascending=False).reset_index(drop=True)
df['名次'] = df.index + 1

report.append('\n===== 总分前 5 名 =====')
for _, row in df.head(5).iterrows():
    report.append(f"第{int(row['名次'])}名 {row['姓名']}：总分 {row['总分']:.0f}")

# ---------- 4. 打印报告 + 保存报告文件 ----------
text = '\n'.join(report)
print(text)
with open(os.path.join(base, '成绩统计报告.txt'), 'w', encoding='utf-8') as f:
    f.write(text + '\n')

# ---------- 5. 画图：各科平均分柱状图 ----------
avg_score = df[SUBJECTS].mean()
avg_score.plot(kind='bar', color=['#4C78A8', '#F58518', '#54A24B'])
plt.title('各科平均分')
plt.ylabel('分数')
plt.ylim(0, 100)
plt.tight_layout()
plt.savefig(os.path.join(base, '各科平均分.png'), dpi=150)

print('\n报告已保存为 成绩统计报告.txt，图已保存为 各科平均分.png')
