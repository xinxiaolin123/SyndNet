if(.Platform$OS.type=="windows") invisible(Sys.setlocale("LC_CTYPE","English_United States.utf8"))
root <- normalizePath(Sys.getenv("SYNDNET_MRMC_ROOT","."),mustWork=TRUE)
result <- read.csv(file.path(root,"03_results","primary_imrmc_Ustat.csv"))
r <- read.csv(file.path(root,"03_results","reader_descriptive_auc.csv"))
expected <- read.csv(file.path(root,"04_QC","expected_auc_fingerprint.csv"))
observed <- data.frame(metric=c("unaided","assisted","difference"),observed=c(mean(r$unaided),mean(r$assisted),mean(r$difference)))
observed$expected <- expected$expected[match(observed$metric,expected$metric)]
observed$pass <- abs(observed$observed-observed$expected)<1e-8
write.csv(observed,file.path(root,"04_QC","MRMC_AUROC_FINGERPRINT_QC.csv"),row.names=FALSE)
stopifnot(all(observed$pass))
checks <- data.frame(check=c("primary_reader_mean_unaided","primary_reader_mean_assisted","primary_difference","condition_records"),pass=c(abs(result$AUCA[result$modalityA=="unaided"&result$modalityB=="NO_MOD"]-mean(r$unaided))<1e-12,abs(result$AUCA[result$modalityA=="AI-assisted"&result$modalityB=="NO_MOD"]-mean(r$assisted))<1e-12,abs(result$AUCAminusAUCB[result$modalityA=="AI-assisted"&result$modalityB=="unaided"]-mean(r$difference))<1e-12,nrow(read.csv(file.path(root,"01_input","MRMC_REAL_LONG_FINAL.csv")))==61500))
write.csv(checks,file.path(root,"04_QC","MRMC_POST_ANALYSIS_CHECKS.csv"),row.names=FALSE)
stopifnot(all(checks$pass))
print(observed);print(checks)
