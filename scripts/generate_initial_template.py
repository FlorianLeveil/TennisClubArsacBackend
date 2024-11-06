import json
import uuid

IMAGE_PROPS = ['title', 'tags', 'type', 'imageUrl']

NAVIGATION_ITEM_PROPS = ['title', 'description', 'image', 'route', 'navBarRender', 'pageRenders',
                         'childrenNavigationItems', 'enabled']

RENDER_PROPS = ['order', 'navBarPosition', 'visible', 'type', 'color', 'isButton']

PAGE_RENDER_PROPS = ['route', 'render']

NAVIGATION_BAR_PROPS = ['logo', 'routeLogo', 'navigationItems']

HOME_PAGE_PROPS = ['title', 'navigationItems']


def get_initial_data_template(model_name, extra_props):
    _uuid = str(uuid.uuid4())
    extra_props_dict = {prop_name: '' for prop_name in extra_props}
    extra_props_dict['createAt'] = '2024-05-30T11:01:26.151680+02:00'
    extra_props_dict['updateAt'] = '2024-05-30T11:01:26.151680+02:00'

    template = {
        'model': f'BackendTennis.{model_name}',
        'pk': _uuid,
        'fields': {
            'id': _uuid,
        }
    }
    template['fields'].update(extra_props_dict)

    return template


def main():
    nb_to_generate = 1
    model_name = 'HomePage'
    extra_props = HOME_PAGE_PROPS

    full_template = []
    for i in range(nb_to_generate):
        full_template.append(get_initial_data_template(model_name, extra_props))

    print(json.dumps(full_template))


if __name__ == '__main__':
    main()
