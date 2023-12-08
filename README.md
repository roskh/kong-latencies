# Kong Latency

This repository is a test setup to understand exactly what the [latency metrics](https://docs.konghq.com/hub/kong-inc/file-log/#json-object-considerations) from `file-log` kong plugin say.
It also tries to test if it's possible to tease out the latency for just the plugin execution time.

## Test Setup

A custom Kong plugin (`slowdown`) and a custom upstream server (`sleeping-requests.py`) is implemented and configured with Kong to tease out different scenarios:
- slowdown: will sleep for 0.5 seconds. Simulates work done in Kong plugins, etc before sending the first bytes to upstream.
- sleeping-requests: will sleep for 1.0 seconds before sending any bytes back, and in the middle of sending response body bytes for 2.0 seconds to simulate a service doing useful work and streaming a response in events mode respectively.

Run:

```sh
docker compose build
docker compose up
curl http://localhost:8000/echo/1 # a few times
cat logs/file-log.json | jq ".latencies"
```

## Results

On a particular MacOS machine the results were:
```json
{
  "proxy": 1015,
  "request": 3561,
  "x_pre_upstream": 541,
  "kong": 2546
}
{
  "proxy": 1033,
  "request": 3548,
  "x_pre_upstream": 510,
  "kong": 2515
}
{
  "proxy": 1005,
  "request": 3514,
  "x_pre_upstream": 508,
  "kong": 2509
}
```

Which seems to indicate that:
- `latencies.kong`: is the plugin processing time + time to download bytes from upstream
- `latencies.proxy`: is the time from sending bytes to upstream to receiving first byte back from it
- `latencies.request`: is `latencies.kong` + `latencies.proxy`. [But it might not be exactly the same in all cases](https://github.com/Kong/kong/blob/2784bf54d8cbf3dbffe743837c1cbac2338c69f3/kong/pdk/log.lua#L844-L847).
- custom `x_pre_upstream`: is the time it took to process plugins. Seems to be confirmed in the [source code](https://github.com/Kong/kong/blob/2784bf54d8cbf3dbffe743837c1cbac2338c69f3/kong/init.lua#L1409-L1411)

The custom field can be added to `file-log` (see kong.yml):
```yaml
  - name: file-log
    config:
      path: "/tmp/logs/file-log.json"
      custom_fields_by_lua: 
        <name of new field>: "return (ngx.ctx.KONG_PROXY_LATENCY or 0)"
```
