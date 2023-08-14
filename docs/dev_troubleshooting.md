## Incidents

### AWS S3 Access Denied
In prod, it looks like there's some issue with accessing AWS S3 where (at least) the students' recordings are stored.

#### Details
* `https://api-musiccpr-prod.s3.amazonaws.com/media/student-recoding_On2htn8.mp3` gets `403` (clicked from https://api.musiccpr.org/jZ7CPecDiNpqsubmissions/submissionattachment/ )

1. confirm file exists in S3 (sign in to AWS web console as root musiccpr aws account )
    * file exists and has Object URL: `https://api-musiccpr-prod.s3.us-east-2.amazonaws.com/media/student-recoding_On2htn8.mp3`
        * this differs from the one above... is that ok?
1. try to get the file from aws CLI locally
    1. ensure that my ~/.aws/credentials file has a profile that matches what prod uses (added [cprprod])
    1. `aws s3 cp s3://api-musiccpr-prod/media/student-recoding_On2htn8.mp3 . --profile cprprod`
        * `download SUCCEEDED: s3://api-musiccpr-prod/media/student-recoding_On2htn8.mp3 to ./student-recoding_On2htn8.mp3 An error occurred (403) when calling the HeadObject operation: Forbidden`
1. 
