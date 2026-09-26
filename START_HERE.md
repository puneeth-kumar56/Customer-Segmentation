# 🚀 START HERE

Welcome to the Customer Segmentation Analysis Project!

This guide will help you get started in 3 minutes.

## ⚡ Quick Start (3 minutes)

### 1️⃣ Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

**All set?** → Skip to step 3

### 2️⃣ Run the Analysis (1 minute)

```bash
python run.py
```

Watch the magic happen! ✨

### 3️⃣ View Results (1 minute)

Open the `plots/` folder to see your visualizations:
- 📊 Customer distributions
- 🔥 Feature correlations  
- 📈 Cluster visualization
- 💰 Spending by segment

## 📚 Which Document Should I Read?

### 🏃 "I just want to run it!"
→ Read: **QUICKSTART.md**

### 🤔 "What's in this project?"
→ Read: **README.md** (complete guide)

### 🔬 "I want to customize the analysis"
→ Read: **ADVANCED_USAGE.md**

### 📋 "Show me file-by-file breakdown"
→ Read: **PROJECT_MANIFEST.md**

### 📺 "What will the output look like?"
→ Read: **EXAMPLE_OUTPUT.md**

## 📂 Project Structure

```
customer_segmentation_project/
├── segmentation.py          ← Main code (run this)
├── run.py                   ← Entry point script
├── requirements.txt         ← Python packages
├── data/
│   └── customer_segmentation.csv  ← Your input data
└── plots/                   ← Output visualizations (created after running)
```

## ✅ Before You Start

Make sure you have:
- ✓ Python 3.9 or higher (`python --version`)
- ✓ CSV file in `data/` folder (already included)
- ✓ Terminal or command prompt
- ✓ VS Code (optional, but recommended)

## 🎯 What You'll Learn

This project teaches:
- Data preprocessing & feature engineering
- Exploratory data analysis (EDA)
- K-Means clustering
- Principal Component Analysis (PCA)
- Data visualization
- Customer segmentation insights

## 🎓 For Different Experience Levels

### Beginner
1. Run `python run.py`
2. View the 6 generated plots
3. Read the console output for insights
4. Explore `data/customer_segmentation_with_clusters.csv` in Excel

### Intermediate
1. Read `README.md` for understanding
2. Modify clustering parameters in `segmentation.py`
3. Run analysis with different settings
4. Create additional visualizations

### Advanced
1. Read `ADVANCED_USAGE.md`
2. Use individual functions for custom workflows
3. Implement additional clustering algorithms
4. Extend analysis with RFM, CLV, etc.

## 🐛 Troubleshooting

**Q: "ImportError: No module named 'pandas'"**
A: Run `pip install -r requirements.txt`

**Q: "FileNotFoundError: customer_segmentation.csv"**
A: Make sure CSV is in the `data/` folder

**Q: "Takes too long to run"**
A: It should take 5-10 seconds. Check your system resources.

For more help → See README.md or QUICKSTART.md

## 🚀 Ready?

### Option A: Terminal
```bash
pip install -r requirements.txt
python run.py
```

### Option B: VS Code
1. Open project folder in VS Code
2. Open `run.py`
3. Click "Run" button (▶️)

### Option C: Python Shell
```python
from segmentation import main
main()
```

## 📊 What to Expect

- **Runtime**: 5-10 seconds
- **Output**: 6 PNG files + 1 CSV file
- **Console**: Detailed step-by-step progress
- **Insights**: Customer segment profiles and recommendations

## 📈 Example: After Running

```
Cluster 0 (Premium): 425 customers
├─ Avg Age: 54 years
├─ Avg Income: $88,362
├─ Avg Spend: $1,246
└─ Strategy: VIP treatment & exclusive offers

Cluster 1 (Mid-Tier): 532 customers
├─ Avg Age: 50 years
├─ Avg Income: $65,234
├─ Avg Spend: $654
└─ Strategy: Loyalty programs & personalization

Cluster 2 (Budget): 758 customers
├─ Avg Age: 50 years
├─ Avg Income: $42,156
├─ Avg Spend: $246
└─ Strategy: Discounts & value bundles

Cluster 3 (Core): 525 customers
├─ Avg Age: 52 years
├─ Avg Income: $58,234
├─ Avg Spend: $512
└─ Strategy: Growth & upselling
```

## 🎁 Bonus: Use Cases

After segmentation, you can:
- 📧 Send targeted marketing campaigns
- 💰 Optimize pricing by segment
- 📦 Recommend products per cluster
- 🎯 Allocate sales resources efficiently
- 📊 Forecast revenue by segment
- 👥 Improve customer retention

## 💡 Pro Tips

1. **Customize features**: Edit `preprocess_data()` function
2. **Change cluster count**: Modify `max_k` parameter
3. **Add visualizations**: Create new plotting functions
4. **Export results**: CSV file ready for Excel/BI tools
5. **Rerun anytime**: Results are reproducible

## 📞 Need Help?

- Check the **README.md** for comprehensive documentation
- Review **EXAMPLE_OUTPUT.md** to see typical results
- Read inline comments in **segmentation.py**
- Try **ADVANCED_USAGE.md** for customization

## 🎉 You're Ready!

```bash
pip install -r requirements.txt && python run.py
```

Enjoy your customer segmentation journey! 🚀📊

---

**Next Steps**: Choose a guide above and dive in!

**Estimated Time**: 
- Setup: 2 minutes
- Running Analysis: 5-10 minutes
- Reviewing Results: 10-15 minutes
- Total: ~20 minutes to first insights

---

Questions? See **README.md** → Troubleshooting section
