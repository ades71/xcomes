import json

from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        errors = data.get('errors', None)

        token = data.get('token', None)

        if errors is not None:
            return super(UserJSONRenderer, self).render(data)

        # token이 byte형태일 경우
        if token is not None and isinstance(token, bytes):
            # 'utf-8'로 decode 해준 후 다시 data의 'token' 부분에 추가합니다.
            data['token'] = token.decode('utf-8')

        # 그리고 우린 data를 'user' 안에 담아 json 형태로 render 해줍니다.
        return json.dumps({
            'user': data
        })
