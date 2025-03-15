from app import app, db
from server.models import Customer, Item, Review

class TestReview:
    '''Review model in models.py'''

    def setup_method(self, method):
        '''Reset the database before each test'''
        with app.app_context():
            db.session.rollback()
            db.drop_all()
            db.create_all()

    def test_can_be_instantiated(self):
        '''can be invoked to create a Python object.'''
        r = Review()
        assert r
        assert isinstance(r, Review)

    def test_has_comment(self):
        '''can be instantiated with a comment attribute.'''
        r = Review(comment='great product!')
        assert r.comment == 'great product!'

    def test_can_be_saved_to_database(self):
        '''can be added to a transaction and committed to the review table with a comment column.'''
        with app.app_context():
            assert 'comment' in Review.__table__.columns

            # Create customer and item before adding a review
            c = Customer(name="John Doe")
            i = Item(name="Laptop", price=1000.0)
            db.session.add_all([c, i])
            db.session.commit()

            # Create review with valid foreign keys
            r = Review(comment='great!', customer_id=c.id, item_id=i.id)
            db.session.add(r)
            db.session.commit()

            # Verify review was saved
            assert hasattr(r, 'id')
            assert db.session.query(Review).filter_by(id=r.id).first()

    def test_is_related_to_customer_and_item(self):
        '''has foreign keys and relationships'''
        with app.app_context():
            assert 'customer_id' in Review.__table__.columns
            assert 'item_id' in Review.__table__.columns

            # Create customer and item
            c = Customer(name="Jane Doe")
            i = Item(name="Phone", price=500.0)
            db.session.add_all([c, i])
            db.session.commit()

            # Create a review linked to the customer and item
            r = Review(comment='awesome!', customer=c, item=i)
            db.session.add(r)
            db.session.commit()

            # Check foreign keys
            assert r.customer_id == c.id
            assert r.item_id == i.id

            # Check relationships
            assert r.customer == c
            assert r.item == i
            assert r in c.reviews
            assert r in i.reviews
