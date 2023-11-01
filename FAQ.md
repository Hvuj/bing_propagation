## Handling Event Data with Different Conversion Times

When you upload event data to Google Ads, you can specify the `conversion_time` field. This field is used to track the date and time of the conversion. If you upload the same event data with different `conversion_time` values, Google Ads will accept both values.

For example, let's say you upload the following event data:

```
{
  "event_name": "purchase",
  "click_id": "1234567890",
  "order_id": 123,
  "conversion_time": "2023-08-01"
}
```

And then you upload the following event data:

```
{
  "event_name": "purchase",
  "click_id": "1234567890",
  "order_id": 123,
  "conversion_time": "2023-08-02"
}
```

Google Ads will treat these two events as separate conversions. The first event will be recorded as occurring on August 1, 2023, and the second event will be recorded as occurring on August 2, 2023.

It's important to note that the `conversion_time` field is not mandatory. If you don't specify a `conversion_time`, Google Ads will use the current time as the conversion time.

Here are some other examples of how you can use the `conversion_time` field:

- To track conversions that happen over a period of time, such as a week or a month.
- To track conversions that happen in different time zones.
- To track conversions that happen on different devices.

## The GCLID (Google Click Identifier)

The GCLID (Google Click Identifier) is a unique identifier that is generated when a user clicks on an ad. It can be used to track conversions by click.

However, the GCLID is not unique to a user. This means that the same GCLID can be used for multiple conversions by the same user. For example, let's say User A clicks on an ad for your product. The GCLID for this click is 1234567890. User A then closes the browser and reopens it. Later that day, User A visits your website and converts. The conversion is tracked with the same GCLID, 1234567890.

If you need to track conversions by user, you should use a different tracking method, such as a cookie. Cookies are unique identifiers that are stored on the user's browser and can be used to track a user's activity across multiple sessions and devices.

## Conclusion

When handling event data with different conversion times, it's important to understand how the `conversion_time` field works. You should also be aware of the limitations of the GCLID. By understanding these concepts, you can ensure that your conversion data is accurate and reliable.
