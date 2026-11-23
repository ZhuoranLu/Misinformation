#!/usr/bin/env Rscript
# Run verbatim Rmd chunks against their frozen author exports.
file_arg <- grep('^--file=',commandArgs(FALSE),value=TRUE)[1]
root <- dirname(normalizePath(sub('^--file=','',file_arg)))
out <- file.path(root,'results')
dir.create(out,showWarnings=FALSE)
setwd(file.path(root,'data'))
chunks <- c('experiment_3_sharing.R',
            'experiment_3_accuracy.R',
            'experiment_3_moderation.R',
            'experiment_2_sharing.R',
            'experiment_1_moderation.R',
            'experiment_2_moderation.R')
models <- list(); rows <- list()
env <- new.env(parent=globalenv())
sink(file.path(out,'R_log.txt'))
for (chunk in chunks) {
  cat('\n### ORIGINAL CHUNK:',chunk,'\n')
  expressions <- parse(file.path(root,'analysis_code',chunk))
  for (expression in expressions) {
    value <- withVisible(eval(expression,env))
    if (value$visible) print(value$value)
    if (is.call(expression) && as.character(expression[[1]])[1] %in% c('=','<-')) {
      name <- as.character(expression[[2]])
      object <- get(name,env)
      if (inherits(object,'glm')) {
        key <- paste(chunk,name,sep=':')
        models[[key]] <- object
        s <- coef(summary(object))
        rows[[key]] <- data.frame(source_chunk=chunk,object=name,term=rownames(s),
          estimate=s[,1],se=s[,2],statistic=s[,3],p=s[,4],n=nobs(object),
          family=object$family$family,formula=paste(deparse(formula(object)),collapse=' '))
      }
    }
  }
}
sink()
write.csv(do.call(rbind,rows),file.path(out,'R_coefficients.csv'),row.names=FALSE)
saveRDS(models,file.path(out,'R_models.rds'))
writeLines(capture.output(sessionInfo()),file.path(out,'R_environment.txt'))
cat('Original R chunks completed.\n')
