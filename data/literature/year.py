import matplotlib.pyplot as plt
import numpy as np

## LONG-TERM SLAM PUBLICATION DATA
lt_years  = [ 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022 ]
lt_counts = [    1,    0,    0,    0,    0,    1,    0,    6,    3,    2,    4,   13,    4,   10,   10,    8,   20,   15,   14,   23,    8 ]

plt.figure()

lt_bars = plt.bar(lt_years, lt_counts,
                  color='tab:blue', edgecolor='black')

lt_bars[-1].set_hatch('///')
lt_bars[-1].set_edgecolor('black')
lt_bars[-1].set_linewidth(1.0)

plt.xlabel(r'year $\rightarrow$')
plt.ylabel(r'#records $\rightarrow$')
plt.title('Number of Included Records in the Review per Year', fontweight='bold')

plt.xticks(lt_years, rotation=45, ha='right')

for bar in lt_bars:
    height = bar.get_height()

    if int(height) > 0:
      plt.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}',
               ha='center', va='bottom')

plt.tight_layout()
plt.savefig('../../latex/figures/literature/year_included-review.eps',
            format='eps', bbox_inches='tight')
plt.show()

## LONG-TERM SLAM VERSUS LONG-TERM + DYNAMIC PUBLICATION DATA (SCOPUS, WOS)
lt_sw_years             = [ 2009, 2010, 2011, 2012, 2013, 2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026 ]
lt_sw_counts_scopus_all = [   12,   13,   16,   13,   32,   22,  38,  39,  36,  48,  64,  55,  76,  77,  72, 106, 113,  21 ]
lt_sw_counts_wos_all    = [   13,    8,    9,   10,   19,   17,  28,  41,  18,  39,  51,  37,  63,  54,  48,  76,  81,   9 ]
lt_sw_counts_scopus_dyn = [    5,    4,    5,    7,    7,    9,  10,   9,  11,  19,  11,  16,  25,  20,  19,  40,  53,   8 ]
lt_sw_counts_wos_dyn    = [    5,    2,    3,    5,    4,    7,   8,  11,   7,  17,   9,  12,  19,  17,  12,  29,  35,   3 ]

# Set up the first figure - "All" query
fig1, ax1 = plt.subplots()

# Bar width and positions
x = np.arange(len(lt_sw_years))
width = 0.35

# First figure: "All" query comparison
bars1_all = ax1.bar(x - width/2, lt_sw_counts_scopus_all, width, label='Scopus',
                    color='tab:orange', edgecolor='black')
bars2_all = ax1.bar(x + width/2, lt_sw_counts_wos_all, width, label='Web of Science',
                    color='tab:blue', edgecolor='black')

# Apply hatched pattern to last bars (2026)
bars1_all[-1].set_hatch('///')
bars1_all[-1].set_linewidth(1.0)
bars2_all[-1].set_hatch('///')
bars2_all[-1].set_linewidth(1.0)

# Add value labels on bars for first figure
for bar in bars1_all:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}',
             ha='center', va='bottom', fontsize=7)

for bar in bars2_all:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}',
             ha='center', va='bottom', fontsize=7)

# Customize first figure
ax1.set_xlabel(r'year $\rightarrow$')
ax1.set_ylabel(r'#records $\rightarrow$')
ax1.set_ylim([0,120])
ax1.set_title('Publications per Year', fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(lt_sw_years, rotation=45, ha='right')
ax1.legend(loc='upper left', frameon=True)

plt.tight_layout()
plt.savefig('../../latex/figures/literature/year_scopus-wos_all.eps',
            format='eps', bbox_inches='tight')
plt.show()

# Set up the second figure - "Dyn" query
fig2, ax2 = plt.subplots()
# Second figure: "Dyn" query comparison
bars1_dyn = ax2.bar(x - width/2, lt_sw_counts_scopus_dyn, width, label='Scopus',
                    color='tab:orange', edgecolor='black')
bars2_dyn = ax2.bar(x + width/2, lt_sw_counts_wos_dyn, width, label='Web of Science',
                    color='tab:blue', edgecolor='black')

# Apply hatched pattern to last bars (2026)
bars1_dyn[-1].set_hatch('///')
bars1_dyn[-1].set_linewidth(1.0)
bars2_dyn[-1].set_hatch('///')
bars2_dyn[-1].set_linewidth(1.0)

# Add value labels on bars for second figure
for bar in bars1_dyn:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}',
             ha='center', va='bottom', fontsize=7)

for bar in bars2_dyn:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}',
             ha='center', va='bottom', fontsize=7)

# Customize second figure
ax2.set_xlabel(r'year $\rightarrow$')
ax2.set_ylabel(r'#records $\rightarrow$')
ax2.set_ylim([0,120])
ax2.set_title('Publications per Year', fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(lt_sw_years, rotation=45, ha='right')
ax2.legend(loc='upper left', frameon=True)

plt.tight_layout()
plt.savefig('../../latex/figures/literature/year_scopus-wos_dyn.eps',
            format='eps', bbox_inches='tight')
plt.show()
