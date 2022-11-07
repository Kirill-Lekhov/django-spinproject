_V1_CONTENT = {
	'templates': {
		'.gitlab-ci.yml': '''stages:
- check
- deploy

image: python:3.8

services:
  - postgres:13.1-alpine

variables:
  DJANGO_DATABASE_URL: pgsql://postgres:@postgres/postgres
  DJANGO_SECRET_KEY: 'static'
  DJANGO_ALLOWED_HOSTS: '127.0.0.1,localhost'
  ### CI database configuration
  POSTGRES_HOST_AUTH_METHOD: trust
  #POSTGRES_DB: nice_marmot
  #POSTGRES_USER: runner
  POSTGRES_PASSWORD: ""
  ### CI configuration
  # Change pip's cache directory to be inside the project directory since we can
  # only cache local items.
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  # Faster CI caching
  FF_USE_FASTZIP: 1

cache:
  paths:
    - .cache/pip
    - .cache/pypoetry
    - venv/

before_script:
  - python -V  # Print out python version for debugging
  - pip install -q poetry
  - poetry config cache-dir "$CI_PROJECT_DIR/.cache/pypoetry"
  - poetry config virtualenvs.create true

test:
  stage: check
  script:
    - script/setup
    - script/cibuild
  coverage: '/^TOTAL.+?(\d+\%)$/'
  artifacts:
    reports:
      cobertura: coverage.xml

deploy_bleeding:
  when: manual
  stage: deploy
  image: "docker:19.03.1"
  before_script:
    - docker info
  script:
    - echo 'TODO: change registry address and image name' && exit 1
    - echo $DOCKER_PASSWORD | docker login --username user --password-stdin {login_repository}
    - docker build -t '{image_repository}{image}:bleeding' .
    - docker push '{image_repository}{image}:bleeding'

deploy_main:
  when: manual
  stage: deploy
  image: "docker:19.03.1"
  before_script:
    - docker info
  script:
    - echo 'TODO: change registry address and image name' && exit 1
    - echo $DOCKER_PASSWORD | docker login --username user --password-stdin {login_repository}
    - docker build -t '{image_repository}{image}' .
    - docker push '{image_repository}{image}'

# ISSUE: nobody can guarantee that image did not change between deploy_bleeding and deploy_promote. Use at your own risk.
# deploy_promote:
#   when: manual
#   stage: deploy
#   script:
#     - docker tag '{image_repository}{image}:bleeding' '{image_repository}{image}'
#     - docker push '{image_repository}{image}'


# pages:
#   script:
#     - pip install sphinx sphinx-rtd-theme
#     - cd doc ; make html
#     - mv build/html/ ../public/
#   artifacts:
#     paths:
#       - public
#   only:
#     - master
'''
	}
}
