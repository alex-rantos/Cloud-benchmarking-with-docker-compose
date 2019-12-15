import docker

client = docker.from_env()

client.images.pull("nclcloudcomputing/javabenchmarkapp")
client.containers.run("nclcloudcomputing/javabenchmarkapp", detach=True)