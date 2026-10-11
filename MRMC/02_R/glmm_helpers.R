if(.Platform$OS.type=="windows") invisible(Sys.setlocale("LC_CTYPE","English_United States.utf8"))
root <- normalizePath(Sys.getenv("SYNDNET_MRMC_ROOT", "."),mustWork=TRUE)
library(lme4)
d <- read.csv(file.path(root,"01_input","MRMC_REAL_LONG_FINAL.csv"),stringsAsFactors=FALSE)
d$reader_id <- factor(d$reader_id); d$case_id <- factor(d$case_id)
d$condition <- factor(d$condition,levels=c("unaided","AI-assisted")); d$period <- factor(d$period); d$sequence <- factor(d$sequence); d$specialty <- factor(d$specialty)
rd <- unique(d[c("reader_id","experience_years")]); experience_mean <- mean(rd$experience_years); experience_sd <- sd(rd$experience_years)
d$experience_sd <- (d$experience_years-experience_mean)/experience_sd
d$correct <- as.integer(d$decision==d$truth)
write.csv(data.frame(mean=experience_mean,sd=experience_sd),file.path(root,"03_results","experience_scaling.csv"),row.names=FALSE)
control <- glmerControl(optimizer="bobyqa",optCtrl=list(maxfun=200000))
fit_model <- function(formula,data,name) {
  fit <- glmer(formula,data=data,family=binomial(),control=control,nAGQ=1)
  saveRDS(fit,file.path(root,"03_results",paste0(name,".rds")))
  writeLines(c(paste(deparse(formula),collapse=" "),capture.output(summary(fit))),file.path(root,"03_results",paste0(name,"_summary.txt")))
  diagnostics <- data.frame(model=name,singular=isSingular(fit),optimizer_code=paste(fit@optinfo$conv$opt,collapse=";"),convergence_messages=paste(fit@optinfo$conv$lme4$messages,collapse=";"),max_scaled_gradient=if(!is.null(fit@optinfo$derivs)) max(abs(solve(chol(fit@optinfo$derivs$Hessian),fit@optinfo$derivs$gradient))) else NA_real_)
  write.csv(diagnostics,file.path(root,"04_QC",paste0(name,"_diagnostics.csv")),row.names=FALSE)
  fit
}
marginal <- function(fit,population) {
  beta <- fixef(fit); V <- as.matrix(vcov(fit)); variance <- sum(vapply(VarCorr(fit),function(z) z[1,1],numeric(1)))
  gh <- statmod::gauss.quad.prob(40,dist="normal")
  one <- function(condition) {
    nd <- population; nd$condition <- factor(condition,levels=levels(d$condition))
    X <- model.matrix(delete.response(terms(reformulas::nobars(formula(fit)))),nd); X <- X[,names(beta),drop=FALSE]
    eta <- drop(X%*%beta); probabilities <- rep(0,nrow(X)); derivative <- rep(0,nrow(X))
    for(j in seq_along(gh$nodes)) {p <- plogis(eta+sqrt(variance)*gh$nodes[j]); probabilities <- probabilities+gh$weights[j]*p; derivative <- derivative+gh$weights[j]*p*(1-p)}
    list(p=mean(probabilities),g=colMeans(X*derivative))
  }
  a <- one("unaided"); b <- one("AI-assisted"); delta <- b$p-a$p; dg <- b$g-a$g
  se <- sqrt(drop(t(dg)%*%V%*%dg)); ci <- function(z) {sl <- sqrt(drop(t(z$g)%*%V%*%z$g))/(z$p*(1-z$p)); plogis(qlogis(z$p)+c(-1,1)*qnorm(.975)*sl)}
  aci <- ci(a); bci <- ci(b)
  data.frame(unaided=a$p,unaided_low=aci[1],unaided_high=aci[2],assisted=b$p,assisted_low=bci[1],assisted_high=bci[2],difference=delta,difference_low=delta-qnorm(.975)*se,difference_high=delta+qnorm(.975)*se,p_value=2*pnorm(-abs(delta/se)))
}


