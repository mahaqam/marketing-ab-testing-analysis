-- Experiment summaries. Load marketing_AB.csv into marketing_ab.
SELECT test_group, COUNT(*) users,
 SUM(CASE WHEN converted THEN 1 ELSE 0 END) conversions,
 ROUND(100.0*AVG(CASE WHEN converted THEN 1.0 ELSE 0.0 END),3) conversion_pct
FROM marketing_ab GROUP BY test_group ORDER BY test_group;

SELECT most_ads_day,test_group,COUNT(*) users,
 ROUND(100.0*AVG(CASE WHEN converted THEN 1.0 ELSE 0.0 END),3) conversion_pct
FROM marketing_ab GROUP BY most_ads_day,test_group ORDER BY most_ads_day,test_group;

SELECT most_ads_hour,test_group,COUNT(*) users,
 ROUND(100.0*AVG(CASE WHEN converted THEN 1.0 ELSE 0.0 END),3) conversion_pct
FROM marketing_ab GROUP BY most_ads_hour,test_group ORDER BY most_ads_hour,test_group;
