local dp = import '../base/device_profile.jsonnet';
local service_template = import '../base/service_capability_template.jsonnet';

dp
{
    descriptor+:
    {
        type: dp.descriptor.type +  "/" + "test",
        dummy1 : error "Must define an integer dummy1 value",
        dummy2_list: error "Must define an array of values for dummy2_list)",
        dummy3: error "Must define a string for dummy1"
    },

    capabilities+:
    {
        testService1: service_template+ {
            type: "service",
            srv_type: "interfaces/testService1",
            request_channel: $.descriptor.id + "/testService1" + "/request1",
            response_channel: $.descriptor.id + "/testService1" + "/response1",
            description: "Does fuck all"
        },
        testService2: service_template+ {
            type: "service",
            srv_type: "interfaces/testService2",
            request_channel: $.descriptor.id + "/testService2" + "/request",
            response_channel: $.descriptor.id + "/testService2" + "/response",
            description: "Does fuck all 2"
        }

    }
}