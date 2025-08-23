//Our very first profile :O

//We create a copy + pasteable schema

local BaseProfile = {
    descriptor:
    {
    id: error "Must define an 'id''",
    vendor: error "Must define a vendor",
    product: error "Must define a product",
    type: "base",
    description: error "Must define a description"
    },
    capabilities:
    {

    }
};

BaseProfile
