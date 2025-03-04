############################
# Use this script to generate fixtures structures of MODEL
############################

import json
import uuid

CATEGORY_PROPS = ['name', 'icon']

EVENT_PROPS = ['title', 'description', 'dateType', 'start', 'end', 'image', 'category']

IMAGE_PROPS = ['title', 'tags', 'type', 'imageUrl']

NAVIGATION_ITEM_PROPS = ['title', 'description', 'image', 'route', 'navBarRender', 'pageRenders',
                         'childrenNavigationItems', 'enabled']

NEWS_PROPS = ['title', 'content', 'subtitle', 'images', 'category']

RENDER_PROPS = ['order', 'navBarPosition', 'visible', 'type', 'color', 'isButton']

TOURNAMENT_PROPS = [
    'name',
    'participants',
    'unregisteredParticipants',
    'cancel',
    'start',
    'end'
]

PAGE_RENDER_PROPS = ['route', 'render']

ROUTE_PROPS = ['name', 'protocol', 'domainUrl', 'pathUrl', 'componentPath', 'metaTitle', 'metaTags']

CLUB_VALUE_PROPS = ['title', 'description', 'order']

SPONSOR_PROPS = ['brandName', 'image', 'order']

NAVIGATION_BAR_PROPS = ['logo', 'routeLogo', 'navigationItems']

PRICING_PAGE_PROPS = ['title', 'description', 'pricing']

HOME_PAGE_PROPS = ['title', 'navigationItems']

ABOUT_PAGE_PROPS = [
    'clubTitle', 'clubDescription', 'clubImage', 'dataCounter',
    'clubValueTitle', 'clubValues', 'sponsorTitle', 'sponsors'
]

TEAM_PAGE_PROPS = [
    'professorsTitle', 'professorsDescription', 'professors', 'teamMembersTitle',
    'teamMembers', 'dataCounter',
]

TEAM_MEMBER_PROPS = [
    'fullNames', 'role', 'images', 'description',
    'order'
]

PROFESSOR_PROPS = [
    'fullNames', 'role', 'images', 'diploma',
    'order', 'year_experience', 'best_rank'
]


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
    nb_to_generate = 7
    model_name = 'Image'
    extra_props = IMAGE_PROPS

    full_template = []
    for i in range(nb_to_generate):
        full_template.append(get_initial_data_template(model_name, extra_props))

    print(json.dumps(full_template))


if __name__ == '__main__':
    main()
