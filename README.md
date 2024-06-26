# ov2xmp-django

[![ov2xmp-django](https://github.com/EV4EU/ov2xmp-django/actions/workflows/docker-image.yml/badge.svg)](https://github.com/EV4EU/ov2xmp-django/actions/workflows/docker-image.yml) 


This is the main module of the O-V2X-MP that implements all the OCPP functionalities of the platform. In summary, the module consists of the following microservices:

- The CSMS service (`ov2xmp-csms`), which runs the OCPP server using the `sanic` web framework.
- The `daphne` web server (`ov2xmp-daphne`), which serves the Django system.
- The `celery` worker (`ov2xmp-celery`), which receives and executes tasks asynchronously.

## Deployment Guide

All the above microservices utilise the same source code of Django. The services can run either directly from the source code, as separate python instances on a Linux machine, or as docker containers that use the same docker image (`ov2xmp-django`).

### Deploy O-V2X-MP from source code

> Please note that steps 1-6 are executed only once, when deploying to a new VM. However, since migrations must be included in the source code, it is suggested to execute `python manage.py migrate` each time pulling new source code from the repo. Moreover, `python manage.py makemigrations` must be executed each time there is a change in the django models.

1. Clone the project (skip this step if you have already cloned `ov2xmp-django` as git submodule of `ov2xmp`)

    ```shell
    git clone https://gitlab.trsc-ppc.gr/ev4eu/ov2xmp/ov2xmp-django/
    ```

2. Inside the `ov2xmp-django` folder, create a Python virtual environment:

    ```sh
    cd ov2xmp-django
    python3 -m venv venv
    ```

3. Install the build dependencies for the `python-ldap` library. Then, activate the environment and install the python requirements:

    ```sh
    apt install gcc libldap2-dev libsasl2-dev ldap-utils python3-dev
    source ./venv/bin/activate
    (venv) pip install -r requirements.txt
    ```

4. Load the environment variables that configure `ov2xmp-django`:

    ```sh
    (venv) export $(xargs <.env-local)
    ```

5. Make Migrations and Migrate:

    ```sh
    (venv) python manage.py makemigrations
    (venv) python manage.py migrate
    ```

6. Create a superuser, if it does not already exist:

    ```sh
    (venv) python manage.py createsuperuser
    ```

7. Open a new tmux session:

    ```sh
    (venv) tmux
    ```

8. Inside the tmux session, activate the environment, load the environment variables, and run the daphne server in development mode:

    ```sh
    source ./venv/bin/activate
    (venv) export $(xargs <.env-local)
    (venv) python manage.py runserver 0.0.0.0:8000
    ```

    Detach from the tmux session, by pressing `CTRL + B` and `D`.

9. Open a new tmux session by issuing the `tmux` command. Inside the new tmux session, activate the environment, load the environment variables, and start the Sanic webserver:

    ```sh
    source ./venv/bin/activate
    (venv) export $(xargs <.env-local)
    (venv) sanic csms:app --host=0.0.0.0 --port=9000 --reload
    ```

    Alternatively, if you need to record the CSMS logs to a file, issue the following instead:

    ```sh
    (venv) sanic csms:app --host=0.0.0.0 --port=9000 --reload 2>&1 | tee ./logs/central_system_output-3.log
    ```

    Detach from the tmux session, by pressing `CTRL + B` and `D`.

10. Open a new tmux session by issuing the `tmux` command, and start the Celery worker:

    ```sh
    source ./venv/bin/activate
    (venv) export $(xargs <.env-local)
    (venv) celery -A ov2xmp worker -l info
    ```

    Detach from the tmux session, by pressing `CTRL + B` and `D`.

### Build the `ov2xmp-django` docker image locally

```sh
cd ov2xmp-django
docker build -t ov2xmp-django:latest .
```

## O-V2X-MP REST API

To access the Swagger page of the O-V2X-MP REST API, visit the following page:

`http://ov2xmp.trsc.net:8000/api`

Follow the steps bellow to get authorization based on JWT:

1. In the Swagger page, scroll down to the `token` section in order to generate a new JWT token (in case you dont have a token already)

2. Click on the `/api/token/` endpoint, then click on the `Try it out` button.

3. In the request body, specify your username and password credentials. Then, click `Execute`.

    The result will be something like this:

    ```json
    {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5MzM4NjEzMSwiaWF0IjoxNjkzMjk5NzMxLCJqdGkiOiJhZjdjZWZmNmVkYTk0ZjljOTY0YTQ0NDljYmQ3NDE2OCIsInVzZXJfaWQiOjF9.kVQ1N8NH2RMkQBE1fbEAC7RwqDPD-nlKZbozxuTmPlQ",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk1ODkxNzMxLCJpYXQiOjE2OTMyOTk3MzEsImp0aSI6IjlkNjkyNTU2ZWYzMDQ3YTFiZDg0Mzc5ZTZiMzJiMTExIiwidXNlcl9pZCI6MX0.up0gL5vhVlTMkQ1qRgrxIXo4rUbZl1N4tzlA47O4PxA"
    }
    ```

4. Copy the value of the `access` key.

5. Scroll up and click on the `Authorize` button and paste the value in the `jwtAuth` field. Finally, click the `Authorize` button.

## O-V2X-MP Django Admin page

The django admin page allows you to view and modify all the django objects of O-V2X-MP (e.g., chargepoints, idTags, charging profiles, tasks, etc). To access that page, visit the following link:

`http://ov2xmp.trsc.net:8000/admin`

## Overview of task management pipeline for OCPP requests

In summary, in order for someone to initiate a synchronous request to the O-V2X-MP for an underlying EVCS (i.e., if `sync` is set to `true`):

```plantuml
@startuml
actor user as "User app"
participant ov2xmp as "OV2XMP \nREST API"
entity celery as "Celery Task"
participant csms as "CSMS \nREST API"
entity cp as "ChargePoint\n (mobilityhouse)"

user -> ov2xmp : REST API request
activate user
ov2xmp -> celery : Call task \nfunction
celery -> csms : REST API call
csms -> cp : Call method
cp -> csms : Call resonse
csms -> celery : REST API \nresponse
celery -> ov2xmp : Call response
ov2xmp -> user : REST API \nresponse
deactivate user
@enduml
```

In case of an asynchronous request (i.e., if `sync` is set to the default value (`false`):

```plantuml
@startuml
actor user as "User app"
participant ov2xmp as "OV2XMP \nREST API"
entity celery as "Celery Task"
participant csms as "CSMS \nREST API"
entity cp as "ChargePoint\n (mobilityhouse)"

user -> ov2xmp : REST API call
activate user
ov2xmp -> celery : submit task
celery -> ov2xmp : task ID
activate celery
ov2xmp -> user : task ID
deactivate user
celery -> csms : REST API call
csms -> cp : Call method
cp -> csms : Call resonse
csms -> celery : REST API \nresponse
celery -> celery : Update task \nstatus
user -> ov2xmp : Request task status
activate user
ov2xmp -> celery : Request task status
celery -> ov2xmp : Task status
ov2xmp -> user : Task status
deactivate user
@enduml
```

## How to develop REST API endpoints for OCPP commands

To implement a REST API endpoint for issuing an OCPP 1.6 or 2.0.1 command that is initiated by the CSMS (e.g., a Reset command), follow the steps bellow:

1. First, we have to extend the ChargePoint class of the `ocpp` library, in order to define the entire logic of the new OCPP command. So, in `ov2xmp-django/chargepoint/ChargePoint16.py` or `ov2xmp/chargepoint/ChargePoint201.py`, under the "ACTIONS INITIATED BY THE CSMS" comment header, create a function for the overloaded ChargePoint class, like this:

    ```python
    # Reset
    async def reset(self, reset_type):
        request = call.ResetPayload(type = reset_type)
        return await self.call(request)
    ```

    Some notes:

    - Start with a comment that refers to the OCPP command name
    - The function must be `async`.
    - The function parameters can be determined by checking the corresponding class inside `ocpp.v16.call`. For the Reset command, the parameters are derived from the `ResetPayload` class. This class has the `type` attribute, therefore we define the corresponding argument.
    - Inside the function, we define the entire logic of the OCPP command and make all the Django ORM calls. Note that in the end we must return the entire object (dataclass) that the `call()` function returns

2. Next, we have to add a REST API endpoint to the Sanic server of the CSMS (this is utilised by Django to initiate actions towards the OCPP server and the ChargePoint objects). In particular, under the CSMS REST API comment section of the `ov2xmp-django/csms.py` file, create a new function, like this:

    ```python
    # Reset (hard or soft)
    @app.route("/ocpp16/reset/<chargepoint_id:str>", methods=["POST"])
    async def reset(request: Request, chargepoint_id: str):
        if chargepoint_id in app.ctx.CHARGEPOINTS_V16 and request.json is not None:
            resetType = request.json["reset_type"]
            result = await app.ctx.CHARGEPOINTS_V16[chargepoint_id].reset(resetType)
            return json_ocpp(result)
        else:
            return json_ocpp(CSMS_MESSAGE_CODE.CHARGING_STATION_DOES_NOT_EXIST)
    ```

    Some notes:
    - Start with a comment that refers to the OCPP command name
    - The `@app.route()` decorator defines the URL of the new OCPP command. It must follow the following format: `/ocpp16/XXX/<chargepoint_id>` (replace `ocpp16` with `ocpp201` if writing an endpoint for 2.0.1), where `XXX` is the name of the OCPP command. Always the method is POST and all parameters are provided in the JSON payload, except the `chargepoint_id`, which is always defined in the URL.
    - At the beginning, the check `if chargepoint_id in app.ctx.CHARGEPOINTS_V16 and request.json is not None` is always performed. If successful, the parameters are extracted from `request.json` and the corresponding function that we implemented in step 1 is awaited.
    - The result is provided to `json_ocpp()`, which is a custom-made function that converts the dataclass of the response to json and then sends the HTTP reply.

3. Next, create a celery task that calls the REST API endpoint previously defined. To do that, define a function inside `api/tasks.py` like this:

    ```python
    @shared_task()
    def ocpp16_reset_task(chargepoint_id, reset_type):
        message = requests.post("http://localhost:9000/ocpp16/reset/" + chargepoint_id, json={"reset_type": reset_type}).json()
        send_task_update(message)
        return message
    ```

    Some notes:
    - Each function starts with the `@shared_task()` decorator.
    - Note the function name. It always starts with `ocpp16_` or `ocpp201_`, then the OCPP command name follows, and it ends with `_task`.
    - All command parameters are provided in the function arguments (e.g., `reset_type`)
    - Command parameters are transfered to the CSMS service via the `json` argument of the `requests.post()` function.
    - At the end, the command respond is provided to the `send_task_update()`, which broadcasts the results via Django Channels.

    > Please note that after changing `tasks.py`, you need to restart the celery worker in order for the changes to take effect.

4. Next, we can start by defining the external REST API endpoint exposed by the Django system (OpenAPI). To do this, start by defining the serializer in `api/serializers.py`. In this file, create a serializer for the endpoint, like the following:

    ```python
    class Ocpp16ResetSerializer(OcppCommandSerializer):
        reset_type = serializers.ChoiceField(choices=tuple(member.value for member in ocppv16_enums.ResetType))
    ```

    Some notes:
    - Note the class name. It starts with `Ocpp16` (or `Ocpp201`), then the OCPP commmand name follows, and it ends with `Serializer`.
    - It inherits the `OcppCommandSerializer`, which defines the parameters that are accepted by all OCPP commands. In particular, all OCPP commands must accept the `chargepoint_id` and the `sync` parameter.
    - The new serializer needs to define only the extra parameters that are associated with the corresponding OCPP command.

5. Next, define the API View inside `api/views.py` like the following:

    ```python
    class Ocpp16ResetApiView(CreateAPIView):
        authentication_classes = [JWTAuthentication]
        serializer_class = Ocpp16ResetSerializer

        def post(self, request, *args, **kwargs):
            '''
            Send a Reset command (hard or soft)
            '''

            serializer = Ocpp16ResetSerializer(data=request.data)
            if serializer.is_valid():
                if serializer.data["sync"]:
                    task = ocpp16_reset_task(serializer.data["chargepoint_id"], serializer.data["reset_type"])
                    return Response(task, status=status.HTTP_200_OK)
                else:
                    task = ocpp16_reset_task.delay(serializer.data["chargepoint_id"], serializer.data["reset_type"]) # type: ignore
                    return Response({"message_code": CSMS_MESSAGE_CODE.TASK_SUBMITTED.name, "message": CSMS_MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    ```

    Some notes:
    - Keep the above structure/logic.
    - Replace the serializer in `serializer_class`.
    - It is important to provide a command description in the comment under the `post()` function (this comment is parsed in order to automatically generate the OpenAPI spec).
    - In `serializer = Ocpp16ResetSerializer(data=request.data)` replace the serializer with yours.
    - Inside the `if serializer.data["sync"]:` statement, replace the task function and its corresponding parameters.

6. Include the new endpoint in `api/urls.py`, like so:

    ```python
    path('ocpp16/reset/', Ocpp16ResetApiView.as_view()),
    ```

    Some notes:
    - In `ocpp16/reset/`, replace `reset` with the command name
    - Replace `Ocpp16ResetApiView` with the name of the API view class defined previously.
