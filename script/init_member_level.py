import base
from web import models


def run():
    models.MemberLevel.objects.create(
        category=3,
        name='SVIP用户',
        price=49.99,
        project_num=50,
        project_member=25,
        single_project_space=50,
        single_file_space=500,
    )


if __name__ == '__main__':
    run()
