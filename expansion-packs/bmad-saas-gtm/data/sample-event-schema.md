# Sample Analytics Event Schema

```yaml
events:
  - name: user_signed_up
    properties:
      - name: plan
        type: string
      - name: referrer
        type: string
  - name: activated_feature
    properties:
      - name: feature_name
        type: string
      - name: variant
        type: string
      - name: timestamp
        type: timestamp
```

Use this as a starting point for instrumentation conversations with engineering.
