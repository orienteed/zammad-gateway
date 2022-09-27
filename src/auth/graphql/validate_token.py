from gql import gql


def magento_validate_token():
    query = gql(
        """
    query verifyToken{ 
        customer {
            email,
            firstname,
            lastname
        }
    }
    """
    )
    return query
