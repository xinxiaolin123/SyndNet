if(.Platform$OS.type=="windows") invisible(Sys.setlocale("LC_CTYPE","English_United States.utf8"))
root <- normalizePath(Sys.getenv("SYNDNET_READER_STUDY_ROOT","."),mustWork=TRUE)
w <- read.csv(file.path(root,"input","MRMC_REAL_READER_CASE_FINAL.csv"))
set.seed(20261011)
B <- 10000L
r <- do.call(rbind,lapply(split(w,w$reader_id),function(z) {
  levels25 <- 1:25; bin <- (z$reader_score_unaided-1)*5+z$reader_score_assisted
  count <- function(truth) tabulate(bin[z$truth==truth],nbins=25)
  neg <- rmultinom(B,sum(z$truth==0),count(0)/sum(z$truth==0)); pos <- rmultinom(B,sum(z$truth==1),count(1)/sum(z$truth==1))
  auc <- function(pos,neg,which_score) {
    code <- if(which_score==1) rep(1:5,each=5) else rep(1:5,times=5)
    p <- rowsum(pos,code,reorder=FALSE); n <- rowsum(neg,code,reorder=FALSE); p <- p[order(as.integer(rownames(p))),]; n <- n[order(as.integer(rownames(n))),]
    value <- rep(0,ncol(pos)); cumulative <- rep(0,ncol(pos))
    for(i in 1:5) {value <- value+p[i,]*(cumulative+n[i,]/2); cumulative <- cumulative+n[i,]}
    value/(colSums(p)*colSums(n))
  }
  a <- auc(pos,neg,1); b <- auc(pos,neg,2)
  q <- function(v) unname(quantile(v,c(.025,.975),type=7))
  au <- function(s) {n1 <- sum(z$truth==1); n0 <- sum(z$truth==0); (sum(rank(s)[z$truth==1])-n1*(n1+1)/2)/(n1*n0)}
  qa <- q(a); qb <- q(b); qd <- q(b-a)
  data.frame(reader_id=z$reader_id[1],unaided=au(z$reader_score_unaided),unaided_low=qa[1],unaided_high=qa[2],assisted=au(z$reader_score_assisted),assisted_low=qb[1],assisted_high=qb[2],difference=au(z$reader_score_assisted)-au(z$reader_score_unaided),difference_low=qd[1],difference_high=qd[2])
}))
write.csv(r,file.path(root,"results","reader_paired_bootstrap.csv"),row.names=FALSE)
writeLines("Individual-reader percentile intervals: 10,000 paired reference-class-stratified case bootstrap resamples. Score-pair multinomial counts are an exact distributional implementation of case resampling for discrete scores. Seed 20261011; quantile type 7. These descriptive intervals condition on each reader.",file.path(root,"results","reader_interval_method.txt"))
print(r)

