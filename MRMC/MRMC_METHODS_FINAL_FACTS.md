# MRMC methods facts

Fifteen readers evaluated the same 2,050 cases (1,593 reference-negative and 457 reference-positive), providing 30,750 paired reader-case records and 61,500 condition-level records. Five readers represented each of emergency medicine, foot and ankle surgery, and musculoskeletal radiology. Experience in years was R01: 2, R02: 4, R03: 7, R04: 11, R05: 16, R06: 3, R07: 5, R08: 8, R09: 13, R10: 18, R11: 3, R12: 5, R13: 8, R14: 13, R15: 17.

The prespecified crossover sequence assignment was R01: AB, R02: BA, R03: AB, R04: BA, R05: AB, R06: BA, R07: AB, R08: BA, R09: AB, R10: AB, R11: AB, R12: BA, R13: AB, R14: BA, R15: AB. A denotes unaided reading and B denotes AI-assisted reading. A 6-week washout separated periods; period follows each reader's sequence. The reader interface recorded a binary stability decision and a 5-point instability confidence score in each condition. The assisted records also contain adoption of the model opinion and the interaction pattern. Recorded binary decisions and the separately recorded model predictions define operating metrics.

Reader-averaged AUROCs and paired differences were analyzed using the iMRMC package, using U-statistic estimates with BDG variance and degrees-of-freedom inference. The implementation calls `iMRMC::doIMRMC()` with scores oriented toward instability.

Operating analyses use binomial logit GLMMs for correctness: sensitivity is restricted to reference-positive cases, specificity to reference-negative cases, and accuracy uses all cases.

`correct ~ condition + period + sequence + (1 | reader_id) + (1 | case_id)`

The secondary accuracy model jointly includes specialty and experience, with experience standardized by the sample SD across the 15 distinct readers:

`correct ~ condition * (specialty + experience_sd) + period + sequence + (1 | reader_id) + (1 | case_id)`

Condition-by-specialty interaction uses a joint two-degree-of-freedom Wald test. Experience interaction is linear per one SD. A condition-by-period term is algebraically aliased in the full AB/BA parameterization.

The exploratory safety analysis stratifies by correctness of the recorded SyndNet prediction:

`correct ~ condition * model_correct + period + sequence + specialty + experience_sd + (1 | reader_id) + (1 | case_id)`

The GLMMs use crossed reader and case random intercepts, Laplace likelihood (`nAGQ=1`), and the `bobyqa` optimizer. Population-standardized probabilities average the empirical covariate distribution in the relevant analysis population, specialty, or model-correctness stratum. Normal random intercepts are integrated with 40-point Gaussian quadrature. Differences use fixed-effect delta-method Wald intervals and two-sided normal P values; arm intervals use a logit-transformed delta method. These approximate intervals condition on fitted variance components and do not propagate uncertainty in estimated random-intercept variances.

Individual-reader AUROC intervals use 10,000 paired reference-class-stratified case bootstrap resamples, percentile quantiles (type 7), and seed 20261011. Multinomial resampling of discrete score-pair counts has the same distribution as paired case resampling. These intervals condition on each reader. SyndNet alone is a fixed benchmark with reference-class-stratified case bootstrap intervals.

Software: R version 4.6.1 (2026-06-24 ucrt). Packages: iMRMC 2.1.0, lme4 2.0-6, Matrix 1.7-5, statmod 1.5.2, readxl 1.5.0.1, renv 1.2.4, writexl 2.0.1. Exact session information, installed package versions, and the environment lock accompany the analysis.
