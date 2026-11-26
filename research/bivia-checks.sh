#!/bin/bash
B=~/workspace/custom-connectors/custom.bivia/bin/bivia_decide.py
OUT=research/bivia-results.txt
: > "$OUT"
run() {
  echo "=== $1 ===" | tee -a "$OUT"
  python3 "$B" boolean --question "$2" --state "$3" --mode deep --allow-abstain 2>&1 | tee -a "$OUT"
  echo | tee -a "$OUT"
}
run "Q1 Dhaka 17000" \
  "Bangladesh's garment minimum wage was set at Tk17,000 (not Tk17,500) on 25 November 2026, a 36 percent rise from Tk12,500." \
  "TBS News and Daily Star report the board set Tk17,000 after a 4-2 vote, announced after 4am Wednesday 25 Nov by chairman Syed Azad Subhani; 17000/12500 = 1.36 exactly. An early Reuters wire said 17,500, which would be +40 percent."
run "Q2 Tariffs 14 partners 20pct China" \
  "On 25 November 2026 the USTR proposed tariffs on 14 trading partners, with China facing a proposed 20 percent excess-capacity tariff on top of existing duties." \
  "Reuters 25 Nov: USTR proposed tariffs on 14 partners after an 8-month Section 301 probe into 16; China highest at proposed 20 percent excess-capacity tariff on top of about 25 percent first-term tariffs; EU/Japan/South Korea/Taiwan capped 15 percent; Malaysia 19 percent; Mexico and Norway not proposed."
run "Q3 KOSPI close" \
  "South Korea's KOSPI index closed at 4,697.51 on 25 November 2026, down 6.16 percent." \
  "WSJ/Reuters: KOSPI closed 4,697.51, down 308.52 points (-6.16 percent, reported as -6.2 percent), lowest close since Jan 13; Samsung -9.87 percent, SK hynix -11.05 percent; prior day +6.32 percent to 5,006.03."
run "Q4 Shenzhou first foreigner" \
  "Shenzhou-24 launched on 25 November 2026 carrying Muhammad Zeeshan Ali of Pakistan, the first foreigner to visit China's Tiangong space station." \
  "Xinhua/CMSA: launch 25 Nov 2026 00:18:52 UTC from Jiuquan; docked Tianhe 03:56 UTC; crew Tang Hongbo, Wu Yi, Muhammad Zeeshan Ali (Pakistan payload specialist, ex-PAF pilot); first foreigner to Tiangong, first Pakistani in orbit."
run "Q5 Ofgem 26pct" \
  "Ofgem announced on 25 November 2026 that the UK energy price cap will rise about 26 percent from 1 January, typical dual-fuel bill GBP 1,723 to GBP 2,166." \
  "Ofgem announced Wed 25 Nov: cap +25.7 percent from 1 Jan; typical dual-fuel direct debit 1,723 to 2,166 pounds (+443/yr); electricity 26.32p to 32.69p/kWh, gas 7.97p to 10.96p/kWh; highest since Q2 2023."
run "Q6 Hamas chief killed 24 Nov" \
  "Hamas internal security chief Naeem Abu Nahel was killed in an Israeli strike on Tuesday 24 November 2026, not on 25 November." \
  "Reuters dateline Nov 24: Israeli airstrike killed Naeem Abu Nahel, director of Hamas internal security apparatus, in western Gaza City on Tuesday; BBC, Times of Israel, Algemeiner all dated 24 Nov; at least seven Palestinians killed that day."
run "Q7 Zaporizhzhia strike 24 Nov" \
  "The Russian strike on Zaporizhzhia that killed two people and injured dozens happened in the early hours of Tuesday 24 November 2026, not on 25 November." \
  "AP via Nagaland Post (Kyiv, Nov 24): Russian nighttime attack on Zaporizhzhia killed two civilians and wounded 44, officials said Tuesday; 112.ua: early hours of November 24; explosions about 4am in Voznesenivskyi district."
run "Q8 Farmgate panel voided 25 Nov" \
  "On 25 November 2026 the Western Cape High Court set aside the 2022 Section 89 independent panel report on President Ramaphosa's Farmgate matter as unlawful in its entirety." \
  "Reuters/Business Day 25 Nov: full bench (Mabindla-Boqwana, Sher, Mayosi, unanimous) set aside the panel report chaired by ex-Chief Justice Sandile Ngcobo as unlawful; parliamentary impeachment process falls away; case concerns 2020 theft of about 580,000 dollars cash at Phala Phala farm."
echo "ALL DONE" | tee -a "$OUT"
