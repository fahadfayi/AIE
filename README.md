# AIE
 this is a small project that can upload CSV File and view the data in HTML table

 functionality:
 * can upload only csv file that given
 * set option UPDATE_IF_DATA = True in settings to update the data if data is already present. it will not insert duplicate data
 * set ENABLE_DATATABLE = True to view data in thirdparty table called DataTable. it has in build sorting and searching feature
 * if ENABLE_DATATABLE = false the data is shown in custom table. it has sorting function (click heading to sort coulumn) and also same page has feature to filter data. all filter except time and date do icontains search in backend meaning it will search the given are present in the data (no need to give exact name and it is case insensitive)
 * if you upload worng csv file it will show error
 * if you upload file other than "csv" it will show the error
