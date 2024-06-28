# StockAnaylsis Scraper

- Financial Statements Supported:
  - Income Statement (Annual & Quarterly)
  - Balance Sheet (Annual & Quarterly)
  - Cash Flow Statement (Annual & Quarterly)
  - Custom Ratio Statement (Annual & Quarterly)

---

### Setup

1. Clone git repository: `https://github.com/PrimalFinance/StockAnalysisScraper.git`
1. Configure the "config.json" file.

```
    {
        "chrome_driver_path": "D:\\PATH TO CHROME DRIVER\\chromedriver.exe",
        "data_export_path": "D:\\PATH TO EXPORT DATA\\Statements"
    }

```

3. Install the projects requirements with `pip install -r requirements.txt`

---

### Instructions

- Create a class instance. For this example we will be using **AAPL**.

```
    s = StockAnalysis("AAPL")
```

###### Income Statement

- **NOTE** When getting any financial statement such as `get_income_statement("q")`, if no local data exists it will be scraped and saved locally.

```
    s.get_income_statement("q")

    # Output

    ~AAPL/Quarter/income_statement.csv

                            2023-04-01 2023-07-01 2023-09-30 2023-12-30 2024-03-30
index
Revenue                         94,836     81,797     89,498    119,575     90,753
Revenue Growth (YoY)            -2.51%     -1.40%     -0.72%      2.07%     -4.31%
Cost of Revenue                 52,860     45,384     49,071     64,720     48,482
Gross Profit                    41,976     36,413     40,427     54,855     42,271
Selling, General & Admin         6,201      5,973      6,151      6,786      6,468
Research & Development           7,457      7,442      7,307      7,696      7,903
......
Dividend Per Share               0.230      0.240      0.240      0.240      0.240
Dividend Growth                  4.55%      4.35%      4.35%      4.35%      4.35%
Gross Margin                    44.26%     44.52%     45.17%     45.87%     46.58%
Operating Margin                29.86%     28.12%     30.13%     33.76%     30.74%
Profit Margin                   25.48%     24.31%     25.65%     28.36%     26.04%
Free Cash Flow Margin           27.04%     29.69%     21.72%     31.36%     22.80%
Effective Tax Rate              14.88%     12.55%     14.97%     15.89%     15.76%
EBITDA                          31,280     26,783     30,653     43,171     30,894
EBITDA Margin                   32.98%     32.74%     34.25%     36.10%     34.04%
Depreciation & Amortization      2,898      3,052      2,653      2,848      2,836
EBIT                            28,382     23,731     28,000     40,323     28,058
EBIT Margin                     29.93%     29.01%     31.29%     33.72%     30.92%

```

###### Balance Sheet

```
    s.get_balance_sheet("q")

    # Output

    ~AAPL/Quarter/balance_sheet.csv

                            2023-04-01 2023-07-01 2023-09-30 2023-12-30 2024-03-30
index
Cash & Equivalents              24,687     28,408     29,965     40,760     32,695
Short-Term Investments          31,185     34,074     31,590     32,340     34,455
Cash & Cash Equivalents        166,333    166,543    162,099    172,575    162,337
Cash Growth                    -13.70%     -7.12%     -4.15%      4.31%     -2.40%
Receivables                     35,899     39,186     60,985     50,102     41,150
Inventory                        7,482      7,351      6,331      6,511      6,232
......
Total Liabilities              270,002    274,764    290,437    279,414    263,217
Total Debt                     109,615    109,280    111,088    108,040    104,590
Debt Growth                     -8.64%     -8.70%     -7.48%     -2.76%     -4.58%
Retained Earnings                4,336      1,408       -214      8,242      4,339
Comprehensive Income           -11,746    -11,801    -11,452     -9,378     -8,960
Shareholders' Equity            62,158     60,274     62,146     74,100     74,194
Net Cash / Debt                 56,718     57,263     51,011     64,535     57,747
Net Cash / Debt Growth         -22.04%     -3.95%      4.02%     18.76%      1.81%
Net Cash Per Share                3.58       3.63       3.25       4.14       3.73
Working Capital                 -7,162     -2,304     -1,742      9,719      4,594
Book Value Per Share              3.94       3.84       3.98       4.78       4.82

```

