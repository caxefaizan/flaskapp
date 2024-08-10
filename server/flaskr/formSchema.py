sections = [
    "Personal Details",
    "Sibling Details",
    "Parents Details",
    "Lifestyle Details",
    "Residence Details",
    "Spouse Preference Details",
]
profileInputs = {
    "Personal Details": {
        "clientGender": {
            "label": "Gender",
            "type": "radio",
            "values": ["M", "F"],
        },
        "clientCast": {
            "label": "Surname",
            "type": "text",
            "placeHolder": "Surname",
        },
        "clientOccupation": {
            "label": "Occupation",
            "type": "text",
            "placeHolder": "Current Occupation",
        },
        "clientEducation": {
            "label": "Education",
            "type": "text",
            "placeHolder": "Highest Qualification",
        },
        "clientAge": {
            "label": "Age",
            "type": "text",
            "placeHolder": "Age",
            "min": 18,
            "max": 60,
            "step": 1,
        },
        "clientHeight": {
            "label": "Height",
            "type": "text",
            "placeHolder": "Height in Feet.inch eg 6.1",
        },
        "clientComplexion": {
            "label": "Complexion",
            "type": "radio",
            "placeHolder": "Skin Complexion",
            "values": ["Fair", "Wheat", "Brown"],
        },
    },
    "Sibling Details": {
        "siblingGender": {
            "label": "Gender",
            "type": "radio",
            "values": ["M", "F"],
        },
        "siblingOccupation": {
            "label": "Occupation",
            "type": "text",
            "placeHolder": "Current Occupation",
        },
        "siblingSpouseCast": {
            "label": "Spouse Surname",
            "type": "text",
            "placeHolder": "Surname",
        },
        "siblingSpouseOccupation": {
            "label": "Spouse Occupation",
            "type": "text",
            "placeHolder": "Current Occupation",
        },
    },
    "Parents Details": {
        "fathersOccupation": {
            "label": "Father's Occupation",
            "type": "text",
            "placeHolder": "eg. Business",
        },
        "mothersOccupation": {
            "label": "Mother's Occupation",
            "type": "text",
            "placeHolder": "eg. HomeMaker",
        },
        "mothersCast": {
            "label": "Mother's Surname",
            "type": "text",
            "placeHolder": "Surname",
        },
        "otherRelations": {
            "label": "Family Relations",
            "type": "text",
            "placeHolder": "eg. Shah, Wani , Mir",
        },
    },
    "Lifestyle Details": {
        "smoking": {
            "label": "Smoking",
            "type": "radio",
            "values": ["Yes", "No"],
        },
        "prayers": {
            "label": "Prayers",
            "type": "radio",
            "values": ["Regular", "Irregular"],
        },
        "religiousSect": {
            "label": "Religious Identity",
            "type": "text",
            "placeHolder": "eg. Sunni, AhleHadees",
        },
    },
    "Residence Details": {
        "presentAddress": {
            "label": "Present Address",
            "type": "text",
            "placeHolder": "eg. Lalchowk,Srinagar",
        },
        "permanentAddress": {
            "label": "Permanent Address",
            "type": "text",
            "placeHolder": "eg. Dalgate, Srinagar",
        },
        "oldAddress": {
            "label": "Old Address",
            "type": "text",
            "placeHolder": "eg. Dalgate, Srinagar",
        },
    },
    "Spouse Preference Details": {
        "preferenceOccupation": {
            "label": "Preferred Occupation",
            "type": "text",
            "placeHolder": "eg. Lecturer",
        },
        "preferenceEducation": {
            "label": "Preferred Education",
            "type": "text",
            "placeHolder": "eg. M.A",
        },
        "preferenceAge": {
            "label": "Preferred Age",
            "type": "number",
            "placeHolder": "Preferred Age Max",
            "min": 18,
            "max": 60,
            "step": 1,
        },
        "preferenceHeight": {
            "label": "Preferred Height",
            "type": "text",
            "placeHolder": "Preferred Height Max",
        },
        "preferenceComplexion": {
            "label": "Preferred Complexion",
            "type": "radio",
            "placeHolder": "rg. Wheat",
            "values": ["Fair", "Wheat", "Brown"],
        },
    },
}
