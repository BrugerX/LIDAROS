
local bp = import 'base_profile.jsonnet';
local topic_template = import '../base/topic_capability_template.jsonnet';


bp {
  descriptor+: {
    type: bp.descriptor.type + "/" + "static_component"
  }
}







