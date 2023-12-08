local Slowdown = {
  PRIORITY = 940,
  VERSION  = "0.0.1",
}

-- sleep before upstreaming request, should contribute to 'latency.kong'
function Slowdown:access()
  kong.log.info("Sleeping")
  ngx.sleep(0.5)
end

return Slowdown
