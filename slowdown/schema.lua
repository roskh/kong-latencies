local typedefs = require "kong.db.schema.typedefs"

return {
  name = "slowdown",
  fields = {
    { consumer = typedefs.no_consumer },
    { protocols = typedefs.protocols_http },
  }
}
