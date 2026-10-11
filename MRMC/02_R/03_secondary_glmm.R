if(.Platform$OS.type=="windows") invisible(Sys.setlocale("LC_CTYPE","English_United States.utf8"))
source(file.path(Sys.getenv("SYNDNET_MRMC_ROOT","."),"02_R","glmm_helpers.R"))
f <- correct ~ condition*(specialty+experience_sd)+period+sequence+(1|reader_id)+(1|case_id)
fit <- fit_model(f,d,"secondary_glmm")
co <- as.data.frame(coef(summary(fit))); co$term <- rownames(co); co$low <- co$Estimate-qnorm(.975)*co$`Std. Error`; co$high <- co$Estimate+qnorm(.975)*co$`Std. Error`
write.csv(co,file.path(root,"03_results","secondary_coefficients.csv"),row.names=FALSE)
terms <- grep("condition.*:specialty",names(fixef(fit))); B <- fixef(fit)[terms]; V <- as.matrix(vcov(fit))[terms,terms,drop=FALSE]; stat <- drop(t(B)%*%solve(V,B))
write.csv(data.frame(term="Condition x specialty",chi_square=stat,df=length(B),p_value=pchisq(stat,length(B),lower.tail=FALSE)),file.path(root,"03_results","secondary_specialty_interaction.csv"),row.names=FALSE)
sp <- do.call(rbind,lapply(levels(d$specialty),function(s) cbind(specialty=s,marginal(fit,d[d$specialty==s,]))))
write.csv(sp,file.path(root,"03_results","secondary_specialty_margins.csv"),row.names=FALSE)
print(co); print(sp)

