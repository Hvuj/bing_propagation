# This service is for propagating click conversions

## Requirements

### Env Variables

- PROJECT_ID - Default should be `peppy-castle-368715`
- SECRET_ID - The secret name under secrets manager in `PROJECT_ID`

### Request Variables

- project_id - The Google BigQuery Project ID of the project that we want to query.
- dataset_id - The Google BigQuery Dataset ID of the project that we want to query.
- table_name - The Google BigQuery Table Name of the project that we want to query.

### Acceptable Values in query due to Google Ads API limitations

- `value` - The conversions Value
- `date` - The conversions date. For daily usage It must look like this: `timestamp(concat(cast(date(date) as string), ' 23:59:59+00:00')) as date`.
  For hourly usage - please leave it as is just make sure to add the timezoe i.e. `+00:00`, `+01:00` etc.
  Note! the `+00:00` i.e. time zone is only necessary if it is not UTC.
- `email` - The email address.
- `phone` - The phone number.
- `order_id` - The transaction ID of the transaction.
- `click_id` - The click ID associated with Google Ads platform click conversion.
- `gbraid` - The GBRAID for the iOS app conversion. If set, the `gclid` and `wbraid` parameters must be None.
- `wbraid` - The WBRAID for the iOS app conversion. If set, the `gclid` and `gbraid` parameters must be None.
- `conversion_action_id` - The Conversion ID of the conversion that belongs to the customer id on the Google Ads
  platform.

## Super important!

- Uploaded conversions are reflected in reports for the impression date of the original click, not the date of the upload request or the date of the conversion_date_time of the ClickConversion.
- It takes up to 3 hours for imported conversion statistics to appear in your Google Ads account for last-click attribution. For other search attribution models, it can take longer than 3 hours.

## Links to Docs

- [Google Ads click conversion general docs](https://developers.google.com/google-ads/api/docs/conversions/upload-clicks)
- [Google Ads click conversion custom variables docs](https://developers.google.com/google-ads/api/reference/rpc/v12/ClickConversion#custom_variables)
- [Google Ads click conversion user identifier docs](https://developers.google.com/google-ads/api/reference/rpc/v12/UserIdentifier)
- [Google Ads click conversion user identifier docs example code](https://developers.google.com/google-ads/api/docs/conversions/upload-identifiers)

## Best practices

- [Google Ads click conversion best practices](https://developers.google.com/google-ads/api/docs/best-practices/overview)
