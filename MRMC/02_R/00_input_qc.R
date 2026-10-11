if(.Platform$OS.type=="windows") invisible(Sys.setlocale("LC_CTYPE","English_United States.utf8"))
root <- normalizePath(Sys.getenv("SYNDNET_MRMC_ROOT","."),mustWork=TRUE)
w <- read.csv(file.path(root,"01_input","MRMC_REAL_READER_CASE_FINAL.csv"),stringsAsFactors=FALSE)
pred <- read.csv(file.path(root,"01_input","MRMC_LOCKED_CASE_PREDICTIONS.csv"),stringsAsFactors=FALSE)
assignment <- setNames(c("AB","BA","AB","BA","AB","BA","AB","BA","AB","AB","AB","BA","AB","BA","AB"),sprintf("R%02d",1:15))
metadata <- unique(w[c("reader_id","specialty","experience_years","sequence")])
checks <- c(readers=length(unique(w$reader_id))==15,cases=length(unique(w$case_id))==2050,records=nrow(w)==30750,unique_keys=!anyDuplicated(w[c("reader_id","case_id")]),truth_complete=!anyNA(w$truth),truth_binary=all(w$truth %in% 0:1),scores_complete=!anyNA(w$reader_score_unaided) && !anyNA(w$reader_score_assisted),score_range=all(w$reader_score_unaided %in% 1:5 & w$reader_score_assisted %in% 1:5),decisions_binary=all(w$reader_decision_unaided %in% 0:1 & w$reader_decision_assisted %in% 0:1),cases_per_reader=all(table(w$reader_id)==2050),sequence_locked=all(w$sequence==assignment[w$reader_id]),metadata_consistent=nrow(metadata)==15,specialty_balance=all(table(metadata$specialty)==5),prediction_cases=nrow(pred)==2050 && !anyDuplicated(pred$case_id),prediction_labels=all(pred$syndnet_predicted_label %in% c("stable","unstable")),case_truth_consistent=nrow(unique(w[c("case_id","truth")]))==2050,probability_consistent=nrow(unique(w[c("case_id","syndnet_probability")]))==2050,probability_range=all(is.finite(w$syndnet_probability)&w$syndnet_probability>=0&w$syndnet_probability<=1))
qc <- data.frame(check=names(checks),pass=unname(checks))
write.csv(qc,file.path(root,"04_QC","MRMC_INPUT_QC.csv"),row.names=FALSE)
if(!all(checks)) stop("Structural input validation failed.")
a <- w; a$condition <- "unaided"; a$period <- ifelse(a$sequence=="AB",1,2); a$score <- a$reader_score_unaided; a$decision <- a$reader_decision_unaided
b <- w; b$condition <- "AI-assisted"; b$period <- ifelse(b$sequence=="AB",2,1); b$score <- b$reader_score_assisted; b$decision <- b$reader_decision_assisted
long <- rbind(a,b); stopifnot(nrow(long)==61500)
write.csv(long,file.path(root,"01_input","MRMC_REAL_LONG_FINAL.csv"),row.names=FALSE)
auc <- function(y,s) {n1 <- sum(y==1); n0 <- sum(y==0); (sum(rank(s,ties.method="average")[y==1])-n1*(n1+1)/2)/(n1*n0)}
r <- do.call(rbind,lapply(split(w,w$reader_id),function(z) data.frame(reader_id=z$reader_id[1],unaided=auc(z$truth,z$reader_score_unaided),assisted=auc(z$truth,z$reader_score_assisted))))
r$difference <- r$assisted-r$unaided
write.csv(r,file.path(root,"03_results","reader_descriptive_auc.csv"),row.names=FALSE)
write.csv(metadata[order(metadata$reader_id),],file.path(root,"03_results","reader_metadata.csv"),row.names=FALSE)
print(qc)
