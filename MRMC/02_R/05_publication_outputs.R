if(.Platform$OS.type=="windows") invisible(Sys.setlocale("LC_CTYPE","English_United States.utf8"))
root <- normalizePath(Sys.getenv("SYNDNET_MRMC_ROOT","."),mustWork=TRUE)
read_result <- function(name) read.csv(file.path(root,"03_results",name),check.names=FALSE,stringsAsFactors=FALSE)
w <- read.csv(file.path(root,"01_input","MRMC_REAL_READER_CASE_FINAL.csv"),stringsAsFactors=FALSE)
r <- read_result("reader_descriptive_auc.csv")
metadata <- unique(w[c("reader_id","specialty","experience_years","sequence")])
descriptive <- do.call(rbind,lapply(split(w,w$reader_id),function(z) {
 au <- r[r$reader_id==z$reader_id[1],]
 do.call(rbind,lapply(c("unaided","assisted"),function(condition) {
 score <- z[[paste0("reader_score_",condition)]]; decision <- z[[paste0("reader_decision_",condition)]]
 sensitivity <- mean(decision[z$truth==1]==1); specificity <- mean(decision[z$truth==0]==0)
 data.frame(reader_id=z$reader_id[1],condition=condition,sensitivity=sensitivity,specificity=specificity,accuracy=mean(decision==z$truth),balanced_accuracy=(sensitivity+specificity)/2,accuracy_standardized_42pct=.42*sensitivity+.58*specificity,auc=au[[condition]],score_decision_inconsistency=mean((score<=2 & decision==1)|(score>=4 & decision==0)))
 }))
}))
write.csv(descriptive,file.path(root,"03_results","reader_observed_metrics.csv"),row.names=FALSE)
roc <- do.call(rbind,lapply(split(w,w$reader_id),function(z) do.call(rbind,lapply(c("unaided","assisted"),function(condition) {
 score <- z[[paste0("reader_score_",condition)]]
 data.frame(reader_id=z$reader_id[1],condition=condition,threshold=c(Inf,5:1),fpr=c(0,vapply(5:1,function(k) mean(score[z$truth==0]>=k),numeric(1))),tpr=c(0,vapply(5:1,function(k) mean(score[z$truth==1]>=k),numeric(1))))
}))))
write.csv(roc,file.path(root,"03_results","reader_score_roc.csv"),row.names=FALSE)
pred <- read.csv(file.path(root,"01_input","MRMC_LOCKED_CASE_PREDICTIONS.csv"))
cases <- unique(w[c("case_id","truth","syndnet_probability")]); cases$prediction <- as.integer(pred$syndnet_predicted_label[match(cases$case_id,pred$case_id)]=="unstable")
model <- data.frame(auc={n1<-sum(cases$truth==1);n0<-sum(cases$truth==0);(sum(rank(cases$syndnet_probability)[cases$truth==1])-n1*(n1+1)/2)/(n1*n0)},sensitivity=mean(cases$prediction[cases$truth==1]==1),specificity=mean(cases$prediction[cases$truth==0]==0),accuracy=mean(cases$prediction==cases$truth),brier=mean((cases$syndnet_probability-cases$truth)^2))
write.csv(model,file.path(root,"03_results","locked_model_descriptive.csv"),row.names=FALSE)
# Publication summaries retain inferential estimates and descriptive score-based ROC points.
primary <- read_result("primary_imrmc_Ustat.csv"); op <- read_result("operating_glmm.csv"); safety <- read_result("safety_glmm.csv"); sp <- read_result("secondary_specialty_margins.csv"); co <- read_result("secondary_coefficients.csv"); specialty_test <- read_result("secondary_specialty_interaction.csv"); reader <- read_result("reader_paired_bootstrap.csv")
ua <- primary[primary$modalityA=="unaided" & primary$modalityB=="NO_MOD",]; aa <- primary[primary$modalityA=="AI-assisted" & primary$modalityB=="NO_MOD",]; delta <- primary[primary$modalityA=="AI-assisted" & primary$modalityB=="unaided",]
table4 <- rbind(data.frame(endpoint="AUROC",unaided=ua$AUCA,unaided_low=ua$botCIBDG,unaided_high=ua$topCIBDG,assisted=aa$AUCA,assisted_low=aa$botCIBDG,assisted_high=aa$topCIBDG,difference=delta$AUCAminusAUCB,difference_low=delta$botCIBDG,difference_high=delta$topCIBDG,p_value=delta$pValueBDG),op)
write.csv(table4,file.path(root,"03_results","publication_table4.csv"),row.names=FALSE)
write.csv(safety,file.path(root,"03_results","publication_tableS6.csv"),row.names=FALSE)
write.csv(merge(reader,metadata,by="reader_id",sort=TRUE),file.path(root,"03_results","publication_tableS9.csv"),row.names=FALSE)
co$statistical_interpretation <- ifelse(co$`Pr(>|z|)`<.05,"statistically significant","not statistically significant")
write.csv(co,file.path(root,"03_results","publication_tableS7_coefficients.csv"),row.names=FALSE)
write.csv(sp,file.path(root,"03_results","publication_tableS7_specialties.csv"),row.names=FALSE)
write.csv(specialty_test,file.path(root,"03_results","publication_tableS7_interaction.csv"),row.names=FALSE)
print(table4)
pairs <- do.call(rbind,lapply(split(descriptive,descriptive$reader_id),function(z) {
 a <- z[z$condition=="unaided",]; b <- z[z$condition=="assisted",]
 data.frame(reader_id=a$reader_id,delta_auc=b$auc-a$auc,delta_sensitivity=b$sensitivity-a$sensitivity,delta_specificity=b$specificity-a$specificity)
}))
write.csv(pairs,file.path(root,"03_results","reader_observed_effects.csv"),row.names=FALSE)
operating_points <- do.call(rbind,lapply(c("unaided","assisted"),function(condition) {
 sens <- op[op$endpoint=="sensitivity",]; spec <- op[op$endpoint=="specificity",]
 data.frame(condition=condition,fpr=1-spec[[condition]],fpr_low=1-spec[[paste0(condition,"_high")]],fpr_high=1-spec[[paste0(condition,"_low")]],sensitivity=sens[[condition]],sensitivity_low=sens[[paste0(condition,"_low")]],sensitivity_high=sens[[paste0(condition,"_high")]])
}))
write.csv(operating_points,file.path(root,"03_results","figure_operating_points.csv"),row.names=FALSE)
confusion <- do.call(rbind,lapply(c("unaided","assisted"),function(condition) {
 sens <- op[op$endpoint=="sensitivity",condition]; spec <- op[op$endpoint=="specificity",condition]
 data.frame(condition=condition,reference=c("Stable","Stable","Unstable","Unstable"),prediction=c("Stable","Unstable","Stable","Unstable"),row_percentage=100*c(spec,1-spec,1-sens,sens))
}))
write.csv(confusion,file.path(root,"03_results","figure_confusion_percentages.csv"),row.names=FALSE)
ord <- order(cases$syndnet_probability,decreasing=TRUE); ys <- cases$truth[ord]; ps <- cases$syndnet_probability[ord]; ends <- which(!duplicated(ps,fromLast=TRUE)); tps <- cumsum(ys)[ends]; fps <- cumsum(1-ys)[ends]
if(length(tps)>2) {keep <- c(TRUE,diff(fps,differences=2)!=0 | diff(tps,differences=2)!=0,TRUE); tps<-tps[keep];fps<-fps[keep];ps<-ps[ends][keep]} else ps <- ps[ends]
model_roc <- data.frame(fpr=c(0,fps/sum(cases$truth==0)),tpr=c(0,tps/sum(cases$truth==1)),threshold=c(Inf,ps))
write.csv(model_roc,file.path(root,"03_results","locked_model_roc.csv"),row.names=FALSE)
benchmark_ci <- read.csv(file.path(dirname(root),"results","reproduced_bootstrap_ci.csv"),stringsAsFactors=FALSE)
benchmark_ci <- benchmark_ci[benchmark_ci$table=="Table4",]
benchmark <- data.frame(endpoint=c("AUROC","sensitivity","specificity","accuracy"),estimate=unlist(model[c("auc","sensitivity","specificity","accuracy")]),ci_low=NA_real_,ci_high=NA_real_)
for(i in seq_len(nrow(benchmark))) {
 z <- benchmark_ci[tolower(benchmark_ci$metric)==tolower(benchmark$endpoint[i]),]
 stopifnot(nrow(z)==1)
 benchmark$ci_low[i] <- z$ci_low;benchmark$ci_high[i] <- z$ci_high
}
write.csv(benchmark,file.path(root,"03_results","locked_model_benchmark.csv"),row.names=FALSE)
model$balanced_accuracy <- (model$sensitivity+model$specificity)/2
model$accuracy_standardized_42pct <- .42*model$sensitivity+.58*model$specificity
write.csv(model,file.path(root,"03_results","locked_model_descriptive.csv"),row.names=FALSE)
