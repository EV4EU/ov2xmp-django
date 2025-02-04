# ov2xmp-django

[![ov2xmp-django](https://github.com/EV4EU/ov2xmp-django/actions/workflows/docker-image.yml/badge.svg)](https://github.com/EV4EU/ov2xmp-django/actions/workflows/docker-image.yml) 

## Citation

If you want to use this work, please cite the following paper:

```bibtex
@article{DALAMAGKAS2025102494,
title = {The Open V2X Management Platform: An intelligent charging station management system},
journal = {Information Systems},
volume = {129},
pages = {102494},
year = {2025},
issn = {0306-4379},
doi = {https://doi.org/10.1016/j.is.2024.102494},
url = {https://www.sciencedirect.com/science/article/pii/S0306437924001522},
author = {Christos Dalamagkas and V.D. Melissianos and George Papadakis and Angelos Georgakis and Vasileios-Martin Nikiforidis and Kostas Hrissagis-Chrysagis}
}
```

## Introduction

This is the main module of the O-V2X-MP that implements all the OCPP functionalities of the platform. In summary, the module consists of the following microservices:

- The CSMS service (`ov2xmp-csms`), which runs the OCPP server using the `sanic` web framework.
- The `daphne` web server (`ov2xmp-daphne`), which serves the Django system.
- The `celery` worker (`ov2xmp-celery`), which receives and executes tasks asynchronously.

## Deployment

Check the [Deployment Guide](https://github.com/EV4EU/ov2xmp-django/wiki/Deployment-Guide) wiki page on how to deploy the O-V2X-MP microservices from source code.

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
