from ..models import CustomersData
from ..utils import address_to_coordinate

def get_or_create_customer(customer_name, address):
    """
    Get or create a customer by name and address.
    If the customer is created or doesn't have coordinates, update the coordinate using address_to_coordinate.
    Returns:
        CustomersData instance.
    """
    customer, created = CustomersData.objects.get_or_create(
        name=customer_name,
        defaults={'address': address, 'coordinate': None}
    )
    if created or not customer.coordinate:
        lat, lng = address_to_coordinate(address)
        if lat and lng:
            customer.coordinate = f"{lat},{lng}"
            customer.save()
    return customer
