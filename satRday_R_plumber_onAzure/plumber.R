# plumber.R

combine_df <- readRDS("combine_data.rds")

#* @param taxno
#* @post /result
function(taxno)
{
  df <- jsonlite::toJSON(subset(combine_df, TaxidNo==taxno))
  return(df)
}
