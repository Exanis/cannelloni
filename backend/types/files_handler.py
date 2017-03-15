# -*- coding: utf8 -*-

"Files-related handler"

import os
from cannelloni.settings import BASE_DIR

def files_handler(request, variable):
    "Handle file upload"
    target = os.path.join(BASE_DIR, 'files', str(variable.uuid))
    with open(target, 'wb+') as destination:
        for chunk in request.FILES[str(variable.uuid)].chunks():
            destination.write(chunk)
    variable.value = target
