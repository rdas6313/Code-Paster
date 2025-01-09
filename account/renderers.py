from rest_framework import renderers


class JsonRenderer(renderers.JSONRenderer):
    """ Use as a json renderer  """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if 'ErrorDetail' in str(data):
            data = {'errors': data}
        return super().render(data, accepted_media_type, renderer_context)