###### Cash Flow

```
    s.get_cash_flow("q")

    # Output

    ~AAPL/Quarter/cash_flow.csv

                            2023-04-01 2023-07-01 2023-09-30 2023-12-30 2024-03-30
index
Net Income                      24,160     19,881     22,956     33,916     23,636
Depreciation & Amortization      2,898      3,052      2,653      2,848      2,836
Share-Based Compensation         2,686      2,617      2,625      2,997      2,964
Other Operating Activities      -1,184        830     -6,636        134     -6,746
Operating Cash Flow             28,560     26,380     21,598     39,895     22,690
Operating Cash Flow Growth       1.40%     15.24%    -10.48%     17.32%    -20.55%
Capital Expenditures            -2,916     -2,093     -2,163     -2,392     -1,996
Acquisitions                         0          0          0          0          0
Change in Investments            5,341      3,036      5,141      4,603      2,131
Other Investing Activities        -106       -506       -584       -284       -445
Investing Cash Flow              2,319        437      2,394      1,927       -310
Dividends Paid                  -3,650     -3,849     -3,758     -3,825     -3,710
Share Issuance / Repurchase    -19,594    -17,478    -21,003    -20,139    -23,205
Debt Issued / Paid              -1,996       -283      1,993     -3,984     -3,148
Other Financing Activities        -484     -2,438       -385     -2,637       -370
Financing Cash Flow            -25,724    -24,048    -23,153    -30,585    -30,433
Net Cash Flow                    5,155      2,769        839     11,237     -8,053
Free Cash Flow                  25,644     24,287     19,435     37,503     20,694
Free Cash Flow Growth           -0.03%     16.82%     -6.73%     24.11%    -19.30%
Free Cash Flow Margin           27.04%     29.69%     21.72%     31.36%     22.80%
Free Cash Flow Per Share          1.62       1.55       1.25       2.42       1.34

```

###### Ratios

```
    s.get_ratios("q")

    # Output

    ~AAPL/Quarter/ratios.csv

                        2023-04-01 2023-07-01 2023-09-30 2023-12-30 2024-03-30    Current
index
Market Capitalization     2,609,039  3,050,896  2,676,737  2,994,371  2,647,974  3,283,031
Market Cap Growth            -8.50%     33.06%     10.72%     44.87%      1.49%          -
Enterprise Value          2,552,321  2,993,633  2,625,726  2,929,836  2,590,227  3,225,284
PE Ratio                      27.66      32.20      27.60      29.67      26.38      33.30
PS Ratio                       6.78       7.95       6.98       7.76       6.94       8.60
PB Ratio                      41.97      50.62      43.07      40.41      35.69      44.25
P/FCF Ratio                   26.76      30.21      26.88      28.02      25.98      32.21
P/OCF Ratio                   23.81      26.98      24.21      25.72      23.95      29.69
Debt / Equity Ratio            1.76       1.81       1.79       1.46       1.41       1.41
Quick Ratio                    0.76       0.81       0.84       0.92       0.87       0.87
Current Ratio                  0.94       0.98       0.99       1.07       1.04       1.04
Interest Coverage                 -      23.78      27.94          -          -      60.06
Return on Capital (ROIC)     56.95%     55.19%     56.31%     56.27%     55.51%     56.22%
Dividend Yield                0.60%      0.50%      0.50%      0.50%      0.60%      0.47%
Payout Ratio                 15.00%     18.90%     16.30%     11.00%     15.70%     15.55%
Buyback Yield / Dilution      3.39%      3.00%      2.77%      2.38%      2.41%      2.41%
Total Shareholder Return      3.99%      3.50%      3.27%      2.88%      3.01%      2.88%

```
