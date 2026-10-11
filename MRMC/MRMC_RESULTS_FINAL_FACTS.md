# MRMC results facts

Estimates below are the final reader analysis. Operating probabilities and differences are population-standardized; differences are assisted minus unaided.

- AUROC: unaided 0.7871765744 (95% CI 0.7503512504 to 0.8240018984); AI-assisted 0.9701425776 (95% CI 0.9585273890 to 0.9817577663); difference 0.1829660033 (95% CI 0.1537314786 to 0.2122005279) AUROC units; P=1.605160449e-11.
- sensitivity: unaided 65.9498929826 (95% CI 61.3289815426 to 70.2861623514); AI-assisted 92.5507080950 (95% CI 90.5911598709 to 94.1285980219); difference 26.6008151124 (95% CI 23.6408670047 to 29.5607632201) percentage points; P=1.922280382e-69.
- specificity: unaided 90.1825679511 (95% CI 89.1073369914 to 91.1621881700); AI-assisted 92.1963771614 (95% CI 91.2781278038 to 93.0253391021); difference 2.0138092104 (95% CI 1.6394713756 to 2.3881470451) percentage points; P=5.418366327e-26.
- accuracy: unaided 85.0629625684 (95% CI 83.7643254869 to 86.2747463048); AI-assisted 92.1712820536 (95% CI 91.3277413749 to 92.9391161010); difference 7.1083194852 (95% CI 6.5280359322 to 7.6886030382) percentage points; P=2.237573879e-127.

Exploratory safety analysis (accuracies in percent; differences in percentage points):

- SyndNet incorrect: unaided 85.4686363015 (95% CI 81.6978409907 to 88.5712152078); AI-assisted 74.3914550454 (95% CI 69.4434161223 to 78.7830571719); difference -11.0771812561 (95% CI -13.1379435340 to -9.0164189783); P=5.935455701e-26.
- SyndNet correct: unaided 85.1077513381 (95% CI 83.9776215188 to 86.1712945211); AI-assisted 93.4638217757 (95% CI 92.8084185810 to 94.0633157000); difference 8.3560704376 (95% CI 7.7584257722 to 8.9537151030); P=2.48665512e-165.

Secondary crossover accuracy analysis:

- Period: log-odds coefficient -0.0213071897 (95% CI -0.0909030208 to 0.0482886414); P=0.5484696014; not statistically significant.
- Sequence: log-odds coefficient 0.1129408819 (95% CI -0.0100126769 to 0.2358944408); P=0.07180459319; not statistically significant.
- Experience interaction: log-odds coefficient 0.0306820630 (95% CI -0.0409499962 to 0.1023141221); P=0.4011838973; not statistically significant.
- Specialty interaction: joint Wald chi-square 17.4711991739, df=2, P=0.000160759743; statistically significant.
- Emergency medicine: unaided 81.8139144300 (95% CI 80.4253162779 to 83.1246764691)%; AI-assisted 90.9005812091 (95% CI 89.9836485434 to 91.7412785460)%; difference 9.0866667791 (95% CI 8.2823116510 to 9.8910219072) percentage points; P=1.262850504e-108.
- Foot and ankle surgery: unaided 86.5313864640 (95% CI 85.3613405575 to 87.6214740107)%; AI-assisted 92.5095251894 (95% CI 91.6997530375 to 93.2461145869)%; difference 5.9781387254 (95% CI 5.2895185672 to 6.6667588837) percentage points; P=6.347146498e-65.
- Musculoskeletal radiology: unaided 86.8505559010 (95% CI 85.6971877885 to 87.9240232682)%; AI-assisted 92.9877274697 (95% CI 92.2112241388 to 93.6921127986)%; difference 6.1371715687 (95% CI 5.4448076508 to 6.8295354867) percentage points; P=1.314800621e-67.

Individual-reader unaided AUROC ranged from 0.6718472914 to 0.8622165354; AI-assisted AUROC ranged from 0.9226141173 to 0.9919732253. All 15 reader identifiers, specialties, experience values, sequences, point estimates, and bootstrap intervals are provided in `03_results/publication_tableS9.csv`.
