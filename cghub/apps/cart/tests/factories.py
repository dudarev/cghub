from ..models import Cart as CartModel, Analysis, CartItem


class AnalysisFactory(object):

    counter = 0

    IDS = [
        {
            'analysis_id': '016b792f-e659-4143-b833-163141e21363',
            'last_modified': '2013-05-16T20:43:40Z'
        }, {
            'analysis_id': '015be8a5-fafc-458e-9ae9-7e721f95fe8b',
            'last_modified': '2013-05-16T20:43:40Z'
        }, {
            'analysis_id': '015fd6a5-a77e-4bd1-9430-b44d1c043b54',
            'last_modified': '2013-05-16T20:43:40Z'
        }, {
            'analysis_id': '015090b8-86f3-4e60-a1ec-89b16d0be113',
            'last_modified': '2013-05-16T20:43:40Z'
        }, {
            'analysis_id': '016a7ba7-a154-4702-9c6d-f2de4c01a3c0',
            'last_modified': '2013-05-16T20:43:40Z'
        }, {
            'analysis_id': '01349f1a-362a-42b3-881a-53c33ac19c97',
            'last_modified': '2013-07-03T23:32:01Z'
        }, {
            'analysis_id': '01344cac-79d7-48ed-9179-7af7470f9afa',
            'last_modified': '2013-07-03T23:31:02Z'
        }
        
    ]

    @classmethod
    def create(
                self, analysis_id=None, last_modified=None,
                state='live', files_size=None):
        self.counter += 1
        analysis_id = analysis_id or self.IDS[self.counter - 1]['analysis_id']
        last_modified = last_modified or self.IDS[self.counter - 1]['last_modified']
        files_size = files_size or (466684944 + self.counter)
        return Analysis.objects.create(
                analysis_id=analysis_id, last_modified=last_modified,
                state=state, files_size=files_size)


class CartItemFactory(object):

    @classmethod
    def create(self, cart, analysis=None):
        if not analysis:
            analysis = AnalysisFactory.create()
        return CartItem.objects.create(cart=cart, analysis=analysis)


class CartFactory(object):

    @classmethod
    def create(self, session, items_count=1):
        cart = CartModel.objects.create(session=session)
        for i in range(items_count):
            CartItemFactory.create(cart=cart)
        return cart
