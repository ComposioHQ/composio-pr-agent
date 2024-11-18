IMAGE_NAME = composio/pr-review
TAG = latest
API_KEY = afv0m4yt65evll5p38m09k
AWS_ACCESS_KEY_ID = AKIAQEFWAZKVQDLXUM34
AWS_SECRET_ACCESS_KEY = 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
AWS_DEFAULT_REGION = us-west-2

.PHONY: all clean build run

all: clean build run

clean:
	docker rm -f $$(docker ps -a -q --filter ancestor=$(IMAGE_NAME):$(TAG))
	docker rmi -f $(IMAGE_NAME):$(TAG)

build:
	docker build -f Dockerfile -t $(IMAGE_NAME):$(TAG) .

delete:
	docker rm -f $$(docker ps -a -q --filter ancestor=$(IMAGE_NAME):$(TAG))

run:
	docker run --name composio-pr-agent --env-file .env $(IMAGE_NAME):$(TAG)