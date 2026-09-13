import matplotlib.pyplot as plt

# Plot 1 Data (Miss Rates for hmmer)
lru_miss_rates = [33.89, 26.93, 25.94]      # [4-way, 8-way, 16-way]
hawkeye_miss_rates = [37.25, 30.26, 26.91]  # [4-way, 8-way, 16-way]
associativities = [4, 8, 16]

# Plot 2 Data (Miss Rate Reductions at 16-way)
# Calculation: (LRU_miss_rate - Hawkeye_miss_rate) / LRU_miss_rate * 100
reduction_hmmer = -3.71
reduction_mcf = -44.87
reduction_astar = -270.72

benchmarks = ['456.hmmer', '429.mcf', '473.astar']
reductions = [reduction_hmmer, reduction_mcf, reduction_astar]

# PLOT 1: Miss Rate vs Associativity
plt.figure(figsize=(8, 5))
plt.plot(associativities, lru_miss_rates, marker='o', label='LRU', linewidth=2)
plt.plot(associativities, hawkeye_miss_rates, marker='s', label='Hawkeye', linewidth=2)

plt.title('LLC Miss Rate vs. Associativity (456.hmmer-191B)')
plt.xlabel('LLC Associativity (Ways)')
plt.ylabel('LLC Miss Rate (%)')
plt.xticks([4, 8, 16])
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.savefig('plot1_associativity.pdf', format='pdf', bbox_inches='tight')
plt.close()

# PLOT 2: Miss Rate Reduction over LRU
plt.figure(figsize=(8, 5))
bars = plt.bar(benchmarks, reductions, color='skyblue', edgecolor='black')

plt.title('LLC Miss-Rate Reduction over LRU (16-way, 2MB)')
plt.ylabel('Miss-Rate Reduction (%)')
plt.grid(axis='y', linestyle='--', alpha=0.7)

for bar in bars:
    yval = bar.get_height()
    offset = 5 if yval >= 0 else -15 
    plt.annotate(f'{yval:.1f}%',
                 xy=(bar.get_x() + bar.get_width() / 2, yval),
                 xytext=(0, offset),  
                 textcoords="offset points",
                 ha='center', va='bottom' if yval >= 0 else 'top')

plt.axhline(0, color='black', linewidth=1)
plt.ylim(-320, 20)
plt.savefig('plot2_reduction.pdf', format='pdf', bbox_inches='tight')
plt.close()