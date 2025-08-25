
local laser_profile = import 'laser_profile.jsonnet';

local Toptica_Ibeam_Descriptor = {
  id: 'lazer',
  vendor: 'Toptica',
  product: 'IBeam Pro',
  wavelength: 445,
  TEM_modes: ['00'],
  nr_channels: 2,
  description: 'A Toptica IBeam laser'
};


laser_profile
{
 descriptor+: Toptica_Ibeam_Descriptor
}