import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("user_study.csv")

# Calculate average accuracy per condition
accuracy = df.groupby('condition')[['correct_task1','correct_task2','correct_task3']].mean().mean(axis=1)
time = df.groupby('condition')['time_sec'].mean()
load = df.groupby('condition')['cognitive_load'].mean()

conditions = ['A (Manual)', 'B (LLM)', 'C (Ours)']
x = np.arange(len(conditions))

fig, axes = plt.subplots(1, 3, figsize=(12, 4))

axes[0].bar(x, accuracy, color=['#e41a1c','#377eb8','#4daf4a'])
axes[0].set_xticks(x)
axes[0].set_xticklabels(conditions)
axes[0].set_ylabel('Accuracy')
axes[0].set_ylim(0,1)
axes[0].set_title('Insight Accuracy')

axes[1].bar(x, time, color=['#e41a1c','#377eb8','#4daf4a'])
axes[1].set_xticks(x)
axes[1].set_xticklabels(conditions)
axes[1].set_ylabel('Time (seconds)')
axes[1].set_title('Completion Time')

axes[2].bar(x, load, color=['#e41a1c','#377eb8','#4daf4a'])
axes[2].set_xticks(x)
axes[2].set_xticklabels(conditions)
axes[2].set_ylabel('Cognitive Load (1-5)')
axes[2].set_title('Mental Effort')

plt.tight_layout()
plt.savefig('user_study_results.png', dpi=150)
print("Saved user_study_results.png successfully.")