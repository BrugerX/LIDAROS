
local bp = import 'base_profile.jsonnet';


bp {
  descriptor+: {
    type: bp.descriptor.type + "/" + "component"
  },
capabilities+: {
  turnOn: {
    topic: $.descriptor.id + "/turnOn"
  }
}
}







