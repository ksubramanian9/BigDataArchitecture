# Synthetic Data Generator Configs

This folder contains **60 ready-made JSON configs** for the `generator_template.py` (no external deps).

## How to use
```bash
python generator_template.py --config /path/to/config.json --out ./data.csv --n 500000 --format csv --seed 123 --gzip
```

## Index
- **Agriculture** — Crop yield prediction using soil and weather data → `Agriculture/01_crop_yield_prediction_using_soil_and_weather_data.json`
- **Agriculture** — Precision farming with IoT sensor streams → `Agriculture/02_precision_farming_with_iot_sensor_streams.json`
- **Agriculture** — Market price trend analysis for major crops → `Agriculture/03_market_price_trend_analysis_for_major_crops.json`
- **Agriculture** — Pest/disease outbreak detection via image/IoT feeds → `Agriculture/04_pest_disease_outbreak_detection_via_image_iot_feeds.json`
- **Agriculture** — Irrigation optimization using weather and soil moisture → `Agriculture/05_irrigation_optimization_using_weather_and_soil_moisture.json`
- **Agriculture** — Farm-to-market supply chain analytics → `Agriculture/06_farm_to_market_supply_chain_analytics.json`
- **Healthcare** — Patient readmission risk prediction → `Healthcare/01_patient_readmission_risk_prediction.json`
- **Healthcare** — Real-time epidemic spread monitoring → `Healthcare/02_real_time_epidemic_spread_monitoring.json`
- **Healthcare** — Hospital resource utilization analytics → `Healthcare/03_hospital_resource_utilization_analytics.json`
- **Healthcare** — Medical image metadata lake & analysis → `Healthcare/04_medical_image_metadata_lake_analysis.json`
- **Healthcare** — Wearables IoT patient vitals monitoring → `Healthcare/05_wearables_iot_patient_vitals_monitoring.json`
- **Healthcare** — Drug effectiveness and adverse reaction detection → `Healthcare/06_drug_effectiveness_and_adverse_reaction_detection.json`
- **Finance_Banking** — Card transaction fraud detection → `Finance_Banking/01_card_transaction_fraud_detection.json`
- **Finance_Banking** — Customer segmentation and offers → `Finance_Banking/02_customer_segmentation_and_offers.json`
- **Finance_Banking** — Credit scoring with alternate data → `Finance_Banking/03_credit_scoring_with_alternate_data.json`
- **Finance_Banking** — Real-time transaction anomaly detection → `Finance_Banking/04_real_time_transaction_anomaly_detection.json`
- **Finance_Banking** — Market sentiment vs price movement → `Finance_Banking/05_market_sentiment_vs_price_movement.json`
- **Finance_Banking** — ATM cash demand forecasting → `Finance_Banking/06_atm_cash_demand_forecasting.json`
- **Retail_ECommerce** — Product recommendation events → `Retail_ECommerce/01_product_recommendation_events.json`
- **Retail_ECommerce** — Shopping basket analysis → `Retail_ECommerce/02_shopping_basket_analysis.json`
- **Retail_ECommerce** — Dynamic pricing optimization → `Retail_ECommerce/03_dynamic_pricing_optimization.json`
- **Retail_ECommerce** — Customer churn prediction → `Retail_ECommerce/04_customer_churn_prediction.json`
- **Retail_ECommerce** — Review sentiment analysis → `Retail_ECommerce/05_review_sentiment_analysis.json`
- **Retail_ECommerce** — Supply chain and logistics analytics → `Retail_ECommerce/06_supply_chain_and_logistics_analytics.json`
- **Transportation** — Route optimization for buses → `Transportation/01_route_optimization_for_buses.json`
- **Transportation** — Delay/breakdown detection → `Transportation/02_delay_breakdown_detection.json`
- **Transportation** — Ride demand forecasting → `Transportation/03_ride_demand_forecasting.json`
- **Transportation** — Traffic congestion prediction → `Transportation/04_traffic_congestion_prediction.json`
- **Transportation** — Ticketing revenue leakage analysis → `Transportation/05_ticketing_revenue_leakage_analysis.json`
- **Transportation** — Multi-modal integration analytics → `Transportation/06_multi_modal_integration_analytics.json`
- **Energy_Utilities** — Smart grid load forecasting → `Energy_Utilities/01_smart_grid_load_forecasting.json`
- **Energy_Utilities** — Predictive maintenance of transformers → `Energy_Utilities/02_predictive_maintenance_of_transformers.json`
- **Energy_Utilities** — Energy theft anomaly detection → `Energy_Utilities/03_energy_theft_anomaly_detection.json`
- **Energy_Utilities** — Solar/wind generation forecasting → `Energy_Utilities/04_solar_wind_generation_forecasting.json`
- **Energy_Utilities** — Household consumption patterns → `Energy_Utilities/05_household_consumption_patterns.json`
- **Energy_Utilities** — Dynamic electricity pricing → `Energy_Utilities/06_dynamic_electricity_pricing.json`
- **Telecommunications** — Call drop analysis and network tuning → `Telecommunications/01_call_drop_analysis_and_network_tuning.json`
- **Telecommunications** — Subscriber churn modeling → `Telecommunications/02_subscriber_churn_modeling.json`
- **Telecommunications** — Usage behavior segmentation → `Telecommunications/03_usage_behavior_segmentation.json`
- **Telecommunications** — SIM/identity fraud detection → `Telecommunications/04_sim_identity_fraud_detection.json`
- **Telecommunications** — Real-time network anomaly detection → `Telecommunications/05_real_time_network_anomaly_detection.json`
- **Telecommunications** — Call/data social graph analytics → `Telecommunications/06_call_data_social_graph_analytics.json`
- **Education** — Student performance risk alerts → `Education/01_student_performance_risk_alerts.json`
- **Education** — Adaptive learning recommendations → `Education/02_adaptive_learning_recommendations.json`
- **Education** — MOOC clickstream engagement → `Education/03_mooc_clickstream_engagement.json`
- **Education** — Skill gap analysis from course data → `Education/04_skill_gap_analysis_from_course_data.json`
- **Education** — Placement/job market trend analytics → `Education/05_placement_job_market_trend_analytics.json`
- **Education** — Admin resource allocation optimization → `Education/06_admin_resource_allocation_optimization.json`
- **Social_Media** — Topic sentiment tracking → `Social_Media/01_topic_sentiment_tracking.json`
- **Social_Media** — Fake news/rumor detection → `Social_Media/02_fake_news_rumor_detection.json`
- **Social_Media** — Influencer network analytics → `Social_Media/03_influencer_network_analytics.json`
- **Social_Media** — Video recommendation telemetry → `Social_Media/04_video_recommendation_telemetry.json`
- **Social_Media** — Toxic comment moderation cues → `Social_Media/05_toxic_comment_moderation_cues.json`
- **Social_Media** — User engagement and churn analytics → `Social_Media/06_user_engagement_and_churn_analytics.json`
- **Government_PublicPolicy** — Smart city sensor analytics → `Government_PublicPolicy/01_smart_city_sensor_analytics.json`
- **Government_PublicPolicy** — Crime hotspot prediction → `Government_PublicPolicy/02_crime_hotspot_prediction.json`
- **Government_PublicPolicy** — Tax fraud detection in filings → `Government_PublicPolicy/03_tax_fraud_detection_in_filings.json`
- **Government_PublicPolicy** — Public welfare scheme usage → `Government_PublicPolicy/04_public_welfare_scheme_usage.json`
- **Government_PublicPolicy** — Disaster response analytics → `Government_PublicPolicy/05_disaster_response_analytics.json`
- **Government_PublicPolicy** — Citizen feedback policy sentiment → `Government_PublicPolicy/06_citizen_feedback_policy_sentiment.json`
