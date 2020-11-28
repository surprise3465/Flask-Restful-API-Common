def seller_schema(seller):
    return {
            'id': seller.id,
            'name': seller.name,
        }

def customer_schema(customer):
    return {
            'id': customer.id,
            'name': customer.name,
        }

def user_schema(user):
    return {
            'id': user.id,
            'name': user.email,
        }


InputUserSchema = {
    "type": "object",
    "properties": {
        "password":{"type": "string"}, 
        "email":{"type": "string"}, 
    },

    "required":[
        "email", "password",
    ]
}

InputSellerSchema = {
    "type": "object",
    "properties": {
        "name":{"type": "string"}, 
    },

    "required":[
        "name",
    ]
}

InputCustormerSchema = {
    "type": "object",
    "properties": {

        "name":{"type": "string"}, 
        "money": {"type": "number"},
        "status": {"type": "number"}, 
        "seller_id": {"type": "number"}, 
    },

    "required":[
        "name",
        "money",
        "status",
        "seller_id",
    ]
}


input_schema_dic = {
    "customer":InputCustormerSchema,
    "seller":InputSellerSchema,
    "users":InputUserSchema,  
}

output_schema_dic = {
    "customer":customer_schema,
    "seller":seller_schema,
    "users":user_schema
}