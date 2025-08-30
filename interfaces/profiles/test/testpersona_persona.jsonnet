//The profile we use for the persona and criteria test
local test_profile = import "testpersona_profile.jsonnet";

local persona_descriptor =
{
    id:"right",
    description: "Used for testing with the persona and criterion unit tests.",
    product: "Nuffin'",
    vendor: "None",
    dummy1: 195, //Guess the code (Latin)
    dummy2_list: [82,85,66,73,67,79,78], #Guess the word (Hint to the previous code)
    dummy3: "CAESAR" //(Hint to both)

};



test_profile
{
 descriptor+: persona_descriptor
}