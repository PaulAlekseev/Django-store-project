### Main purpose:
_____
Provide an opportunity for users to see the selection of products in the store.
### Key concepts:
_____
- Products and Categories are added to the database by the admin;
- Product has a detail page with info, description and reviews sections;
- Every Product has a set of customised features that can be different for every Product instanse;
- Every Category has a set of features that purpose is to filter products that it contains;
    - Every Category's feature has:
        - Requested fields - that purpose is to contain information about fields that is requested;
        - Fields - caching every Product's requested fields instance (generated automatically);
- Category's features created automatically after first instance, you __don't need to fill in the feautures field__;
- After the Category model is instantiated requested fields can be changed;
- Categories have a tree like structure;
- Products is contained in Inner Categories which are contained in one of the Category descendants, all can be edit via admin panel;
- Products can be filtered:
    - By requested fields that are specified in the Category's feature field;
    - By name with search form;
- Every Product has a set of features that purpose is to show its specific characteristics;
- Non-authenticated users can read product's info, description and reviews, but they can't write reviews;
- Authenticated users can write reviews, edit or delete them. Every authenticated user has a limit of maximum one review per product;
- Review contains its title, pros, cons, comentary and product rating from 1 to 5;
- Products can be contained in the basket after clicking Add ot basket;
- In the basket:
    - User can watch all products that he added to it;
    - Product's amount cant be changed until it hits its maximum amount that is stored in all of stores;
    - Product can be deleted;
    - Products are shown as Ouf of stock if this product is out of stock;
    - User can transfer all Products, that Basket contains, to the Order instance with help of checkout functionality;
- Order contains:
    - OrderProducts instances that contains:
        - Order field - Order foreign key;
        - Product field - Product foreign key;
        - Amount field - contains information about how many of concrete Product this Order contains;
    - OrderStore insances that contains:
        - Order field - Order foreign key;
        - StoreProduct - foreign key to a intermediate StoreProduct instance that contains information about amount of Product in concrete shop;
        - Amount field - contains information about how many of concreate Product has been taken from each Store;
    - Order himself that combines it all together and contains its date;
- All reviews and Orders can be found in user's profile;

### To run application on local machine:
____
__1. Clone the repository:__

        git clone https://github.com/PaulAlekseev/Django-store-project.git

__2. Create a virtual environment:__

        python -m venv venv

__3. Activate the virtual environment:___

        source venv/bin/activate

__4. Install all required dependencies:__

        pip install -r requirements.txt

__5. Apply the migrations:__

        python manage.py migrate

__6. Create superuser:__

        python manage.py createsuperuser

__7. Run server:__

        python manage.py runserver

__NOTE: Project cannot be run with sqlite, because it contains JSON fields, by standart it will require environment variable for Postgresql database__


