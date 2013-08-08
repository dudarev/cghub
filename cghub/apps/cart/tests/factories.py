from ..models import Cart as CartModel, Analysis, CartItem


class AnalysisFactory(object):

    counter = 0

    @classmethod
    def create(
                self, analysis_id=None, last_modified=None,
                state='live', files_size=None):
        self.counter += 1
        analysis_id = analysis_id or (
                '017a4d4e-9f4b-4904-824e-060fde3ca22%d' % self.counter)
        last_modified = last_modified or (
                '2013-05-16T20:43:4%dZ' % self.counter)
        files_size = files_size or (466684944 + self.counter)
        return Analysis.objects.create(
                analysis_id=analysis_id, last_modified=last_modified,
                state=state, files_size=files_size)


class CartItemFactory(object):

    @classmethod
    def create(cart, analysis=None):
        if not analysis:
            analysis = AnalysisFactory.create()
        return CartItem.objects.create(cart=cart, analysis=analysis)


class CartFactory(object):

    @classmethod
    def create(session, items_count=1):
        cart = CartModel.objects.create(session=session)
        for i in range(items_count):
            CartItemFactory.create(cart=cart)
        return cart
