Vanguard Digital Interface A/B Testing Project

Project Overview

This project was conducted to analyze the impact of a new user interface (UI) design for Vanguard's online client process. The main goal was to determine whether the new UI, featuring in-context prompts, improves user engagement and completion rates compared to the existing design.

The project specifically focused on two groups:

•	Control Group: Clients using the old interface.

•	Test Group: Clients using the new interface with enhanced prompts.

Key metrics such as completion rates, logons vs calls and time spent on each step were analyzed to evaluate the effectiveness of the new interface.

Data Sources

The data used for this analysis included the following columns:

•	client_id: Unique ID for each client.

•	visitor_id: Unique ID for each visitor.

•	visit_id: Unique ID for each session.

•	process_step: Stage of the process the client is currently in.

•	date_time: Timestamp of the event.

•	variation: Whether the client was in the Control or Test group.

•	tenure_year, tenure_month: Client’s tenure with Vanguard.

•	age, gender, balance: Client demographic and financial details.

•	calls_6_month, logons_6_month: Interaction metrics (calls and logons) over the past 6 months.

Methodology

1. Data Cleaning and Processing

•	Missing and incomplete data entries were cleaned to ensure accurate analysis.

•	Duplicates were removed, and session data was aggregated to avoid over-counting client interactions.

•	Process steps were analyzed based on the timestamps and were segmented by age, gender, and other demographics.

2. Hypothesis Testing

Several key hypotheses were tested using statistical methods:

•	Completion Rates:

o	H0: There is no significant difference in completion rates between the Test and Control groups.

o	H1: The Test group has a significantly higher completion rate.

o	Result: The Test group showed a 9.45% increase in completion rates (p-value: 1.4e-187), supporting the alternative hypothesis.

•	Logons vs Calls:

o	H0: There is no significant difference in logon-to-call ratio between the Test and Control groups.

o	H1: The Test group shows a higher logon-to-call ratio, indicating greater independence.

o	Result: The Test group had significantly more logons and fewer calls (p-value: 0.0009), indicating better engagement and user independence.

•	Time Spent on Each Step:

o	H0: There is no significant difference in time spent on each process step between the Test and Control groups.

o	H1: The Test group spends less time on each step compared to the Control group.

o	Result: Although the time spent on individual steps was similar, the total completion time was slightly higher for the Test group.

Key Findings

•	Completion Rate Improvement: The Test group saw a 9.45% improvement in completion rates, proving the effectiveness of the new UI.

•	Increased Independence: The Test group demonstrated greater independence, with more logons and fewer calls to customer support.

•	Time Spent: The total time spent completing the process was slightly higher for the Test group, which suggests users are still adjusting to the new layout.

Visualization
To better understand the data, several visualizations were created using Tableau:

•	Logons vs Calls by Group: A line chart showing the number of logons and calls over time for both groups.

•	Process Step Analysis: A bar chart displaying the drop-off points in the process by age segment and group.

•	Balance Distribution: A comparison of users' balance distribution across the Control and Test groups.

Challenges & Learnings

•	Handling Multi-Session Data: Managing multiple sessions per client was challenging. Session-based metrics were calculated carefully to avoid duplication.

•	Selecting Appropriate Statistical Tests: The correct hypothesis tests were chosen to ensure reliable insights. This was crucial in proving the impact of the new UI.

•	Time-Consuming Visualization Setup: Creating effective dashboards in Tableau took time but was crucial in presenting data insights clearly.

Contributing Contributions are welcome! Feel free to fork the repository and submit a pull request if you'd like to make improvements or fix issues.
presentation here: https://docs.google.com/presentation/d/1QU2aALBVmMp50K6Pf4-QNitBAM85_o0OSCamA4cT57w/edit#slide=id.gb190eedfe6_0_2
