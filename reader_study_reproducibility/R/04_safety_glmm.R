if(.Platform$OS.type=="windows") invisible(Sys.setlocale("LC_CTYPE","English_United States.utf8"))
source(file.path(Sys.getenv("SYNDNET_READER_STUDY_CODE_ROOT"),"glmm_helpers.R"))
pred <- read.csv(file.path(root,"input","MRMC_LOCKED_CASE_PREDICTIONS.csv"))
d$model_correct <- factor(as.integer((pred$syndnet_predicted_label[match(d$case_id,pred$case_id)]=="unstable")==d$truth),levels=c(0,1),labels=c("SyndNet incorrect","SyndNet correct"))
f <- correct ~ condition*model_correct+period+sequence+specialty+experience_sd+(1|reader_id)+(1|case_id)
fit <- fit_model(f,d,"safety_glmm")
r <- do.call(rbind,lapply(levels(d$model_correct),function(s) cbind(stratum=s,marginal(fit,d[d$model_correct==s,]))))
write.csv(r,file.path(root,"results","safety_glmm.csv"),row.names=FALSE); print(r)

