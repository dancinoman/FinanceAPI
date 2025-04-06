image_name = my-app-image
container_name = my-running-app
host_port = 8080
container_port = 80

test_target:
	echo "Hello from make!"

build_image:
	docker build -t $(image_name) .

run_docker: build_image
	docker run -d --name $(container_name) -p $(host_port):$(container_port) $(image_name)

stop_docker:
	docker stop $(container_name)

remove_docker: stop_docker
	docker rm $(container_name)

clean: remove_docker
	docker rmi $(image_name)

.PHONY: build_image run_docker stop_docker remove_docker clean
