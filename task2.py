import docker 

client = docker.from_env()
client.swarm.init() # docker should not be part of swarm. If that's the case run 'docker swarm leave' without any running containers 

benchmark_endspec = docker.types.EndpointSpec(ports={80:(8080,'tcp')})
visualizer_endspec = docker.types.EndpointSpec(ports = {88:(8080,'tcp')})
cadvisor_endspec = docker.types.EndpointSpec(ports = {8080:(8080,'tcp')})

client.services.create(
    image = "mongo",
    name = "mongodb",
    endpoint_spec = docker.types.EndpointSpec(ports = {3306:(27017,'tcp')})
)

srvMode = docker.types.ServiceMode(mode="replicated", replicas = 2)

client.services.create(
    image= "nclcloudcomputing/javabenchmarkapp",
    name = "benchmark",
    mode = srvMode,
    endpoint_spec = benchmark_endspec
)

client.services.create(
    image = "dockersamples/visualizer",
    endpoint_spec = visualizer_endspec,
    mounts = [
        "/var/run/docker.sock:/var/run/docker.sock:ro"
    ]
)

client.services.create(
    image = "google/cadvisor:latest",
    endpoint_spec = cadvisor_endspec,
    mounts = [
      "/:/rootfs:ro",
      "/var/run:/var/run:ro",
      "/sys:/sys:ro",
      "/var/lib/docker/:/var/lib/docker:ro",
      "/dev/disk/:/dev/disk:ro"
    ]
)
