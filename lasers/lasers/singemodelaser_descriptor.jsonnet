local dp = import 'device_profile.jsonnet';
local service_template = import 'service_capability_template.jsonnet';


dp
{
    descriptor+:
    {
        type: dp.descriptor.type +  "/" + "laser",
        wavelength : error "Must define an integer wavelength in nanometer",
        nr_channels: error "Must define an integer number of channels (1-indexed)",
        TEM_modes: error "Must define a string array of TEM modes"
    },

    capabilities+:
    {
        setPower: service_template+ {
            type: "service",
            srv_type: "interaces.setlaserpower",
            request_channel: $.descriptor.id + "/setPower" + "/request",
            response_channel: $.descriptor.id + "/setPower" + "/response",
            description: "Sets the output power of the specific channel in watts"
        }

    }
}


