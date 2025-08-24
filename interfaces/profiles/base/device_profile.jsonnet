
local bp = import 'base_profile.jsonnet';


bp {
  descriptor+: {
    type: bp.descriptor.type + "/" + "device"
  },
capabilities+: {
  turnOn: {
    topic: $.descriptor.id + "/turnOn"
  }
}
}







