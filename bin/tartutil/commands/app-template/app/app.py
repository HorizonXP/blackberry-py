import tart


class App(tart.Application):
    def __init__(self):
        super().__init__(debug=False)   # set True for some extra debug output


    def onUiReady(self):
        print('UI is ready')
