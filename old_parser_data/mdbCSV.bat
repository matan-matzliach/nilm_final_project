curl --form files[]=@1.mdb "https://www.rebasedata.com/api/v1/convert?outputFormat=csv&errorResponse=zip" -o output1.zip
curl --form files[]=@2.mdb "https://www.rebasedata.com/api/v1/convert?outputFormat=csv&errorResponse=zip" -o output2.zip
curl --form files[]=@3.mdb "https://www.rebasedata.com/api/v1/convert?outputFormat=csv&errorResponse=zip" -o output3.zip